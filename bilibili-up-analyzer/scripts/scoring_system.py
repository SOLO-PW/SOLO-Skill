"""
Bilibili UP主多维度评分系统

提供基于UP主内容类型的差异化评分算法。
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class UpType(Enum):
    """UP主类型枚举"""
    KNOWLEDGE = "knowledge"      # 知识区
    ENTERTAINMENT = "entertainment"  # 娱乐区
    GAME = "game"                # 游戏区
    LIFE = "life"                # 生活区
    MUSIC = "music"              # 音乐区
    TECH = "tech"                # 科技区
    FOOD = "food"                # 美食区
    ANIME = "anime"              # 动画区
    UNKNOWN = "unknown"          # 未知类型


@dataclass
class ScoreDimension:
    """评分维度定义"""
    name: str                    # 维度名称
    weight: float               # 权重（0-1）
    description: str            # 描述


@dataclass
class ScoreResult:
    """评分结果"""
    total_score: float          # 总分（0-100）
    grade: str                  # 等级（S/A/B/C/D）
    dimension_scores: Dict[str, float]  # 各维度得分
    summary: str                # 评价摘要


class UpScoringSystem:
    """UP主评分系统"""
    
    # 分区到UP主类型的映射
    PARTITION_TYPE_MAP = {
        "知识": UpType.KNOWLEDGE,
        "科技": UpType.TECH,
        "游戏": UpType.GAME,
        "娱乐": UpType.ENTERTAINMENT,
        "生活": UpType.LIFE,
        "美食": UpType.FOOD,
        "音乐": UpType.MUSIC,
        "舞蹈": UpType.MUSIC,
        "动画": UpType.ANIME,
        "番剧": UpType.ANIME,
        "国创": UpType.ANIME,
        "鬼畜": UpType.ENTERTAINMENT,
        "时尚": UpType.LIFE,
        "影视": UpType.ENTERTAINMENT,
        "资讯": UpType.KNOWLEDGE,
        "运动": UpType.LIFE,
        "汽车": UpType.TECH,
        "动物圈": UpType.LIFE,
    }
    
    # 各类型UP主的评分维度配置
    SCORING_CONFIG = {
        UpType.KNOWLEDGE: [
            ScoreDimension("内容深度", 0.25, "视频的知识密度和深度"),
            ScoreDimension("完播率", 0.20, "观众完整观看的比例"),
            ScoreDimension("收藏率", 0.20, "内容被收藏的比例"),
            ScoreDimension("互动质量", 0.15, "评论质量和讨论深度"),
            ScoreDimension("更新稳定性", 0.10, "内容更新的规律性和持续性"),
            ScoreDimension("粉丝增长", 0.10, "粉丝增长趋势"),
        ],
        UpType.ENTERTAINMENT: [
            ScoreDimension("播放量", 0.25, "视频的播放热度"),
            ScoreDimension("点赞率", 0.20, "观众点赞比例"),
            ScoreDimension("分享率", 0.20, "内容被分享传播的比例"),
            ScoreDimension("互动活跃度", 0.15, "弹幕和评论活跃度"),
            ScoreDimension("爆款率", 0.10, "产生爆款视频的比例"),
            ScoreDimension("内容创新", 0.10, "内容创意和新颖度"),
        ],
        UpType.GAME: [
            ScoreDimension("互动率", 0.25, "观众互动参与度"),
            ScoreDimension("弹幕密度", 0.20, "弹幕活跃程度"),
            ScoreDimension("评论质量", 0.15, "评论的深度和质量"),
            ScoreDimension("技术/攻略价值", 0.15, "游戏技术或攻略的实用性"),
            ScoreDimension("粉丝粘性", 0.15, "粉丝忠诚度和回访率"),
            ScoreDimension("更新频率", 0.10, "内容更新速度"),
        ],
        UpType.LIFE: [
            ScoreDimension("粉丝增长", 0.20, "粉丝增长趋势和速度"),
            ScoreDimension("内容稳定性", 0.20, "内容质量和风格的稳定性"),
            ScoreDimension("互动氛围", 0.15, "评论区和弹幕氛围"),
            ScoreDimension("真实感", 0.15, "内容的真实性和亲和力"),
            ScoreDimension("更新规律", 0.15, "内容更新的规律性"),
            ScoreDimension("多元化", 0.15, "内容主题的丰富程度"),
        ],
        UpType.MUSIC: [
            ScoreDimension("播放量", 0.25, "作品播放热度"),
            ScoreDimension("收藏率", 0.20, "作品被收藏比例"),
            ScoreDimension("分享传播", 0.15, "作品传播度"),
            ScoreDimension("技术水准", 0.15, "演唱/演奏/制作水平"),
            ScoreDimension("原创度", 0.15, "原创作品的占比"),
            ScoreDimension("粉丝互动", 0.10, "粉丝互动质量"),
        ],
        UpType.TECH: [
            ScoreDimension("专业度", 0.25, "技术内容的专业程度"),
            ScoreDimension("实用性", 0.20, "内容的实用价值"),
            ScoreDimension("完播率", 0.15, "观众完整观看比例"),
            ScoreDimension("收藏率", 0.15, "内容被收藏比例"),
            ScoreDimension("互动质量", 0.15, "技术讨论的深度"),
            ScoreDimension("更新频率", 0.10, "内容更新速度"),
        ],
        UpType.FOOD: [
            ScoreDimension("播放量", 0.20, "视频播放热度"),
            ScoreDimension("收藏率", 0.20, "食谱/教程被收藏比例"),
            ScoreDimension("互动氛围", 0.15, "评论区互动活跃度"),
            ScoreDimension("制作质量", 0.15, "视频制作和呈现质量"),
            ScoreDimension("创新性", 0.15, "菜品/内容的创新程度"),
            ScoreDimension("更新稳定性", 0.15, "内容更新的规律性"),
        ],
        UpType.ANIME: [
            ScoreDimension("播放量", 0.25, "作品播放热度"),
            ScoreDimension("弹幕活跃度", 0.20, "弹幕互动活跃度"),
            ScoreDimension("二创质量", 0.15, "二次创作的质量和创意"),
            ScoreDimension("粉丝粘性", 0.15, "核心粉丝活跃度"),
            ScoreDimension("更新频率", 0.15, "内容更新速度"),
            ScoreDimension("话题度", 0.10, "作品引发讨论的热度"),
        ],
        UpType.UNKNOWN: [
            ScoreDimension("综合播放量", 0.25, "整体播放表现"),
            ScoreDimension("互动率", 0.20, "整体互动水平"),
            ScoreDimension("粉丝增长", 0.20, "粉丝增长趋势"),
            ScoreDimension("内容质量", 0.15, "内容整体质量"),
            ScoreDimension("更新稳定性", 0.10, "更新规律性"),
            ScoreDimension("成长潜力", 0.10, "未来发展潜力"),
        ],
    }
    
    def __init__(self):
        """初始化评分系统"""
        pass
    
    def detect_up_type(self, primary_partition: str, video_types: List[str]) -> UpType:
        """
        检测UP主类型
        
        Args:
            primary_partition: 主要发布分区
            video_types: 视频类型列表
            
        Returns:
            UP主类型
        """
        # 优先根据分区判断
        up_type = self.PARTITION_TYPE_MAP.get(primary_partition, UpType.UNKNOWN)
        
        # 如果分区判断为未知，尝试根据视频类型判断
        if up_type == UpType.UNKNOWN and video_types:
            type_mapping = {
                "教程": UpType.KNOWLEDGE,
                "评测": UpType.TECH,
                "vlog": UpType.LIFE,
                "音乐": UpType.MUSIC,
                "混剪": UpType.ANIME,
            }
            for vt in video_types:
                if vt in type_mapping:
                    up_type = type_mapping[vt]
                    break
        
        return up_type
    
    def _calculate_dimension_score(
        self, 
        dimension: ScoreDimension, 
        up_info: Dict[str, Any],
        videos: List[Dict[str, Any]],
        metrics: Dict[str, Any]
    ) -> float:
        """
        计算单个维度得分
        
        Args:
            dimension: 评分维度
            up_info: UP主信息
            videos: 视频列表
            metrics: 互动指标
            
        Returns:
            维度得分（0-100）
        """
        name = dimension.name
        score = 50.0  # 基础分
        
        # 根据维度名称计算得分
        if name in ["播放量", "综合播放量"]:
            avg_views = metrics.get("avg_views", 0)
            if avg_views > 100000:
                score = 95
            elif avg_views > 50000:
                score = 85
            elif avg_views > 10000:
                score = 75
            elif avg_views > 5000:
                score = 65
            elif avg_views > 1000:
                score = 55
            else:
                score = 45
        
        elif name in ["点赞率", "互动率"]:
            like_rate = metrics.get("like_rate", 0)
            if like_rate > 5:
                score = 95
            elif like_rate > 3:
                score = 85
            elif like_rate > 2:
                score = 75
            elif like_rate > 1:
                score = 65
            else:
                score = 50
        
        elif name == "收藏率":
            fav_rate = metrics.get("favorite_rate", 0)
            if fav_rate > 3:
                score = 95
            elif fav_rate > 1.5:
                score = 85
            elif fav_rate > 0.8:
                score = 75
            elif fav_rate > 0.3:
                score = 65
            else:
                score = 50
        
        elif name in ["分享率", "分享传播"]:
            share_rate = metrics.get("share_rate", 0)
            if share_rate > 0.5:
                score = 95
            elif share_rate > 0.2:
                score = 85
            elif share_rate > 0.1:
                score = 75
            elif share_rate > 0.05:
                score = 65
            else:
                score = 50
        
        elif name in ["弹幕密度", "弹幕活跃度"]:
            danmaku_rate = metrics.get("danmaku_rate", 0)
            if danmaku_rate > 2:
                score = 95
            elif danmaku_rate > 1:
                score = 85
            elif danmaku_rate > 0.5:
                score = 75
            elif danmaku_rate > 0.2:
                score = 65
            else:
                score = 50
        
        elif name in ["评论质量", "互动质量", "互动氛围"]:
            reply_rate = metrics.get("reply_rate", 0)
            if reply_rate > 0.5:
                score = 95
            elif reply_rate > 0.3:
                score = 85
            elif reply_rate > 0.15:
                score = 75
            elif reply_rate > 0.08:
                score = 65
            else:
                score = 50
        
        elif name in ["粉丝增长", "粉丝粘性"]:
            follower = up_info.get("follower", 0)
            if follower > 1000000:
                score = 95
            elif follower > 500000:
                score = 90
            elif follower > 100000:
                score = 80
            elif follower > 50000:
                score = 70
            elif follower > 10000:
                score = 60
            else:
                score = 50
        
        elif name in ["更新稳定性", "更新规律", "更新频率"]:
            video_count = len(videos)
            if video_count >= 100:
                score = 90
            elif video_count >= 50:
                score = 80
            elif video_count >= 20:
                score = 70
            elif video_count >= 10:
                score = 60
            else:
                score = 50
        
        elif name in ["内容深度", "专业度", "技术水准"]:
            # 根据收藏率和完播率综合判断
            fav_rate = metrics.get("favorite_rate", 0)
            if fav_rate > 2:
                score = 90
            elif fav_rate > 1:
                score = 80
            elif fav_rate > 0.5:
                score = 70
            else:
                score = 60
        
        elif name == "爆款率":
            # 统计播放量超过平均3倍的视频比例
            avg_views = metrics.get("avg_views", 0)
            if avg_views > 0:
                hit_count = sum(1 for v in videos if v.get("stat", {}).get("view", 0) > avg_views * 3)
                hit_rate = hit_count / len(videos) if videos else 0
                if hit_rate > 0.2:
                    score = 95
                elif hit_rate > 0.1:
                    score = 85
                elif hit_rate > 0.05:
                    score = 75
                else:
                    score = 60
            else:
                score = 50
        
        elif name in ["内容创新", "创新性", "原创度"]:
            # 根据投币率判断（原创度高的内容通常投币率较高）
            coin_rate = metrics.get("coin_rate", 0)
            if coin_rate > 1:
                score = 90
            elif coin_rate > 0.5:
                score = 80
            elif coin_rate > 0.2:
                score = 70
            else:
                score = 60
        
        elif name == "成长潜力":
            # 根据粉丝数和视频数的比例判断
            follower = up_info.get("follower", 0)
            video_count = len(videos)
            if video_count > 0:
                ratio = follower / video_count
                if ratio > 10000:
                    score = 95
                elif ratio > 5000:
                    score = 85
                elif ratio > 1000:
                    score = 75
                elif ratio > 500:
                    score = 65
                else:
                    score = 55
            else:
                score = 50
        
        else:
            # 默认根据平均互动率计算
            avg_rate = (metrics.get("like_rate", 0) + metrics.get("coin_rate", 0) + 
                       metrics.get("favorite_rate", 0)) / 3
            score = min(100, 50 + avg_rate * 10)
        
        return min(100, max(0, score))
    
    def calculate_score(
        self, 
        up_info: Dict[str, Any],
        videos: List[Dict[str, Any]],
        metrics: Dict[str, Any],
        primary_partition: str,
        video_types: List[str]
    ) -> ScoreResult:
        """
        计算UP主综合评分
        
        Args:
            up_info: UP主信息
            videos: 视频列表
            metrics: 互动指标
            primary_partition: 主要发布分区
            video_types: 视频类型列表
            
        Returns:
            评分结果
        """
        # 检测UP主类型
        up_type = self.detect_up_type(primary_partition, video_types)
        
        # 获取评分维度配置
        dimensions = self.SCORING_CONFIG.get(up_type, self.SCORING_CONFIG[UpType.UNKNOWN])
        
        # 计算各维度得分
        dimension_scores = {}
        total_weighted_score = 0
        
        for dim in dimensions:
            score = self._calculate_dimension_score(dim, up_info, videos, metrics)
            dimension_scores[dim.name] = round(score, 2)
            total_weighted_score += score * dim.weight
        
        # 计算总分
        total_score = round(total_weighted_score, 2)
        
        # 确定等级
        if total_score >= 90:
            grade = "S"
            summary = "顶级UP主，在领域内具有极高影响力和专业度"
        elif total_score >= 80:
            grade = "A"
            summary = "优秀UP主，内容质量和影响力都很出色"
        elif total_score >= 70:
            grade = "B"
            summary = "良好UP主，内容稳定，有一定影响力"
        elif total_score >= 60:
            grade = "C"
            summary = "普通UP主，内容尚可，有提升空间"
        else:
            grade = "D"
            summary = "新手UP主，需要持续积累和改进"
        
        return ScoreResult(
            total_score=total_score,
            grade=grade,
            dimension_scores=dimension_scores,
            summary=summary
        )
    
    def get_dimension_descriptions(self, up_type: UpType) -> List[Dict[str, str]]:
        """
        获取评分维度说明
        
        Args:
            up_type: UP主类型
            
        Returns:
            维度说明列表
        """
        dimensions = self.SCORING_CONFIG.get(up_type, self.SCORING_CONFIG[UpType.UNKNOWN])
        return [
            {
                "name": dim.name,
                "weight": f"{dim.weight * 100:.0f}%",
                "description": dim.description
            }
            for dim in dimensions
        ]
