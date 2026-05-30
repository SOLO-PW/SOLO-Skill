#!/usr/bin/env python3
"""
从 scripts/slang_db.json 生成 references/ 下的各领域 .md 词典文件
确保数据源单一（Single Source of Truth）

用法：
    python scripts/build_refs.py
"""

import json
import os
import sys
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(SCRIPT_DIR, '..')
DATA_FILE = os.path.join(SCRIPT_DIR, 'slang_db.json')
REFS_DIR = os.path.join(ROOT_DIR, 'references')

DOMAIN_META = {
    'entertainment': {
        'title': '娱乐圈/饭圈缩写词典',
        'filename': 'entertainment.md',
        'categories': {
            '情感表达类': lambda e: any(kw in e['meaning'] for kw in ['笑', '萌', '爱', '死', '上头', '感情', '磕']),
            '态度表达类': lambda e: any(kw in e['meaning'] for kw in ['认同', '客观', '在意', '不好笑', '抱歉', '打扰', '否定', '确认']),
            '社交/圈层类': lambda e: any(kw in e['meaning'] for kw in ['圈', '朋友', '转发', '评论', '热搜', '数据']),
            '人物相关': lambda e: any(kw in e['meaning'] for kw in ['哥哥', '姐姐', '妹妹', '称呼']),
            '作品相关': lambda e: any(kw in e['full_form'] for kw in ['music', 'background', 'original', 'video']),
        },
    },
    'gaming': {
        'title': '游戏圈缩写词典',
        'filename': 'gaming.md',
        'categories': {
            '游戏结束/礼仪': lambda e: any(kw in e['meaning'] for kw in ['结束', '认输', '好运', '轻松']),
            '状态/行为': lambda e: any(kw in e['meaning'] for kw in ['离开', '回来', '掉线', '延迟', '帧率']),
            '游戏机制': lambda e: any(kw in e['meaning'] for kw in ['超模', '削弱', '增强', '冷却', '生命', '魔法', '经验', '等级', '减益']),
            '玩家相关': lambda e: any(kw in e['meaning'] for kw in ['玩家', '新手', '高手', '小号', '捣乱', '送人头', '有毒', '输不起']),
            '游戏表现': lambda e: any(kw in e['meaning'] for kw in ['精彩', '关键时刻', '团灭', '带飞', '发育', '推进', '防守', '游走']),
        },
    },
    'lifestyle': {
        'title': '生活/网络用语缩写词典',
        'filename': 'lifestyle.md',
        'categories': {
            '常用英文缩写': lambda e: any(kw in e['full_form'] for kw in ['by the way', 'for your information', 'as soon', 'in my', 'to be honest', 'to be fair', "I don't know", "I don't care"]),
            '即时通讯/社交': lambda e: any(kw in e['meaning'] for kw in ['私信', '路上', '现在', '告诉', '联系', '干嘛']),
            '情感表达': lambda e: any(kw in e['meaning'] for kw in ['笑', '无语', '天', '鬼', '难了', '大笑']),
            '网络俚语': lambda e: any(kw in e['meaning'] for kw in ['家人', '老铁', '没问题', '撒谎', '厉害', '八卦', '讽刺', '觉醒', '嗨', '羡慕', '共鸣']),
        },
    },
    'tech': {
        'title': '科技/互联网缩写词典',
        'filename': 'tech.md',
        'categories': {
            '开发/编程': lambda e: any(kw in e['meaning'] for kw in ['接口', '界面', '体验', '开发者', '仓库', '合并', '进行中', '概念验证', '征求意见', '小建议']),
            '运维/部署': lambda e: any(kw in e['meaning'] for kw in ['环境', '持续', '容器', '域名', '安全套接', '分发网络', '服务器', '云', '存储']),
            '数据/AI': lambda e: any(kw in e['meaning'] for kw in ['人工智能', '机器学习', '深度学习', '语言处理', '视觉', '语言模型', '预训练', '数据格式']),
            '项目管理': lambda e: any(kw in e['meaning'] for kw in ['产品', '经理', '分析师', '负责人', '全栈', '研发', '站会', '回顾', '冲刺', '演示']),
            '安全': lambda e: any(kw in e['meaning'] for kw in ['认证', '授权', '令牌', '访问控制', '跨域', '跨站', '防火墙', '漏洞', '证书']),
        },
    },
    'anime': {
        'title': '动漫/二次元缩写词典',
        'filename': 'anime.md',
        'categories': {
            '作品类型': lambda e: any(kw in e['meaning'] for kw in ['片头', '片尾', '原创动画', '蓝光']),
            '制作相关': lambda e: any(kw in e['meaning'] for kw in ['声优', '配音', '角色扮演']),
            '角色/性格': lambda e: any(kw in e['meaning'] for kw in ['傲娇', '病娇', '萌', '可爱']),
            '粉丝文化': lambda e: any(kw in e['meaning'] for kw in ['老婆', '老公', '御宅', '迷恋']),
            '题材分类': lambda e: any(kw in e['meaning'] for kw in ['异世界', '少年', '少女', '青年', '女性', '机甲']),
            '日语空耳': lambda e: e.get('source') == 'builtin' and any(kw in e['full_form'] for kw in ['何', '先生', '先辈', '後輩', '凄い']),
        },
    },
    'finance': {
        'title': '金融/商业缩写词典',
        'filename': 'finance.md',
        'categories': {
            '投资/交易': lambda e: any(kw in e['meaning'] for kw in ['募股', '市盈', '市净', '风险投资', '回报', '基金', '资产', '场外']),
            '市场状态': lambda e: any(kw in e['meaning'] for kw in ['熊市', '牛市', '看涨', '看跌', '最高价', '最低价']),
            '加密货币': lambda e: any(kw in e['meaning'] for kw in ['代币', '自治', '去中心化', '中心化', '交易所', '山寨', '稳定', '手续费', '区块链']),
            '加密文化': lambda e: any(kw in e['meaning'] for kw in ['持有', '错过', '研究', '亏', '大户', '跑路', '飞涨', '空投', '质押', '收益']),
        },
    },
    'academic': {
        'title': '学术/教育缩写词典',
        'filename': 'academic.md',
        'categories': {
            '考试/标准化测试': lambda e: any(kw in e['meaning'] for kw in ['考试', '测试', '入学', '托福', '雅思', '绩点']),
            '学位/学历': lambda e: any(kw in e['meaning'] for kw in ['学士', '硕士', '博士', '文凭', '学位']),
            '学术发表': lambda e: any(kw in e['meaning'] for kw in ['索引', '引文', '论文', '摘要', '引用', '评审']),
            '学术职位': lambda e: any(kw in e['meaning'] for kw in ['助理', '助教', '研究员', '教授']),
        },
    },
}

UNCATEGORIZED = '其他'


def load_db():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def categorize_entry(entry, domain_meta):
    """根据含义关键词将词条归入子类"""
    for cat_name, matcher in domain_meta['categories'].items():
        try:
            if matcher(entry):
                return cat_name
        except (KeyError, TypeError):
            continue
    return UNCATEGORIZED


def generate_domain_md(domain, meta, entries):
    """生成单个领域的 Markdown 文件"""
    lines = [f"# {meta['title']}\n"]

    # 按子类分组
    categorized = defaultdict(list)
    for e in entries:
        cat = categorize_entry(e, meta)
        categorized[cat].append(e)

    # 按定义的类别顺序输出
    cat_order = list(meta['categories'].keys())
    if UNCATEGORIZED in categorized:
        cat_order.append(UNCATEGORIZED)

    for cat_name in cat_order:
        cat_entries = categorized.get(cat_name, [])
        if not cat_entries:
            continue
        lines.append(f"## {cat_name}\n")
        lines.append("| 缩写 | 全称 | 含义 | 置信度 | 例句 |")
        lines.append("|------|------|------|--------|------|")
        for e in sorted(cat_entries, key=lambda x: x['abbreviation']):
            conf = f"{e['confidence']*100:.0f}%"
            example = e['examples'][0] if e.get('examples') else ''
            notes = f" ⚠️ {e['notes']}" if e.get('notes') else ''
            lines.append(f"| {e['abbreviation']} | {e['full_form']} | {e['meaning']}{notes} | {conf} | {example} |")
        lines.append("")

    return "\n".join(lines)


def generate_ambiguous_md(db):
    """生成多义缩写对照表"""
    # 找出有多个不同含义的缩写
    from collections import Counter
    abbr_domains = defaultdict(list)
    for e in db['entries']:
        key = e['abbreviation'].lower()
        abbr_domains[key].append(e)

    lines = ["# 常见多义缩写对照表\n"]
    lines.append("> 自动生成自 scripts/slang_db.json\n")

    multi = {k: v for k, v in abbr_domains.items()
             if len(set(e['domain'] for e in v)) >= 2}

    if not multi:
        lines.append("暂无跨领域多义缩写。")
        return "\n".join(lines)

    lines.append("## 跨领域多义缩写\n")

    for abbr in sorted(multi.keys()):
        entries = multi[abbr]
        lines.append(f"### {abbr.upper()}\n")
        lines.append("| 含义 | 领域 | 置信度 | 说明 |")
        lines.append("|------|------|--------|------|")
        for e in sorted(entries, key=lambda x: -x['confidence']):
            lines.append(f"| {e['full_form']} | {e['domain']} | {e['confidence']*100:.0f}% | {e['meaning']} |")
        lines.append("")

    return "\n".join(lines)


DOMAIN_CN = {
    'entertainment': '娱乐圈', 'gaming': '游戏圈', 'lifestyle': '生活/网络',
    'tech': '科技/互联网', 'anime': '动漫/二次元', 'finance': '金融/商业',
    'academic': '学术/教育', 'unknown': '未知',
}


def generate_templates_md(db):
    """生成用户交互话术模板，内嵌领域示例数据"""
    by_domain = defaultdict(list)
    for e in db['entries']:
        by_domain[e['domain']].append(e)

    # 每领域取置信度最高的3个作为示例
    domain_examples = {}
    for domain, entries in by_domain.items():
        top = sorted(entries, key=lambda x: -x['confidence'])[:3]
        domain_examples[domain] = [e['abbreviation'] for e in top]

    lines = [
        "# 用户交互话术模板库\n",
        "> 自动生成自 scripts/slang_db.json，领域示例基于实际数据。\n",
        "## 1. 发现未知缩写\n",
        "### 1.1 通用询问模板\n",
        "```",
        "我发现了缩写 '{缩写}'，但不在我的知识库中。",
        "",
        "为了帮您准确解析，请告诉我：",
        "1. 场景：这是什么领域的对话？",
        "   - 游戏/电竞",
        "   - 娱乐/饭圈/明星",
        "   - 科技/编程/工作",
        "   - 生活/日常聊天",
        "   - 动漫/二次元",
        "   - 金融/投资",
        "   - 学术/教育",
        "   - 其他：_____",
        "",
        "2. 完整句子：能否提供包含这个缩写的完整句子？",
        "3. 来源：在哪里看到的？（微博/弹幕/游戏/微信群等）",
        "```\n",
        "### 1.2 简短询问模板\n",
        "```",
        "发现了缩写 '{缩写}'，请问这是什么领域的？",
        "```\n",
        "## 2. 多义性歧义处理\n",
        "### 2.1 高歧义缩写\n",
        "```",
        "'{缩写}' 有多种常见含义：",
        "",
        "1. {含义A}（{领域A}）",
        "2. {含义B}（{领域B}）",
        "3. {含义C}（{领域C}）",
        "",
        "请问您遇到的是哪一种？",
        "```\n",
        "### 2.2 上下文推断确认\n",
        "```",
        "根据您的场景，我认为 '{缩写}' 更可能是 {推断含义}。",
        "请问对吗？",
        "```\n",
        "## 3. 搜索结果呈现\n",
        "### 3.1 搜索后确认\n",
        "```",
        "根据网络搜索，'{缩写}' 可能有以下含义：",
        "",
        "1. {含义1}（来源：{来源1}，置信度：{置信度1}）",
        "2. {含义2}（来源：{来源2}，置信度：{置信度2}）",
        "",
        "请问您指的是哪一个？",
        "```\n",
        "## 4. 解析结果呈现\n",
        "### 4.1 单义缩写\n",
        "```",
        "{缩写} = {全称}",
        "含义：{含义}",
        "领域：{领域} | 置信度：{置信度}%",
        "例句：{例句}",
        "```\n",
        "### 4.2 多义缩写\n",
        "```",
        "'{缩写}' 有 {数量} 种常见含义：",
        "",
        "1. {含义A}（{领域A}，置信度：{置信A}%）",
        "2. {含义B}（{领域B}，置信度：{置信B}%）",
        "",
        "告诉我具体场景可以帮您确定最准确的含义。",
        "```\n",
        "## 5. 搜索无结果时\n",
        "```",
        "搜索了缩写 '{缩写}'，但没有找到明确的含义。",
        "",
        "建议：",
        "1. 在搜索引擎中查询 \"{缩写} 是什么意思\"",
        "2. 提供更多上下文帮助判断",
        "3. 直接询问对方是什么意思",
        "```\n",
        "## 6. 搜索降级\n",
        "```",
        "暂时无法联网搜索 '{缩写}'，建议您：",
        "1. 在搜索引擎中查询 \"{缩写} 是什么意思\"",
        "2. 提供更多上下文帮助我判断",
        "```\n",
        "## 7. 领域示例参考\n",
    ]

    for domain, examples in sorted(domain_examples.items()):
        cn = DOMAIN_CN.get(domain, domain)
        lines.append(f"- **{cn}**：{', '.join(examples)}")

    lines.append("")
    return "\n".join(lines)


def main():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found")
        sys.exit(1)

    db = load_db()
    os.makedirs(REFS_DIR, exist_ok=True)

    # 按领域分组
    by_domain = defaultdict(list)
    for e in db['entries']:
        by_domain[e['domain']].append(e)

    # 生成各领域 .md
    generated = []
    for domain, meta in DOMAIN_META.items():
        entries = by_domain.get(domain, [])
        if not entries:
            continue
        content = generate_domain_md(domain, meta, entries)
        path = os.path.join(REFS_DIR, meta['filename'])
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        generated.append(f"  {meta['filename']}: {len(entries)} entries")

    # 生成多义缩写表
    ambiguous_content = generate_ambiguous_md(db)
    ambiguous_path = os.path.join(REFS_DIR, 'ambiguous-abbreviations.md')
    with open(ambiguous_path, 'w', encoding='utf-8') as f:
        f.write(ambiguous_content)
    generated.append(f"  ambiguous-abbreviations.md: {len([k for k in set(e['abbreviation'].lower() for e in db['entries']) if sum(1 for x in db['entries'] if x['abbreviation'].lower() == k and len(set(y['domain'] for y in db['entries'] if y['abbreviation'].lower() == k)) >= 2)])} multi-domain entries")

    # 生成话术模板
    templates_content = generate_templates_md(db)
    templates_path = os.path.join(REFS_DIR, 'templates.md')
    with open(templates_path, 'w', encoding='utf-8') as f:
        f.write(templates_content)
    generated.append(f"  templates.md: {db['total_entries']} entries referenced")

    print(f"Generated {len(generated)} files:")
    for g in generated:
        print(g)
    print(f"\nTotal entries in db: {db['total_entries']}")


if __name__ == '__main__':
    main()
