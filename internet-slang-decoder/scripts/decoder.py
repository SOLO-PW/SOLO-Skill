#!/usr/bin/env python3
"""
互联网缩写解析器
支持多领域缩写识别、搜索验证、多义性排序、搜索结果回填
"""

import re
import json
import sys
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

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
    "academic": "学术/专业",
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
        entertainment_data = [
            ("yyds", "永远的神", "表示某人/某物很厉害", Domain.ENTERTAINMENT, 0.95, ["这首歌真是yyds！"]),
            ("xswl", "笑死我了", "表示非常好笑", Domain.ENTERTAINMENT, 0.95, ["这个段子xswl"]),
            ("awsl", "啊我死了", "表示被萌到或震惊", Domain.ENTERTAINMENT, 0.9, ["小猫太可爱了awsl"]),
            ("zqsg", "真情实感", "表示投入真感情", Domain.ENTERTAINMENT, 0.9, ["zqsg追了这部剧"]),
            ("nbcs", "nobody cares", "没人在意", Domain.ENTERTAINMENT, 0.85, ["他的回应nbcs"]),
            ("u1s1", "有一说一", "客观评价", Domain.ENTERTAINMENT, 0.9, ["u1s1，这个演技确实不错"]),
            ("nsdd", "你说得对", "表示认同", Domain.ENTERTAINMENT, 0.9, ["nsdd，我也这么觉得"]),
            ("bhs", "不好笑", "表示不好笑", Domain.ENTERTAINMENT, 0.85, ["这个梗bhs"]),
            ("bhys", "不好意思", "表示抱歉", Domain.ENTERTAINMENT, 0.85, ["bhys，我来晚了"]),
            ("szd", "是真的", "表示确认", Domain.ENTERTAINMENT, 0.9, ["这对CP szd！"]),
            ("wlsw", "圈外人", "指不了解圈内的人", Domain.ENTERTAINMENT, 0.85, ["wlsw不懂这个梗"]),
            ("sjd", "是假的", "表示否定", Domain.ENTERTAINMENT, 0.85, ["这个传闻sjd"]),
            ("kswl", "磕死我了", "表示对CP很上头", Domain.ENTERTAINMENT, 0.9, ["他们互动kswl！"]),
            ("drl", "打扰了", "表示打扰或告辞", Domain.ENTERTAINMENT, 0.85, ["价格太高，drl"]),
            ("pyq", "朋友圈", "微信朋友圈", Domain.LIFESTYLE, 0.95, ["发pyq了"]),
            ("dbq", "对不起", "表示道歉", Domain.ENTERTAINMENT, 0.9, ["dbq我迟到了"]),
            ("xjj", "小姐姐", "对年轻女性的称呼", Domain.ENTERTAINMENT, 0.85, ["那个xjj好可爱"]),
            ("xgg", "小哥哥", "对年轻男性的称呼", Domain.ENTERTAINMENT, 0.85, ["那个xgg好帅"]),
            ("dd", "弟弟/顶顶", "弟弟或顶帖", Domain.ENTERTAINMENT, 0.8, ["dd帮忙顶一下"]),
            ("ssfd", "瑟瑟发抖", "表示害怕或紧张", Domain.ENTERTAINMENT, 0.85, ["看到那个画面ssfd"]),
            ("nsdd", "你说得对", "表示认同", Domain.ENTERTAINMENT, 0.9, ["nsdd"]),
            ("xfxy", "腥风血雨", "饭圈激烈争斗", Domain.ENTERTAINMENT, 0.8, ["今天又是xfxy的一天"]),
            ("rnm", "饶命/退网", "网络用语", Domain.ENTERTAINMENT, 0.75, ["rnm别再说了"]),
        ]
        gaming_data = [
            ("gg", "good game", "游戏结束/认输", Domain.GAMING, 0.9, ["gg，这局输了"]),
            ("wp", "well played", "打得好", Domain.GAMING, 0.85, ["wp，对手很强"]),
            ("afk", "away from keyboard", "暂时离开", Domain.GAMING, 0.9, ["我去afk一下"]),
            ("brb", "be right back", "马上回来", Domain.GAMING, 0.9, ["brb，接个电话"]),
            ("glhf", "good luck have fun", "祝好运", Domain.GAMING, 0.85, ["glhf，大家加油"]),
            ("op", "overpowered", "太强/超模", Domain.GAMING, 0.9, ["这个英雄太op了"]),
            ("nerf", "削弱", "游戏平衡调整", Domain.GAMING, 0.85, ["这个英雄被nerf了"]),
            ("buff", "增强", "游戏平衡调整", Domain.GAMING, 0.9, ["获得攻击力buff"]),
            ("mvp", "most valuable player", "最有价值玩家", Domain.GAMING, 0.95, ["这局我是mvp"]),
            ("noob", "newbie", "新手/菜鸟", Domain.GAMING, 0.85, ["别欺负noob"]),
            ("pog", "play of the game", "精彩操作", Domain.GAMING, 0.8, ["这波操作pog！"]),
            ("ez", "easy", "轻松", Domain.GAMING, 0.85, ["ez win"]),
            ("clutch", "关键时刻", "关键时刻的表现", Domain.GAMING, 0.8, ["这波clutch太帅了"]),
            ("troll", "捣乱", "故意捣乱", Domain.GAMING, 0.85, ["别troll了，认真玩"]),
            ("int", "intentional feeding", "故意送人头", Domain.GAMING, 0.8, ["他在int"]),
            ("gank", "游走抓人", "偷袭/抓人", Domain.GAMING, 0.85, ["来gank中路"]),
            ("carry", "带飞", "带领队伍获胜", Domain.GAMING, 0.85, ["他carry全场"]),
            ("feed", "送人头", "养肥对手", Domain.GAMING, 0.85, ["别feed了"]),
            ("cd", "cooldown", "冷却时间", Domain.GAMING, 0.9, ["技能还在cd"]),
            ("hp", "health points", "生命值", Domain.GAMING, 0.9, ["hp快没了"]),
            ("ult", "ultimate", "大招", Domain.GAMING, 0.85, ["放ult"]),
            ("adc", "attack damage carry", "射手", Domain.GAMING, 0.9, ["我玩adc"]),
            ("ap", "ability power", "法术强度", Domain.GAMING, 0.85, ["ap伤害"]),
            ("dps", "damage per second", "输出/秒伤", Domain.GAMING, 0.9, ["dps不够"]),
            ("aggro", "aggression", "仇恨值", Domain.GAMING, 0.8, ["拉aggro"]),
            ("cc", "crowd control", "控制技能", Domain.GAMING, 0.8, ["被cc住了"]),
            ("aoe", "area of effect", "范围伤害", Domain.GAMING, 0.85, ["aoe技能"]),
            ("pve", "player vs environment", "玩家对环境", Domain.GAMING, 0.9, ["pve副本"]),
            ("pvp", "player vs player", "玩家对战", Domain.GAMING, 0.9, ["pvp模式"]),
            ("kda", "kill death assist", "击杀死亡助攻比", Domain.GAMING, 0.9, ["kda很好看"]),
            ("smurf", "炸鱼小号", "高手玩低分段", Domain.GAMING, 0.8, ["对面有smurf"]),
            ("toxic", "有毒行为", "负面行为", Domain.GAMING, 0.85, ["这人好toxic"]),
            ("salty", "输不起", "生气/不服", Domain.GAMING, 0.8, ["别salty了"]),
        ]
        lifestyle_data = [
            ("btw", "by the way", "顺便说一下", Domain.LIFESTYLE, 0.95, ["btw，你吃饭了吗"]),
            ("imo", "in my opinion", "在我看来", Domain.LIFESTYLE, 0.9, ["imo，这个更好"]),
            ("imho", "in my humble opinion", "依我拙见", Domain.LIFESTYLE, 0.85, ["imho，这样不太好"]),
            ("fyi", "for your information", "供你参考", Domain.LIFESTYLE, 0.95, ["fyi，会议改时间了"]),
            ("asap", "as soon as possible", "尽快", Domain.LIFESTYLE, 0.95, ["请asap回复"]),
            ("idk", "I don't know", "我不知道", Domain.LIFESTYLE, 0.9, ["idk，你问别人吧"]),
            ("idc", "I don't care", "我不在乎", Domain.LIFESTYLE, 0.9, ["idc，随你便"]),
            ("tbh", "to be honest", "说实话", Domain.LIFESTYLE, 0.9, ["tbh，我不太喜欢"]),
            ("tbf", "to be fair", "公平地说", Domain.LIFESTYLE, 0.85, ["tbf，他也有道理"]),
            ("irl", "in real life", "现实生活中", Domain.LIFESTYLE, 0.9, ["irl没见过面"]),
            ("ftw", "for the win", "必胜/支持", Domain.LIFESTYLE, 0.85, ["Python ftw！"]),
            ("ikr", "I know right", "我知道对吧", Domain.LIFESTYLE, 0.85, ["ikr！我也这么觉得"]),
            ("nvm", "never mind", "没关系", Domain.LIFESTYLE, 0.9, ["nvm，没事了"]),
            ("omw", "on my way", "在路上", Domain.LIFESTYLE, 0.9, ["omw，马上到"]),
            ("rn", "right now", "现在", Domain.LIFESTYLE, 0.9, ["我rn很忙"]),
            ("smh", "shaking my head", "摇头/无语", Domain.LIFESTYLE, 0.85, ["smh，这都能错"]),
            ("lmk", "let me know", "告诉我", Domain.LIFESTYLE, 0.9, ["lmk你的决定"]),
            ("dm", "direct message", "私信", Domain.LIFESTYLE, 0.9, ["dm我详情"]),
            ("pm", "private message", "私信", Domain.LIFESTYLE, 0.9, ["pm聊"]),
            ("lol", "laugh out loud", "大笑", Domain.LIFESTYLE, 0.95, ["lol太好笑了"]),
            ("lmao", "laugh my ass off", "笑死我了", Domain.LIFESTYLE, 0.95, ["lmao哈哈哈"]),
            ("rofl", "roll on floor laughing", "笑到打滚", Domain.LIFESTYLE, 0.9, ["rofl"]),
            ("omg", "oh my god", "我的天", Domain.LIFESTYLE, 0.95, ["omg！"]),
            ("wtf", "what the f**k", "什么鬼", Domain.LIFESTYLE, 0.9, ["wtf？"]),
            ("fml", "f**k my life", "我太难了", Domain.LIFESTYLE, 0.9, ["迟到again，fml"]),
            ("ngl", "not gonna lie", "说实话", Domain.LIFESTYLE, 0.85, ["ngl，我挺喜欢的"]),
            ("hbu", "how about you", "你呢", Domain.LIFESTYLE, 0.85, ["我很好，hbu"]),
            ("wyd", "what you doing", "你在干嘛", Domain.LIFESTYLE, 0.85, ["wyd现在"]),
            ("hmu", "hit me up", "联系我", Domain.LIFESTYLE, 0.85, ["有事hmu"]),
            ("atm", "at the moment", "此刻", Domain.LIFESTYLE, 0.9, ["atm不方便"]),
            ("eta", "estimated time of arrival", "预计到达时间", Domain.LIFESTYLE, 0.9, ["eta是几点"]),
            ("tbd", "to be determined", "待定", Domain.LIFESTYLE, 0.9, ["时间tbd"]),
            ("eod", "end of day", "今天结束前", Domain.LIFESTYLE, 0.9, ["eod前给我"]),
            ("np", "no problem", "没问题", Domain.LIFESTYLE, 0.9, ["np，小事"]),
            ("ty", "thank you", "谢谢", Domain.LIFESTYLE, 0.9, ["ty帮忙"]),
            ("pls", "please", "请", Domain.LIFESTYLE, 0.9, ["pls帮我"]),
            ("sry", "sorry", "对不起", Domain.LIFESTYLE, 0.9, ["sry迟到了"]),
            ("thx", "thanks", "谢谢", Domain.LIFESTYLE, 0.9, ["thx！"]),
            ("gl", "good luck", "祝好运", Domain.LIFESTYLE, 0.9, ["gl考试"]),
            ("hf", "have fun", "玩得开心", Domain.LIFESTYLE, 0.9, ["hf！"]),
            ("gn", "good night", "晚安", Domain.LIFESTYLE, 0.9, ["gn～"]),
            ("gm", "good morning", "早安", Domain.LIFESTYLE, 0.9, ["gm！"]),
            ("wb", "welcome back", "欢迎回来", Domain.LIFESTYLE, 0.9, ["wb！"]),
        ]
        tech_data = [
            ("api", "application programming interface", "应用程序接口", Domain.TECH, 0.95, ["调用api"]),
            ("ui", "user interface", "用户界面", Domain.TECH, 0.95, ["ui设计"]),
            ("ux", "user experience", "用户体验", Domain.TECH, 0.95, ["ux优化"]),
            ("dev", "developer", "开发者", Domain.TECH, 0.9, ["dev团队"]),
            ("prod", "production", "生产环境", Domain.TECH, 0.85, ["部署到prod"]),
            ("qa", "quality assurance", "质量保证", Domain.TECH, 0.9, ["qa测试"]),
            ("pr", "pull request", "合并请求", Domain.TECH, 0.9, ["提交pr"]),
            ("repo", "repository", "代码仓库", Domain.TECH, 0.9, ["克隆repo"]),
            ("lgtm", "looks good to me", "我觉得可以", Domain.TECH, 0.9, ["lgtm，合并吧"]),
            ("sgtm", "sounds good to me", "听起来不错", Domain.TECH, 0.85, ["sgtm，就这么办"]),
            ("ptal", "please take a look", "请看一下", Domain.TECH, 0.85, ["ptal这个pr"]),
            ("nit", "nitpick", "小建议", Domain.TECH, 0.8, ["nit：这里可以优化"]),
            ("wip", "work in progress", "进行中", Domain.TECH, 0.9, ["wip，还没完成"]),
            ("rfc", "request for comments", "征求意见", Domain.TECH, 0.85, ["发一个rfc"]),
            ("poc", "proof of concept", "概念验证", Domain.TECH, 0.85, ["做个poc"]),
            ("ci", "continuous integration", "持续集成", Domain.TECH, 0.9, ["ci流程"]),
            ("cd", "continuous deployment", "持续部署", Domain.TECH, 0.9, ["cd流水线"]),
            ("sdk", "software development kit", "软件开发工具包", Domain.TECH, 0.9, ["下载sdk"]),
            ("orm", "object-relational mapping", "对象关系映射", Domain.TECH, 0.85, ["使用orm"]),
            ("crud", "create read update delete", "增删改查", Domain.TECH, 0.85, ["实现crud"]),
            ("dns", "domain name system", "域名系统", Domain.TECH, 0.9, ["配置dns"]),
            ("ssl", "secure sockets layer", "安全套接层", Domain.TECH, 0.9, ["配置ssl"]),
            ("cdn", "content delivery network", "内容分发网络", Domain.TECH, 0.9, ["用cdn加速"]),
            ("k8s", "kubernetes", "容器编排平台", Domain.TECH, 0.9, ["k8s集群"]),
            ("docker", "docker", "容器技术", Domain.TECH, 0.9, ["用docker部署"]),
            ("sre", "site reliability engineering", "站点可靠性工程", Domain.TECH, 0.85, ["sre团队"]),
            ("okr", "objectives and key results", "目标与关键成果", Domain.TECH, 0.85, ["定okr"]),
            ("kpi", "key performance indicator", "关键绩效指标", Domain.TECH, 0.85, ["kpi考核"]),
            ("ceo", "chief executive officer", "首席执行官", Domain.TECH, 0.95, ["ceo讲话"]),
            ("cto", "chief technology officer", "技术总监", Domain.TECH, 0.95, ["cto决策"]),
            ("fe", "front end", "前端", Domain.TECH, 0.9, ["fe开发"]),
            ("be", "back end", "后端", Domain.TECH, 0.9, ["be接口"]),
            ("ai", "artificial intelligence", "人工智能", Domain.TECH, 0.95, ["ai技术"]),
            ("llm", "large language model", "大语言模型", Domain.TECH, 0.9, ["llm应用"]),
            ("bug", "缺陷", "程序错误", Domain.TECH, 0.95, ["修bug"]),
            ("log", "日志", "运行记录", Domain.TECH, 0.9, ["看log"]),
            ("tag", "标签", "版本标签", Domain.TECH, 0.85, ["打tag"]),
        ]
        for data in entertainment_data + gaming_data + lifestyle_data + tech_data:
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

    def extract_abbreviations(self, text: str) -> List[str]:
        # 中英混合文本中，\b 不起作用，用 [^a-zA-Z] 分割
        pattern = r'[a-zA-Z]{2,6}'
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
            'hard', 'really', 'began', 'since', 'before', 'early', 'body', 'state',
            'white', 'black', 'red', 'blue', 'best', 'door', 'between', 'need',
            'while', 'again', 'car', 'night', 'order', 'paper', 'group', 'children',
            'face', 'plan', 'quite', 'class', 'music', 'mind', 'today', 'money',
            'bring', 'happen', 'stand', 'room', 'book', 'map', 'air', 'write',
            'test', 'table', 'river', 'second', 'hold', 'fire', 'watch', 'listen',
            'build', 'spend', 'grow', 'low', 'true', 'cold', 'eat', 'dog', 'top',
            'road', 'mark', 'rock', 'short', 'food', 'love', 'girl', 'person',
            'art', 'bird', 'fish', 'mountain', 'sing', 'color', 'ball', 'game',
        }
        abbreviations = []
        for match in matches:
            match_lower = match.lower()
            if match_lower in self.db.entries or match_lower not in common_words:
                abbreviations.append(match)
        return list(set(abbreviations))

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
        """为未知缩写生成搜索查询"""
        if not unknown_abbrs:
            return []

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
            if hint:
                q_list.append(f'"{abbr}" {hint} 含义')
            else:
                q_list.append(f'"{abbr}" 网络用语 缩写')
            queries.append({'abbreviation': abbr, 'queries': q_list})
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
        return {'abbreviation': abbreviation, 'matches': added, 'source': 'web_search'}

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

def main():
    import argparse
    parser = argparse.ArgumentParser(description='互联网缩写解析器')
    parser.add_argument('text', help='要解析的文本')
    parser.add_argument('--context', '-c', help='上下文领域')
    parser.add_argument('--json', '-j', action='store_true', help='JSON输出')
    args = parser.parse_args()

    decoder = SlangDecoder()
    result = decoder.decode(args.text, args.context)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    else:
        print(decoder.format_output(result))
        if result['search_queries']:
            print(decoder.format_search_queries(result))

if __name__ == '__main__':
    main()
