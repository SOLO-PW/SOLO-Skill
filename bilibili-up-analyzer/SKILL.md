---
name: bilibili-up-analyzer
description: |
  Bilibili UP主视频内容分析与报告生成工具。用于分析B站UP主的视频数据、生成专业分析报告，包括播放量、互动数据、分区统计、视频类型分类及多维度评分。支持通过UID、用户名或主页链接作为输入，输出Markdown格式的详细分析报告，适用于UP主自我分析、品牌方选号评估、内容研究等场景。
---

# Bilibili UP主视频分析技能

## 功能概述

- **最新视频分析**：获取并分析UP主最新发布的视频数据
- **全部视频分析**：批量分析UP主历史视频内容
- **发布分区统计**：统计视频在各分区的分布并可视化
- **核心数据指标**：播放量、点赞、投币、收藏、分享等数据分析
- **视频类型分类**：自动识别视频类型并统计占比
- **多维度评分系统**：基于UP主内容类型的差异化评分算法

## 使用方法

### 输入方式

支持三种输入方式（自动识别）：

```bash
# 通过UID
python scripts/analyze_up.py 159285873

# 通过用户名
python scripts/analyze_up.py Jason_Shane

# 通过主页链接
python scripts/analyze_up.py "https://space.bilibili.com/159285873"
```

### 常用参数

```bash
# 分析最近20个视频
python scripts/analyze_up.py Jason_Shane --recent 20

# 分析全部视频（带缓存）
python scripts/analyze_up.py Jason_Shane --all --cache

# 指定输出路径和文件名
python scripts/analyze_up.py Jason_Shane --all --output ./reports/ --filename my_report

# 输出JSON格式
python scripts/analyze_up.py Jason_Shane --all --format json

# 显示详细日志
python scripts/analyze_up.py Jason_Shane --all --verbose

# 禁用图表
python scripts/analyze_up.py Jason_Shane --no-charts
```

### 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `target` | string | 是 | UP主UID、用户名或主页链接（位置参数） |
| `--recent` | int | 否 | 分析最近N个视频，默认10 |
| `--all` | flag | 否 | 分析全部视频（覆盖--recent） |
| `--cache` | flag | 否 | 启用数据缓存 |
| `--cache-dir` | string | 否 | 缓存目录，默认./cache |
| `--output` | string | 否 | 报告输出目录，默认./reports |
| `--format` | string | 否 | 报告格式：markdown/json，默认markdown |
| `--filename` | string | 否 | 指定输出文件名 |
| `--no-charts` | flag | 否 | 禁用图表生成 |
| `--clear-cache` | flag | 否 | 清除缓存后运行 |
| `--verbose` | flag | 否 | 显示详细日志 |

## 工作流程

### 1. 输入解析

自动识别输入类型：
- 纯数字 → UID
- 包含 `space.bilibili.com` → 从URL提取UID
- 其他字符串 → 通过搜索API查找用户名对应的UID

### 2. 数据获取（三级策略）

1. **WBI签名接口**：优先使用带签名的官方API
2. **非签名接口**：WBI失败时回退到标准接口
3. **搜索API兜底**：以上均失败时通过搜索API获取数据

### 3. 数据处理

- 数据清洗与格式化
- 计算衍生指标（互动率等）
- 视频类型自动分类
- 分区统计与聚合

### 4. 评分计算

根据UP主内容类型采用差异化评分标准：
- **知识区UP主**：侧重内容深度、完播率、收藏率
- **娱乐区UP主**：侧重播放量、点赞率、分享率
- **游戏区UP主**：侧重互动率、弹幕密度、评论质量
- **生活区UP主**：侧重粉丝增长、内容稳定性

### 5. 报告生成

生成Markdown报告，包含：分析摘要、UP主基础信息、核心数据指标、分区分布图表、视频类型分析、评分雷达图、趋势分析、热门视频、总结建议。

## 目录结构

```
bilibili-up-analyzer/
├── SKILL.md                    # 本文件
├── scripts/
│   ├── analyze_up.py          # 主分析脚本（入口）
│   ├── data_fetcher.py        # 数据采集模块（含WBI签名）
│   ├── data_analyzer.py       # 数据分析模块
│   ├── scoring_system.py      # 评分系统
│   └── report_generator.py    # 报告生成器
└── references/
    ├── api_reference.md       # 接口设计文档
    ├── data_models.md         # 数据模型定义
    └── scoring_algorithm.md   # 评分算法说明
```

## 依赖安装

```bash
pip install requests matplotlib
```

## 错误处理

- **网络异常**：自动重试3次，指数退避
- **风控拦截（412/-352/-799）**：自动等待后重试
- **数据缺失**：搜索API兜底，标记缺失字段继续分析
- **无效输入**：自动识别输入类型，给出明确错误提示

## 注意事项

1. 未登录状态下部分字段（如获赞数）通过视频数据累加补充
2. 频繁请求可能触发风控，建议启用 `--cache`
3. 评分结果仅供参考，不代表官方评价

## 参考文档

- 接口设计详情：[references/api_reference.md](references/api_reference.md)
- 数据模型定义：[references/data_models.md](references/data_models.md)
- 评分算法说明：[references/scoring_algorithm.md](references/scoring_algorithm.md)
