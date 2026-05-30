#!/usr/bin/env python3
"""
互联网缩写搜索验证工具
生成搜索查询、解析搜索结果、验证准确性
"""

import json
import sys
import re
from typing import List, Dict, Optional


DOMAIN_HINTS = {
    '游戏': ['游戏术语', '游戏缩写', '电竞用语'],
    'game': ['gaming term', 'gaming abbreviation'],
    '娱乐': ['饭圈用语', '娱乐圈缩写', '追星用语'],
    'entertainment': ['fandom slang', 'celebrity abbreviation'],
    '生活': ['网络用语', '聊天缩写', '日常用语'],
    'lifestyle': ['internet slang', 'chat abbreviation'],
    '科技': ['技术术语', '编程缩写', 'IT术语'],
    'tech': ['tech term', 'programming abbreviation'],
    '动漫': ['动漫用语', '二次元用语', 'ACG术语'],
    'anime': ['anime slang', 'ACG abbreviation'],
    '金融': ['金融术语', '投资用语', '财经缩写'],
    'finance': ['finance term', 'trading abbreviation'],
}


def generate_search_queries(abbreviation: str, context: Optional[str] = None) -> List[str]:
    """生成搜索查询，按优先级排序"""
    queries = [f'"{abbreviation}" 是什么意思 网络用语']

    if context:
        ctx_lower = context.lower()
        for key, hints in DOMAIN_HINTS.items():
            if key in ctx_lower or ctx_lower in key:
                queries.append(f'"{abbreviation}" {hints[0]} 含义')
                break
    else:
        queries.append(f'"{abbreviation}" 缩写 全称 含义')

    return queries


def parse_search_results(abbreviation: str, search_snippets: List[str]) -> List[Dict]:
    """
    从搜索结果片段中提取缩写含义

    Args:
        abbreviation: 要解析的缩写
        search_snippets: WebSearch 返回的搜索结果片段列表

    Returns:
        结构化的含义列表
    """
    findings = []
    abbr_lower = abbreviation.lower()

    # 常见含义提取模式
    patterns = [
        # "XX"是XXX的意思 / XX是XXX的意思 / XX代表XXX / XX全称是XXX
        rf'[""「]?(?:{abbreviation})[""」]?\s*(?:是|代表|全称(?:是|为)|指| stands? for| means?)\s*[：:]?\s*(.+?)(?:[。，；;！!？?\s,]|$)',
        # XX = XXX / XX：XXX
        rf'(?:^|[\s，。；]){abbreviation}\s*[=＝:：]\s*(.+?)(?:[。，；;！!？?\s]|$)',
        # XX（XXX） 括号注释
        rf'{abbreviation}[（(]([^)）]+)[)）]',
        # XX指的是XXX / XX即XXX / XX叫做XXX
        rf'(?:{abbreviation})\s*(?:指的是|即|叫做|意思是|含义是|表示)\s*(.+?)(?:[。，；;！!？?\s,]|$)',
        # XX, which stands for XXX / XX, meaning XXX
        rf'(?:{abbreviation})\s*,\s*(?:which\s+)?(?:stands?\s+for|meaning|means?|refers?\s+to)\s+(.+?)(?:[.。，；;！!？?\s,]|$)',
        # 全称XXX / 缩写XXX
        rf'(?:全称|缩写|简称)\s*(?:为|是|：)?\s*({abbreviation})\s*(?:是|代表|指)?\s*(.+?)(?:[。，；;！!？?\s,]|$)',
    ]

    for snippet in search_snippets:
        for pattern in patterns:
            matches = re.findall(pattern, snippet, re.IGNORECASE)
            for match in matches:
                full_form = match.strip() if isinstance(match, str) else match[-1].strip()
                if len(full_form) < 2 or len(full_form) > 100:
                    continue
                if full_form.lower() == abbr_lower:
                    continue

                findings.append({
                    'full_form': full_form,
                    'meaning': full_form,
                    'confidence': 0.7,
                    'source': 'web_search',
                    'examples': [],
                })

    # 统计频率（去重前）
    def normalize(s):
        return re.sub(r'(的意思|的含义|的全称|，.*|。.*)', '', s).strip()

    freq = {}
    for f in findings:
        key = normalize(f['full_form']).lower()
        if key and key != abbr_lower:
            freq[key] = freq.get(key, 0) + 1

    # 去重
    seen = set()
    unique = []
    for f in findings:
        key = normalize(f['full_form']).lower()
        if not key or key == abbr_lower:
            continue
        if key not in seen:
            seen.add(key)
            f['meaning'] = normalize(f['full_form'])
            f['full_form'] = normalize(f['full_form'])
            f['_freq'] = freq[key]
            unique.append(f)

    return unique[:5]


def validate_findings(abbreviation: str, findings: List[Dict], context: Optional[str] = None) -> List[Dict]:
    """
    验证搜索发现的准确性

    验证规则：
    1. 多个来源一致 → 置信度提升
    2. 与上下文匹配 → 置信度提升
    3. 单一来源且无上下文 → 保持默认置信度
    4. 含义过于宽泛 → 置信度降低
    5. 含义长度合理 → 置信度微调
    """
    if not findings:
        return []

    # 统计各含义出现频率
    freq = {}
    for f in findings:
        key = f['full_form'].lower()
        freq[key] = freq.get(key, 0) + 1

    for f in findings:
        key = f['full_form'].lower()
        base = f['confidence']

        # 多来源一致 → 提升置信度
        count = f.get('_freq', freq.get(key, 1))
        if count >= 3:
            base = min(0.95, base + 0.2)
        elif count >= 2:
            base = min(0.95, base + 0.15)

        # 与上下文匹配 → 提升置信度
        if context:
            ctx_lower = context.lower()
            meaning_lower = f['meaning'].lower()
            domain = f.get('domain', infer_domain_from_meaning(f['full_form']))
            # 上下文关键词与领域匹配
            domain_keywords = {
                'gaming': ['游戏', '电竞', '开黑', '排位', '游戏圈'],
                'entertainment': ['娱乐', '饭圈', '明星', '追星', '偶像'],
                'tech': ['科技', '编程', '开发', '代码', '技术', '工作'],
                'lifestyle': ['生活', '日常', '聊天', '网络', '社交'],
                'anime': ['动漫', '二次元', '番剧', '漫画'],
                'finance': ['金融', '股票', '投资', '币圈'],
            }
            if domain in domain_keywords:
                if any(kw in ctx_lower for kw in domain_keywords[domain]):
                    base = min(0.95, base + 0.1)

        # 含义过于宽泛 → 降低置信度
        vague_words = ['某个', '一种', '一些', 'something', 'some', '某个东西', '某种']
        if any(w in f['meaning'].lower() for w in vague_words):
            base = max(0.4, base - 0.2)

        # 含义长度过短 → 降低置信度
        if len(f['meaning']) < 3:
            base = max(0.4, base - 0.1)
        # 含义长度合理 → 微调提升
        elif 5 <= len(f['meaning']) <= 30:
            base = min(0.95, base + 0.05)

        f['confidence'] = round(base, 2)

    # 按置信度排序
    findings.sort(key=lambda x: x['confidence'], reverse=True)
    return findings


def infer_domain_from_meaning(full_form: str) -> str:
    """从含义文本推断领域，使用评分机制选择最佳匹配"""
    text = full_form.lower()

    domain_keywords = {
        'gaming': {
            'keywords': ['游戏', 'game', '英雄', '技能', '装备', '副本', '玩家', 'player', 'hero',
                        '击杀', '团战', '排位', '段位', '对战', '竞技', '手游', '端游', 'gaming',
                        '电竞', '开黑', '补刀', '推塔', '野怪', 'boss', 'buff', 'nerf', 'mvp'],
            'weight': 1.0,
        },
        'entertainment': {
            'keywords': ['饭圈', '明星', '偶像', '粉丝', '追星', '综艺', '选秀', '娱乐',
                        '爱豆', '应援', '打榜', '热搜', '微博', '超话', 'cp', '磕', '追剧',
                        '演员', '歌手', '出道', '专辑', '演唱会', '应援', '控评'],
            'weight': 1.0,
        },
        'tech': {
            'keywords': ['技术', '编程', '开发', '代码', 'tech', 'programming', 'software', 'api',
                        '程序', '软件', '算法', '数据', '服务器', '接口', '框架', '部署', '运维',
                        '前端', '后端', '数据库', 'git', 'github', '代码审查', '测试', '上线'],
            'weight': 1.0,
        },
        'lifestyle': {
            'keywords': ['网络', '聊天', '日常', 'internet', 'chat', 'social', '社交',
                        '微信', 'qq', '朋友圈', '点赞', '评论', '私信', '表情包', '网络用语',
                        '生活', '工作', '学习', '购物', '消费'],
            'weight': 0.8,
        },
        'anime': {
            'keywords': ['动漫', '番剧', '漫画', 'anime', 'manga', '二次元', '声优', '配音',
                        '动画', '手办', 'cosplay', 'cos', '萌', '傲娇', '病娇', '异世界',
                        '机甲', '番', '追番', '新番', '完结', 'ova', 'bd'],
            'weight': 1.0,
        },
        'finance': {
            'keywords': ['金融', '股票', '投资', '基金', 'finance', 'stock', 'trading',
                        '币圈', '加密', '交易', '收益', '理财', '牛市', '熊市', '涨跌',
                        '区块链', 'defi', 'nft', '交易所', '行情', 'k线', '止损', '杠杆'],
            'weight': 1.0,
        },
    }

    scores = {}
    for domain, config in domain_keywords.items():
        score = 0
        for kw in config['keywords']:
            if kw in text:
                score += config['weight']
        if score > 0:
            scores[domain] = score

    if not scores:
        return 'unknown'

    return max(scores, key=scores.get)


def format_search_report(abbreviation: str, queries: List[str],
                         findings: List[Dict]) -> str:
    """格式化完整的搜索报告"""
    lines = []
    lines.append("=" * 55)
    lines.append(f"缩写搜索报告：{abbreviation}")
    lines.append("=" * 55)

    lines.append(f"\n📡 执行的搜索查询：")
    for i, q in enumerate(queries, 1):
        lines.append(f"  {i}. {q}")

    if findings:
        lines.append(f"\n✅ 搜索发现 {len(findings)} 种可能含义：\n")
        for i, f in enumerate(findings, 1):
            conf_pct = f['confidence'] * 100
            domain = f.get('domain', infer_domain_from_meaning(f['full_form']))
            lines.append(f"  {i}. {f['full_form']}")
            lines.append(f"     置信度：{conf_pct:.0f}% | 领域：{domain}")
            if f.get('source') and f['source'] != 'web_search':
                lines.append(f"     来源：{f['source']}")
    else:
        lines.append("\n❌ 未能从搜索结果中提取到明确含义。")
        lines.append("\n建议：")
        lines.append("  1. 尝试提供更多上下文")
        lines.append("  2. 直接询问对方")
        lines.append("  3. 在相关社区/论坛搜索")

    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='互联网缩写搜索验证工具')
    parser.add_argument('abbreviation', help='要搜索的缩写')
    parser.add_argument('--context', '-c', help='上下文领域')
    parser.add_argument('--json', '-j', action='store_true', help='JSON输出')
    parser.add_argument('--snippets', '-s', nargs='*', help='搜索结果片段（用于解析）')

    args = parser.parse_args()

    queries = generate_search_queries(args.abbreviation, args.context)

    findings = []
    if args.snippets:
        findings = parse_search_results(args.abbreviation, args.snippets)
        findings = validate_findings(args.abbreviation, findings, args.context)
        for f in findings:
            if 'domain' not in f or f['domain'] == 'unknown':
                f['domain'] = infer_domain_from_meaning(f['full_form'])

    if args.json:
        result = {
            'abbreviation': args.abbreviation,
            'context': args.context,
            'search_queries': queries,
            'findings': findings,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_search_report(args.abbreviation, queries, findings))


if __name__ == '__main__':
    main()
