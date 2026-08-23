"""
Bilibili UP主数据采集模块

实现WBI签名算法，支持通过UID、用户名、主页链接获取UP主信息和视频数据。
三级数据获取策略：WBI签名接口 -> 非签名接口 -> 搜索API兜底。
"""

import requests
import json
import os
import time
import hashlib
import re
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse, urlencode

# WBI 签名重排表
_WBI_MIXED_TABLE = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35,
    27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13,
    37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4,
    22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11, 36, 20, 34, 44, 52
]
# 不会被过滤的合法 WBI 参数过滤集
_WBI_CHAR_FILTER = set("!'()*")


def mix_key_enc_wbi(img_key: str, sub_key: str) -> str:
    """从 img/sub 两张密钥表派生 WBI 的 mixin_key（32 位）"""
    combined = img_key + sub_key
    return "".join(combined[i] for i in _WBI_MIXED_TABLE[:32])


class BilibiliDataFetcher:
    """Bilibili数据采集器（内置WBI签名）"""

    API_BASE = "https://api.bilibili.com/x"

    def __init__(self, cache_dir: str = "./cache", enable_cache: bool = True,
                 cookie: Optional[str] = None, sessdata: Optional[str] = None):
        self.cache_dir = cache_dir
        self.enable_cache = enable_cache
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        })
        # 登录态：提升 like_num/follower 等字段完整度
        if cookie:
            self.session.headers["Cookie"] = cookie.strip()
        elif sessdata:
            self.session.headers["Cookie"] = f"SESSDATA={sessdata.strip()}"
        self._wbi_keys: Optional[tuple] = None  # (img_key, sub_key)
        if enable_cache:
            os.makedirs(cache_dir, exist_ok=True)

    # ==================== WBI 签名 ====================

    def _get_wbi_keys(self) -> Optional[tuple]:
        """获取WBI签名密钥（带缓存）"""
        if self._wbi_keys:
            return self._wbi_keys
        try:
            resp = self.session.get(
                f"{self.API_BASE}/web-interface/nav",
                headers={"Referer": "https://www.bilibili.com"},
                timeout=10,
            )
            data = resp.json()
            wbi_img = data.get("data", {}).get("wbi_img")
            if not wbi_img:
                return None
            img_url = wbi_img.get("img_url", "")
            sub_url = wbi_img.get("sub_url", "")
            img_key = os.path.splitext(urlparse(img_url).path)[0].split("/")[-1]
            sub_key = os.path.splitext(urlparse(sub_url).path)[0].split("/")[-1]
            self._wbi_keys = (img_key, sub_key)
            return self._wbi_keys
        except Exception:
            return None

    def _sign_params(self, params: Dict) -> Dict:
        """对请求参数进行WBI签名"""
        keys = self._get_wbi_keys()
        if not keys:
            return params
        img_key, sub_key = keys
        mixin_key = mix_key_enc_wbi(img_key, sub_key)
        params["wts"] = str(int(time.time()))
        params = {k: "".join(c for c in str(v) if c not in _WBI_CHAR_FILTER) for k, v in params.items()}
        query = urlencode(sorted(params.items())) + mixin_key
        params["w_rid"] = hashlib.md5(query.encode()).hexdigest()[:32]
        return params

    # ==================== 网络请求 ====================

    def _request(self, url: str, params: Dict = None, use_wbi: bool = False,
                 retries: int = 3, base_delay: float = 3,
                 headers: Dict = None) -> Optional[Dict]:
        """发送HTTP请求，支持WBI签名和自动重试"""
        if params is None:
            params = {}
        if use_wbi:
            params = self._sign_params(dict(params))
        req_headers = dict(self.session.headers)
        if headers:
            req_headers.update(headers)

        for attempt in range(retries):
            try:
                resp = self.session.get(url, params=params, headers=req_headers, timeout=15)
                if resp.status_code == 412:
                    time.sleep(base_delay * (attempt + 2))
                    continue
                resp.raise_for_status()
                data = resp.json()
                code = data.get("code")
                if code == 0:
                    return data
                if code in (-352, -799):
                    time.sleep(base_delay * (attempt + 1))
                    continue
                return None
            except requests.exceptions.HTTPError as e:
                if "412" in str(e):
                    time.sleep(base_delay * (attempt + 2))
                    continue
                if attempt < retries - 1:
                    time.sleep(base_delay)
            except Exception:
                if attempt < retries - 1:
                    time.sleep(base_delay)
        return None

    def _warm_up(self):
        """预热：访问B站主页获取基础Cookie"""
        try:
            self.session.get("https://www.bilibili.com/", timeout=10)
        except Exception:
            pass

    # ==================== 输入解析 ====================

    def resolve_uid(self, input_str: str) -> Optional[str]:
        """
        从任意输入解析UID，支持：
        - 纯数字UID: "159285873"
        - 主页链接: "https://space.bilibili.com/159285873"
        - 用户名: "Jason_Shane"（通过搜索API查找）
        """
        input_str = input_str.strip()

        # 1. 纯数字UID
        if re.fullmatch(r'\d+', input_str):
            return input_str

        # 2. URL中提取UID
        m = re.search(r'space\.bilibili\.com/(\d+)', input_str)
        if m:
            return m.group(1)

        # 3. 用户名 -> 搜索API
        uid = self._search_uid_by_name(input_str)
        if uid:
            return uid

        return None

    def _search_uid_by_name(self, name: str) -> Optional[str]:
        """通过搜索API根据用户名查找UID"""
        params = {"search_type": "bili_user", "keyword": name}
        data = self._request(
            "https://api.bilibili.com/x/web-interface/search/type",
            params=params,
            headers={"Referer": "https://search.bilibili.com/"},
        )
        if data:
            results = data.get("data", {}).get("result", [])
            for r in results:
                if r.get("uname") == name or name.lower() in r.get("uname", "").lower():
                    return str(r.get("mid"))
            if results:
                return str(results[0].get("mid"))
        return None

    # ==================== 缓存 ====================

    def _cache_path(self, prefix: str, identifier: str) -> str:
        h = hashlib.md5(f"{prefix}:{identifier}".encode()).hexdigest()[:12]
        return os.path.join(self.cache_dir, f"{prefix}_{h}.json")

    def _load_cache(self, path: str, max_age: int = 86400) -> Optional[Dict]:
        if not self.enable_cache or not os.path.exists(path):
            return None
        try:
            if time.time() - os.path.getmtime(path) > max_age:
                return None
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None

    def _save_cache(self, path: str, data: Dict) -> None:
        if not self.enable_cache:
            return
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    # ==================== 断点续传 ====================

    def load_checkpoint(self, uid: str) -> Optional[Dict]:
        """读取断点续传进度（不按 TTL 过期，便于中断后继续）"""
        path = self._cache_path("checkpoint", uid)
        if not os.path.exists(path):
            return None
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None

    def save_checkpoint(self, uid: str, data: Dict) -> None:
        """写入断点续传进度"""
        if not self.enable_cache:
            return
        try:
            with open(self._cache_path("checkpoint", uid), 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    # ==================== 数据获取 ====================

    def _parse_up_info(self, info: Dict[str, Any]) -> Dict[str, Any]:
        """将 acc/info 接口的 info 段解析为统一结构"""
        return {
            "uid": str(info.get("mid", "")),
            "name": info.get("name", ""),
            "face": info.get("face", ""),
            "sign": info.get("sign", ""),
            "level": info.get("level", 0),
            "follower": info.get("follower", 0) or 0,
            "following": info.get("following", 0) or 0,
            "archive_count": info.get("archive_count", 0) or 0,
            "article_count": info.get("article_count", 0) or 0,
            "like_num": info.get("like_num", 0) or 0,
        }

    def get_up_info(self, uid: str) -> Optional[Dict[str, Any]]:
        """获取UP主基础信息（WBI签名接口优先）"""
        cache_file = self._cache_path("up_info", uid)
        cached = self._load_cache(cache_file, max_age=43200)
        if cached:
            return cached

        params = {"mid": uid}
        referer = {"Referer": f"https://space.bilibili.com/{uid}"}

        # 策略1: WBI签名接口
        data = self._request(
            f"{self.API_BASE}/space/wbi/acc/info", params,
            use_wbi=True, retries=2,
        )
        # 策略2: 非签名接口
        if not data:
            data = self._request(
                f"{self.API_BASE}/space/acc/info", params,
                retries=2,
            )
        if not data:
            return None

        info = data["data"]
        result = self._parse_up_info(info)
        result["uid"] = str(uid)

        # 未登录时B站不返回follower/like_num等字段，通过搜索API补充
        if (result["follower"] == 0 or result["like_num"] == 0) and result["name"]:
            self._enrich_up_info_from_search(result)

        self._save_cache(cache_file, result)
        return result

    def _enrich_up_info_from_search(self, up_info: Dict) -> None:
        """通过搜索API补充UP主粉丝数等字段"""
        params = {"search_type": "bili_user", "keyword": up_info["name"]}
        data = self._request(
            "https://api.bilibili.com/x/web-interface/search/type",
            params,
            headers={"Referer": "https://search.bilibili.com/"},
        )
        if not data:
            return
        for r in data.get("data", {}).get("result", []):
            if str(r.get("mid")) == str(up_info["uid"]):
                up_info["follower"] = r.get("fans", 0) or 0
                up_info["archive_count"] = r.get("videos", 0) or up_info["archive_count"]
                break

    def get_video_list(self, uid: str, page: int = 1,
                       page_size: int = 30):
        """获取UP主视频列表（单页）"""
        params = {"mid": uid, "pn": page, "ps": page_size, "order": "pubdate"}
        referer = {"Referer": f"https://space.bilibili.com/{uid}/video"}

        # 策略1: WBI签名接口
        data = self._request(
            f"{self.API_BASE}/space/wbi/arc/search", params,
            use_wbi=True, retries=2,
        )
        # 策略2: 非签名接口
        if not data:
            data = self._request(
                f"{self.API_BASE}/space/arc/search", params,
                retries=2,
            )
        if not data:
            return [], 0

        return self._parse_video_list(data)

    def _parse_video_item(self, v: Dict[str, Any]) -> Dict[str, Any]:
        """将视频列表项 vlist item 解析为统一样式"""
        return {
            "bvid": v.get("bvid"),
            "title": v.get("title", ""),
            "description": v.get("description", ""),
            "created": v.get("created"),
            "length": v.get("length", ""),
            "play": v.get("play", 0) or 0,
            "comment": v.get("comment", 0) or 0,
            "typeid": v.get("typeid", 0) or 0,
            "typename": v.get("typename", ""),
            "video_review": v.get("video_review", 0) or 0,
        }

    def _parse_video_list(self, data: Dict[str, Any]):
        """解析 arc/search 接口返回，返回 (videos, total)"""
        vlist = data.get("data", {}).get("list", {}).get("vlist", [])
        page_info = data.get("data", {}).get("page", {})
        total = page_info.get("count", 0)
        videos = [self._parse_video_item(v) for v in vlist]
        return videos, total

    def _parse_video_detail(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """解析 view 接口返回为统一结构"""
        d = data.get("data", {})
        stat = d.get("stat", {})
        return {
            "bvid": d.get("bvid"),
            "aid": d.get("aid"),
            "title": d.get("title"),
            "description": d.get("desc"),
            "duration": d.get("duration"),
            "pubdate": d.get("pubdate"),
            "owner": {
                "mid": d.get("owner", {}).get("mid"),
                "name": d.get("owner", {}).get("name"),
            },
            "stat": {
                "view": stat.get("view", 0) or 0,
                "danmaku": stat.get("danmaku", 0) or 0,
                "reply": stat.get("reply", 0) or 0,
                "favorite": stat.get("favorite", 0) or 0,
                "coin": stat.get("coin", 0) or 0,
                "share": stat.get("share", 0) or 0,
                "like": stat.get("like", 0) or 0,
                "dislike": stat.get("dislike", 0) or 0,
            },
            "tname": d.get("tname", ""),
            "tid": d.get("tid", 0),
        }

    def get_videos_via_search(self, uid: str, up_name: str) -> List[Dict[str, Any]]:
        """通过搜索API获取视频列表（兜底方案）"""
        all_videos = []
        page = 1
        while True:
            params = {
                "search_type": "video",
                "keyword": up_name,
                "order": "pubdate",
                "page": page,
            }
            data = self._request(
                "https://api.bilibili.com/x/web-interface/search/type",
                params,
                headers={"Referer": "https://search.bilibili.com/"},
            )
            if not data:
                break
            results = data.get("data", {}).get("result", [])
            if not results:
                break
            for item in results:
                if str(item.get("mid")) != str(uid):
                    continue
                all_videos.append({
                    "bvid": item.get("bvid"),
                    "title": item.get("title", "").replace('<em class="keyword">', '').replace('</em>', ''),
                    "description": item.get("description", ""),
                    "created": item.get("pubdate"),
                    "length": item.get("duration", ""),
                    "play": item.get("play", 0) or 0,
                    "comment": item.get("review", 0) or 0,
                    "typeid": int(item.get("typeid", 0) or 0),
                    "typename": item.get("typename", ""),
                    "video_review": item.get("danmaku", 0) or 0,
                    # 搜索API额外互动数据（视频详情获取失败时的兜底）
                    "_search_like": item.get("like", 0) or 0,
                    "_search_favorites": item.get("favorites", 0) or 0,
                })
            num_pages = data.get("data", {}).get("numPages", 1)
            if page >= num_pages:
                break
            page += 1
            time.sleep(1)
        return all_videos

    def get_all_videos(self, uid: str, up_name: str = "",
                       max_videos: Optional[int] = None) -> List[Dict[str, Any]]:
        """获取UP主全部视频（自动选择最优策略）"""
        # 策略1: 标准分页接口
        first_page = self.get_video_list(uid, page=1)
        if first_page and isinstance(first_page, tuple):
            videos, total = first_page
            if videos:
                page = 2
                while len(videos) < total:
                    if max_videos and len(videos) >= max_videos:
                        break
                    result = self.get_video_list(uid, page=page)
                    if result and isinstance(result, tuple):
                        page_videos, _ = result
                        if not page_videos:
                            break
                        videos.extend(page_videos)
                    else:
                        break
                    page += 1
                    time.sleep(1)
                if max_videos:
                    videos = videos[:max_videos]
                return videos

        # 策略2: 搜索API兜底
        if not up_name:
            up_info = self.get_up_info(uid)
            up_name = up_info.get("name", "") if up_info else ""
        if up_name:
            videos = self.get_videos_via_search(uid, up_name)
            if max_videos:
                videos = videos[:max_videos]
            return videos

        return []

    def get_video_detail(self, bvid: str) -> Optional[Dict[str, Any]]:
        """获取视频详细信息（不需要WBI签名）"""
        cache_file = self._cache_path("video", bvid)
        cached = self._load_cache(cache_file, max_age=86400)
        if cached:
            return cached

        params = {"bvid": bvid}
        data = self._request(
            f"{self.API_BASE}/web-interface/view", params,
            retries=2, base_delay=2,
        )
        if not data:
            return None

        result = self._parse_video_detail(data)
        result["bvid"] = bvid
        self._save_cache(cache_file, result)
        return result

    def enrich_video_stat(self, video: Dict) -> Dict:
        """为视频补充stat字段（优先详情接口，兜底搜索数据）"""
        if video.get("stat") and video["stat"].get("view", 0) > 0:
            return video

        detail = self.get_video_detail(video.get("bvid"))
        if detail:
            video.update(detail)
            return video

        # 兜底：使用搜索API的数据
        if "_search_like" in video or video.get("play", 0) > 0:
            video["stat"] = {
                "view": video.get("play", 0),
                "danmaku": video.get("video_review", 0),
                "reply": video.get("comment", 0),
                "favorite": video.get("_search_favorites", 0),
                "coin": 0,
                "share": 0,
                "like": video.get("_search_like", 0),
            }
            if not video.get("pubdate"):
                video["pubdate"] = video.get("created")
            if not video.get("tname"):
                video["tname"] = video.get("typename", "")
            if not video.get("tid"):
                video["tid"] = video.get("typeid", 0)
        return video

    def clear_cache(self, uid: Optional[str] = None) -> None:
        """
        清除缓存目录下所有 JSON 缓存（含断点续传 checkpoint）。

        边界说明：
        - 缓存采用 TTL 自动过期（up_info 12h、video 24h），无需手动清理。
        - `--clear-cache` 用于强制刷新，保证拿到最新数据。
        - 视频详情缓存以 bvid 为键、无法按 uid 精确归属，因此显式清理时
          统一清空整个缓存目录，避免跨 UP 主残留脏数据。
        """
        if not os.path.exists(self.cache_dir):
            return
        removed = 0
        for f in os.listdir(self.cache_dir):
            if f.endswith('.json'):
                try:
                    os.remove(os.path.join(self.cache_dir, f))
                    removed += 1
                except OSError:
                    pass
        return removed
