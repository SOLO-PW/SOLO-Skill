#!/usr/bin/env python3
"""
互联网废话文学生成器
根据用户输入的情景对话等内容，分析合适的言论话术，并转化为废话文学
"""

import re
import json
import random
from pathlib import Path
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
    
    # 开头无意义的发语词/条件词（从句首整段剔除，用于话题提取）
    LEADING_STOPWORDS = [
        "如果", "面对", "请问", "关于", "帮我", "能帮我", "我想",
        "你可以", "能不能", "请问一下", "你说",
    ]
    
    # 结尾的语气词/疑问尾缀（从句尾整段剔除，用于话题提取）
    TRAILING_STOPWORDS = [
        "呢", "吧", "啊", "吗", "么", "怎么", "怎么办", "怎么样",
        "是什么", "怎么了", "如何", "好不好", "了吗",
    ]
    
    def __init__(self):
        self._data = self._load_json_data()
        self._setup_vocab()
        self.templates = self._load_templates()
        self.scene_keywords = self._load_scene_keywords()
    
    def _load_json_data(self) -> Dict:
        """
        读取 references/templates.json（单一数据源）
        
        使用 __file__ 定位文件，确保从任意 cwd 运行都能找到。
        """
        json_path = Path(__file__).resolve().parent.parent / "references" / "templates.json"
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def _setup_vocab(self) -> None:
        """从 JSON 加载词表到实例属性"""
        vocab = self._data.get("vocab", {})
        self.EMOTIONS = vocab.get("EMOTIONS", ["急"])
        self.OBJECTS = vocab.get("OBJECTS", ["西红柿"])
        self.ACTION_RESULT_PAIRS = [
            (a, r) for a, r in vocab.get("ACTION_RESULT_PAIRS", [["胖", "体重变重"]])
        ]
        self.QUALITIES = vocab.get("QUALITIES", ["本事"])
        self.NEGATIVE_POSITIVE_PAIRS = [
            (n, p) for n, p in vocab.get("NEGATIVE_POSITIVE_PAIRS", [["丑", "好看"]])
        ]
        self.REMOVE_WORDS = vocab.get("REMOVE_WORDS", [])
    
    @staticmethod
    def _parse_keywords(keywords: List) -> List:
        """解析模板关键词：单元素字符串原样保留，双元素数组转为配对元组"""
        parsed = []
        for kw in keywords:
            if isinstance(kw, list):
                parsed.append(tuple(kw))
            else:
                parsed.append(kw)
        return parsed
    
    def _load_templates(self) -> Dict[NonsenseType, List[NonsenseTemplate]]:
        """从 JSON 加载废话文学模板"""
        templates: Dict[NonsenseType, List[NonsenseTemplate]] = {}
        for item in self._data.get("templates", []):
            tp = NonsenseType(item["type"])
            template = NonsenseTemplate(
                type=tp,
                template=item["template"],
                examples=item.get("examples", []),
                keywords=self._parse_keywords(item.get("keywords", [])),
            )
            templates.setdefault(tp, []).append(template)
        return templates
    
    def _load_scene_keywords(self) -> Dict[str, List[NonsenseType]]:
        """从 JSON 加载场景关键词映射"""
        scene_keywords: Dict[str, List[NonsenseType]] = {}
        for scene, types in self._data.get("scene_keywords", {}).items():
            scene_keywords[scene] = [NonsenseType(t) for t in types]
        return scene_keywords
    
    def analyze_scene(self, user_input: str) -> Tuple[Optional[str], List[NonsenseType]]:
        """
        分析用户输入的场景
        
        Args:
            user_input: 用户输入文本
            
        Returns:
            (场景名称, 推荐的废话类型列表)
        """
        # 加权匹配：更长关键词、出现次数更多者权重更高，降低短词误触发
        scene_weights = {}  # 场景名 -> 权重
        for scene in self.scene_keywords:
            count = user_input.count(scene)
            if count <= 0:
                continue
            # 权重 = 出现次数 * 词长（更精确的长词贡献更高）
            scene_weights[scene] = count * len(scene)
        
        # 未命中任何场景，直接回退默认
        if not scene_weights:
            return None, list(NonsenseType)
        
        # 取权重最高的场景（权重相同取更长关键词）
        best_scene = max(scene_weights, key=lambda s: (scene_weights[s], len(s)))
        
        # 按权重从高到低汇总推荐类型，去重并保留场景内顺序
        recommended_types = []
        for scene in sorted(scene_weights, key=scene_weights.get, reverse=True):
            for t in self.scene_keywords[scene]:
                if t not in recommended_types:
                    recommended_types.append(t)
        
        return best_scene, recommended_types
    
    def extract_topic(self, user_input: str) -> str:
        """
        从用户输入中提取话题
        
        策略：不在全文粗暴剔除人称代词与虚词，而是只剔除开头/收尾的
        无意义成分与中间安全元词/虚词，尽量保留核心名词短语；若结果为空
        则回退到兜底话题词。
        """
        topic = user_input.strip()
        # 剔除开头无意义的发语词/条件词（整段移除，避免把话题拆散）
        for prefix in self.LEADING_STOPWORDS:
            if topic.startswith(prefix):
                topic = topic[len(prefix):]
                break
        # 剔除结尾的语气词/疑问尾缀
        for suffix in self.TRAILING_STOPWORDS:
            if topic.endswith(suffix):
                topic = topic[:-len(suffix)]
        # 剔除中间安全虚词/元词（不含 你我他/们 等可能构成名词短语的代词）
        for word in self.REMOVE_WORDS:
            topic = topic.replace(word, "")
        # 去除标点
        topic = re.sub(r'[，。！？、；：“”‘’"\'（）【】《》\s]', '', topic)
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
                # 优先命中使用户输入中的关键词（更贴合原意）
                hit_word = None
                for kw in template.keywords:
                    if isinstance(kw, str) and kw in user_input:
                        hit_word = kw
                        break
                if hit_word is not None:
                    short_topic = hit_word
                else:
                    # 未命中则从候选池随机选取，提升多样性（不再固定为「情况」）
                    candidate_pool = [kw for kw in template.keywords if isinstance(kw, str)]
                    # 提取到的话题词如果简短且有意义，也纳入候选池
                    if topic and topic != "这个" and len(topic) <= 4 and topic not in candidate_pool:
                        candidate_pool.append(topic)
                    if not candidate_pool:
                        candidate_pool = ["情况"]
                    short_topic = random.choice(candidate_pool)
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
