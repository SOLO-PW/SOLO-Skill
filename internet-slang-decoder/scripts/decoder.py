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

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(SCRIPT_DIR, '..', 'cache')
CACHE_FILE = os.path.join(CACHE_DIR, 'search_cache.json')
CACHE_TTL = 30 * 24 * 3600  # 30 天过期

COMMON_WORDS_FILE = os.path.join(SCRIPT_DIR, 'common_words.json')
HOTWORDS_FILE = os.path.join(SCRIPT_DIR, 'hotwords.json')
MAX_INPUT_LEN = 500  # 输入长度阈值（字符）

# common_words.json 缺失时的内置回退（精简最小集），避免脚本因数据文件缺失而报错
_FALLBACK_COMMON_WORDS = frozenset(
    "a an and the is are was were be been being have has had do does did "
    "i you he she it we they me him her us them my your his our their this that "
    "these those of in on at to from for with by about into over after under between "
    "as but or not so than then if else while when where how why what which who whom whose "
    "can could will would shall should may might must all any both few more most much some such "
    "no yes own same very just too also almost only even ever never now here there of "
    "to be".split()
)


def _load_common_words() -> set:
    """加载停用/常见英文高频词表（小型词频字典）。空则回退到内置最小集。"""
    try:
        if os.path.exists(COMMON_WORDS_FILE):
            with open(COMMON_WORDS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            words = data.get('words', []) if isinstance(data, dict) else data
            if words:
                return {str(w).lower() for w in words}
    except (json.JSONDecodeError, IOError, AttributeError):
        pass
    return set(_FALLBACK_COMMON_WORDS)

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
        self.hotwords: List[SlangEntry] = []
        self._load_builtin_data()
        self._load_hotwords()

    def _load_hotwords(self):
        """从 hotwords.json 加载热词更新层，覆盖/追加到主词库"""
        if os.path.exists(HOTWORDS_FILE):
            try:
                with open(HOTWORDS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except (json.JSONDecodeError, IOError):
                return
            domain_map = {d.value: d for d in Domain}
            for item in data.get('entries', []):
                try:
                    domain = domain_map.get(item.get('domain', 'unknown'), Domain.UNKNOWN)
                    entry = SlangEntry(
                        abbreviation=item['abbreviation'],
                        full_form=item['full_form'],
                        meaning=item.get('meaning', ''),
                        domain=domain,
                        confidence=item.get('confidence', 0.7),
                        examples=item.get('examples', []),
                        source=item.get('source', 'hotword'),
                        notes=item.get('notes'),
                    )
                except KeyError:
                    continue
                self.hotwords.append(entry)
                abbr_lower = entry.abbreviation.lower()
                # 覆盖同缩写+同全称的内置旧词条
                if abbr_lower in self.entries:
                    self.entries[abbr_lower] = [e for e in self.entries[abbr_lower]
                                                if not (e.full_form.lower() == entry.full_form.lower())]
                self.add_entry(entry)

    def add_hotword(self, abbreviation: str, full_form: str, meaning: str,
                    domain: Optional[Domain] = None, confidence: float = 0.7,
                    examples: Optional[List[str]] = None, notes: Optional[str] = None) -> SlangEntry:
        """新增/覆盖热词并持久化到 hotwords.json（词条更新机制）"""
        entry = SlangEntry(
            abbreviation=abbreviation, full_form=full_form, meaning=meaning,
            domain=domain if domain else Domain.UNKNOWN,
            confidence=confidence, examples=examples or [],
            source='hotword', notes=notes,
        )
        # 处理与现有热词重复，覆盖同缩写+同全称
        abbr_lower = entry.abbreviation.lower()
        self.hotwords = [e for e in self.hotwords if not (
            e.abbreviation.lower() == abbr_lower and e.full_form.lower() == entry.full_form.lower()
        )]
        self.hotwords.append(entry)
        self.add_entry(entry)
        self._persist_hotwords()
        return entry

    def _persist_hotwords(self):
        """将内存热词写回 hotwords.json"""
        payload = {
            "version": "1.0.0",
            "title": "Hotword update layer",
            "description": "热词更新层：独立于 slang_db.json 主词库，用于增量添加/更新词条。",
            "updated_at": time.strftime('%Y-%m-%d'),
            "entries": [
                {
                    "abbreviation": e.abbreviation,
                    "full_form": e.full_form,
                    "meaning": e.meaning,
                    "domain": e.domain.value,
                    "confidence": e.confidence,
                    "examples": e.examples,
                    "source": e.source,
                    "notes": e.notes,
                }
                for e in sorted(self.hotwords, key=lambda x: x.abbreviation.lower())
            ],
        }
        try:
            with open(HOTWORDS_FILE, 'w', encoding='utf-8') as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
        except IOError:
            pass

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
        self.common_words = _load_common_words()

    def extract_abbreviations(self, text: str, truncate: bool = False) -> List[str]:
        # 输入长度阈值：默认不静默截断，超限时通过返回值告知调用方
        truncated = False
        if len(text) > MAX_INPUT_LEN:
            if truncate:
                text = text[:MAX_INPUT_LEN]
                truncated = True
            # 不截断时仍继续处理全文，但由 `decode()` 负责提示用户

        # 匹配纯字母 2-10 位（覆盖 tsundere/yandere/stablecoin 等）+ 混合数字字母（如 u1s1, k8s）
        pattern = r'[a-zA-Z]{2,10}|[a-zA-Z][0-9][a-zA-Z0-9]{0,4}'
        matches = re.findall(pattern, text)
        abbreviations = []
        for match in matches:
            match_lower = match.lower()
            # 已知缩写优先匹配，不在过滤列表中
            if match_lower in self.db.entries:
                abbreviations.append(match)
            elif match_lower not in self.common_words and len(match) >= 2:
                abbreviations.append(match)
        # 最多返回 20 个缩写，避免超长文本性能问题
        MAX_ABBR = 20
        result = list(set(abbreviations))
        result.sort(key=len, reverse=True)
        return result[:MAX_ABBR]

    def infer_domain(self, text: str, context: Optional[str] = None) -> Optional[Domain]:
        """从文本和上下文推断领域"""
        combined = (text + " " + (context or "")).lower()
        for domain, keywords in DOMAIN_KEYWORDS.items():
            for kw in keywords:
                if kw in combined:
                    return domain
        return None

    def decode(self, text: str, context: Optional[str] = None, truncate: bool = False,
               allow_partial: bool = False) -> Dict:
        # 输入超长处理：不再静默截断，超限时返回提示由用户决定（除非显式 truncate）
        too_long = len(text) > MAX_INPUT_LEN
        if too_long and not truncate and not allow_partial:
            return self._too_long_result(text, context)

        processed_text = text[:MAX_INPUT_LEN] if truncate else text

        abbreviations = self.extract_abbreviations(processed_text, truncate=truncate)
        inferred_domain = self.infer_domain(text, context)

        results = []
        unknown_abbrs = []

        for abbr in abbreviations:
            entries = self.db.lookup(abbr)
            if entries:
                disambiguated = self._disambiguate_entries(entries, inferred_domain, context)
                sorted_entries, top_candidate = disambiguated
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
                            'recommended': e is top_candidate,
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

        result = {
            'original_text': processed_text,
            'context': context,
            'inferred_domain': inferred_domain.value if inferred_domain else None,
            'truncated': bool(too_long) and truncate,
            'too_long': too_long,
            'found': results,
            'unknown': unknown_abbrs,
            'total_found': len(results),
            'total_unknown': len(unknown_abbrs),
            'search_queries': self._generate_search_queries(unknown_abbrs, context, inferred_domain),
        }
        if too_long and not truncate:
            result['notice'] = (f"输入长度 {len(text)} 字符超过阈值 {MAX_INPUT_LEN} 字符。"
                                f"为避免静默截断丢失内容，本次已按全文解析；如需截断请显式指定 truncate=True。")
        return result

    def _too_long_result(self, text: str, context: Optional[str]) -> Dict:
        """返回超长提示结果，交由用户决定而非静默丢弃内容"""
        return {
            'original_text': text,
            'context': context,
            'inferred_domain': None,
            'truncated': False,
            'too_long': True,
            'notice': (f"输入长度 {len(text)} 字符超过阈值 {MAX_INPUT_LEN} 字符。"
                       f"为使解析聚焦且避免超限误判，本次未对全文做强制截断解析。"
                       f"请精简输入后重试，或显式传入 truncate=True 允许按前 {MAX_INPUT_LEN} 字符解析。"),
            'found': [],
            'unknown': [],
            'total_found': 0,
            'total_unknown': 0,
            'search_queries': [],
        }

    def _disambiguate_entries(self, entries: List[SlangEntry],
                              inferred_domain: Optional[Domain],
                              context: Optional[str] = None) -> Tuple[List[SlangEntry], Optional[SlangEntry]]:
        """
        上下文消歧：在置信度排序基础上引入 领域匹配 + 词性/上下文 先验。

        - 与推断领域一致的词条大幅加分（领域匹配是强信号）
        - 多义条目按 (领域一致性, 置信度) 排序，避免只靠置信度排序
        - 返回 (排序后的条目, 推荐词条)
        """
        if len(entries) <= 1:
            return list(entries), (entries[0] if entries else None)

        ctx_text = ((context or "") + " " + " ".join([e.meaning or "" for e in entries])).lower()
        # 简单词性/用法先验：名词性、动词性线索（轻量启发，不依赖外部 POS 工具）
        pos_boost = {
            Domain.GAMING: ['动词', '动作', '技能', '命令', '发', '用'],
            Domain.ENTERTAINMENT: ['名词', '称谓', '粉丝', '饭圈', '夸'],
            Domain.TECH: ['技术', '编程', '接口', '系统', '开发'],
            Domain.FINANCE: ['交易', '投资', '涨', '跌', '买入', '卖出'],
        }

        def pos_match(e: SlangEntry) -> float:
            if e.domain in pos_boost:
                if any(kw in ctx_text for kw in pos_boost[e.domain]):
                    return 0.05
            return 0.0

        scored = []
        for e in entries:
            score = e.confidence
            if inferred_domain is not None and e.domain == inferred_domain:
                score += 0.3  # 领域一致强加分
            score += pos_match(e)
            scored.append((e, min(1.0, score)))

        scored.sort(key=lambda x: x[1], reverse=True)
        ordered = [e for e, _ in scored]
        return ordered, ordered[0]

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
        if result.get('too_long'):
            lines.append(f"⚠️ 输入超过阈值：{result.get('notice', '')}")
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
                    lines.append(f"  发现 {len(matches)} 种可能（上下文消歧后排序）：")
                    for i, m in enumerate(matches, 1):
                        tag = " ★推荐" if m.get('recommended') else ""
                        lines.append(f"    {i}. {m['full_form']} - {m['meaning']}{tag}")
                        lines.append(f"       领域：{DOMAIN_CN.get(m['domain'], m['domain'])} | 置信度：{m['confidence']*100:.0f}%")
                lines.append("")

        if result['unknown']:
            lines.append(f"\n? 未识别的缩写（{len(result['unknown'])}个）：")
            for abbr in result['unknown']:
                lines.append(f"  - {abbr}")
            lines.append("\n💡 将通过搜索补充这些缩写的含义...")

        if result.get('truncated'):
            lines.append("\n⚠️ 输入超过阈值，已按显式 truncate 仅解析前 500 字符。")

        if not result['found'] and not result['unknown'] and not result.get('truncated'):
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
    parser.add_argument('text', nargs='?', help='要解析的文本')
    parser.add_argument('--context', '-c', help='上下文领域')
    parser.add_argument('--json', '-j', action='store_true', help='JSON输出')
    parser.add_argument('--format', '-f', choices=['text', 'json', 'markdown'], default='text',
                        help='输出格式：text/json/markdown')
    parser.add_argument('--truncate', action='store_true',
                        help='超长输入时显式截断为前500字符（默认不做静默截断）')
    parser.add_argument('--allow-partial', action='store_true',
                        help='超长输入时按全文解析并仅提示，不返回阻断结果')
    parser.add_argument('--add', nargs='+', metavar='ABBR_FULL_FORM_MEANING',
                        help='向热词库添加词条（词条更新机制），例如 --add gd 搞对象 脱单/谈恋爱 --domain lifestyle --confidence 0.9')
    parser.add_argument('--domain', default='unknown', help='词条领域（--add 使用）')
    parser.add_argument('--confidence', type=float, default=0.7, help='词条置信度（--add 使用）')
    parser.add_argument('--notes', help='词条备注（--add 使用）')
    args = parser.parse_args()

    decoder = SlangDecoder()

    if args.add:
        if len(args.add) < 3:
            parser.error("--add 需要至少3个参数：ABBR FULL_FORM MEANING")
        domain_map = {d.value: d for d in Domain}
        domain = domain_map.get(args.domain.lower(), Domain.UNKNOWN)
        entry = decoder.db.add_hotword(abbreviation=args.add[0], full_form=args.add[1],
                                       meaning=args.add[2], domain=domain,
                                       confidence=args.confidence, notes=args.notes)
        print(f"✅ 已写入热词库：{entry.abbreviation} = {entry.full_form}（{DOMAIN_CN.get(entry.domain.value)}）")
        return

    if not args.text:
        parser.error("缺少要解析的文本 text，或使用 --add 添加词条")

    if args.truncate and args.allow_partial:
        parser.error("--truncate 与 --allow-partial 不能同时使用")

    result = decoder.decode(args.text, args.context,
                             truncate=args.truncate, allow_partial=args.allow_partial)

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
