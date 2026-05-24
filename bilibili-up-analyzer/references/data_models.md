# Bilibili UP主分析技能 - 数据模型定义文档

## 概述

本文档定义Bilibili UP主分析技能中使用的所有数据模型，包括输入模型、内部模型和输出模型。

## 核心数据模型

### 1. UP主信息模型 (UpInfo)

存储UP主的基础信息。

```python
class UpInfo:
    """UP主信息"""
    
    # 基础字段
    uid: str                    # UP主UID（唯一标识）
    name: str                   # 昵称
    face: str                   # 头像URL
    sign: str                   # 个性签名
    level: int                  # 账号等级（0-6）
    
    # 统计数据
    follower: int               # 粉丝数
    following: int              # 关注数
    archive_count: int          # 视频投稿数
    article_count: int          # 专栏投稿数
    like_num: int               # 获赞数
```

**示例**:

```json
{
  "uid": "123456",
  "name": "示例UP主",
  "face": "https://i0.hdslb.com/bfs/face/xxx.jpg",
  "sign": "这是一个示例签名",
  "level": 6,
  "follower": 100000,
  "following": 100,
  "archive_count": 500,
  "article_count": 10,
  "like_num": 500000
}
```

### 2. 视频基础模型 (VideoBase)

视频列表中获取的基础信息。

```python
class VideoBase:
    """视频基础信息"""
    
    # 标识字段
    bvid: str                   # 视频BV号（唯一标识）
    
    # 内容字段
    title: str                  # 视频标题
    description: str            # 视频简介
    pic: str                    # 封面URL
    length: str                 # 视频时长（字符串格式，如"10:30"）
    
    # 时间字段
    created: int                # 发布时间戳（Unix时间戳）
    
    # 统计字段
    play: int                   # 播放量
    comment: int                # 评论数
    video_review: int           # 弹幕数
    
    # 分区字段
    typeid: int                 # 分区ID
    typename: str               # 分区名称
```

**示例**:

```json
{
  "bvid": "BV1xx411c7mD",
  "title": "示例视频标题",
  "description": "这是一个示例视频简介",
  "pic": "https://i0.hdslb.com/bfs/archive/xxx.jpg",
  "length": "10:30",
  "created": 1609459200,
  "play": 10000,
  "comment": 100,
  "video_review": 500,
  "typeid": 36,
  "typename": "知识"
}
```

### 3. 视频详情模型 (VideoDetail)

包含完整统计数据的视频信息。

```python
class VideoDetail:
    """视频详细信息"""
    
    # 标识字段
    bvid: str                   # 视频BV号
    aid: int                    # 视频AV号
    
    # 内容字段
    title: str                  # 视频标题
    description: str            # 视频描述
    duration: int               # 视频时长（秒）
    
    # 时间字段
    pubdate: int                # 发布时间戳
    
    # 作者字段
    owner: OwnerInfo            # 作者信息
    
    # 统计字段
    stat: VideoStat             # 统计数据
    
    # 分区字段
    tname: str                  # 分区名称
    tid: int                    # 分区ID


class OwnerInfo:
    """作者信息"""
    mid: int                    # UP主UID
    name: str                   # UP主昵称


class VideoStat:
    """视频统计数据"""
    view: int                   # 播放量
    danmaku: int                # 弹幕数
    reply: int                  # 评论数
    favorite: int               # 收藏数
    coin: int                   # 投币数
    share: int                  # 分享数
    like: int                   # 点赞数
    dislike: int                # 点踩数
```

**示例**:

```json
{
  "bvid": "BV1xx411c7mD",
  "aid": 12345678,
  "title": "示例视频标题",
  "description": "这是一个示例视频描述",
  "duration": 630,
  "pubdate": 1609459200,
  "owner": {
    "mid": 123456,
    "name": "示例UP主"
  },
  "stat": {
    "view": 10000,
    "danmaku": 500,
    "reply": 100,
    "favorite": 1000,
    "coin": 500,
    "share": 200,
    "like": 2000,
    "dislike": 10
  },
  "tname": "知识",
  "tid": 36
}
```

## 分析结果模型

### 4. 分区分析模型 (PartitionAnalysis)

视频分区分布分析结果。

```python
class PartitionAnalysis:
    """分区分析结果"""
    
    total_videos: int           # 视频总数
    partition_count: int        # 涉及分区数
    primary_partition: str      # 主要发布分区
    distribution: List[PartitionItem]  # 分区分布详情


class PartitionItem:
    """分区统计项"""
    
    partition: str              # 分区名称
    count: int                  # 视频数量
    percentage: float           # 占比（%）
    total_views: int            # 该分区总播放量
    avg_views: int              # 该分区平均播放量
```

**示例**:

```json
{
  "total_videos": 100,
  "partition_count": 3,
  "primary_partition": "知识",
  "distribution": [
    {
      "partition": "知识",
      "count": 60,
      "percentage": 60.0,
      "total_views": 600000,
      "avg_views": 10000
    },
    {
      "partition": "生活",
      "count": 30,
      "percentage": 30.0,
      "total_views": 150000,
      "avg_views": 5000
    },
    {
      "partition": "科技",
      "count": 10,
      "percentage": 10.0,
      "total_views": 50000,
      "avg_views": 5000
    }
  ]
}
```

### 5. 视频类型分析模型 (VideoTypeAnalysis)

视频类型分类分析结果。

```python
class VideoTypeAnalysis:
    """视频类型分析结果"""
    
    total_videos: int           # 视频总数
    type_count: int             # 类型数量
    primary_type: str           # 主要视频类型
    distribution: List[TypeItem]  # 类型分布详情


class TypeItem:
    """类型统计项"""
    
    type: str                   # 视频类型
    count: int                  # 视频数量
    percentage: float           # 占比（%）
```

**视频类型定义**:

| 类型 | 说明 | 关键词 |
|------|------|--------|
| 教程 | 教学类内容 | 教程、教学、入门、指南、攻略 |
| 评测 | 测评体验类 | 评测、测评、体验、开箱、上手 |
| 解说 | 解说类内容 | 解说、解说员、解说版 |
| vlog | 日常记录类 | vlog、日常、记录、生活记录 |
| 混剪 | 剪辑创作类 | 混剪、MAD、AMV、GMV |
| 直播回放 | 直播录像 | 直播、回放、录播 |
| 搬运 | 转载内容 | 搬运、转载 |
| 原创 | 原创内容 | 原创、自制 |
| 搞笑 | 娱乐搞笑类 | 搞笑、沙雕、爆笑 |
| 音乐 | 音乐类内容 | 翻唱、演奏、音乐、歌曲 |
| 其他 | 无法分类 | - |

**示例**:

```json
{
  "total_videos": 100,
  "type_count": 4,
  "primary_type": "教程",
  "distribution": [
    {
      "type": "教程",
      "count": 50,
      "percentage": 50.0
    },
    {
      "type": "评测",
      "count": 30,
      "percentage": 30.0
    },
    {
      "type": "vlog",
      "count": 15,
      "percentage": 15.0
    },
    {
      "type": "其他",
      "count": 5,
      "percentage": 5.0
    }
  ]
}
```

### 6. 互动指标模型 (InteractionMetrics)

视频互动数据统计。

```python
class InteractionMetrics:
    """互动指标统计"""
    
    # 平均值
    avg_views: int              # 平均播放量
    avg_likes: int              # 平均点赞数
    avg_coins: int              # 平均投币数
    avg_favorites: int          # 平均收藏数
    avg_shares: int             # 平均分享数
    avg_replies: int            # 平均评论数
    avg_danmaku: int            # 平均弹幕数
    
    # 互动率（相对于播放量）
    like_rate: float            # 点赞率（%）
    coin_rate: float            # 投币率（%）
    favorite_rate: float        # 收藏率（%）
    share_rate: float           # 分享率（%）
    reply_rate: float           # 评论率（%）
    danmaku_rate: float         # 弹幕率（%）
```

**示例**:

```json
{
  "avg_views": 10000,
  "avg_likes": 500,
  "avg_coins": 100,
  "avg_favorites": 200,
  "avg_shares": 50,
  "avg_replies": 30,
  "avg_danmaku": 150,
  "like_rate": 5.0,
  "coin_rate": 1.0,
  "favorite_rate": 2.0,
  "share_rate": 0.5,
  "reply_rate": 0.3,
  "danmaku_rate": 1.5
}
```

### 7. 趋势分析模型 (TrendAnalysis)

发布趋势分析结果。

```python
class TrendAnalysis:
    """趋势分析结果"""
    
    total_days: int             # 分析时间跨度（天）
    avg_videos_per_month: float # 月均发布量
    avg_videos_per_week: float  # 周均发布量
    most_active_month: str      # 最活跃月份（YYYY-MM格式）
    activity_trend: str         # 活跃度趋势（上升/下降/稳定/数据不足）
    monthly_distribution: Dict[str, int]  # 月度发布分布
```

**示例**:

```json
{
  "total_days": 365,
  "avg_videos_per_month": 8.3,
  "avg_videos_per_week": 1.9,
  "most_active_month": "2024-01",
  "activity_trend": "上升",
  "monthly_distribution": {
    "2023-06": 5,
    "2023-07": 6,
    "2023-08": 8,
    "2023-09": 10,
    "2023-10": 12,
    "2023-11": 15
  }
}
```

### 8. 热门视频模型 (TopVideo)

热门视频排名信息。

```python
class TopVideo:
    """热门视频信息"""
    
    bvid: str                   # 视频BV号
    title: str                  # 视频标题
    views: int                  # 播放量
    likes: int                  # 点赞数
    coins: int                  # 投币数
    favorites: int              # 收藏数
    heat_score: int             # 热度分（计算值）
    pubdate: int                # 发布时间戳
```

**热度分计算公式**:

```
热度分 = 播放量 + 点赞数 × 5 + 投币数 × 10 + 收藏数 × 10
```

**示例**:

```json
{
  "bvid": "BV1xx411c7mD",
  "title": "热门视频标题",
  "views": 100000,
  "likes": 5000,
  "coins": 2000,
  "favorites": 3000,
  "heat_score": 180000,
  "pubdate": 1609459200
}
```

### 9. 内容模式模型 (ContentPattern)

内容创作模式分析。

```python
class ContentPattern:
    """内容模式分析"""
    
    is_series_creator: bool     # 是否为系列创作者
    series_prefix: Optional[str]  # 系列前缀（如果有）
    has_fixed_format: bool      # 是否有固定格式
    update_frequency: str       # 更新频率描述
```

**更新频率分类**:

| 频率 | 判断标准 | 说明 |
|------|----------|------|
| 高频（日更或隔日更） | 平均间隔 ≤ 2天 | 更新非常频繁 |
| 中频（周更） | 2天 < 平均间隔 ≤ 7天 | 每周更新 |
| 低频（月更） | 7天 < 平均间隔 ≤ 30天 | 每月更新 |
| 极低频 | 平均间隔 > 30天 | 更新很少 |
| 数据不足 | 视频数 < 2 | 无法判断 |

**示例**:

```json
{
  "is_series_creator": true,
  "series_prefix": "【教程】",
  "has_fixed_format": true,
  "update_frequency": "中频（周更）"
}
```

## 评分模型

### 10. 评分维度模型 (ScoreDimension)

评分维度定义。

```python
class ScoreDimension:
    """评分维度"""
    
    name: str                   # 维度名称
    weight: float              # 权重（0-1）
    description: str           # 维度描述
```

**示例**:

```python
ScoreDimension(
    name="内容深度",
    weight=0.25,
    description="视频的知识密度和深度"
)
```

### 11. 评分结果模型 (ScoreResult)

综合评分结果。

```python
class ScoreResult:
    """评分结果"""
    
    total_score: float          # 总分（0-100）
    grade: str                  # 等级（S/A/B/C/D）
    dimension_scores: Dict[str, float]  # 各维度得分
    summary: str                # 评价摘要
```

**等级划分标准**:

| 等级 | 分数范围 | 说明 |
|------|----------|------|
| S | 90-100 | 顶级UP主，在领域内具有极高影响力和专业度 |
| A | 80-89 | 优秀UP主，内容质量和影响力都很出色 |
| B | 70-79 | 良好UP主，内容稳定，有一定影响力 |
| C | 60-69 | 普通UP主，内容尚可，有提升空间 |
| D | 0-59 | 新手UP主，需要持续积累和改进 |

**示例**:

```json
{
  "total_score": 85.5,
  "grade": "A",
  "dimension_scores": {
    "内容深度": 88.0,
    "完播率": 82.0,
    "收藏率": 85.0,
    "互动质量": 80.0,
    "更新稳定性": 90.0,
    "粉丝增长": 87.0
  },
  "summary": "优秀UP主，内容质量和影响力都很出色"
}
```

## 输出报告模型

### 12. 分析报告模型 (AnalysisReport)

完整的分析报告数据结构。

```python
class AnalysisReport:
    """分析报告"""
    
    # 元数据
    up_name: str                # UP主昵称
    analysis_time: str          # 分析时间
    video_count: int            # 分析视频数
    
    # 基础信息
    up_info: UpInfo             # UP主信息
    
    # 分析结果
    partition_analysis: PartitionAnalysis    # 分区分析
    type_analysis: VideoTypeAnalysis         # 类型分析
    interaction_metrics: InteractionMetrics  # 互动指标
    trend_analysis: TrendAnalysis            # 趋势分析
    top_videos: List[TopVideo]               # 热门视频
    content_pattern: ContentPattern          # 内容模式
    
    # 评分结果
    score: ScoreResult          # 综合评分
    
    # 建议
    strengths: List[str]        # 优势分析
    suggestions: List[str]      # 改进建议
```

## 数据流转图

```
┌─────────────────┐
│   用户输入      │
│  (UID/URL)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   数据采集      │
│  (DataFetcher)  │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌────────┐
│UpInfo  │ │Video   │
│(基础)  │ │List    │
└────────┘ └────┬───┘
                │
                ▼
           ┌────────┐
           │Video   │
           │Detail  │
           │(详细)  │
           └────┬───┘
                │
                ▼
┌─────────────────┐
│   数据分析      │
│ (VideoAnalyzer) │
└────────┬────────┘
         │
    ┌────┼────┬────────┬────────┐
    ▼    ▼    ▼        ▼        ▼
┌────┐┌────┐┌────┐ ┌──────┐ ┌──────┐
│分区││类型││互动│ │ 趋势 │ │ 热门 │
│分析││分析││指标│ │ 分析 │ │ 视频 │
└────┘└────┘└────┘ └──────┘ └──────┘
         │
         ▼
┌─────────────────┐
│   评分计算      │
│(ScoringSystem)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   报告生成      │
│(ReportGenerator)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Markdown报告   │
│  / JSON数据     │
└─────────────────┘
```

## 数据验证规则

### 字段验证

| 模型 | 字段 | 验证规则 |
|------|------|----------|
| UpInfo | uid | 必须为数字字符串 |
| UpInfo | name | 非空，最大长度50 |
| UpInfo | level | 整数，范围0-6 |
| VideoBase | bvid | 必须以"BV"开头 |
| VideoBase | title | 非空，最大长度100 |
| VideoBase | created | Unix时间戳，正整数 |
| VideoStat | view | 非负整数 |
| ScoreResult | total_score | 浮点数，范围0-100 |
| ScoreResult | grade | 必须是S/A/B/C/D之一 |

### 业务规则

1. **播放量有效性**: view > 0 的视频才参与互动率计算
2. **时间有效性**: pubdate 必须在合理范围内（2009年至今）
3. **分区有效性**: typeid 必须在已知分区映射表中
4. **评分有效性**: 各维度得分必须在0-100范围内

## 版本历史

### v1.0.0

- 初始版本
- 定义核心数据模型
- 建立分析结果模型体系
