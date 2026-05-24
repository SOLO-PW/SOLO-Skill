"""
Bilibili UP主数据分析模块

提供视频数据的分析、分类、统计功能。
"""

import re
from typing import Dict, List, Any, Tuple
from datetime import datetime
from collections import Counter


class VideoAnalyzer:
    """视频数据分析器"""
    
    # B站分区映射表（含子分区）
    PARTITION_MAP = {
        # 主分区
        1: ("动画", "anime"),
        13: ("番剧", "bangumi"),
        167: ("国创", "guochuang"),
        3: ("音乐", "music"),
        129: ("舞蹈", "dance"),
        4: ("游戏", "game"),
        36: ("知识", "knowledge"),
        188: ("科技", "tech"),
        234: ("运动", "sport"),
        223: ("汽车", "car"),
        160: ("生活", "life"),
        211: ("美食", "food"),
        217: ("动物圈", "animal"),
        119: ("鬼畜", "kichiku"),
        155: ("时尚", "fashion"),
        202: ("资讯", "info"),
        5: ("娱乐", "ent"),
        181: ("影视", "cinephile"),
        # 子分区 -> 主分区（常见子分区）
        21: ("日常", "life"),
        27: ("综合", "life"),
        31: ("搞笑", "ent"),
        37: ("野生技术协会", "knowledge"),
        47: ("单机游戏", "game"),
        95: ("数码", "tech"),
        96: ("手机平板", "tech"),
        114: ("鬼畜调教", "kichiku"),
        121: ("美食制作", "food"),
        126: ("音MAD", "kichiku"),
        130: ("宅舞", "dance"),
        137: ("明星", "ent"),
        144: ("脱口秀", "ent"),
        152: ("时尚", "fashion"),
        154: ("化妆", "fashion"),
        171: ("MAD·AMV", "anime"),
        172: ("MMD·3D", "anime"),
        173: ("短片·手书", "anime"),
        174: ("配音", "anime"),
        190: ("社科人文", "knowledge"),
        191: ("科学科普", "knowledge"),
        192: ("财经商业", "knowledge"),
        193: ("校园学习", "knowledge"),
        197: ("职业职场", "knowledge"),
        198: ("野生技术协会", "knowledge"),
        207: ("汽车", "car"),
        208: ("摩托车", "car"),
        209: ("购车攻略", "car"),
        210: ("新能源车", "car"),
        0: ("其他", "unknown"),
    }
    
    # 视频类型关键词映射
    VIDEO_TYPE_KEYWORDS = {
        "教程": ["教程", "教学", "入门", "基础", "进阶", "指南", "攻略", "how to", "教学视频"],
        "评测": ["评测", "测评", "体验", "开箱", "试玩", "上手", "测评", "review"],
        "解说": ["解说", "解说员", "解说版", "解说视频"],
        "vlog": ["vlog", "Vlog", "日常", "记录", "生活记录"],
        "混剪": ["混剪", "剪辑", "MAD", "AMV", "GMV"],
        "直播回放": ["直播", "回放", "录播", "直播录像"],
        "搬运": ["搬运", "转载", "来源", "原视频"],
        "原创": ["原创", "自制"],
        "搞笑": ["搞笑", "沙雕", "逗比", "爆笑", "搞笑视频"],
        "音乐": ["翻唱", "演奏", "音乐", "歌曲", "MV"],
    }
    
    def __init__(self):
        """初始化分析器"""
        pass
    
    def analyze_partition_distribution(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析视频分区分布
        
        Args:
            videos: 视频列表
            
        Returns:
            分区统计结果
        """
        partition_counts = Counter()
        partition_views = {}
        
        for video in videos:
            # 优先使用视频详情的tname（更准确），其次用typeid映射
            tname = video.get("tname", "") or ""
            if tname and tname.strip():
                partition_name = tname.strip()
            else:
                typeid = video.get("typeid", 0)
                partition_name = self.PARTITION_MAP.get(typeid, ("其他", "other"))[0]
            partition_counts[partition_name] += 1
            
            # 统计各分区播放量（优先stat.view，其次play）
            views = (video.get("stat", {}).get("view", 0) or video.get("play", 0) or 0)
            if partition_name not in partition_views:
                partition_views[partition_name] = 0
            partition_views[partition_name] += views
        
        total = len(videos)
        distribution = []
        
        for partition, count in partition_counts.most_common():
            distribution.append({
                "partition": partition,
                "count": count,
                "percentage": round(count / total * 100, 2) if total > 0 else 0,
                "total_views": partition_views.get(partition, 0),
                "avg_views": round(partition_views.get(partition, 0) / count) if count > 0 else 0,
            })
        
        return {
            "total_videos": total,
            "partition_count": len(partition_counts),
            "primary_partition": distribution[0]["partition"] if distribution else "未知",
            "distribution": distribution,
        }
    
    def classify_video_type(self, title: str, description: str = "") -> str:
        """
        根据标题和描述分类视频类型
        
        Args:
            title: 视频标题
            description: 视频描述
            
        Returns:
            视频类型
        """
        text = f"{title} {description}".lower()
        
        type_scores = {}
        for video_type, keywords in self.VIDEO_TYPE_KEYWORDS.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in text:
                    score += 1
            if score > 0:
                type_scores[video_type] = score
        
        if type_scores:
            return max(type_scores, key=type_scores.get)
        
        return "其他"
    
    def analyze_video_types(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析视频类型分布
        
        Args:
            videos: 视频列表
            
        Returns:
            视频类型统计结果
        """
        type_counts = Counter()
        
        for video in videos:
            video_type = self.classify_video_type(
                video.get("title", ""),
                video.get("description", "")
            )
            type_counts[video_type] += 1
        
        total = len(videos)
        distribution = []
        
        for video_type, count in type_counts.most_common():
            distribution.append({
                "type": video_type,
                "count": count,
                "percentage": round(count / total * 100, 2) if total > 0 else 0,
            })
        
        return {
            "total_videos": total,
            "type_count": len(type_counts),
            "primary_type": distribution[0]["type"] if distribution else "其他",
            "distribution": distribution,
        }
    
    def calculate_interaction_metrics(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        计算互动指标
        
        Args:
            videos: 视频列表（需包含stat字段）
            
        Returns:
            互动指标统计
        """
        total_views = 0
        total_likes = 0
        total_coins = 0
        total_favorites = 0
        total_shares = 0
        total_replies = 0
        total_danmaku = 0
        
        valid_videos = 0
        
        for video in videos:
            stat = video.get("stat", {})
            views = stat.get("view", 0) or 0
            
            if views > 0:
                valid_videos += 1
                total_views += views
                total_likes += stat.get("like", 0) or 0
                total_coins += stat.get("coin", 0) or 0
                total_favorites += stat.get("favorite", 0) or 0
                total_shares += stat.get("share", 0) or 0
                total_replies += stat.get("reply", 0) or 0
                total_danmaku += stat.get("danmaku", 0) or 0
        
        if valid_videos == 0 or total_views == 0:
            return {
                "avg_views": 0,
                "avg_likes": 0,
                "avg_coins": 0,
                "avg_favorites": 0,
                "avg_shares": 0,
                "avg_replies": 0,
                "avg_danmaku": 0,
                "like_rate": 0,
                "coin_rate": 0,
                "favorite_rate": 0,
                "share_rate": 0,
                "reply_rate": 0,
                "danmaku_rate": 0,
            }
        
        return {
            "avg_views": round(total_views / valid_videos),
            "avg_likes": round(total_likes / valid_videos),
            "avg_coins": round(total_coins / valid_videos),
            "avg_favorites": round(total_favorites / valid_videos),
            "avg_shares": round(total_shares / valid_videos),
            "avg_replies": round(total_replies / valid_videos),
            "avg_danmaku": round(total_danmaku / valid_videos),
            "like_rate": round(total_likes / total_views * 100, 2),
            "coin_rate": round(total_coins / total_views * 100, 2),
            "favorite_rate": round(total_favorites / total_views * 100, 2),
            "share_rate": round(total_shares / total_views * 100, 2),
            "reply_rate": round(total_replies / total_views * 100, 2),
            "danmaku_rate": round(total_danmaku / total_views * 100, 2),
        }
    
    def analyze_trends(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析发布趋势
        
        Args:
            videos: 视频列表
            
        Returns:
            趋势分析结果
        """
        if not videos:
            return {
                "total_days": 0,
                "avg_videos_per_month": 0,
                "avg_videos_per_week": 0,
                "most_active_month": "未知",
                "activity_trend": "稳定",
            }
        
        # 提取发布时间
        timestamps = []
        for video in videos:
            created = video.get("created") or video.get("pubdate")
            if created:
                timestamps.append(created)
        
        if not timestamps:
            return {
                "total_days": 0,
                "avg_videos_per_month": 0,
                "avg_videos_per_week": 0,
                "most_active_month": "未知",
                "activity_trend": "稳定",
            }
        
        timestamps.sort()
        first_date = datetime.fromtimestamp(timestamps[-1])  # 最早的视频
        last_date = datetime.fromtimestamp(timestamps[0])    # 最新的视频
        
        total_days = (last_date - first_date).days + 1
        total_months = max(1, total_days / 30)
        total_weeks = max(1, total_days / 7)
        
        # 按月统计
        month_counts = Counter()
        for ts in timestamps:
            dt = datetime.fromtimestamp(ts)
            month_key = dt.strftime("%Y-%m")
            month_counts[month_key] += 1
        
        most_active_month = month_counts.most_common(1)[0][0] if month_counts else "未知"
        
        # 判断趋势（最近3个月 vs 前3个月）
        if len(month_counts) >= 6:
            sorted_months = sorted(month_counts.keys(), reverse=True)
            recent_3 = sum(month_counts[m] for m in sorted_months[:3])
            previous_3 = sum(month_counts[m] for m in sorted_months[3:6])
            
            if recent_3 > previous_3 * 1.2:
                trend = "上升"
            elif recent_3 < previous_3 * 0.8:
                trend = "下降"
            else:
                trend = "稳定"
        else:
            trend = "数据不足"
        
        return {
            "total_days": total_days,
            "avg_videos_per_month": round(len(videos) / total_months, 2),
            "avg_videos_per_week": round(len(videos) / total_weeks, 2),
            "most_active_month": most_active_month,
            "activity_trend": trend,
            "monthly_distribution": dict(month_counts.most_common()),
        }
    
    def identify_top_videos(self, videos: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, Any]]:
        """
        识别表现最佳的视频
        
        Args:
            videos: 视频列表
            top_n: 返回前N个
            
        Returns:
            热门视频列表
        """
        # 计算综合热度分
        scored_videos = []
        
        for video in videos:
            stat = video.get("stat", {})
            views = stat.get("view", 0) or 0
            likes = stat.get("like", 0) or 0
            coins = stat.get("coin", 0) or 0
            favorites = stat.get("favorite", 0) or 0
            
            # 热度分 = 播放量 + 点赞*5 + 投币*10 + 收藏*10
            heat_score = views + likes * 5 + coins * 10 + favorites * 10
            
            scored_videos.append({
                "bvid": video.get("bvid"),
                "title": video.get("title"),
                "views": views,
                "likes": likes,
                "coins": coins,
                "favorites": favorites,
                "heat_score": heat_score,
                "pubdate": video.get("pubdate") or video.get("created"),
            })
        
        # 按热度分排序
        scored_videos.sort(key=lambda x: x["heat_score"], reverse=True)
        
        return scored_videos[:top_n]
    
    def detect_content_pattern(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        检测内容模式特征
        
        Args:
            videos: 视频列表
            
        Returns:
            内容模式分析
        """
        if not videos:
            return {
                "is_series_creator": False,
                "has_fixed_format": False,
                "update_frequency": "未知",
            }
        
        # 检测是否为系列创作者（标题中有序号或相同前缀）
        titles = [v.get("title", "") for v in videos]
        
        # 检查是否有共同前缀
        common_prefix = ""
        if titles:
            first_title = titles[0]
            for i in range(1, min(len(first_title), 20)):
                prefix = first_title[:i]
                if all(t.startswith(prefix) for t in titles[:min(10, len(titles))]):
                    common_prefix = prefix
        
        has_series_pattern = bool(common_prefix) and len(common_prefix) >= 3
        
        # 检测更新频率
        timestamps = [v.get("created") or v.get("pubdate") for v in videos if v.get("created") or v.get("pubdate")]
        if len(timestamps) >= 2:
            timestamps.sort()
            intervals = [timestamps[i] - timestamps[i+1] for i in range(len(timestamps)-1)]
            avg_interval = sum(intervals) / len(intervals)
            
            if avg_interval <= 86400 * 2:  # 2天内
                frequency = "高频（日更或隔日更）"
            elif avg_interval <= 86400 * 7:  # 1周内
                frequency = "中频（周更）"
            elif avg_interval <= 86400 * 30:  # 1月内
                frequency = "低频（月更）"
            else:
                frequency = "极低频"
        else:
            frequency = "数据不足"
        
        return {
            "is_series_creator": has_series_pattern,
            "series_prefix": common_prefix if has_series_pattern else None,
            "has_fixed_format": has_series_pattern,
            "update_frequency": frequency,
        }
