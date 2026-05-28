#!/usr/bin/env python3
"""
互联网废话文学生成器
根据用户输入的情景对话等内容，分析合适的言论话术，并转化为废话文学
"""

import re
import json
import random
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# 废话文学类型枚举
class NonsenseType(Enum):
    """废话文学类型"""
    SYNONYM_REPEAT = "synonym_repeat"  # 同义反复
    TIME_LOOP = "time_loop"  # 时间循环
    CONDITIONAL = "conditional"  # 条件假设
    UNIT_CONVERSION = "unit_conversion"  # 单位转换
    OBVIOUS = "obvious"  # 众所周知
    LEADER_SPEECH = "leader_speech"  # 领导讲话
    REVERSAL = "reversal"  # 逆转
    ASSUMPTION = "assumption"  # 假设
    FOLLOW_UP = "follow_up"  # 顺接
    RHYME = "rhyme"  # 押韵
    LONG_SENTENCE = "long_sentence"  # 长句式
    CONTRADICTION = "contradiction"  # 前后矛盾
    LITERATURE = "literature"  # 文学改编
    HOPE = "hope"  # 美好希望
    REDUNDANCY = "redundancy"  # 冗余信息

# 废话文学类型中文映射
NONSESE_TYPE_CN = {
    NonsenseType.SYNONYM_REPEAT: "同义反复",
    NonsenseType.TIME_LOOP: "时间循环",
    NonsenseType.CONDITIONAL: "条件假设",
    NonsenseType.UNIT_CONVERSION: "单位转换",
    NonsenseType.OBVIOUS: "众所周知",
    NonsenseType.LEADER_SPEECH: "领导讲话",
    NonsenseType.REVERSAL: "逆转",
    NonsenseType.ASSUMPTION: "假设",
    NonsenseType.FOLLOW_UP: "顺接",
    NonsenseType.RHYME: "押韵",
    NonsenseType.LONG_SENTENCE: "长句式",
    NonsenseType.CONTRADICTION: "前后矛盾",
    NonsenseType.LITERATURE: "文学改编",
    NonsenseType.HOPE: "美好希望",
    NonsenseType.REDUNDANCY: "冗余信息",
}

@dataclass
class NonsenseTemplate:
    """废话文学模板"""
    type: NonsenseType
    template: str
    examples: List[str]
    keywords: List[str]

class NonsenseGenerator:
    """废话文学生成器"""
    
    # 情绪词列表
    EMOTIONS = ["急", "忙", "饿", "困", "累", "无语", "好笑", "生气", "开心"]
    
    # 对象词列表
    OBJECTS = ["西红柿", "番茄", "鸡蛋", "苹果", "手机"]
    
    # 动作-结果配对
    ACTION_RESULT_PAIRS = [("胖", "体重变重"), ("饿", "想吃饭"), ("困", "想睡觉")]
    
    # 品质词列表
    QUALITIES = ["本事", "能力", "耐心", "毅力"]
    
    # 负面-正面词配对
    NEGATIVE_POSITIVE_PAIRS = [("丑", "好看"), ("笨", "聪明"), ("懒", "勤快")]
    
    # 需要移除的常见词
    REMOVE_WORDS = ["如果", "怎么", "如何", "说", "用", "废话", "文学", "回复", "面对", "情况", "有人", "我", "你", "他", "她", "它", "们", "在", "了", "的", "吗", "呢", "吧", "啊"]
    
    def __init__(self):
        self.templates = self._load_templates()
        self.scene_keywords = self._load_scene_keywords()
    
    def _load_templates(self) -> Dict[NonsenseType, List[NonsenseTemplate]]:
        """加载废话文学模板"""
        templates = {
            NonsenseType.SYNONYM_REPEAT: [
                NonsenseTemplate(
                    type=NonsenseType.SYNONYM_REPEAT,
                    template="情况就是这么个情况，但具体{topic}，还得看{topic}",
                    examples=["情况就是这么个情况，但具体什么情况，还得看情况"],
                    keywords=["情况", "问题", "事情"]
                ),
                NonsenseTemplate(
                    type=NonsenseType.SYNONYM_REPEAT,
                    template="说{topic}也{topic}，说不{topic}也不{topic}",
                    examples=["说重要也重要，说不重要也不重要"],
                    keywords=["重要", "紧急", "困难"]
                ),
                NonsenseTemplate(
                    type=NonsenseType.SYNONYM_REPEAT,
                    template="有没有{topic}是要根据有没有{topic}来判定的",
                    examples=["有没有意义是要根据有没有意义来判定的"],
                    keywords=["意义", "价值", "作用"]
                ),
            ],
            NonsenseType.TIME_LOOP: [
                NonsenseTemplate(
                    type=NonsenseType.TIME_LOOP,
                    template="上次这么{emotion}的时候，还是上次",
                    examples=["上次这么无语的时候，还是上次"],
                    keywords=["无语", "好笑", "生气", "开心"]
                ),
                NonsenseTemplate(
                    type=NonsenseType.TIME_LOOP,
                    template="一日不见如隔一日",
                    examples=["一日不见如隔一日"],
                    keywords=["见面", "时间"]
                ),
            ],
            NonsenseType.CONDITIONAL: [
                NonsenseTemplate(
                    type=NonsenseType.CONDITIONAL,
                    template="但凡你有点{quality}，也不至于一点{quality}没有",
                    examples=["但凡你有点本事，也不至于一点本事没有"],
                    keywords=["本事", "能力", "耐心"]
                ),
                NonsenseTemplate(
                    type=NonsenseType.CONDITIONAL,
                    template="你要是不{negative}的话，其实还挺{positive}的",
                    examples=["你要是不丑的话，其实还挺好看的"],
                    keywords=[("丑", "好看"), ("笨", "聪明"), ("懒", "勤快")]
                ),
            ],
            NonsenseType.UNIT_CONVERSION: [
                NonsenseTemplate(
                    type=NonsenseType.UNIT_CONVERSION,
                    template="每呼吸六十秒，就过去了一分钟",
                    examples=["每呼吸六十秒，就过去了一分钟"],
                    keywords=["时间", "呼吸"]
                ),
                NonsenseTemplate(
                    type=NonsenseType.UNIT_CONVERSION,
                    template="每过一天，就离昨天更远了一天",
                    examples=["每过一天，就离昨天更远了一天"],
                    keywords=["时间", "天"]
                ),
            ],
            NonsenseType.OBVIOUS: [
                NonsenseTemplate(
                    type=NonsenseType.OBVIOUS,
                    template="这个{object}，有一股{object}味儿",
                    examples=["这个西红柿，有一股番茄味儿"],
                    keywords=["西红柿", "番茄", "鸡蛋"]
                ),
                NonsenseTemplate(
                    type=NonsenseType.OBVIOUS,
                    template="我发现，我{action}之后，就{result}了",
                    examples=["我发现，我胖了之后，体重就变重了"],
                    keywords=[("胖", "体重变重"), ("饿", "想吃饭")]
                ),
            ],
            NonsenseType.LEADER_SPEECH: [
                NonsenseTemplate(
                    type=NonsenseType.LEADER_SPEECH,
                    template="既然让我讲两句，那我就来讲两句，具体哪两句呢? 我先随便讲两句",
                    examples=["既然让我讲两句，那我就来讲两句，具体哪两句呢? 我先随便讲两句"],
                    keywords=["讲话", "发言"]
                ),
                NonsenseTemplate(
                    type=NonsenseType.LEADER_SPEECH,
                    template="全文内容大概是这么个事啊，我们讲不是说，不是说不办。但是……",
                    examples=["全文内容大概是这么个事啊，我们讲不是说，不是说不办。但是……"],
                    keywords=["事情", "问题"]
                ),
            ],
            NonsenseType.REVERSAL: [
                NonsenseTemplate(
                    type=NonsenseType.REVERSAL,
                    template="我知道你很{emotion}，但是你先别{emotion}",
                    examples=["我知道你很急，但是你先别急"],
                    keywords=["急", "忙", "饿", "困"]
                ),
                NonsenseTemplate(
                    type=NonsenseType.REVERSAL,
                    template="给你提个建议，你不要随便给别人提建议",
                    examples=["给你提个建议，你不要随便给别人提建议"],
                    keywords=["建议"]
                ),
            ],
            NonsenseType.ASSUMPTION: [
                NonsenseTemplate(
                    type=NonsenseType.ASSUMPTION,
                    template="如果我有{object}，那么这句话就不用加如果两个字了",
                    examples=["如果我有男朋友，那么这句话就不用加如果两个字了"],
                    keywords=["男朋友", "女朋友", "钱"]
                ),
            ],
            NonsenseType.FOLLOW_UP: [
                NonsenseTemplate(
                    type=NonsenseType.FOLLOW_UP,
                    template="俗话说得好：俗话说得好",
                    examples=["俗话说得好：俗话说得好"],
                    keywords=["俗话", "古话"]
                ),
                NonsenseTemplate(
                    type=NonsenseType.FOLLOW_UP,
                    template="能力越大，能力就越大",
                    examples=["能力越大，能力就越大"],
                    keywords=["能力", "责任"]
                ),
            ],
            NonsenseType.RHYME: [
                NonsenseTemplate(
                    type=NonsenseType.RHYME,
                    template="我前脚刚走，后脚就跟上了",
                    examples=["我前脚刚走，后脚就跟上了"],
                    keywords=["走", "跟"]
                ),
                NonsenseTemplate(
                    type=NonsenseType.RHYME,
                    template="你跟我搁这儿搁这儿呢",
                    examples=["你跟我搁这儿搁这儿呢"],
                    keywords=["这儿", "那儿"]
                ),
            ],
            NonsenseType.LONG_SENTENCE: [
                NonsenseTemplate(
                    type=NonsenseType.LONG_SENTENCE,
                    template="关于{topic}，我简单说两句，第一句是我要说两句，第二句是我说完了",
                    examples=["关于这个问题，我简单说两句，第一句是我要说两句，第二句是我说完了"],
                    keywords=["问题", "事情", "项目"]
                ),
                NonsenseTemplate(
                    type=NonsenseType.LONG_SENTENCE,
                    template="这个{topic}很重要，重要到什么程度呢？重要到很重要",
                    examples=["这个事情很重要，重要到什么程度呢？重要到很重要"],
                    keywords=["事情", "问题", "项目"]
                ),
                NonsenseTemplate(
                    type=NonsenseType.LONG_SENTENCE,
                    template="既然你问到了{topic}，那我就不得不回答一下{topic}，{topic}问得好，好在哪里呢？好在问得好",
                    examples=["既然你问到了这个问题，那我就不得不回答一下这个问题，这个问题问得好，好在哪里呢？好在问得好"],
                    keywords=["问题", "事情", "项目"]
                ),
                NonsenseTemplate(
                    type=NonsenseType.LONG_SENTENCE,
                    template="我简单说三点，第一点是我要说三点，第二点是我说完了，第三点是补充前两点",
                    examples=["我简单说三点，第一点是我要说三点，第二点是我说完了，第三点是补充前两点"],
                    keywords=["三点", "三点"]
                ),
            ],
            NonsenseType.CONTRADICTION: [
                NonsenseTemplate(
                    type=NonsenseType.CONTRADICTION,
                    template="我上次这么{emotion}的时候，还是上次，具体什么时候呢？就是上次",
                    examples=["我上次这么无语的时候，还是上次，具体什么时候呢？就是上次"],
                    keywords=["无语", "好笑", "生气", "开心"]
                ),
                NonsenseTemplate(
                    type=NonsenseType.CONTRADICTION,
                    template="这个方案可行不可行呢？可行，但具体怎么行，还得看怎么不行",
                    examples=["这个方案可行不可行呢？可行，但具体怎么行，还得看怎么不行"],
                    keywords=["方案", "计划", "项目"]
                ),
                NonsenseTemplate(
                    type=NonsenseType.CONTRADICTION,
                    template="你说的话但凡有一点{quality}也不至于一点{quality}没有",
                    examples=["你说的话但凡有一点意义也不至于一点意义也没有"],
                    keywords=["意义", "价值", "作用"]
                ),
            ],
            NonsenseType.LITERATURE: [
                NonsenseTemplate(
                    type=NonsenseType.LITERATURE,
                    template="听君一席话，如听一席话",
                    examples=["听君一席话，如听一席话"],
                    keywords=["一席话", "说话"]
                ),
                NonsenseTemplate(
                    type=NonsenseType.LITERATURE,
                    template="三人行则必有三人",
                    examples=["三人行则必有三人"],
                    keywords=["三人", "行"]
                ),
                NonsenseTemplate(
                    type=NonsenseType.LITERATURE,
                    template="一日不见如隔一日",
                    examples=["一日不见如隔一日"],
                    keywords=["一日", "不见"]
                ),
            ],
            NonsenseType.HOPE: [
                NonsenseTemplate(
                    type=NonsenseType.HOPE,
                    template="如果我有{object}，那么这句话就不用加如果两个字了",
                    examples=["如果我有男朋友，那么这句话就不用加如果两个字了"],
                    keywords=["男朋友", "女朋友", "钱"]
                ),
                NonsenseTemplate(
                    type=NonsenseType.HOPE,
                    template="如果你愿意多花点时间了解我，你就会发现多花了点时间",
                    examples=["如果你愿意多花点时间了解我，你就会发现多花了点时间"],
                    keywords=["时间", "了解"]
                ),
                NonsenseTemplate(
                    type=NonsenseType.HOPE,
                    template="如果我不说的话，你就不知道我要说什么",
                    examples=["如果我不说的话，你就不知道我要说什么"],
                    keywords=["说", "知道"]
                ),
            ],
            NonsenseType.REDUNDANCY: [
                NonsenseTemplate(
                    type=NonsenseType.REDUNDANCY,
                    template="每呼吸六十秒，就过去了一分钟",
                    examples=["每呼吸六十秒，就过去了一分钟"],
                    keywords=["呼吸", "时间"]
                ),
                NonsenseTemplate(
                    type=NonsenseType.REDUNDANCY,
                    template="每过一天，就离昨天更远了一天",
                    examples=["每过一天，就离昨天更远了一天"],
                    keywords=["时间", "天"]
                ),
                NonsenseTemplate(
                    type=NonsenseType.REDUNDANCY,
                    template="每吃一顿饭，就少了一顿饭",
                    examples=["每吃一顿饭，就少了一顿饭"],
                    keywords=["吃饭", "饭"]
                ),
            ],
        }
        return templates
    
    def _load_scene_keywords(self) -> Dict[str, List[NonsenseType]]:
        """加载场景关键词映射"""
        return {
            "工作": [NonsenseType.LEADER_SPEECH, NonsenseType.SYNONYM_REPEAT, NonsenseType.LONG_SENTENCE],
            "会议": [NonsenseType.LEADER_SPEECH, NonsenseType.SYNONYM_REPEAT, NonsenseType.LONG_SENTENCE],
            "汇报": [NonsenseType.LEADER_SPEECH, NonsenseType.SYNONYM_REPEAT, NonsenseType.LONG_SENTENCE],
            "生活": [NonsenseType.OBVIOUS, NonsenseType.CONDITIONAL],
            "吃饭": [NonsenseType.OBVIOUS, NonsenseType.UNIT_CONVERSION, NonsenseType.REDUNDANCY],
            "天气": [NonsenseType.SYNONYM_REPEAT, NonsenseType.OBVIOUS],
            "外貌": [NonsenseType.CONDITIONAL, NonsenseType.OBVIOUS],
            "社交": [NonsenseType.TIME_LOOP, NonsenseType.REVERSAL],
            "聊天": [NonsenseType.TIME_LOOP, NonsenseType.FOLLOW_UP],
            "网络": [NonsenseType.FOLLOW_UP, NonsenseType.RHYME],
            "评论": [NonsenseType.FOLLOW_UP, NonsenseType.RHYME],
            "表白": [NonsenseType.REVERSAL, NonsenseType.ASSUMPTION, NonsenseType.HOPE],
            "被夸": [NonsenseType.FOLLOW_UP, NonsenseType.SYNONYM_REPEAT],
            "被批评": [NonsenseType.CONDITIONAL, NonsenseType.REVERSAL],
            "催婚": [NonsenseType.ASSUMPTION, NonsenseType.CONDITIONAL, NonsenseType.HOPE],
            "尴尬": [NonsenseType.SYNONYM_REPEAT, NonsenseType.TIME_LOOP],
            "发言": [NonsenseType.LONG_SENTENCE, NonsenseType.LEADER_SPEECH],
            "总结": [NonsenseType.LONG_SENTENCE, NonsenseType.SYNONYM_REPEAT],
            "矛盾": [NonsenseType.CONTRADICTION, NonsenseType.SYNONYM_REPEAT],
            "文学": [NonsenseType.LITERATURE, NonsenseType.FOLLOW_UP],
            "希望": [NonsenseType.HOPE, NonsenseType.ASSUMPTION],
            "冗余": [NonsenseType.REDUNDANCY, NonsenseType.UNIT_CONVERSION],
        }
    
    def analyze_scene(self, user_input: str) -> Tuple[Optional[str], List[NonsenseType]]:
        """
        分析用户输入的场景
        
        Args:
            user_input: 用户输入文本
            
        Returns:
            (场景名称, 推荐的废话类型列表)
        """
        # 提取关键词
        keywords = []
        for word in self.scene_keywords.keys():
            if word in user_input:
                keywords.append(word)
        
        # 根据关键词确定场景和推荐类型
        if keywords:
            scene = keywords[0]
            recommended_types = []
            for kw in keywords:
                recommended_types.extend(self.scene_keywords.get(kw, []))
            return scene, list(set(recommended_types))
        
        # 默认返回
        return None, list(NonsenseType)
    
    def extract_topic(self, user_input: str) -> str:
        """
        从用户输入中提取话题
        
        Args:
            user_input: 用户输入文本
            
        Returns:
            提取的话题词
        """
        # 提取核心话题：去掉常见关键词和标点
        topic = user_input
        for word in self.REMOVE_WORDS:
            topic = topic.replace(word, "")
        # 去掉标点
        topic = re.sub(r'[，。！？、；：""''（）【】《》]', '', topic)
        topic = topic.strip()
        # 如果话题太长，只取前10个字
        if len(topic) > 10:
            topic = topic[:10]
        return topic if topic else "这个"
    
    def generate_nonsense(self, user_input: str, count: int = 1) -> List[Dict]:
        """
        生成废话文学
        
        Args:
            user_input: 用户输入文本
            count: 生成数量
            
        Returns:
            废话文学结果列表
        """
        scene, recommended_types = self.analyze_scene(user_input)
        topic = self.extract_topic(user_input)
        
        results = []
        
        # 如果有推荐类型，优先使用
        if recommended_types:
            for _ in range(min(count, len(recommended_types))):
                nonsense_type = random.choice(recommended_types)
                templates = self.templates.get(nonsense_type, [])
                if templates:
                    template = random.choice(templates)
                    nonsense = self._apply_template(template, topic, user_input)
                    results.append({
                        "type": nonsense_type.value,
                        "type_cn": NONSESE_TYPE_CN.get(nonsense_type, nonsense_type.value),
                        "nonsense": nonsense,
                        "scene": scene,
                        "topic": topic
                    })
        
        # 如果结果不够，随机补充
        while len(results) < count:
            nonsense_type = random.choice(list(NonsenseType))
            templates = self.templates.get(nonsense_type, [])
            if templates:
                template = random.choice(templates)
                nonsense = self._apply_template(template, topic, user_input)
                results.append({
                    "type": nonsense_type.value,
                    "type_cn": NONSESE_TYPE_CN.get(nonsense_type, nonsense_type.value),
                    "nonsense": nonsense,
                    "scene": scene,
                    "topic": topic
                })
        
        return results
    
    def _apply_template(self, template: NonsenseTemplate, topic: str, user_input: str) -> str:
        """
        应用模板生成废话
        
        Args:
            template: 废话文学模板
            topic: 话题词
            user_input: 用户输入文本
            
        Returns:
            生成的废话文本
        """
        result = template.template
        
        # 替换模板中的占位符
        if "{topic}" in result:
            # 对于同义反复类型，使用更简短的关键词
            if template.type == NonsenseType.SYNONYM_REPEAT:
                # 从模板的keywords中选择一个合适的词
                short_topic = "情况"  # 默认
                for kw in template.keywords:
                    if kw in user_input:
                        short_topic = kw
                        break
                result = result.replace("{topic}", short_topic)
            else:
                result = result.replace("{topic}", topic)
        
        if "{emotion}" in result:
            found_emotion = "急"  # 默认
            for emotion in self.EMOTIONS:
                if emotion in user_input:
                    found_emotion = emotion
                    break
            result = result.replace("{emotion}", found_emotion)
        
        if "{object}" in result:
            found_object = "西红柿"  # 默认
            for obj in self.OBJECTS:
                if obj in user_input:
                    found_object = obj
                    break
            result = result.replace("{object}", found_object)
        
        if "{action}" in result and "{result}" in result:
            found_action, found_result = "胖", "体重变重"  # 默认
            for action, res in self.ACTION_RESULT_PAIRS:
                if action in user_input:
                    found_action, found_result = action, res
                    break
            result = result.replace("{action}", found_action)
            result = result.replace("{result}", found_result)
        
        if "{quality}" in result:
            found_quality = "本事"  # 默认
            for quality in self.QUALITIES:
                if quality in user_input:
                    found_quality = quality
                    break
            result = result.replace("{quality}", found_quality)
        
        if "{negative}" in result and "{positive}" in result:
            found_neg, found_pos = "丑", "好看"  # 默认
            for neg, pos in self.NEGATIVE_POSITIVE_PAIRS:
                if neg in user_input:
                    found_neg, found_pos = neg, pos
                    break
            result = result.replace("{negative}", found_neg)
            result = result.replace("{positive}", found_pos)
        
        return result
    
    def format_output(self, results: List[Dict]) -> str:
        """
        格式化输出
        
        Args:
            results: 废话文学结果列表
            
        Returns:
            格式化后的输出文本
        """
        if not results:
            return "没有生成废话文学"
        
        lines = ["=" * 50]
        lines.append("废话文学生成结果")
        lines.append("=" * 50)
        
        for i, result in enumerate(results, 1):
            lines.append(f"\n【{i}】类型：{result['type_cn']}")
            if result['scene']:
                lines.append(f"场景：{result['scene']}")
            lines.append(f"话题：{result['topic']}")
            lines.append(f"废话：{result['nonsense']}")
        
        lines.append("\n" + "=" * 50)
        return "\n".join(lines)

def main():
    """主函数"""
    import argparse
    parser = argparse.ArgumentParser(description='互联网废话文学生成器')
    parser.add_argument('input', help='用户输入的情景或对话')
    parser.add_argument('--count', '-c', type=int, default=1, help='生成数量')
    parser.add_argument('--json', '-j', action='store_true', help='JSON输出')
    args = parser.parse_args()
    
    generator = NonsenseGenerator()
    results = generator.generate_nonsense(args.input, args.count)
    
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(generator.format_output(results))

if __name__ == '__main__':
    main()
