#!/usr/bin/env python3
"""
互联网缩写解析器
支持多领域缩写识别、搜索验证、多义性排序、搜索结果回填
"""

import re
import json
import sys
import os
import time
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cache')
CACHE_FILE = os.path.join(CACHE_DIR, 'search_cache.json')
CACHE_TTL = 30 * 24 * 3600  # 30 天过期

class SearchCache:
    """搜索结果缓存，持久化到 JSON 文件"""

    def __init__(self):
        self.cache: Dict[str, Dict] = {}
        self._load()

    def _load(self):
        """从文件加载缓存"""
        try:
            if os.path.exists(CACHE_FILE):
                with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                    self.cache = json.load(f)
                # 清理过期条目
                self._cleanup()
        except (json.JSONDecodeError, IOError):
            self.cache = {}

    def _save(self):
        """保存缓存到文件"""
        try:
            os.makedirs(CACHE_DIR, exist_ok=True)
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except IOError:
            pass

    def _cleanup(self):
        """清理过期缓存"""
        now = time.time()
        expired = [
            key for key, val in self.cache.items()
            if now - val.get('timestamp', 0) > CACHE_TTL
        ]
        for key in expired:
            del self.cache[key]
        if expired:
            self._save()

    def get(self, abbreviation: str) -> Optional[List[Dict]]:
        """获取缓存的搜索结果"""
        key = abbreviation.lower()
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry.get('timestamp', 0) <= CACHE_TTL:
                return entry.get('findings', [])
        return None

    def put(self, abbreviation: str, findings: List[Dict]):
        """缓存搜索结果"""
        key = abbreviation.lower()
        self.cache[key] = {
            'findings': findings,
            'timestamp': time.time(),
        }
        self._save()

    def has(self, abbreviation: str) -> bool:
        """检查是否有有效缓存"""
        return self.get(abbreviation) is not None

class Domain(Enum):
    ENTERTAINMENT = "entertainment"
    GAMING = "gaming"
    LIFESTYLE = "lifestyle"
    TECH = "tech"
    ACADEMIC = "academic"
    ANIME = "anime"
    FINANCE = "finance"
    UNKNOWN = "unknown"

DOMAIN_CN = {
    "entertainment": "娱乐圈",
    "gaming": "游戏圈",
    "lifestyle": "生活/网络",
    "tech": "科技/互联网",
    "academic": "学术/教育",
    "anime": "动漫/二次元",
    "finance": "金融/商业",
    "unknown": "未知",
}

DOMAIN_KEYWORDS = {
    Domain.ENTERTAINMENT: ["娱乐", "饭圈", "明星", "偶像", "粉丝", "追星", "综艺", "选秀"],
    Domain.GAMING: ["游戏", "电竞", "游戏圈", "开黑", "副本", "排位", "段位"],
    Domain.LIFESTYLE: ["生活", "日常", "聊天", "网络", "社交", "微博", "朋友圈"],
    Domain.TECH: ["科技", "编程", "开发", "代码", "技术", "互联网", "工作", "IT"],
    Domain.ANIME: ["动漫", "二次元", "番剧", "漫画", "cos", "acg", "宅"],
    Domain.FINANCE: ["金融", "股票", "基金", "投资", "财经", "币圈", "交易"],
}

@dataclass
class SlangEntry:
    abbreviation: str
    full_form: str
    meaning: str
    domain: Domain
    confidence: float
    examples: List[str]
    source: str = "builtin"
    notes: Optional[str] = None

class SlangDatabase:
    def __init__(self):
        self.entries: Dict[str, List[SlangEntry]] = {}
        self._load_builtin_data()

    def _load_builtin_data(self):
        """从 scripts/slang_db.json 加载词条，若不存在则回退到内置精简版"""
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'slang_db.json')
        domain_map = {d.value: d for d in Domain}

        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    db = json.load(f)
                for item in db.get('entries', []):
                    domain = domain_map.get(item.get('domain', 'unknown'), Domain.UNKNOWN)
                    entry = SlangEntry(
                        abbreviation=item['abbreviation'],
                        full_form=item['full_form'],
                        meaning=item['meaning'],
                        domain=domain,
                        confidence=item.get('confidence', 0.7),
                        examples=item.get('examples', []),
                        source=item.get('source', 'builtin'),
                        notes=item.get('notes'),
                    )
                    abbr_lower = entry.abbreviation.lower()
                    if abbr_lower not in self.entries:
                        self.entries[abbr_lower] = []
                    self.entries[abbr_lower].append(entry)
                return
            except (json.JSONDecodeError, IOError, KeyError):
                pass

        # JSON 不存在时的回退精简词库
        fallback = [
            ("yyds", "永远的神", "表示某人/某物很厉害", Domain.ENTERTAINMENT, 0.95, ["这首歌真是yyds！"]),
            ("xswl", "笑死我了", "表示非常好笑", Domain.ENTERTAINMENT, 0.95, ["这个段子xswl"]),
            ("gg", "good game", "游戏结束/认输", Domain.GAMING, 0.9, ["gg，这局输了"]),
            ("op", "overpowered", "太强/超模", Domain.GAMING, 0.9, ["这个英雄太op了"]),
            ("btw", "by the way", "顺便说一下", Domain.LIFESTYLE, 0.95, ["btw，你吃饭了吗"]),
            ("api", "application programming interface", "应用程序接口", Domain.TECH, 0.95, ["调用api"]),
        ]
        for data in fallback:
            entry = SlangEntry(*data)
            abbr_lower = entry.abbreviation.lower()
            if abbr_lower not in self.entries:
                self.entries[abbr_lower] = []
            self.entries[abbr_lower].append(entry)


    def lookup(self, abbreviation: str) -> List[SlangEntry]:
        return self.entries.get(abbreviation.lower(), [])

    def add_entry(self, entry: SlangEntry):
        abbr_lower = entry.abbreviation.lower()
        if abbr_lower not in self.entries:
            self.entries[abbr_lower] = []
        self.entries[abbr_lower].append(entry)

    def add_from_search(self, abbreviation: str, full_form: str, meaning: str,
                        domain: Domain, confidence: float, examples: List[str],
                        source: str = "web_search"):
        """从搜索结果添加新词条"""
        entry = SlangEntry(
            abbreviation=abbreviation, full_form=full_form, meaning=meaning,
            domain=domain, confidence=confidence, examples=examples, source=source
        )
        self.add_entry(entry)

class SlangDecoder:
    def __init__(self):
        self.db = SlangDatabase()
        self.cache = SearchCache()

    def extract_abbreviations(self, text: str) -> List[str]:
        # 输入长度限制：超过 500 字符截断
        MAX_INPUT_LEN = 500
        if len(text) > MAX_INPUT_LEN:
            text = text[:MAX_INPUT_LEN]

        # 匹配纯字母 2-10 位（覆盖 tsundere/yandere/stablecoin 等）+ 混合数字字母（如 u1s1, k8s）
        pattern = r'[a-zA-Z]{2,10}|[a-zA-Z][0-9][a-zA-Z0-9]{0,4}'
        matches = re.findall(pattern, text)
        common_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'had', 'her',
            'was', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its',
            'may', 'new', 'now', 'old', 'see', 'two', 'who', 'boy', 'did', 'she',
            'use', 'way', 'many', 'oil', 'sit', 'set', 'run', 'eat', 'far', 'sea',
            'eye', 'ago', 'off', 'too', 'any', 'try', 'ask', 'end', 'why', 'let',
            'put', 'own', 'tell', 'very', 'when', 'much', 'there', 'their', 'what',
            'said', 'each', 'which', 'will', 'about', 'could', 'other', 'after',
            'first', 'never', 'these', 'think', 'where', 'being', 'every', 'great',
            'might', 'shall', 'still', 'those', 'while', 'this', 'that', 'with',
            'have', 'from', 'they', 'been', 'were', 'time', 'than', 'them', 'into',
            'just', 'like', 'over', 'also', 'back', 'only', 'know', 'take', 'year',
            'good', 'some', 'come', 'make', 'well', 'work', 'life', 'even', 'more',
            'want', 'here', 'look', 'down', 'most', 'long', 'last', 'find', 'give',
            'does', 'made', 'part', 'such', 'keep', 'call', 'came', 'need', 'feel',
            'seem', 'turn', 'hand', 'sure', 'upon', 'head', 'help', 'home', 'side',
            'move', 'both', 'five', 'once', 'same', 'must', 'name', 'left', 'done',
            'open', 'case', 'show', 'live', 'play', 'went', 'told', 'seen', 'hear',
            'talk', 'soon', 'read', 'stop', 'face', 'fact', 'land', 'line', 'kind',
            'next', 'word', 'thing', 'world', 'house', 'night', 'found', 'thought',
            'went', 'story', 'point', 'right', 'number', 'place', 'small', 'water',
            'young', 'learn', 'change', 'light', 'power', 'large', 'until', 'group',
            'began', 'often', 'later', 'start', 'close', 'question', 'against',
            'high', 'school', 'every', 'leave', 'family', 'city', 'tree', 'cross',
            'in', 'on', 'at', 'to', 'of', 'by', 'up', 'or', 'an', 'if', 'so',
            'do', 'no', 'go', 'be', 'he', 'we', 'me', 'it', 'am', 'as', 'is',
            'us', 'my', 'vs', 'ie', 'eg',
            # 7-10 字母常见词
            'about', 'after', 'again', 'being', 'below', 'could', 'doing', 'during',
            'every', 'first', 'found', 'given', 'going', 'great', 'having', 'help',
            'house', 'large', 'later', 'least', 'learn', 'never', 'often', 'other',
            'place', 'plant', 'point', 'right', 'since', 'small', 'sound', 'still',
            'story', 'study', 'taken', 'their', 'there', 'these', 'thing', 'think',
            'those', 'three', 'under', 'until', 'water', 'where', 'which', 'while',
            'world', 'would', 'write', 'above', 'along', 'among', 'begin', 'black',
            'bring', 'build', 'carry', 'catch', 'cause', 'check', 'child', 'choose',
            'class', 'clean', 'clear', 'climb', 'color', 'cover', 'cross', 'dance',
            'doubt', 'dream', 'drink', 'drive', 'early', 'earth', 'eight', 'enjoy',
            'enter', 'equal', 'event', 'field', 'fight', 'final', 'force', 'front',
            'fruit', 'guess', 'happy', 'heart', 'heavy', 'horse', 'image', 'inner',
            'issue', 'knife', 'known', 'label', 'laugh', 'layer', 'level', 'local',
            'lower', 'lucky', 'magic', 'major', 'march', 'match', 'metal', 'model',
            'money', 'month', 'moral', 'music', 'night', 'noise', 'north', 'noted',
            'offer', 'order', 'outer', 'owner', 'paint', 'paper', 'party', 'peace',
            'phone', 'photo', 'piano', 'piece', 'pilot', 'pitch', 'pixel', 'plain',
            'plane', 'plate', 'plaza', 'pound', 'press', 'price', 'pride', 'prime',
            'prince','proof', 'proud', 'queen', 'quick', 'quiet', 'quite', 'radio',
            'raise', 'range', 'rapid', 'reach', 'ready', 'reply', 'ridge', 'river',
            'robot', 'roger', 'round', 'route', 'royal', 'rural', 'scale', 'scene',
            'scope', 'score', 'sense', 'serve', 'seven', 'share', 'sharp', 'sheet',
            'shift', 'shine', 'shirt', 'shock', 'shore', 'short', 'sight', 'since',
            'sixty', 'skill', 'sleep', 'slide', 'smart', 'smile', 'smoke', 'solar',
            'solid', 'solve', 'sorry', 'south', 'space', 'spare', 'speak', 'speed',
            'spend', 'spice', 'split', 'sport', 'squad', 'staff', 'stage', 'stake',
            'stand', 'start', 'state', 'steam', 'steel', 'steep', 'stick', 'stock',
            'stone', 'store', 'storm', 'story', 'strip', 'stuck', 'style', 'sugar',
            'suite', 'super', 'sweet', 'swing', 'table', 'taste', 'teach', 'theme',
            'thick', 'tiger', 'tight', 'tired', 'title', 'today', 'token', 'total',
            'touch', 'tough', 'tower', 'track', 'trade', 'train', 'trait', 'treat',
            'trend', 'trial', 'tribe', 'trick', 'truck', 'truly', 'trust', 'truth',
            'twice', 'twist', 'uncle', 'under', 'union', 'unite', 'upper', 'upset',
            'urban', 'usual', 'valid', 'value', 'video', 'virus', 'visit', 'vital',
            'vocal', 'voice', 'watch', 'wheel', 'where', 'white', 'whole', 'whose',
            'woman', 'worse', 'worst', 'worth', 'wound', 'write', 'wrong', 'youth',
            'zero', 'zone',
            'hard', 'really', 'since', 'before', 'early', 'body', 'state',
            'white', 'black', 'red', 'blue', 'best', 'door', 'between',
            'while', 'again', 'car', 'order', 'paper', 'children',
            'plan', 'quite', 'class', 'music', 'mind', 'today', 'money',
            'bring', 'happen', 'stand', 'room', 'book', 'map', 'air', 'write',
            'table', 'river', 'second', 'fire', 'watch', 'listen',
            'build', 'spend', 'grow', 'low', 'true', 'cold', 'dog', 'top',
            'road', 'mark', 'rock', 'short', 'food', 'love', 'girl', 'person',
            'art', 'bird', 'fish', 'mountain', 'sing', 'color', 'ball',
            # 补充常见 3-4 字母单词
            'can', 'may', 'yet', 'own', 'few', 'six', 'ten', 'big', 'bit',
            'cut', 'dry', 'eat', 'far', 'fit', 'fly', 'gap', 'god', 'gun',
            'hat', 'hit', 'hot', 'ill', 'job', 'joy', 'key', 'kid', 'lab',
            'law', 'lay', 'led', 'leg', 'lie', 'lip', 'log', 'lot', 'low',
            'met', 'mix', 'net', 'nor', 'odd', 'oil', 'pay', 'per', 'pie',
            'pin', 'pot', 'raw', 'row', 'sad', 'sat', 'saw', 'son', 'tip',
            'toe', 'ton', 'trip', 'van', 'war', 'win', 'yes', 'yet', 'zoo',
            'area', 'army', 'baby', 'base', 'body', 'born', 'camp', 'card',
            'care', 'cash', 'cell', 'chip', 'club', 'coat', 'code', 'cold',
            'copy', 'core', 'cost', 'crew', 'crop', 'data', 'dawn', 'deal',
            'dear', 'deep', 'desk', 'diet', 'dirt', 'dish', 'disk', 'door',
            'dose', 'down', 'draw', 'dust', 'duty', 'earn', 'ease', 'east',
            'edge', 'else', 'even', 'evil', 'exam', 'exit', 'face', 'fact',
            'fair', 'fall', 'fame', 'farm', 'fear', 'file', 'fill', 'film',
            'fine', 'firm', 'fish', 'flag', 'flat', 'flow', 'fold', 'folk',
            'font', 'food', 'foot', 'ford', 'form', 'fort', 'four', 'free',
            'from', 'fuel', 'full', 'fund', 'gain', 'gate', 'gift', 'glad',
            'goal', 'gold', 'golf', 'grab', 'gray', 'grip', 'gulf', 'hair',
            'half', 'hall', 'halt', 'hang', 'harm', 'hate', 'have', 'head',
            'hear', 'heat', 'heel', 'hell', 'help', 'hide', 'high', 'hill',
            'hint', 'hire', 'hold', 'hole', 'holy', 'hook', 'hope', 'horn',
            'host', 'hour', 'huge', 'hunt', 'hurt', 'idea', 'inch', 'iron',
            'item', 'jack', 'jane', 'jean', 'join', 'joke', 'jump', 'jury',
            'jury', 'just', 'keen', 'kick', 'kill', 'king', 'kiss', 'knee',
            'knock', 'know', 'lack', 'lady', 'lake', 'lamp', 'land', 'lane',
            'last', 'late', 'lead', 'leaf', 'lean', 'left', 'lend', 'lift',
            'like', 'limit', 'line', 'link', 'list', 'live', 'load', 'loan',
            'lock', 'long', 'look', 'lord', 'lose', 'loss', 'lost', 'lots',
            'luck', 'lung', 'mail', 'main', 'make', 'male', 'mall', 'many',
            'mark', 'mass', 'mate', 'math', 'meal', 'mean', 'meat', 'meet',
            'menu', 'mere', 'mild', 'mile', 'milk', 'mill', 'mind', 'mine',
            'miss', 'mode', 'mood', 'moon', 'more', 'most', 'move', 'much',
            'must', 'myth', 'nail', 'navy', 'near', 'neat', 'neck', 'need',
            'news', 'nice', 'nine', 'node', 'none', 'noon', 'norm', 'nose',
            'note', 'noun', 'odds', 'okay', 'once', 'only', 'onto', 'open',
            'oral', 'oven', 'over', 'pace', 'pack', 'page', 'pain', 'pair',
            'pale', 'palm', 'park', 'part', 'pass', 'past', 'path', 'peak',
            'peer', 'pick', 'pile', 'pine', 'pink', 'pipe', 'plan', 'play',
            'plot', 'plug', 'plus', 'poem', 'poet', 'poll', 'pond', 'pool',
            'poor', 'pope', 'port', 'pose', 'post', 'pour', 'pray', 'pull',
            'pump', 'pure', 'push', 'quit', 'race', 'rail', 'rain', 'rank',
            'rare', 'rate', 'read', 'real', 'rear', 'rely', 'rent', 'rest',
            'rice', 'rich', 'ride', 'ring', 'rise', 'risk', 'role', 'roll',
            'roof', 'root', 'rope', 'rose', 'ruin', 'rush', 'safe', 'sake',
            'sale', 'salt', 'same', 'sand', 'save', 'seat', 'seed', 'seek',
            'seem', 'self', 'sell', 'send', 'shed', 'ship', 'shop', 'shot',
            'show', 'shut', 'sick', 'side', 'sigh', 'sign', 'silk', 'sing',
            'sink', 'site', 'size', 'skin', 'slip', 'slow', 'snap', 'snow',
            'soft', 'soil', 'sole', 'some', 'song', 'soon', 'sort', 'soul',
            'span', 'spin', 'spot', 'star', 'stay', 'step', 'stop', 'such',
            'suit', 'sure', 'swim', 'tail', 'tale', 'talk', 'tall', 'tank',
            'tape', 'task', 'team', 'tear', 'tell', 'tend', 'tent', 'term',
            'test', 'text', 'that', 'them', 'then', 'they', 'thin', 'this',
            'thus', 'tiny', 'tire', 'tone', 'tool', 'tour', 'town', 'tree',
            'trip', 'tube', 'tuck', 'turn', 'twin', 'type', 'ugly', 'unit',
            'upon', 'urge', 'used', 'user', 'vast', 'very', 'vice', 'view',
            'vine', 'vote', 'wade', 'wage', 'wait', 'wake', 'walk', 'wall',
            'want', 'ward', 'warm', 'warn', 'wash', 'wave', 'weak', 'wear',
            'weed', 'week', 'well', 'west', 'what', 'when', 'whom', 'wide',
            'wife', 'wild', 'will', 'wind', 'wine', 'wing', 'wire', 'wise',
            'wish', 'with', 'wolf', 'wood', 'wool', 'word', 'work', 'wrap',
            'yard', 'yeah', 'zero', 'zone',
        }
        abbreviations = []
        for match in matches:
            match_lower = match.lower()
            # 已知缩写优先匹配，不在过滤列表中
            if match_lower in self.db.entries:
                abbreviations.append(match)
            elif match_lower not in common_words and len(match) >= 2:
                abbreviations.append(match)
        # 最多返回 20 个缩写，避免超长文本性能问题
        MAX_ABBR = 20
        result = list(set(abbreviations))
        return result[:MAX_ABBR]

    def infer_domain(self, text: str, context: Optional[str] = None) -> Optional[Domain]:
        """从文本和上下文推断领域"""
        combined = (text + " " + (context or "")).lower()
        for domain, keywords in DOMAIN_KEYWORDS.items():
            for kw in keywords:
                if kw in combined:
                    return domain
        return None

    def decode(self, text: str, context: Optional[str] = None) -> Dict:
        abbreviations = self.extract_abbreviations(text)
        inferred_domain = self.infer_domain(text, context)

        results = []
        unknown_abbrs = []

        for abbr in abbreviations:
            entries = self.db.lookup(abbr)
            if entries:
                sorted_entries = sorted(entries, key=lambda x: x.confidence, reverse=True)
                target = inferred_domain
                if target:
                    for entry in sorted_entries:
                        if entry.domain == target:
                            entry.confidence = min(1.0, entry.confidence + 0.1)
                    sorted_entries = sorted(sorted_entries, key=lambda x: x.confidence, reverse=True)
                results.append({
                    'abbreviation': abbr,
                    'matches': [
                        {
                            'full_form': e.full_form,
                            'meaning': e.meaning,
                            'domain': e.domain.value,
                            'confidence': e.confidence,
                            'examples': e.examples,
                            'source': e.source,
                        }
                        for e in sorted_entries
                    ]
                })
            else:
                # 检查缓存
                cached = self.cache.get(abbr)
                if cached:
                    self.db.add_from_search(
                        abbreviation=abbr,
                        full_form=cached[0].get('full_form', ''),
                        meaning=cached[0].get('meaning', ''),
                        domain=Domain(cached[0].get('domain', 'unknown')),
                        confidence=cached[0].get('confidence', 0.7),
                        examples=cached[0].get('examples', []),
                        source='cache',
                    )
                    results.append({
                        'abbreviation': abbr,
                        'matches': cached,
                        'source': 'cache',
                    })
                else:
                    unknown_abbrs.append(abbr)

        return {
            'original_text': text,
            'context': context,
            'inferred_domain': inferred_domain.value if inferred_domain else None,
            'found': results,
            'unknown': unknown_abbrs,
            'total_found': len(results),
            'total_unknown': len(unknown_abbrs),
            'search_queries': self._generate_search_queries(unknown_abbrs, context, inferred_domain),
        }

    def _generate_search_queries(self, unknown_abbrs: List[str], context: Optional[str],
                                  inferred_domain: Optional[Domain]) -> List[Dict]:
        """为未知缩写生成搜索查询，带预算控制"""
        if not unknown_abbrs:
            return []

        # 搜索预算：未知缩写越多，每个缩写的查询越精简
        n = len(unknown_abbrs)
        if n <= 2:
            max_queries_per_abbr = 2
        elif n <= 5:
            max_queries_per_abbr = 1
        else:
            # 超过5个，只处理前5个，其余引导用户
            unknown_abbrs = unknown_abbrs[:5]
            max_queries_per_abbr = 1

        domain_hint_map = {
            Domain.GAMING: "游戏术语",
            Domain.ENTERTAINMENT: "饭圈用语",
            Domain.LIFESTYLE: "网络用语",
            Domain.TECH: "技术术语",
            Domain.ANIME: "动漫用语",
            Domain.FINANCE: "金融术语",
        }
        hint = domain_hint_map.get(inferred_domain, "") if inferred_domain else ""

        queries = []
        for abbr in unknown_abbrs:
            q_list = [f'"{abbr}" 是什么意思']
            if hint and max_queries_per_abbr >= 2:
                q_list.append(f'"{abbr}" {hint} 含义')
            elif max_queries_per_abbr >= 2:
                q_list.append(f'"{abbr}" 网络用语 缩写')
            queries.append({'abbreviation': abbr, 'queries': q_list[:max_queries_per_abbr]})
        return queries

    def add_search_results(self, abbreviation: str, search_findings: List[Dict]) -> Dict:
        """
        将搜索结果回填到数据库并返回解析结果

        Args:
            abbreviation: 缩写
            search_findings: 搜索发现列表，每项包含 full_form, meaning, domain, examples, source

        Returns:
            解析结果
        """
        domain_map = {d.value: d for d in Domain}
        added = []
        for finding in search_findings:
            domain = domain_map.get(finding.get('domain', 'unknown'), Domain.UNKNOWN)
            confidence = finding.get('confidence', 0.7)
            examples = finding.get('examples', [])
            source = finding.get('source', 'web_search')
            self.db.add_from_search(
                abbreviation=abbreviation,
                full_form=finding['full_form'],
                meaning=finding['meaning'],
                domain=domain,
                confidence=confidence,
                examples=examples,
                source=source,
            )
            added.append({
                'full_form': finding['full_form'],
                'meaning': finding['meaning'],
                'domain': domain.value,
                'confidence': confidence,
                'examples': examples,
                'source': source,
            })

        added.sort(key=lambda x: x['confidence'], reverse=True)
        # 缓存搜索结果
        self.cache.put(abbreviation, added)
        return {'abbreviation': abbreviation, 'matches': added, 'source': 'web_search'}

    def parse_and_add_from_snippets(self, abbreviation: str, search_snippets: List[str],
                                     context: Optional[str] = None) -> Dict:
        """
        从搜索结果片段中自动提取含义并回填（桥接 search_slang.py）。

        Args:
            abbreviation: 缩写
            search_snippets: WebSearch 返回的搜索结果片段列表
            context: 用户上下文

        Returns:
            解析结果（同 add_search_results）
        """
        try:
            from search_slang import parse_search_results, validate_findings
        except ImportError:
            # fallback: 如果 search_slang 不可用，返回空结果
            return {'abbreviation': abbreviation, 'matches': [], 'source': 'parse_failed'}

        findings = parse_search_results(abbreviation, search_snippets)
        findings = validate_findings(abbreviation, findings, context)
        if not findings:
            return {'abbreviation': abbreviation, 'matches': [], 'source': 'no_match'}

        return self.add_search_results(abbreviation, findings)

    def format_output(self, result: Dict) -> str:
        lines = []
        lines.append("=" * 50)
        lines.append(f"原文：{result['original_text']}")
        if result['context']:
            lines.append(f"上下文：{result['context']}")
        if result.get('inferred_domain'):
            lines.append(f"推断领域：{DOMAIN_CN.get(result['inferred_domain'], result['inferred_domain'])}")
        lines.append("=" * 50)

        if result['found']:
            lines.append(f"\n✓ 识别到 {result['total_found']} 个缩写：\n")
            for item in result['found']:
                abbr = item['abbreviation']
                matches = item['matches']
                lines.append(f"【{abbr}】")
                if len(matches) == 1:
                    m = matches[0]
                    lines.append(f"  → {m['full_form']}")
                    lines.append(f"    含义：{m['meaning']}")
                    lines.append(f"    领域：{DOMAIN_CN.get(m['domain'], m['domain'])} | 置信度：{m['confidence']*100:.0f}%")
                    if m.get('examples') and m['examples']:
                        lines.append(f"    例句：{m['examples'][0]}")
                    if m.get('source') and m['source'] != 'builtin':
                        lines.append(f"    来源：{m['source']}")
                else:
                    lines.append(f"  发现 {len(matches)} 种可能（按置信度排序）：")
                    for i, m in enumerate(matches, 1):
                        lines.append(f"    {i}. {m['full_form']} - {m['meaning']}")
                        lines.append(f"       领域：{DOMAIN_CN.get(m['domain'], m['domain'])} | 置信度：{m['confidence']*100:.0f}%")
                lines.append("")

        if result['unknown']:
            lines.append(f"\n? 未识别的缩写（{len(result['unknown'])}个）：")
            for abbr in result['unknown']:
                lines.append(f"  - {abbr}")
            lines.append("\n💡 将通过搜索补充这些缩写的含义...")

        if not result['found'] and not result['unknown']:
            lines.append("\n未发现明显缩写。")

        return "\n".join(lines)

    def format_search_queries(self, result: Dict) -> str:
        """格式化搜索查询输出，供 agent 调用 WebSearch"""
        queries = result.get('search_queries', [])
        if not queries:
            return ""

        lines = ["\n🔍 需要搜索以下缩写：\n"]
        for item in queries:
            abbr = item['abbreviation']
            lines.append(f"【{abbr}】")
            for i, q in enumerate(item['queries'], 1):
                lines.append(f"  查询{i}: {q}")
            lines.append("")
        lines.append("请使用 WebSearch 执行上述查询，然后调用 add_search_results() 回填结果。")
        return "\n".join(lines)

    def format_output_markdown(self, result: Dict) -> str:
        """Markdown 格式输出"""
        lines = []
        lines.append(f"# 缩写解析结果\n")
        lines.append(f"**原文**：{result['original_text']}")
        if result['context']:
            lines.append(f"**上下文**：{result['context']}")
        if result.get('inferred_domain'):
            lines.append(f"**推断领域**：{DOMAIN_CN.get(result['inferred_domain'], result['inferred_domain'])}")
        lines.append("")

        if result['found']:
            lines.append(f"## 已识别缩写（{result['total_found']}个）\n")
            lines.append("| 缩写 | 全称 | 含义 | 领域 | 置信度 | 来源 |")
            lines.append("|------|------|------|------|--------|------|")
            for item in result['found']:
                abbr = item['abbreviation']
                for m in item['matches']:
                    domain_cn = DOMAIN_CN.get(m['domain'], m['domain'])
                    conf = f"{m['confidence']*100:.0f}%"
                    source = m.get('source', 'builtin')
                    lines.append(f"| {abbr} | {m['full_form']} | {m['meaning']} | {domain_cn} | {conf} | {source} |")
            lines.append("")

        if result['unknown']:
            lines.append(f"## 未识别缩写（{result['total_unknown']}个）\n")
            for abbr in result['unknown']:
                lines.append(f"- `{abbr}`")
            lines.append("\n> 将通过搜索补充这些缩写的含义...\n")

        if not result['found'] and not result['unknown']:
            lines.append("\n未发现明显缩写。")

        return "\n".join(lines)

    def format_search_queries_markdown(self, result: Dict) -> str:
        """Markdown 格式搜索查询输出"""
        queries = result.get('search_queries', [])
        if not queries:
            return ""

        lines = ["\n## 待搜索缩写\n"]
        for item in queries:
            abbr = item['abbreviation']
            lines.append(f"### {abbr}\n")
            for i, q in enumerate(item['queries'], 1):
                lines.append(f"{i}. `{q}`")
            lines.append("")
        lines.append("> 请使用 WebSearch 执行上述查询，然后调用 `add_search_results()` 回填结果。")
        return "\n".join(lines)

def main():
    import argparse
    import io
    # 设置 stdout 编码为 utf-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(description='互联网缩写解析器')
    parser.add_argument('text', help='要解析的文本')
    parser.add_argument('--context', '-c', help='上下文领域')
    parser.add_argument('--json', '-j', action='store_true', help='JSON输出')
    parser.add_argument('--format', '-f', choices=['text', 'json', 'markdown'], default='text',
                        help='输出格式：text/json/markdown')
    args = parser.parse_args()

    decoder = SlangDecoder()
    result = decoder.decode(args.text, args.context)

    if args.json or args.format == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == 'markdown':
        print(decoder.format_output_markdown(result))
        if result['search_queries']:
            print(decoder.format_search_queries_markdown(result))
    else:
        print(decoder.format_output(result))
        if result['search_queries']:
            print(decoder.format_search_queries(result))

if __name__ == '__main__':
    main()
