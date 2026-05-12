---
name: trae-user-distiller
description: 从 Trae 论坛提取用户历史发言数据，生成模仿其语言风格的个性化数字人格技能。
---

# Trae 用户蒸馏器

从 Trae 论坛 (https://forum.trae.cn/) 提取指定用户的公开历史发言，生成可模仿其语言风格、逻辑思维和性格特点的数字人格技能（标准 SKILL.md 格式）。

## 工作流程

```
用户提供论坛用户名 → Discourse API 提取数据 → 多维风格分析 → 生成 SKILL.md
```

## 执行步骤

### 一键模式（推荐）

```bash
python scripts/fetch_user_data.py <用户名> --output <输出目录> --generate
```

自动完成数据提取 + 技能生成，一步到位。

### 分步模式

**提取数据**:
```bash
python scripts/fetch_user_data.py <用户名> --output <输出目录> [--max-topics 50]
```

**生成技能**:
```bash
python scripts/generate_persona_skill.py <数据JSON文件> --output <输出目录>
```

依赖: `requests`（`python -m pip install requests`）

### 输出结构

```
trae-<用户名>/
├── SKILL.md                         # 人格技能（progressive disclosure）
├── user_data.json                   # 原始数据（含完整风格分析）
└── references/
    └── conversation_history.md      # 完整历史发言记录
```

## 风格分析维度

| 维度 | 指标 |
|------|------|
| 基础统计 | 总字数、中/英文占比、句子数、段落数 |
| 句式特征 | 平均句长、平均段落长度 |
| 正式度 | 0-1 评分（正式/非正式标记词比例，词边界匹配） |
| 标点习惯 | 感叹号/问号/省略号/逗号/句号使用比例 |
| 语气词 | 14 种常见语气词频率 |
| 表情使用 | 表情数量、每百字符表情率 |
| 表达风格 | 举例/反问/强调/结构化/谦逊频率 |
| Markdown | 代码块/列表/引用/加粗/标题检测 |
| 回复长度 | 短(<50)/中(50-200)/长(>200)分布 |
| 高频词汇 | 中文 bigram + 英文单词 Top 15（停用词过滤） |
| **分场景分析** | **发帖 vs 回复的正式度、句长、语气词差异** |
| **负面指令** | **基于数据自动生成「不要做什么」约束，防止过度模仿** |

## 故障排除

| 问题 | 解决 |
|------|------|
| 用户不存在 (404) | 检查用户名拼写 |
| 数据量不足 | 需至少 3 条内容和 200 字 |
| 限流 (429) | 脚本自动重试（最多 3 次） |
| requests 未安装 | `python -m pip install requests` |
