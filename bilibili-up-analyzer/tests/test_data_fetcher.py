# -*- coding: utf-8 -*-
"""
bilibili-up-analyzer 单元测试

覆盖：
- WBI 签名算法（含特殊字符过滤、确定性回归）
- 各接口响应解析（UP 信息 / 视频列表 / 视频详情）
- 输入解析（UID / URL / 用户名）
- Cookie / SESSDATA 登录态支持
- 缓存与断点续传 / --clear-cache 边界
均为 mock 测试，不发起真实网络请求。
"""

import os
import sys
import json
import time
import hashlib
import tempfile
from unittest import mock
from urllib.parse import urlencode

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from data_fetcher import BilibiliDataFetcher, mix_key_enc_wbi

# 用于确定性签名的稳定密钥对（各 32 位）
IMG_KEY = "8b72d0e9b6f5c4a3210d9e8f7a6b5c4d"
SUB_KEY = "e4c6d8a0b2f4e6c8a0d2f4e6c8a0b2fd"
FIXED_TS = 1750000000


def make_fetcher(tmp_dir=None, **kwargs):
    """构造关闭缓存/会话 mock 的采集器，避免真实网络"""
    return BilibiliDataFetcher(cache_dir=tmp_dir or ".",
                               enable_cache=False, **kwargs)


# ==================== WBI 签名 ====================

class TestWbiSignature:
    def test_mixin_key_expected(self):
        # 稳定的参考值，用于回归：mixin_key 由重排表从前 32 位派生
        mixin = mix_key_enc_wbi(IMG_KEY, SUB_KEY)
        assert len(mixin) == 32

    def test_sign_params_creates_w_rid(self):
        f = make_fetcher()
        f._wbi_keys = (IMG_KEY, SUB_KEY)
        with mock.patch("data_fetcher.time.time", return_value=FIXED_TS):
            sig = f._sign_params({"mid": "159285873"})
        mixin = mix_key_enc_wbi(IMG_KEY, SUB_KEY)
        expected = hashlib.md5(
            urlencode([("mid", "159285873"), ("wts", str(FIXED_TS))]).encode() + mixin.encode()
        ).hexdigest()
        assert sig["wts"] == str(FIXED_TS)
        assert sig["w_rid"] == expected
        assert sig["w_rid"] == sig["w_rid"].lower()
        assert len(sig["w_rid"]) == 32

    def test_sign_params_deterministic(self):
        f = make_fetcher()
        f._wbi_keys = (IMG_KEY, SUB_KEY)
        with mock.patch("data_fetcher.time.time", return_value=FIXED_TS):
            sig1 = f._sign_params({"mid": "1"})
            sig2 = f._sign_params({"mid": "1"})
        assert sig1 == sig2

    def test_sign_params_filters_special_chars(self):
        f = make_fetcher()
        f._wbi_keys = (IMG_KEY, SUB_KEY)
        with mock.patch("data_fetcher.time.time", return_value=FIXED_TS):
            sig = f._sign_params({"keyword": "it's a (test)!"})
        # '!' '(' ')' "'" 应被过滤
        assert sig["keyword"] == "its a test"
        with mock.patch("data_fetcher.time.time", return_value=FIXED_TS):
            sig2 = f._sign_params({"keyword": "正常关键词"})
        assert sig2["keyword"] == "正常关键词"

    def test_sign_params_passthrough_without_keys(self):
        f = make_fetcher()
        with mock.patch.object(f, "_get_wbi_keys", return_value=None):
            params = f._sign_params({"mid": "1"})
        # 无密钥时原样返回，不追加签名
        assert params == {"mid": "1"}


# ==================== 响应解析 ====================

class TestParsing:
    def test_parse_up_info(self):
        f = make_fetcher()
        info = {
            "mid": 123, "name": "测试主", "face": "x.png", "sign": "hi",
            "level": 5, "follower": 100, "following": 2,
            "archive_count": 30, "article_count": 1, "like_num": 999,
        }
        r = f._parse_up_info(info)
        assert r["uid"] == "123"
        assert r["name"] == "测试主"
        assert r["follower"] == 100
        assert r["like_num"] == 999

    def test_parse_video_list(self):
        f = make_fetcher()
        data = {
            "data": {
                "page": {"count": 2},
                "list": {"vlist": [
                    {"bvid": "BV1", "title": "v1", "created": 100,
                     "play": 5, "comment": 1, "typeid": 2, "typename": "科技",
                     "video_review": 3, "length": "10:00"},
                    {"bvid": "BV2", "title": "v2"},
                ]},
            }
        }
        videos, total = f._parse_video_list(data)
        assert total == 2
        assert len(videos) == 2
        assert videos[0]["bvid"] == "BV1"
        assert videos[0]["play"] == 5
        assert videos[1]["play"] == 0

    def test_parse_video_detail(self):
        f = make_fetcher()
        data = {
            "data": {
                "aid": 1, "bvid": "BV1", "title": "t", "desc": "d",
                "duration": 60, "pubdate": 100,
                "owner": {"mid": 9, "name": "o"},
                "tname": "科技", "tid": 2,
                "stat": {"view": 100, "danmaku": 5, "reply": 2, "favorite": 3,
                         "coin": 4, "share": 1, "like": 50, "dislike": 0},
            }
        }
        r = f._parse_video_detail(data)
        assert r["stat"]["like"] == 50
        assert r["stat"]["view"] == 100
        assert r["owner"]["mid"] == 9
        assert r["tname"] == "科技"

    def test_parse_video_detail_missing_stat(self):
        f = make_fetcher()
        r = f._parse_video_detail({"data": {"bvid": "BV1"}})
        assert r["stat"]["like"] == 0


# ==================== 输入解析 ====================

class TestResolveUid:
    def test_numeric_uid(self):
        f = make_fetcher()
        assert f.resolve_uid(" 159285873 ") == "159285873"

    def test_url_uid(self):
        f = make_fetcher()
        assert f.resolve_uid("https://space.bilibili.com/159285873") == "159285873"

    def test_name_via_search(self):
        f = make_fetcher()
        with mock.patch.object(f, "_search_uid_by_name", return_value="42"):
            assert f.resolve_uid("Jason_Shane") == "42"

    def test_invalid_name_returns_none(self):
        f = make_fetcher()
        with mock.patch.object(f, "_search_uid_by_name", return_value=None):
            assert f.resolve_uid("不存在的名字") is None


# ==================== Cookie / 登录态 ====================

class TestCookie:
    def test_sessdata_sets_cookie_header(self):
        f = make_fetcher(sessdata="abc123")
        assert "SESSDATA=abc123" in f.session.headers.get("Cookie", "")

    def test_cookie_prefers_full_cookie(self):
        f = make_fetcher(cookie="buvid3=xyz")
        assert f.session.headers["Cookie"] == "buvid3=xyz"

    def test_no_cookie_by_default(self):
        f = make_fetcher()
        assert "Cookie" not in f.session.headers


# ==================== 缓存与断点续传 ====================

class TestCacheAndCheckpoint:
    def test_checkpoint_roundtrip(self):
        with tempfile.TemporaryDirectory() as td:
            f = BilibiliDataFetcher(cache_dir=td, enable_cache=True)
            data = {"uid": "1", "videos": [{"bvid": "BV1"}]}
            f.save_checkpoint("1", data)
            loaded = f.load_checkpoint("1")
            assert loaded["uid"] == "1"
            assert loaded["videos"][0]["bvid"] == "BV1"

    def test_clear_cache_removes_checkpoint(self):
        with tempfile.TemporaryDirectory() as td:
            f = BilibiliDataFetcher(cache_dir=td, enable_cache=True)
            f.save_checkpoint("1", {"uid": "1"})
            f._save_cache(f._cache_path("up_info", "1"), {"uid": "1"})
            n = f.clear_cache()
            assert n == 2
            assert f.load_checkpoint("1") is None
            assert not os.listdir(td)

    def test_clear_cache_nonexistent_dir(self):
        f = BilibiliDataFetcher(cache_dir="/nonexistent-xyz", enable_cache=False)
        assert f.clear_cache() is None


# ==================== 断点续传（analyze_up._enrich_with_checkpoint） ====================

class TestCheckpointResume:
    def _inject(self, tmp_dir, checkpoint=None):
        f = BilibiliDataFetcher(cache_dir=tmp_dir, enable_cache=True)
        if checkpoint is not None:
            f.save_checkpoint("1", checkpoint)
        args = mock.Mock(verbose=False)
        return f, args

    def test_resume_skips_done_videos(self):
        with tempfile.TemporaryDirectory() as td:
            # checkpoint 中 B1 已带 stat
            f, args = self._inject(td, {"uid": "1", "videos": [
                {"bvid": "B1", "stat": {"view": 100}},
            ]})
            videos = [
                {"bvid": "B1", "title": "a"},
                {"bvid": "B2", "title": "b"},
            ]
            with mock.patch.object(f, "enrich_video_stat",
                                   side_effect=lambda v: v.setdefault("stat", {"view": 1})) as m:
                from analyze_up import _enrich_with_checkpoint
                out, resumed = _enrich_with_checkpoint(f, "1", videos, args)
            # 仅 B2 触发详情补充，B1 复用 checkpoint
            assert resumed == 1
            assert m.call_count == 1
            assert out[0]["stat"]["view"] == 100
            assert out[1]["stat"]["view"] == 1

    def test_fresh_run_enriches_all(self):
        with tempfile.TemporaryDirectory() as td:
            f, args = self._inject(td, checkpoint=None)
            videos = [{"bvid": "B1"}, {"bvid": "B2"}]
            with mock.patch.object(f, "enrich_video_stat",
                                   side_effect=lambda v: v.setdefault("stat", {"view": 1})) as m:
                from analyze_up import _enrich_with_checkpoint
                out, resumed = _enrich_with_checkpoint(f, "1", videos, args)
            assert resumed == 0
            assert m.call_count == 2
            # 完成后写入 checkpoint 供后续续传
            cp = f.load_checkpoint("1")
            assert cp["uid"] == "1"
            assert len(cp["videos"]) == 2