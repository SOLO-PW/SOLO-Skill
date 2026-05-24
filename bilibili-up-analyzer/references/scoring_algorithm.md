# Bilibili UP主分析技能 - 评分算法说明文档

## 概述

本文档详细说明Bilibili UP主分析技能中的多维度评分系统算法，包括UP主类型识别、评分维度定义、得分计算方法和等级划分标准。

## 设计原则

### 1. 类型差异化

不同类型的UP主采用不同的评分维度和权重，确保评分的公平性和针对性：

- **知识区UP主**：侧重内容深度和学习价值
- **娱乐区UP主**：侧重传播力和互动活跃度
- **游戏区UP主**：侧重技术价值和社区氛围
- **生活区UP主**：侧重真实感和粉丝粘性

### 2. 数据驱动

评分完全基于可量化的数据指标，避免主观判断：

- 所有维度都有明确的计算公式
- 评分标准基于平台数据分布设定
- 支持自定义阈值调整

### 3. 可扩展性

评分系统支持新增UP主类型和评分维度：

- 模块化设计，易于扩展
- 权重配置化，可动态调整
- 支持自定义评分策略

## UP主类型识别

### 类型定义

系统支持以下UP主类型：

| 类型 | 标识 | 典型分区 | 内容特征 |
|------|------|----------|----------|
| 知识区 | knowledge | 知识、资讯 | 教学、科普、专业内容 |
| 娱乐区 | entertainment | 娱乐、影视、鬼畜 | 搞笑、娱乐、轻松内容 |
| 游戏区 | game | 游戏 | 攻略、实况、评测 |
| 生活区 | life | 生活、美食、时尚、运动、动物圈 | 日常、vlog、生活方式 |
| 音乐区 | music | 音乐、舞蹈 | 翻唱、演奏、原创音乐 |
| 科技区 | tech | 科技、汽车 | 评测、教程、前沿技术 |
| 美食区 | food | 美食 | 食谱、探店、美食制作 |
| 动画区 | anime | 动画、番剧、国创 | 二创、MAD、AMV |
| 未知 | unknown | - | 无法明确分类 |

### 识别算法

```python
def detect_up_type(primary_partition: str, video_types: List[str]) -> UpType:
    """
    检测UP主类型
    
    算法逻辑:
    1. 优先根据主要发布分区判断
    2. 如分区判断为未知，根据视频类型辅助判断
    3. 返回最匹配的类型
    """
    
    # 分区映射表
    partition_type_map = {
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
    
    # 类型映射表（辅助判断）
    type_mapping = {
        "教程": UpType.KNOWLEDGE,
        "评测": UpType.TECH,
        "vlog": UpType.LIFE,
        "音乐": UpType.MUSIC,
        "混剪": UpType.ANIME,
    }
    
    # 优先根据分区判断
    up_type = partition_type_map.get(primary_partition, UpType.UNKNOWN)
    
    # 如分区判断为未知，尝试根据视频类型判断
    if up_type == UpType.UNKNOWN and video_types:
        for vt in video_types:
            if vt in type_mapping:
                up_type = type_mapping[vt]
                break
    
    return up_type
```

## 评分维度体系

### 维度定义

每个评分维度包含：

```python
@dataclass
class ScoreDimension:
    name: str           # 维度名称
    weight: float      # 权重（0-1）
    description: str   # 维度描述
```

### 各类型评分维度配置

#### 1. 知识区 (Knowledge)

| 维度 | 权重 | 说明 | 计算依据 |
|------|------|------|----------|
| 内容深度 | 25% | 视频的知识密度和深度 | 收藏率、完播率 |
| 完播率 | 20% | 观众完整观看的比例 | 播放完成度数据 |
| 收藏率 | 20% | 内容被收藏的比例 | favorite_rate |
| 互动质量 | 15% | 评论质量和讨论深度 | 评论率、评论长度 |
| 更新稳定性 | 10% | 内容更新的规律性和持续性 | 视频数量、更新频率 |
| 粉丝增长 | 10% | 粉丝增长趋势 | follower数量 |

#### 2. 娱乐区 (Entertainment)

| 维度 | 权重 | 说明 | 计算依据 |
|------|------|------|----------|
| 播放量 | 25% | 视频的播放热度 | avg_views |
| 点赞率 | 20% | 观众点赞比例 | like_rate |
| 分享率 | 20% | 内容被分享传播的比例 | share_rate |
| 互动活跃度 | 15% | 弹幕和评论活跃度 | danmaku_rate + reply_rate |
| 爆款率 | 10% | 产生爆款视频的比例 | 超平均3倍播放量视频占比 |
| 内容创新 | 10% | 内容创意和新颖度 | 投币率（原创度指标） |

#### 3. 游戏区 (Game)

| 维度 | 权重 | 说明 | 计算依据 |
|------|------|------|----------|
| 互动率 | 25% | 观众互动参与度 | like_rate + coin_rate |
| 弹幕密度 | 20% | 弹幕活跃程度 | danmaku_rate |
| 评论质量 | 15% | 评论的深度和质量 | reply_rate |
| 技术/攻略价值 | 15% | 游戏技术或攻略的实用性 | 收藏率 |
| 粉丝粘性 | 15% | 粉丝忠诚度和回访率 | follower数量 |
| 更新频率 | 10% | 内容更新速度 | 视频数量 |

#### 4. 生活区 (Life)

| 维度 | 权重 | 说明 | 计算依据 |
|------|------|------|----------|
| 粉丝增长 | 20% | 粉丝增长趋势和速度 | follower数量 |
| 内容稳定性 | 20% | 内容质量和风格的稳定性 | 播放量标准差 |
| 互动氛围 | 15% | 评论区和弹幕氛围 | reply_rate + danmaku_rate |
| 真实感 | 15% | 内容的真实性和亲和力 | 点赞率 |
| 更新规律 | 15% | 内容更新的规律性 | 更新频率 |
| 多元化 | 15% | 内容主题的丰富程度 | 分区数量 |

#### 5. 音乐区 (Music)

| 维度 | 权重 | 说明 | 计算依据 |
|------|------|------|----------|
| 播放量 | 25% | 作品播放热度 | avg_views |
| 收藏率 | 20% | 作品被收藏比例 | favorite_rate |
| 分享传播 | 15% | 作品传播度 | share_rate |
| 技术水准 | 15% | 演唱/演奏/制作水平 | 点赞率 |
| 原创度 | 15% | 原创作品的占比 | 投币率 |
| 粉丝互动 | 10% | 粉丝互动质量 | reply_rate |

#### 6. 科技区 (Tech)

| 维度 | 权重 | 说明 | 计算依据 |
|------|------|------|----------|
| 专业度 | 25% | 技术内容的专业程度 | 收藏率 |
| 实用性 | 20% | 内容的实用价值 | 收藏率 + 分享率 |
| 完播率 | 15% | 观众完整观看比例 | 完播率数据 |
| 收藏率 | 15% | 内容被收藏比例 | favorite_rate |
| 互动质量 | 15% | 技术讨论的深度 | reply_rate |
| 更新频率 | 10% | 内容更新速度 | 视频数量 |

#### 7. 美食区 (Food)

| 维度 | 权重 | 说明 | 计算依据 |
|------|------|------|----------|
| 播放量 | 20% | 视频播放热度 | avg_views |
| 收藏率 | 20% | 食谱/教程被收藏比例 | favorite_rate |
| 互动氛围 | 15% | 评论区互动活跃度 | reply_rate |
| 制作质量 | 15% | 视频制作和呈现质量 | 点赞率 |
| 创新性 | 15% | 菜品/内容的创新程度 | 投币率 |
| 更新稳定性 | 15% | 内容更新的规律性 | 更新频率 |

#### 8. 动画区 (Anime)

| 维度 | 权重 | 说明 | 计算依据 |
|------|------|------|----------|
| 播放量 | 25% | 作品播放热度 | avg_views |
| 弹幕活跃度 | 20% | 弹幕互动活跃度 | danmaku_rate |
| 二创质量 | 15% | 二次创作的质量和创意 | 投币率 |
| 粉丝粘性 | 15% | 核心粉丝活跃度 | follower数量 |
| 更新频率 | 15% | 内容更新速度 | 视频数量 |
| 话题度 | 10% | 作品引发讨论的热度 | 评论率 |

#### 9. 未知类型 (Unknown)

| 维度 | 权重 | 说明 | 计算依据 |
|------|------|------|----------|
| 综合播放量 | 25% | 整体播放表现 | avg_views |
| 互动率 | 20% | 整体互动水平 | like_rate + coin_rate |
| 粉丝增长 | 20% | 粉丝增长趋势 | follower数量 |
| 内容质量 | 15% | 内容整体质量 | 收藏率 |
| 更新稳定性 | 10% | 更新规律性 | 视频数量 |
| 成长潜力 | 10% | 未来发展潜力 | follower/video_count |

## 维度得分计算

### 基础得分计算

每个维度的基础得分为50分，根据实际数据表现进行加减：

```python
def calculate_dimension_score(dimension_name: str, metrics: Dict, up_info: Dict) -> float:
    """
    计算单个维度得分
    
    基础分: 50
    根据数据表现调整
    """
    base_score = 50.0
    
    # 根据维度类型应用不同的计算规则
    if dimension_name == "播放量":
        return calculate_views_score(metrics.get("avg_views", 0))
    elif dimension_name == "点赞率":
        return calculate_like_rate_score(metrics.get("like_rate", 0))
    # ... 其他维度
    
    return base_score
```

### 各维度评分标准

#### 1. 播放量评分

| 平均播放量 | 得分 |
|------------|------|
| > 100,000 | 95 |
| > 50,000 | 85 |
| > 10,000 | 75 |
| > 5,000 | 65 |
| > 1,000 | 55 |
| ≤ 1,000 | 45 |

```python
def calculate_views_score(avg_views: int) -> float:
    if avg_views > 100000:
        return 95
    elif avg_views > 50000:
        return 85
    elif avg_views > 10000:
        return 75
    elif avg_views > 5000:
        return 65
    elif avg_views > 1000:
        return 55
    else:
        return 45
```

#### 2. 点赞率评分

| 点赞率 | 得分 |
|--------|------|
| > 5% | 95 |
| > 3% | 85 |
| > 2% | 75 |
| > 1% | 65 |
| ≤ 1% | 50 |

#### 3. 收藏率评分

| 收藏率 | 得分 |
|--------|------|
| > 3% | 95 |
| > 1.5% | 85 |
| > 0.8% | 75 |
| > 0.3% | 65 |
| ≤ 0.3% | 50 |

#### 4. 分享率评分

| 分享率 | 得分 |
|--------|------|
| > 0.5% | 95 |
| > 0.2% | 85 |
| > 0.1% | 75 |
| > 0.05% | 65 |
| ≤ 0.05% | 50 |

#### 5. 弹幕率评分

| 弹幕率 | 得分 |
|--------|------|
| > 2% | 95 |
| > 1% | 85 |
| > 0.5% | 75 |
| > 0.2% | 65 |
| ≤ 0.2% | 50 |

#### 6. 评论率评分

| 评论率 | 得分 |
|--------|------|
| > 0.5% | 95 |
| > 0.3% | 85 |
| > 0.15% | 75 |
| > 0.08% | 65 |
| ≤ 0.08% | 50 |

#### 7. 粉丝数评分

| 粉丝数 | 得分 |
|--------|------|
| > 1,000,000 | 95 |
| > 500,000 | 90 |
| > 100,000 | 80 |
| > 50,000 | 70 |
| > 10,000 | 60 |
| ≤ 10,000 | 50 |

#### 8. 更新稳定性评分

| 视频数量 | 得分 |
|----------|------|
| ≥ 100 | 90 |
| ≥ 50 | 80 |
| ≥ 20 | 70 |
| ≥ 10 | 60 |
| < 10 | 50 |

#### 9. 内容深度/专业度评分

基于收藏率判断：

| 收藏率 | 得分 |
|--------|------|
| > 2% | 90 |
| > 1% | 80 |
| > 0.5% | 70 |
| ≤ 0.5% | 60 |

#### 10. 爆款率评分

统计播放量超过平均值3倍的视频比例：

| 爆款比例 | 得分 |
|----------|------|
| > 20% | 95 |
| > 10% | 85 |
| > 5% | 75 |
| ≤ 5% | 60 |

#### 11. 原创度/创新性评分

基于投币率判断（原创度高的内容通常投币率较高）：

| 投币率 | 得分 |
|--------|------|
| > 1% | 90 |
| > 0.5% | 80 |
| > 0.2% | 70 |
| ≤ 0.2% | 60 |

#### 12. 成长潜力评分

基于粉丝数与视频数的比例：

```python
def calculate_potential_score(follower: int, video_count: int) -> float:
    if video_count == 0:
        return 50
    
    ratio = follower / video_count
    
    if ratio > 10000:
        return 95
    elif ratio > 5000:
        return 85
    elif ratio > 1000:
        return 75
    elif ratio > 500:
        return 65
    else:
        return 55
```

## 综合评分计算

### 计算公式

```python
def calculate_total_score(
    dimensions: List[ScoreDimension],
    dimension_scores: Dict[str, float]
) -> float:
    """
    计算综合评分
    
    公式: 总分 = Σ(维度得分 × 维度权重)
    """
    total_score = 0.0
    
    for dim in dimensions:
        score = dimension_scores.get(dim.name, 0)
        total_score += score * dim.weight
    
    return round(total_score, 2)
```

### 计算示例

假设一个知识区UP主的各维度得分：

| 维度 | 权重 | 得分 | 加权得分 |
|------|------|------|----------|
| 内容深度 | 25% | 88 | 22.0 |
| 完播率 | 20% | 82 | 16.4 |
| 收藏率 | 20% | 85 | 17.0 |
| 互动质量 | 15% | 80 | 12.0 |
| 更新稳定性 | 10% | 90 | 9.0 |
| 粉丝增长 | 10% | 87 | 8.7 |
| **合计** | 100% | - | **85.1** |

综合评分：**85.1分**

## 等级划分

### 等级标准

| 等级 | 分数范围 | 说明 | 颜色标识 |
|------|----------|------|----------|
| S | 90-100 | 顶级UP主，在领域内具有极高影响力和专业度 | 🟣 紫色 |
| A | 80-89 | 优秀UP主，内容质量和影响力都很出色 | 🔵 蓝色 |
| B | 70-79 | 良好UP主，内容稳定，有一定影响力 | 🟢 绿色 |
| C | 60-69 | 普通UP主，内容尚可，有提升空间 | 🟡 黄色 |
| D | 0-59 | 新手UP主，需要持续积累和改进 | 🔴 红色 |

### 等级判定

```python
def determine_grade(total_score: float) -> Tuple[str, str]:
    """
    判定等级和评价
    
    Returns:
        (等级, 评价摘要)
    """
    if total_score >= 90:
        return "S", "顶级UP主，在领域内具有极高影响力和专业度"
    elif total_score >= 80:
        return "A", "优秀UP主，内容质量和影响力都很出色"
    elif total_score >= 70:
        return "B", "良好UP主，内容稳定，有一定影响力"
    elif total_score >= 60:
        return "C", "普通UP主，内容尚可，有提升空间"
    else:
        return "D", "新手UP主，需要持续积累和改进"
```

## 评分结果解读

### 高分特征 (S/A级)

- **内容质量高**：收藏率、点赞率高于平均水平
- **影响力大**：粉丝数多，播放量稳定
- **互动活跃**：评论、弹幕活跃度高
- **更新规律**：保持稳定的更新频率

### 中等分数特征 (B/C级)

- **内容尚可**：基础数据达标但不够突出
- **有提升空间**：某些维度表现较弱
- **需要优化**：可能在互动、更新或内容深度方面有改进空间

### 低分特征 (D级)

- **新手阶段**：视频数量少，粉丝积累不足
- **数据较弱**：各项互动指标偏低
- **需要成长**：建议学习同类型优秀UP主

## 算法优化建议

### 1. 动态阈值

根据平台整体数据分布动态调整评分阈值：

```python
class DynamicThreshold:
    """动态阈值管理"""
    
    def __init__(self, platform_data: Dict):
        self.percentiles = self._calculate_percentiles(platform_data)
    
    def get_threshold(self, metric: str, percentile: float) -> float:
        """获取指定百分位阈值"""
        return self.percentiles[metric][percentile]
```

### 2. 时间衰减

对历史数据应用时间衰减，更重视近期表现：

```python
def apply_time_decay(video_data: List[Dict], half_life_days: int = 90) -> List[Dict]:
    """
    应用时间衰减
    
    越近期的视频权重越高
    """
    decayed_data = []
    now = time.time()
    
    for video in video_data:
        age_days = (now - video['pubdate']) / 86400
        weight = 0.5 ** (age_days / half_life_days)
        video['weight'] = weight
        decayed_data.append(video)
    
    return decayed_data
```

### 3. 横向对比

与同类型UP主进行横向对比，给出相对评分：

```python
def calculate_relative_score(up_data: Dict, peers_data: List[Dict]) -> float:
    """
    计算相对评分
    
    与同类型UP主进行对比
    """
    peer_avg = calculate_peer_average(peers_data)
    relative_score = (up_data['score'] / peer_avg) * 50
    
    return min(100, relative_score)
```

## 版本历史

### v1.0.0

- 初始版本评分系统
- 支持8种UP主类型
- 定义6维度评分体系
- 实现基础得分计算

## 附录：评分配置代码

```python
# 评分维度配置示例
SCORING_CONFIG = {
    UpType.KNOWLEDGE: [
        ScoreDimension("内容深度", 0.25, "视频的知识密度和深度"),
        ScoreDimension("完播率", 0.20, "观众完整观看的比例"),
        ScoreDimension("收藏率", 0.20, "内容被收藏的比例"),
        ScoreDimension("互动质量", 0.15, "评论质量和讨论深度"),
        ScoreDimension("更新稳定性", 0.10, "内容更新的规律性和持续性"),
        ScoreDimension("粉丝增长", 0.10, "粉丝增长趋势"),
    ],
    # ... 其他类型配置
}
```
