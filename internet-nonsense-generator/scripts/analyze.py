"""用户输入分析脚本 - 分析场景、情绪、关键词，推荐废话类型"""
import argparse
import re
from enum import Enum
from typing import List, Tuple


class SceneType(Enum):
    """场景类型枚举"""
    WORK = "work"
    SOCIAL = "social"
    EMOTIONAL = "emotional"
    DAILY = "daily"
    PROFESSIONAL = "professional"


class EmotionType(Enum):
    """情绪类型枚举"""
    ANGRY = "angry"
    SAD = "sad"
    HAPPY = "happy"
    ANXIOUS = "anxious"
    NEUTRAL = "neutral"


SCENE_KEYWORDS = {
    SceneType.WORK: ["工作", "会议", "领导", "同事", "项目", "任务", "加班", "升职", "加薪", "绩效", "考核", "职场", "上班", "下班"],
    SceneType.SOCIAL: ["朋友", "聚餐", "聚会", "社交", "认识", "见面", "聊天", "约会", "派对", "派对"],
    SceneType.EMOTIONAL: ["心情", "难过", "开心", "生气", "焦虑", "压力", "感情", "恋爱", "分手", "喜欢", "爱", "想念"],
    SceneType.DAILY: ["天气", "吃饭", "睡觉", "上班", "下班", "交通", "购物", "做饭", "打扫", "健身", "运动"],
    SceneType.PROFESSIONAL: ["学习", "考试", "面试", "演讲", "汇报", "论文", "研究", "分析", "总结", "计划"]
}

EMOTION_KEYWORDS = {
    EmotionType.ANGRY: ["生气", "愤怒", "讨厌", "烦", "受够了", "不公平", "过分", "气死", "恼火"],
    EmotionType.SAD: ["难过", "伤心", "失望", "可惜", "遗憾", "心痛", "哭", "低落", "郁闷"],
    EmotionType.HAPPY: ["开心", "高兴", "快乐", "幸福", "棒", "太好了", "恭喜", "庆祝", "兴奋"],
    EmotionType.ANXIOUS: ["焦虑", "紧张", "担心", "压力", "不安", "着急", "急死", "慌", "怕"],
    EmotionType.NEUTRAL: ["一般", "还好", "普通", "正常", "平静", "没事"]
}

RECOMMENDED_TYPES = {
    SceneType.WORK: ["leader_speech", "obvious", "synonym_repeat"],
    SceneType.SOCIAL: ["rhyme", "conditional", "follow_up"],
    SceneType.EMOTIONAL: ["hope", "time_loop", "assumption"],
    SceneType.DAILY: ["obvious", "unit_conversion", "synonym_repeat"],
    SceneType.PROFESSIONAL: ["long_sentence", "literature", "redundancy"],
    EmotionType.ANGRY: ["reversal", "contradiction", "time_loop"],
    EmotionType.SAD: ["hope", "assumption", "conditional"],
    EmotionType.HAPPY: ["rhyme", "follow_up", "synonym_repeat"],
    EmotionType.ANXIOUS: ["time_loop", "conditional", "obvious"],
    EmotionType.NEUTRAL: ["obvious", "synonym_repeat", "long_sentence"]
}


def extract_keywords(text: str) -> List[str]:
    """提取文本中的关键词（简单实现）"""
    # 移除标点符号
    text = re.sub(r'[^\w\s]', '', text)
    # 按空格分割
    words = text.split()
    # 移除常见停用词
    stop_words = {"的", "了", "是", "我", "你", "他", "她", "它", "我们", "你们", "他们", "这", "那", "这个", "那个", "在", "有", "没有", "很", "非常", "太", "也", "都", "就", "才", "只", "可以", "会", "要", "想", "不"}
    return [word for word in words if word and word not in stop_words and len(word) > 1]


def analyze_scene(text: str) -> Tuple[SceneType, float]:
    """分析场景类型和置信度"""
    scores = {}
    for scene, keywords in SCENE_KEYWORDS.items():
        count = sum(1 for keyword in keywords if keyword in text)
        if count > 0:
            scores[scene] = count
    
    if not scores:
        return SceneType.DAILY, 0.5
    
    best_scene = max(scores, key=scores.get)
    confidence = min(scores[best_scene] / 3, 1.0)
    return best_scene, confidence


def analyze_emotion(text: str) -> Tuple[EmotionType, float]:
    """分析情绪类型和置信度"""
    scores = {}
    for emotion, keywords in EMOTION_KEYWORDS.items():
        count = sum(1 for keyword in keywords if keyword in text)
        if count > 0:
            scores[emotion] = count
    
    if not scores:
        return EmotionType.NEUTRAL, 0.6
    
    best_emotion = max(scores, key=scores.get)
    confidence = min(scores[best_emotion] / 2, 1.0)
    return best_emotion, confidence


def recommend_nonsense_types(scene: SceneType, emotion: EmotionType) -> List[str]:
    """推荐废话文学类型"""
    scene_types = RECOMMENDED_TYPES.get(scene, ["obvious", "synonym_repeat"])
    emotion_types = RECOMMENDED_TYPES.get(emotion, [])
    
    # 合并并去重，保持顺序
    combined = []
    for t in scene_types + emotion_types:
        if t not in combined:
            combined.append(t)
    
    return combined[:3]


def analyze_input(text: str) -> dict:
    """分析用户输入并返回结果"""
    keywords = extract_keywords(text)
    scene, scene_confidence = analyze_scene(text)
    emotion, emotion_confidence = analyze_emotion(text)
    recommended_types = recommend_nonsense_types(scene, emotion)
    
    return {
        "original_text": text,
        "keywords": keywords,
        "scene": scene.value,
        "scene_confidence": scene_confidence,
        "emotion": emotion.value,
        "emotion_confidence": emotion_confidence,
        "recommended_types": recommended_types
    }


def main():
    """主函数，处理命令行参数"""
    parser = argparse.ArgumentParser(description="分析用户输入并推荐废话文学类型")
    parser.add_argument("input", help="用户输入的文本")
    parser.add_argument("--detail", action="store_true", help="显示详细分析结果")
    
    args = parser.parse_args()
    
    result = analyze_input(args.input)
    
    print("\n=== 分析结果 ===")
    print(f"输入文本: {result['original_text']}")
    print(f"提取关键词: {', '.join(result['keywords'])}")
    
    if args.detail:
        print(f"\n场景分析:")
        print(f"  类型: {result['scene']}")
        print(f"  置信度: {result['scene_confidence']:.2f}")
        print(f"\n情绪分析:")
        print(f"  类型: {result['emotion']}")
        print(f"  置信度: {result['emotion_confidence']:.2f}")
    
    print(f"\n推荐废话类型:")
    for i, nonsense_type in enumerate(result['recommended_types'], 1):
        print(f"  {i}. {nonsense_type}")
    
    print("\n=== 分析完成 ===")


if __name__ == "__main__":
    main()