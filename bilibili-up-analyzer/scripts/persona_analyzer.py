"""
UP主画像分析模块

基于视频数据、互动数据、趋势数据，生成多维度的UP主画像。
包含：内容创作画像、受众画像、商业价值画像、成长潜力画像。
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from collections import Counter
import re


@dataclass
class CreatorPersona:
    """内容创作画像"""
    content_style: str           # 内容风格标签
    creation_pattern: str        # 创作模式
    technical_level: str         # 技术水准
    innovation_score: float      # 创新度评分(0-100)
    consistency_score: float     # 一致性评分(0-100)
    tags: List[str]              # 创作标签


@dataclass
class AudiencePersona:
    """受众画像"""
    engagement_type: str         # 互动类型
    loyalty_level: str           # 忠诚度等级
    preference_tags: List[str]   # 受众偏好标签
    active_hours: str            # 活跃时段特征
    community_vibe: str          # 社区氛围


@dataclass
class CommercialPersona:
    """商业价值画像"""
    monetization_potential: str  # 变现潜力
    brand_fit: List[str]         # 适配品牌类型
    cooperation_value: float     # 合作价值评分(0-100)
    content_safety: str          # 内容安全度
    target_demographics: str     # 目标人群


@dataclass
class GrowthPersona:
    """成长潜力画像"""
    growth_stage: str            # 成长阶段
    growth_momentum: str         # 增长势头
    competitive_position: str    # 竞争定位
    improvement_areas: List[str] # 改进空间
    potential_ceiling: str       # 潜力天花板


@dataclass
class UpPersona:
    """完整UP主画像"""
    creator: CreatorPersona
    audience: AudiencePersona
    commercial: CommercialPersona
    growth: GrowthPersona
    summary: str                 # 画像总结
    persona_type: str            # 画像类型标签


class PersonaAnalyzer:
    """UP主画像分析器"""

    # 内容风格关键词映射
    STYLE_KEYWORDS = {
        "技术流": ["教程", "教学", "攻略", "原理", "分析", "详解"],
        "娱乐向": ["搞笑", "沙雕", "整活", "娱乐", "欢乐"],
        "情感共鸣": ["感动", "泪目", "治愈", "温暖", "故事"],
        "资讯型": ["新闻", "资讯", "热点", "速报", "盘点"],
        "创意剪辑": ["混剪", "MAD", "AMV", "GMV", "踩点"],
        "生活记录": ["vlog", "日常", "记录", "生活"],
        "硬核科普": ["科普", "科学", "原理", "实验"],
        "二创改编": ["改编", "翻唱", "翻跳", "仿妆", "cos"],
    }

    # 受众互动类型
    ENGAGEMENT_TYPES = {
        "高互动型": {"danmaku_rate": 1.0, "reply_rate": 0.3},
        "收藏学习型": {"favorite_rate": 3.0},
        "围观型": {"like_rate": 3.0, "low_interaction": True},
        "讨论型": {"reply_rate": 0.5},
    }

    def __init__(self):
        pass

    def analyze_creator_persona(
        self,
        videos: List[Dict[str, Any]],
        type_analysis: Dict[str, Any],
        content_pattern: Dict[str, Any],
        interaction_metrics: Dict[str, Any]
    ) -> CreatorPersona:
        """分析内容创作画像"""
        
        # 1. 内容风格识别
        titles = " ".join([v.get("title", "") for v in videos])
        style_scores = {}
        for style, keywords in self.STYLE_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in titles)
            if score > 0:
                style_scores[style] = score
        
        if style_scores:
            content_style = max(style_scores, key=style_scores.get)
        else:
            # 根据视频类型判断
            primary_type = type_analysis.get("primary_type", "其他")
            type_to_style = {
                "教程": "技术流",
                "评测": "资讯型",
                "vlog": "生活记录",
                "混剪": "创意剪辑",
                "音乐": "二创改编",
            }
            content_style = type_to_style.get(primary_type, "综合型")
        
        # 2. 创作模式
        if content_pattern.get("is_series_creator"):
            creation_pattern = "系列化创作"
        elif content_pattern.get("update_frequency", "").startswith("高频"):
            creation_pattern = "高频量产"
        elif content_pattern.get("update_frequency", "").startswith("低频"):
            creation_pattern = "精品打磨"
        else:
            creation_pattern = "稳定输出"
        
        # 3. 技术水准（基于收藏率和完播率推断）
        fav_rate = interaction_metrics.get("favorite_rate", 0)
        if fav_rate > 5:
            technical_level = "专业级"
        elif fav_rate > 2:
            technical_level = "进阶"
        else:
            technical_level = "入门"
        
        # 4. 创新度（基于投币率和内容多样性）
        coin_rate = interaction_metrics.get("coin_rate", 0)
        type_count = type_analysis.get("type_count", 1)
        innovation_score = min(100, (coin_rate * 20) + (type_count * 10) + 50)
        
        # 5. 一致性（基于播放量分位数的稳健评分）
        views = [v.get("stat", {}).get("view", 0) or v.get("play", 0) 
               for v in videos if (v.get("stat", {}).get("view", 0) or v.get("play", 0)) > 0]
        if views and len(views) > 1:
            views_sorted = sorted(views)
            q1 = views_sorted[len(views_sorted) // 4]  # 25分位
            q3 = views_sorted[3 * len(views_sorted) // 4]  # 75分位
            median = views_sorted[len(views_sorted) // 2]
            # IQR/median 作为稳健变异指标
            iqr_ratio = (q3 - q1) / median if median > 0 else 1
            # 评分：IQR比例越小，一致性越高
            consistency_score = max(0, min(100, 100 - iqr_ratio * 30))
        else:
            consistency_score = 50
        
        # 6. 创作标签
        tags = [content_style, creation_pattern]
        if innovation_score > 70:
            tags.append("高创新")
        if consistency_score > 70:
            tags.append("质量稳定")
        
        return CreatorPersona(
            content_style=content_style,
            creation_pattern=creation_pattern,
            technical_level=technical_level,
            innovation_score=round(innovation_score, 1),
            consistency_score=round(consistency_score, 1),
            tags=tags
        )

    def analyze_audience_persona(
        self,
        videos: List[Dict[str, Any]],
        interaction_metrics: Dict[str, Any],
        up_info: Dict[str, Any]
    ) -> AudiencePersona:
        """分析受众画像"""
        
        # 1. 互动类型判断
        danmaku_rate = interaction_metrics.get("danmaku_rate", 0)
        reply_rate = interaction_metrics.get("reply_rate", 0)
        favorite_rate = interaction_metrics.get("favorite_rate", 0)
        like_rate = interaction_metrics.get("like_rate", 0)
        
        if favorite_rate > 3:
            engagement_type = "收藏学习型"
        elif danmaku_rate > 1 or reply_rate > 0.3:
            engagement_type = "高互动型"
        elif reply_rate > 0.1:
            engagement_type = "讨论型"
        elif like_rate > 3:
            engagement_type = "围观型"
        else:
            engagement_type = "轻度消费型"
        
        # 2. 忠诚度（基于粉丝/播放比和互动率）
        follower = up_info.get("follower", 0)
        avg_views = interaction_metrics.get("avg_views", 1)
        fan_ratio = follower / avg_views if avg_views > 0 else 0
        
        if fan_ratio > 0.5 and like_rate > 5:
            loyalty_level = "铁粉聚集"
        elif fan_ratio > 0.2:
            loyalty_level = "中度忠诚"
        elif fan_ratio > 0.05:
            loyalty_level = "轻度关注"
        else:
            loyalty_level = "路人为主"
        
        # 3. 受众偏好标签
        preference_tags = []
        if favorite_rate > 2:
            preference_tags.append("实用主义")
        if danmaku_rate > 0.5:
            preference_tags.append("娱乐向")
        if reply_rate > 0.1:
            preference_tags.append("爱讨论")
        if like_rate > 5:
            preference_tags.append("高认可")
        if not preference_tags:
            preference_tags.append("泛娱乐")
        
        # 4. 社区氛围
        if reply_rate > 0.2 and danmaku_rate > 1:
            community_vibe = "热闹活跃"
        elif reply_rate > 0.1:
            community_vibe = "温和讨论"
        elif danmaku_rate > 0.5:
            community_vibe = "弹幕狂欢"
        else:
            community_vibe = "安静观看"
        
        # 5. 活跃时段（基于视频发布时间推断）
        hours = []
        for v in videos:
            ts = v.get("created") or v.get("pubdate")
            if ts:
                from datetime import datetime
                try:
                    hour = datetime.fromtimestamp(ts).hour
                    hours.append(hour)
                except:
                    pass
        
        if hours:
            hour_dist = Counter(hours)
            peak_hour = hour_dist.most_common(1)[0][0]
            if 18 <= peak_hour <= 23:
                active_hours = "晚间活跃"
            elif 12 <= peak_hour <= 17:
                active_hours = "下午活跃"
            elif 6 <= peak_hour <= 11:
                active_hours = "上午活跃"
            else:
                active_hours = "深夜活跃"
        else:
            active_hours = "晚间活跃"
        
        return AudiencePersona(
            engagement_type=engagement_type,
            loyalty_level=loyalty_level,
            preference_tags=preference_tags,
            active_hours=active_hours,
            community_vibe=community_vibe
        )

    def analyze_commercial_persona(
        self,
        up_info: Dict[str, Any],
        videos: List[Dict[str, Any]],
        partition_analysis: Dict[str, Any],
        interaction_metrics: Dict[str, Any],
        score_result: Any
    ) -> CommercialPersona:
        """分析商业价值画像"""
        
        follower = up_info.get("follower", 0)
        avg_views = interaction_metrics.get("avg_views", 0)
        score = score_result.total_score
        
        # 1. 变现潜力
        if follower > 100000 and avg_views > 50000:
            monetization_potential = "头部变现"
        elif follower > 50000 and avg_views > 20000:
            monetization_potential = "优质变现"
        elif follower > 10000 and avg_views > 5000:
            monetization_potential = "稳定变现"
        elif follower > 1000:
            monetization_potential = "潜力变现"
        else:
            monetization_potential = "培育期"
        
        # 2. 适配品牌类型
        primary_partition = partition_analysis.get("primary_partition", "")
        partition_to_brand = {
            "知识": ["教育", "图书", "知识付费"],
            "科技": ["数码", "3C", "互联网"],
            "游戏": ["游戏", "电竞", "硬件"],
            "生活": ["快消", "家居", "本地生活"],
            "美食": ["餐饮", "食品", "厨具"],
            "时尚": ["美妆", "服饰", "奢侈品"],
            "动画": ["二次元", "手办", "动漫"],
            "音乐": ["音乐", "乐器", "演出"],
        }
        brand_fit = partition_to_brand.get(primary_partition, ["综合品牌"])
        
        # 3. 合作价值评分
        cooperation_value = min(100, score * 0.8 + (follower / 10000) * 5)
        
        # 4. 内容安全度
        titles = " ".join([v.get("title", "") for v in videos])
        risky_keywords = ["敏感", "争议", "撕逼", "骂战", "政治"]
        risk_count = sum(1 for kw in risky_keywords if kw in titles)
        if risk_count == 0:
            content_safety = "安全"
        elif risk_count <= 2:
            content_safety = "轻度风险"
        else:
            content_safety = "需注意"
        
        # 5. 目标人群
        if primary_partition in ["知识", "科技"]:
            target_demographics = "高学历/专业人群"
        elif primary_partition in ["动画", "游戏"]:
            target_demographics = "Z世代/年轻用户"
        elif primary_partition in ["生活", "美食"]:
            target_demographics = "大众消费者"
        elif primary_partition in ["时尚"]:
            target_demographics = "都市白领/女性用户"
        else:
            target_demographics = "泛娱乐用户"
        
        return CommercialPersona(
            monetization_potential=monetization_potential,
            brand_fit=brand_fit,
            cooperation_value=round(cooperation_value, 1),
            content_safety=content_safety,
            target_demographics=target_demographics
        )

    def analyze_growth_persona(
        self,
        up_info: Dict[str, Any],
        videos: List[Dict[str, Any]],
        trend_analysis: Dict[str, Any],
        score_result: Any,
        interaction_metrics: Dict[str, Any]
    ) -> GrowthPersona:
        """分析成长潜力画像"""
        
        follower = up_info.get("follower", 0)
        archive_count = up_info.get("archive_count", 0)
        score = score_result.total_score
        trend = trend_analysis.get("activity_trend", "稳定")
        
        # 1. 成长阶段
        if follower > 1000000:
            growth_stage = "头部UP主"
        elif follower > 100000:
            growth_stage = "腰部UP主"
        elif follower > 10000:
            growth_stage = "成长期UP主"
        elif follower > 1000:
            growth_stage = "新手期UP主"
        else:
            growth_stage = "起步期UP主"
        
        # 2. 增长势头
        if trend == "上升":
            growth_momentum = "上升期"
        elif trend == "下降":
            growth_momentum = "调整期"
        else:
            growth_momentum = "稳定期"
        
        # 3. 竞争定位
        like_rate = interaction_metrics.get("like_rate", 0)
        if score >= 80 and like_rate > 5:
            competitive_position = "领域标杆"
        elif score >= 70:
            competitive_position = "中坚力量"
        elif score >= 60:
            competitive_position = "潜力选手"
        else:
            competitive_position = "待观察"
        
        # 4. 改进空间
        improvement_areas = []
        if interaction_metrics.get("danmaku_rate", 0) < 0.5:
            improvement_areas.append("提升互动率")
        if trend == "下降":
            improvement_areas.append("稳定更新频率")
        if interaction_metrics.get("share_rate", 0) < 0.1:
            improvement_areas.append("增强传播性")
        if score < 70:
            improvement_areas.append("提升内容质量")
        if not improvement_areas:
            improvement_areas.append("保持现有优势")
        
        # 5. 潜力天花板
        if score >= 85 and follower > 50000:
            potential_ceiling = "百万粉丝潜力"
        elif score >= 75:
            potential_ceiling = "五十万粉丝潜力"
        elif score >= 65:
            potential_ceiling = "十万粉丝潜力"
        else:
            potential_ceiling = "需突破瓶颈"
        
        return GrowthPersona(
            growth_stage=growth_stage,
            growth_momentum=growth_momentum,
            competitive_position=competitive_position,
            improvement_areas=improvement_areas,
            potential_ceiling=potential_ceiling
        )

    def generate_summary(
        self,
        creator: CreatorPersona,
        audience: AudiencePersona,
        commercial: CommercialPersona,
        growth: GrowthPersona,
        up_info: Dict[str, Any]
    ) -> tuple:
        """生成画像总结和类型标签"""
        
        # 画像类型标签
        tags = []
        tags.append(creator.content_style)
        tags.append(audience.engagement_type)
        tags.append(growth.growth_stage)
        if commercial.cooperation_value > 70:
            tags.append("高商业价值")
        
        persona_type = " | ".join(tags[:3])
        
        # 画像总结
        summary_parts = [
            f"【{up_info.get('name', '该UP主')}】是一位{growth.growth_stage}，",
            f"以{creator.content_style}为主要特色，",
            f"受众以{audience.loyalty_level}为主，",
            f"目前处于{growth.growth_momentum}，",
            f"具备{growth.potential_ceiling}。",
        ]
        
        summary = "".join(summary_parts)
        
        return summary, persona_type

    def analyze(
        self,
        up_info: Dict[str, Any],
        videos: List[Dict[str, Any]],
        type_analysis: Dict[str, Any],
        content_pattern: Dict[str, Any],
        interaction_metrics: Dict[str, Any],
        partition_analysis: Dict[str, Any],
        trend_analysis: Dict[str, Any],
        score_result: Any
    ) -> UpPersona:
        """生成完整UP主画像"""
        
        creator = self.analyze_creator_persona(
            videos, type_analysis, content_pattern, interaction_metrics
        )
        
        audience = self.analyze_audience_persona(
            videos, interaction_metrics, up_info
        )
        
        commercial = self.analyze_commercial_persona(
            up_info, videos, partition_analysis, interaction_metrics, score_result
        )
        
        growth = self.analyze_growth_persona(
            up_info, videos, trend_analysis, score_result, interaction_metrics
        )
        
        summary, persona_type = self.generate_summary(
            creator, audience, commercial, growth, up_info
        )
        
        return UpPersona(
            creator=creator,
            audience=audience,
            commercial=commercial,
            growth=growth,
            summary=summary,
            persona_type=persona_type
        )
