#!/usr/bin/env python3
"""
Trae论坛用户数据提取脚本 v3

基于 Discourse JSON API 从 https://forum.trae.cn/ 提取指定用户的历史数据。
API端点：
  - 用户资料:  GET /u/{username}.json
  - 用户摘要:  GET /u/{username}/summary.json
  - 话题详情:  GET /t/{topic_id}.json
  - 帖子加载:  GET /t/{topic_id}/posts.json?post_ids[]=[...]
  - 搜索补充:  GET /search.json?q=@username
"""

import argparse
import html as html_lib
import json
import re
import sys
import time
from collections import Counter
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://forum.trae.cn"
REQUEST_DELAY = 0.5
MAX_RETRIES = 3
TIMEOUT = 30

TRUST_LEVEL_MAP = {0: "newuser", 1: "basic", 2: "member", 3: "regular", 4: "leader"}

# 中文停用词（用于高频词过滤）
_CN_STOP = frozenset(
    "的 了 是 在 我 有 和 就 不 人 都 一 上 也 很 到 说 要 去 你 会 着 看 好 自己 这 那 他 她 它 "
    "没 把 被 让 给 从 而 但 却 又 与 或 还 已 所 以 可 能 之 为 些 么 什 如 因 此 其 中 于 时 "
    "里 来 对 下 过 吗 吧 啊 呢 哦 嗯 啦 呀 哈 嘿 嘻 哎 噢".split()
)
_EN_STOP = frozenset(
    "the a an is are was were be been to of in for on with at by from it this that and or "
    "but not can do did has have had will would could should may might shall being its my "
    "your his her our their me him us them what which who how when where why if then than "
    "so no up out just about into more some very also only own same other new such each "
    "all both few most other".split()
)


def _create_session() -> requests.Session:
    """创建带自动重试的 HTTP 会话"""
    session = requests.Session()
    session.headers.update({
        "User-Agent": "TraeUserDistiller/3.0 (data extraction for persona skill generation)",
        "Accept": "application/json",
    })
    retry_strategy = Retry(
        total=MAX_RETRIES,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def _api_get(session: requests.Session, path: str, params: dict = None, _depth: int = 0) -> dict | None:
    """发起 API GET 请求，返回 JSON 或 None。429 限流自动重试（最多 3 次）"""
    url = urljoin(BASE_URL, path)
    try:
        resp = session.get(url, params=params, timeout=TIMEOUT)
        if resp.status_code == 404:
            print(f"  [404] 未找到: {path}")
            return None
        if resp.status_code == 429 and _depth < 3:
            wait = int(resp.headers.get("Retry-After", "10"))
            print(f"  [429] 限流，等待 {wait}s...（第 {_depth + 1}/3 次）")
            time.sleep(wait)
            return _api_get(session, path, params, _depth + 1)
        resp.raise_for_status()
        time.sleep(REQUEST_DELAY)
        return resp.json()
    except requests.RequestException as e:
        print(f"  [ERROR] 请求失败 {path}: {e}")
        return None


def _load_categories(session: requests.Session) -> dict[int, str]:
    """加载论坛分类映射（含子分类）"""
    cache: dict[int, str] = {}
    data = _api_get(session, "/categories.json")
    if not data:
        return cache
    for cat in data.get("category_list", {}).get("categories", []):
        cache[cat["id"]] = cat["name"]
        # Discourse 的子分类嵌套在 subcategory_list 中
        for sub in cat.get("subcategory_list", []):
            cache[sub["id"]] = sub["name"]
    return cache


def _clean_html(raw: str) -> str:
    """清理 Discourse cooked HTML 为纯文本（保护代码块内容）"""
    if not raw:
        return ""

    # 先提取代码块，防止内部 < > 被误删
    code_blocks: list[str] = []
    def _placeholder(m):
        idx = len(code_blocks)
        code_blocks.append(m.group(0))
        return f"\n__CODE_BLOCK_{idx}__\n"

    text = re.sub(r"<pre[^>]*>.*?</pre>", _placeholder, raw, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<code[^>]*>.*?</code>", _placeholder, text, flags=re.DOTALL | re.IGNORECASE)

    # HTML 实体解码
    text = html_lib.unescape(text)

    # 块级标签 → 换行
    text = re.sub(r"</?(p|div|li|h[1-6]|br|tr|blockquote)[^>]*>", "\n", text, flags=re.IGNORECASE)
    # 移除其余标签
    text = re.sub(r"<[^>]+>", "", text)
    # 清理多余空白
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n", "\n\n", text)

    # 还原代码块（转为纯文本格式）
    for i, block in enumerate(code_blocks):
        # 提取代码块中的纯文本
        inner = re.sub(r"<[^>]+>", "", html_lib.unescape(block))
        inner = re.sub(r"^\s*```.*?\n", "", inner)  # 移除可能的 markdown 标记
        text = text.replace(f"__CODE_BLOCK_{i}__", f"\n```\n{inner.strip()}\n```\n")

    return text.strip()


# ─── 数据提取函数 ───

def fetch_profile(session: requests.Session, username: str) -> dict:
    """获取用户资料"""
    data = _api_get(session, f"/u/{username}.json")
    if not data or "user" not in data:
        return {"username": username, "error": "用户不存在或请求失败"}

    u = data["user"]
    return {
        "username": u["username"],
        "user_id": u["id"],
        "name": u.get("name", "") or u["username"],
        "profile_url": f"{BASE_URL}/u/{username}/summary",
        "created_at": u.get("created_at", ""),
        "trust_level": TRUST_LEVEL_MAP.get(u.get("trust_level", 0), "unknown"),
        "trust_level_id": u.get("trust_level", 0),
        "title": u.get("title", ""),
        "bio": u.get("bio_raw", "") or "",
        "time_read_seconds": u.get("time_read", 0),
        "profile_views": u.get("profile_view_count", 0),
        "accepted_answers": u.get("accepted_answers", 0),
        "badges": u.get("badge_count", 0),
        "gamification_score": u.get("gamification_score", 0),
    }


def fetch_summary(session: requests.Session, username: str) -> dict:
    """获取用户摘要（含回复列表、参与话题、获赞等）"""
    data = _api_get(session, f"/u/{username}/summary.json")
    if not data or "user_summary" not in data:
        return {"topics": [], "replies": [], "stats": {}}

    summary = data["user_summary"]
    topics_raw = data.get("topics", [])
    replies_raw = summary.get("replies", [])

    replies = [
        {
            "post_number": r.get("post_number"),
            "like_count": r.get("like_count", 0),
            "created_at": r.get("created_at", ""),
            "topic_id": r.get("topic_id"),
        }
        for r in replies_raw
    ]

    topics = [
        {
            "id": t.get("id"),
            "title": t.get("title", ""),
            "slug": t.get("slug", ""),
            "posts_count": t.get("posts_count", 0),
            "category_id": t.get("category_id"),
            "like_count": t.get("like_count", 0),
            "created_at": t.get("created_at", ""),
            "has_accepted_answer": t.get("has_accepted_answer", False),
        }
        for t in topics_raw
    ]

    return {
        "topics": topics,
        "replies": replies,
        "stats": {
            "likes_given": summary.get("likes_given", 0),
            "likes_received": summary.get("likes_received", 0),
            "topics_entered": summary.get("topics_entered", 0),
            "posts_read_count": summary.get("posts_read_count", 0),
            "days_visited": summary.get("days_visited", 0),
            "topic_count": summary.get("topic_count", 0),
            "post_count": summary.get("post_count", 0),
            "solved_count": summary.get("solved_count", 0),
        },
        "top_categories": summary.get("top_categories", []),
        "most_liked_by": summary.get("most_liked_by_users", []),
        "most_liked_users": summary.get("most_liked_users", []),
        "most_replied_to": summary.get("most_replied_to_users", []),
    }


def _parse_like_count(actions_summary: list | None) -> int:
    """从 Discourse actions_summary 中提取点赞数（id=2 为 like）"""
    if not actions_summary:
        return 0
    return next((a.get("count", 0) for a in actions_summary if a.get("id") == 2), 0)


def fetch_topic_detail(session: requests.Session, topic_id: int) -> dict | None:
    """获取话题详情（含首帖内容和帖子流）"""
    data = _api_get(session, f"/t/{topic_id}.json")
    if not data:
        return None

    posts = data.get("post_stream", {}).get("posts", [])
    first_post = posts[0] if posts else {}

    return {
        "id": data.get("id"),
        "title": data.get("title", ""),
        "slug": data.get("slug", ""),
        "category_id": data.get("category_id"),
        "tags": [t.get("name", "") for t in data.get("tags", [])],
        "views": data.get("views", 0),
        "like_count": data.get("like_count", 0),
        "reply_count": data.get("reply_count", 0),
        "posts_count": data.get("posts_count", 0),
        "created_at": data.get("created_at", ""),
        "has_accepted_answer": data.get("has_accepted_answer", False),
        "first_post": {
            "username": first_post.get("username", ""),
            "cooked": first_post.get("cooked", ""),
            "created_at": first_post.get("created_at", ""),
            "like_count": _parse_like_count(first_post.get("actions_summary")),
        },
        "stream": data.get("post_stream", {}).get("stream", []),
    }


def fetch_user_posts_from_topic(
    session: requests.Session, topic_id: int, username: str, stream_ids: list[int]
) -> list[dict]:
    """从话题帖子流中按需加载并提取指定用户的帖子（GET 请求）"""
    if not stream_ids:
        return []

    user_posts: list[dict] = []
    batch_size = 20

    for i in range(0, len(stream_ids), batch_size):
        batch = stream_ids[i : i + batch_size]
        # Discourse 使用 GET 请求加载帖子流中的指定帖子
        params = {"post_ids[]": batch}
        data = _api_get(session, f"/t/{topic_id}/posts.json", params=params)
        if not data:
            continue
        for p in data.get("post_stream", {}).get("posts", []):
            if p.get("username") == username:
                user_posts.append({
                    "post_id": p.get("id"),
                    "post_number": p.get("post_number"),
                    "cooked": p.get("cooked", ""),
                    "created_at": p.get("created_at", ""),
                    "like_count": _parse_like_count(p.get("actions_summary")),
                    "reply_count": p.get("reply_count", 0),
                    "reads": p.get("reads", 0),
                })

    return user_posts


def search_user_posts(session: requests.Session, username: str, page: int = 1) -> list[dict]:
    """通过搜索 API 补充获取用户帖子"""
    data = _api_get(session, "/search.json", params={
        "q": f"@{username}",
        "page": page,
        "order": "latest",
    })
    if not data:
        return []

    posts = []
    for p in data.get("posts", []):
        if p.get("username") == username:
            posts.append({
                "post_id": p.get("id"),
                "topic_id": p.get("topic_id"),
                "blurb": p.get("blurb", ""),
                "like_count": p.get("like_count", 0),
                "created_at": p.get("created_at", ""),
                "post_number": p.get("post_number"),
            })
    return posts


# ─── 风格分析 ───

def _analyze_text_segment(text: str) -> dict:
    """对单段文本做基础风格分析，返回子集指标"""
    if not text or len(text) < 10:
        return None

    cjk_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    en_words = len(re.findall(r"[a-zA-Z]+", text))
    total_words = cjk_chars + en_words
    sentences = [s.strip() for s in re.split(r"[。！？.!?]+", text) if s.strip()]
    avg_sentence_len = total_words / len(sentences) if sentences else 0

    formal_markers = re.findall(
        r"(?:因此|然而|综上所述|由此可见|总而言之|首先|其次|最后"
        r"|基于|根据|鉴于|故而|从而|进而|诚然|毋庸置疑"
        r"|therefore|consequently|furthermore|nevertheless|thus|hence)",
        text, re.IGNORECASE,
    )
    casual_markers = re.findall(
        r"(?:哈哈哈|嘿嘿嘿|呵呵呵|哇塞|嘻嘻嘻|咯咯|嘞嘞"
        r"|\blol\b|\bhaha\b|\bomg\b|\bwtf\b"
        r"|yyds|绝了|太强了|666|2333|233)",
        text, re.IGNORECASE,
    )
    formal_score = len(formal_markers) / max(len(formal_markers) + len(casual_markers), 1)

    emojis = re.findall(
        r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF"
        r"\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U0000FE00-\U0000FE0F"
        r"\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF"
        r"\U00002600-\U000026FF\U00002700-\U000027BF]",
        text,
    )

    particle_patterns = {
        "啊": "啊", "呢": "呢", "吧": "吧", "吗": "吗", "嘛": "嘛",
        "哦": "哦", "哈": "哈", "嘿": "嘿", "嘻": "嘻", "呀": "呀",
        "啦": "啦", "哎": "哎", "嗯": "嗯", "噢": "噢",
    }
    particle_counts = {name: text.count(pat) for name, pat in particle_patterns.items()}

    return {
        "total_chars": len(text),
        "total_words": total_words,
        "avg_sentence_length": round(avg_sentence_len, 1),
        "formal_score": round(formal_score, 2),
        "emoji_count": len(emojis),
        "particle_counts": particle_counts,
        "total_particles": sum(particle_counts.values()),
    }


def analyze_writing_style(topics: list[dict], posts: list[dict]) -> dict:
    """多维度分析用户写作风格（含分场景子分析）"""

    all_texts = []
    for t in topics:
        c = t.get("content_clean", "")
        if c:
            all_texts.append(c)
    for p in posts:
        c = p.get("content_clean", "")
        if c:
            all_texts.append(c)

    full_text = "\n".join(all_texts)
    total_chars = len(full_text)

    if total_chars < 10:
        return _empty_style_analysis()

    # ── 分场景子分析 ──
    topic_texts = [t.get("content_clean", "") for t in topics if t.get("content_clean")]
    reply_texts = [p.get("content_clean", "") for p in posts if p.get("content_clean")]

    topic_segments = [_analyze_text_segment(t) for t in topic_texts]
    reply_segments = [_analyze_text_segment(r) for r in reply_texts]
    topic_segments = [s for s in topic_segments if s]
    reply_segments = [s for s in reply_segments if s]

    scene_analysis = {}
    if topic_segments:
        scene_analysis["topic_style"] = _aggregate_segments(topic_segments)
    if reply_segments:
        scene_analysis["reply_style"] = _aggregate_segments(reply_segments)

    # ── 基础统计 ──
    cjk_chars = len(re.findall(r"[\u4e00-\u9fff]", full_text))
    en_words = len(re.findall(r"[a-zA-Z]+", full_text))
    total_words = cjk_chars + en_words

    sentences = [s.strip() for s in re.split(r"[。！？.!?]+", full_text) if s.strip()]
    avg_sentence_len = total_words / len(sentences) if sentences else 0

    paragraphs = [p.strip() for p in full_text.split("\n") if p.strip()]
    avg_paragraph_len = total_chars / len(paragraphs) if paragraphs else 0

    # ── 标点符号习惯 ──
    punctuation = {
        "exclamation": len(re.findall(r"[!！]", full_text)),
        "question": len(re.findall(r"[?？]", full_text)),
        "ellipsis": len(re.findall(r"[…·]{1,3}|\.{3}", full_text)),
        "comma": len(re.findall(r"[,，]", full_text)),
        "period": len(re.findall(r"[。.]", full_text)),
    }
    total_punct = sum(punctuation.values()) or 1
    punct_ratios = {k: round(v / total_punct, 3) for k, v in punctuation.items()}

    # ── 表情符号 ──
    emojis = re.findall(
        r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF"
        r"\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U0000FE00-\U0000FE0F"
        r"\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF"
        r"\U00002600-\U000026FF\U00002700-\U000027BF]",
        full_text,
    )
    emoji_rate = len(emojis) / max(total_chars / 100, 1)

    # ── 语气词频率 ──
    particle_patterns = {
        "啊": "啊", "呢": "呢", "吧": "吧", "吗": "吗", "嘛": "嘛",
        "哦": "哦", "哈": "哈", "嘿": "嘿", "嘻": "嘻", "呀": "呀",
        "啦": "啦", "哎": "哎", "嗯": "嗯", "噢": "噢",
    }
    particle_counts = {name: full_text.count(pat) for name, pat in particle_patterns.items()}
    total_particles = sum(particle_counts.values())
    top_particles = sorted(particle_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    # ── 正式度评分（0-1）──
    # 使用词边界匹配避免子串误匹配
    formal_markers = re.findall(
        r"(?:因此|然而|综上所述|由此可见|总而言之|首先|其次|最后"
        r"|基于|根据|鉴于|故而|从而|进而|诚然|毋庸置疑"
        r"|therefore|consequently|furthermore|nevertheless|thus|hence)",
        full_text, re.IGNORECASE,
    )
    # 非正式标记：使用独立匹配避免"牛"误匹配"蜗牛"等
    casual_markers = re.findall(
        r"(?:哈哈哈|嘿嘿嘿|呵呵呵|哇塞|嘻嘻嘻|咯咯|嘞嘞"
        r"|\blol\b|\bhaha\b|\bomg\b|\bwtf\b"
        r"|yyds|绝了|太强了|666|2333|233)",
        full_text, re.IGNORECASE,
    )
    formal_score = len(formal_markers) / max(len(formal_markers) + len(casual_markers), 1)

    # ── 表达风格（频率）──
    expression = {
        "examples_rate": len(re.findall(r"(?:比如|例如|举个例子|比如说)", full_text)),
        "questions_rate": punctuation["question"],
        "emphasis_rate": punctuation["exclamation"],
        "structure_rate": len(re.findall(r"(?:第一|第二|第三|首先|其次|最后|一是|二是)", full_text)),
        "humility_rate": len(re.findall(r"(?:可能|也许|大概|个人看法|不一定|仅供参考)", full_text)),
        "code_blocks": len(re.findall(r"```", full_text)) // 2,
        "quotes_usage": len(re.findall(r"[「」""''']", full_text)),
        "mentions": len(re.findall(r"@\w+", full_text)),
    }

    # ── Markdown 使用习惯 ──
    markdown_habits = {
        "uses_lists": bool(re.search(r"^\s*[-*+]\s", full_text, re.MULTILINE)),
        "uses_code_blocks": bool(re.search(r"```", full_text)),
        "uses_bold": bool(re.search(r"\*\*[^*]+\*\*", full_text)),
        "uses_blockquote": bool(re.search(r"^>", full_text, re.MULTILINE)),
        "uses_headers": bool(re.search(r"^#{1,6}\s", full_text, re.MULTILINE)),
        "uses_links": bool(re.search(r"https?://", full_text)),
    }

    # ── 回复长度分布 ──
    post_lengths = [len(p.get("content_clean", "")) for p in posts if p.get("content_clean")]
    length_distribution = _analyze_length_distribution(post_lengths)

    # ── 高频词汇（中文 bigram + 英文单词）──
    high_freq_terms = _extract_high_freq_terms(full_text)

    return {
        "total_chars": total_chars,
        "cjk_chars": cjk_chars,
        "en_words": en_words,
        "total_words": total_words,
        "sentence_count": len(sentences),
        "avg_sentence_length": round(avg_sentence_len, 1),
        "avg_paragraph_length": round(avg_paragraph_len, 1),
        "emoji_count": len(emojis),
        "emoji_rate": round(emoji_rate, 3),
        "particle_counts": particle_counts,
        "total_particles": total_particles,
        "top_particles": top_particles,
        "formal_score": round(formal_score, 2),
        "formality": "formal" if formal_score > 0.65 else "casual" if formal_score < 0.35 else "neutral",
        "punctuation": punctuation,
        "punct_ratios": punct_ratios,
        "expression": expression,
        "markdown_habits": markdown_habits,
        "length_distribution": length_distribution,
        "high_freq_terms": high_freq_terms,
        "scene_analysis": scene_analysis,
    }


def _extract_high_freq_terms(full_text: str) -> list[str]:
    """提取高频词汇：中文 bigram + 英文单词，过滤停用词"""
    if not full_text:
        return []

    # 中文 bigram（2字词组），比 2-4 字 N-gram 更精准
    cjk_chars = re.findall(r"[\u4e00-\u9fff]", full_text)
    cjk_bigrams = [cjk_chars[i] + cjk_chars[i + 1] for i in range(len(cjk_chars) - 1)]
    cjk_bigrams = [w for w in cjk_bigrams if w not in _CN_STOP and all(c not in _CN_STOP for c in w)]

    # 英文单词（≥3字母，过滤停用词）
    en_words = [
        w.lower() for w in re.findall(r"[a-zA-Z]{3,}", full_text)
        if w.lower() not in _EN_STOP
    ]

    cjk_counter = Counter(cjk_bigrams)
    en_counter = Counter(en_words)

    top_cjk = [w for w, _ in cjk_counter.most_common(10)]
    top_en = [w for w, _ in en_counter.most_common(5)]
    return top_cjk + top_en


def _analyze_length_distribution(lengths: list[int]) -> dict:
    """分析回复长度分布"""
    if not lengths:
        return {"short": 0, "medium": 0, "long": 0, "avg": 0, "max": 0, "min": 0}

    short = sum(1 for l in lengths if l < 50)
    medium = sum(1 for l in lengths if 50 <= l < 200)
    long = sum(1 for l in lengths if l >= 200)
    total = len(lengths)

    return {
        "short": short,
        "medium": medium,
        "long": long,
        "short_ratio": round(short / total, 2),
        "medium_ratio": round(medium / total, 2),
        "long_ratio": round(long / total, 2),
        "avg": round(sum(lengths) / total, 1),
        "max": max(lengths),
        "min": min(lengths),
    }


def _aggregate_segments(segments: list[dict]) -> dict:
    """聚合多个文本片段的分析结果为平均值"""
    if not segments:
        return {}
    n = len(segments)
    total_chars = sum(s["total_chars"] for s in segments)
    return {
        "sample_count": n,
        "total_chars": total_chars,
        "avg_words": round(sum(s["total_words"] for s in segments) / n, 1),
        "avg_sentence_length": round(sum(s["avg_sentence_length"] for s in segments) / n, 1),
        "avg_formal_score": round(sum(s["formal_score"] for s in segments) / n, 2),
        "avg_emoji_count": round(sum(s["emoji_count"] for s in segments) / n, 1),
        "avg_particles": round(sum(s["total_particles"] for s in segments) / n, 1),
        # 合并语气词取 top 3
        "top_particles": sorted(
            Counter({k: v for s in segments for k, v in s["particle_counts"].items()}).items(),
            key=lambda x: x[1], reverse=True
        )[:3],
    }


def _empty_style_analysis() -> dict:
    """返回空的风格分析结果"""
    return {
        "total_chars": 0, "cjk_chars": 0, "en_words": 0, "total_words": 0,
        "sentence_count": 0, "avg_sentence_length": 0, "avg_paragraph_length": 0,
        "emoji_count": 0, "emoji_rate": 0, "particle_counts": {}, "total_particles": 0,
        "top_particles": [], "formal_score": 0.5, "formality": "neutral",
        "punctuation": {}, "punct_ratios": {}, "expression": {}, "markdown_habits": {},
        "length_distribution": {}, "high_freq_terms": [], "scene_analysis": {},
    }


# ─── 主流程 ───

def extract_user_data(username: str, output_dir: str = ".", max_topics: int = 50) -> dict:
    """执行完整的数据提取流程"""
    session = _create_session()
    cat_cache = _load_categories(session)

    def cat_name(cat_id: int) -> str:
        return cat_cache.get(cat_id, f"分类#{cat_id}")

    result = {
        "username": username,
        "forum_url": BASE_URL,
        "extracted_at": datetime.now().isoformat(),
        "schema_version": "3.0",
        "profile": {},
        "topics": [],
        "posts": [],
        "stats": {"total_topics": 0, "total_posts": 0, "total_words": 0},
        "style_analysis": {},
    }

    # 1. 获取用户资料
    print(f"[1/5] 获取用户资料 @{username}...")
    result["profile"] = fetch_profile(session, username)
    if "error" in result["profile"]:
        print(f"  ✗ {result['profile']['error']}")
        return result
    print(f"  ✓ ID:{result['profile']['user_id']} 等级:{result['profile']['trust_level']}")

    # 2. 获取用户摘要
    print("[2/5] 获取用户摘要...")
    summary = fetch_summary(session, username)
    summary_topics = summary.get("topics", [])
    summary_replies = summary.get("replies", [])
    summary_stats = summary.get("stats", {})
    print(f"  ✓ 话题:{len(summary_topics)} 回复:{len(summary_replies)}")

    # 3. 获取话题详情（建立缓存避免重复请求）
    print(f"[3/5] 获取话题详情（最多 {max_topics} 个）...")
    topics_detail: list[dict] = []
    topic_cache: dict[int, dict] = {}  # topic_id → detail

    for t in summary_topics[:max_topics]:
        tid = t.get("id")
        if not tid or tid in topic_cache:
            continue
        detail = fetch_topic_detail(session, tid)
        if detail:
            topic_cache[tid] = detail
            detail["category_name"] = cat_name(detail.get("category_id", 0))
            first_post = detail.pop("first_post", {})
            detail["content_clean"] = _clean_html(first_post.get("cooked", ""))
            detail["first_post_likes"] = first_post.get("like_count", 0)
            detail["is_original"] = first_post.get("username") == username
            topics_detail.append(detail)
            print(f"  ✓ {detail['title'][:50]}")

    # 4. 获取用户回复内容（复用话题缓存）
    print("[4/5] 获取回复内容...")
    all_posts: list[dict] = []
    seen_post_ids: set[int] = set()

    for r in summary_replies:
        tid = r.get("topic_id")
        if not tid:
            continue
        # 复用缓存，避免重复请求
        if tid not in topic_cache:
            detail = fetch_topic_detail(session, tid)
            if detail:
                topic_cache[tid] = detail
        detail = topic_cache.get(tid)
        if not detail:
            continue

        stream = detail.get("stream", [])
        user_posts = fetch_user_posts_from_topic(session, tid, username, stream)
        for p in user_posts:
            pid = p.get("post_id")
            if pid and pid not in seen_post_ids:
                seen_post_ids.add(pid)
                p["topic_id"] = tid
                p["topic_title"] = detail.get("title", "")
                p["content_clean"] = _clean_html(p.pop("cooked", ""))
                all_posts.append(p)

    # 通过搜索 API 补充
    print("  搜索补充...")
    search_exhausted = False
    for page in range(1, 4):
        if search_exhausted:
            break
        search_results = search_user_posts(session, username, page)
        if not search_results:
            search_exhausted = True
            break
        for sr in search_results:
            pid = sr.get("post_id")
            if pid and pid not in seen_post_ids:
                seen_post_ids.add(pid)
                sr["content_clean"] = sr.pop("blurb", "")
                sr["topic_title"] = ""
                all_posts.append(sr)
        # Discourse 搜索每页通常返回 20-50 条，少于 5 条视为无更多结果
        if len(search_results) < 5:
            search_exhausted = True

    all_posts.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    print(f"  ✓ 共 {len(all_posts)} 条回复（缓存命中 {len(topic_cache) - len(topics_detail)} 个话题）")

    # 5. 风格分析
    print("[5/5] 分析写作风格...")
    result["topics"] = topics_detail
    result["posts"] = all_posts
    result["style_analysis"] = analyze_writing_style(topics_detail, all_posts)

    result["stats"] = {
        "total_topics": len(topics_detail),
        "total_posts": len(all_posts),
        "total_words": result["style_analysis"].get("total_words", 0),
        "likes_received": summary_stats.get("likes_received", 0),
        "likes_given": summary_stats.get("likes_given", 0),
        "accepted_answers": summary_stats.get("solved_count", 0),
        "days_visited": summary_stats.get("days_visited", 0),
        "posts_read": summary_stats.get("posts_read_count", 0),
    }

    print(f"\n{'='*50}")
    print(f"提取完成! 话题:{result['stats']['total_topics']} "
          f"回复:{result['stats']['total_posts']} "
          f"字数:{result['stats']['total_words']} "
          f"获赞:{result['stats']['likes_received']}")
    print(f"{'='*50}")

    return result


def save_to_file(data: dict, output_dir: str) -> Path:
    """保存数据到 JSON 文件"""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    username = data.get("username", "unknown")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = out / f"trae_user_{username}_{ts}.json"

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"数据已保存: {filepath}")
    return filepath


def main():
    parser = argparse.ArgumentParser(
        description="从 Trae 论坛提取用户历史数据（基于 Discourse API）",
    )
    parser.add_argument("username", help="目标论坛用户名")
    parser.add_argument("--output", "-o", default=".", help="输出目录")
    parser.add_argument("--max-topics", type=int, default=50, help="最大提取话题数")
    parser.add_argument("--generate", "-g", action="store_true",
                        help="提取后自动生成个性化技能（一键模式）")
    args = parser.parse_args()

    if not args.username or not re.match(r"^[\w-]+$", args.username):
        print("错误: 用户名只能包含字母、数字、下划线和连字符")
        sys.exit(1)

    data = extract_user_data(args.username, args.output, args.max_topics)
    json_path = save_to_file(data, args.output)

    total = data["stats"]["total_topics"] + data["stats"]["total_posts"]
    if total < 3:
        print(f"\n⚠ 警告: 仅提取到 {total} 条内容，数据量不足以生成有效人格技能")
        sys.exit(1)

    # 一键模式：自动调用生成器
    if args.generate:
        print("\n[一键模式] 自动生成个性化技能...")
        # 延迟导入避免循环依赖
        from generate_persona_skill import PersonaSkillGenerator
        gen = PersonaSkillGenerator(str(json_path), args.output)
        result = gen.generate()
        if not result:
            print("技能生成失败")
            sys.exit(1)


if __name__ == "__main__":
    main()
