# Trae 用户蒸馏器

从 [Trae 官方中文社区](https://forum.trae.cn/) 提取指定用户的公开历史发言，生成可模仿其语言风格、逻辑思维和性格特点的数字人格技能。

## 功能特性

- **一键蒸馏**：输入用户名，自动完成数据提取 + 技能生成
- **Discourse API**：基于官方 JSON API，数据完整可靠
- **多维风格分析**：11+ 维度深度解析用户表达习惯
- **分场景建模**：区分「主动发帖」与「回复他人」的风格差异
- **负面指令约束**：自动生成「不要做什么」清单，防止 LLM 过度模仿
- **标准输出**：生成符合 skill-creator 最佳实践的 SKILL.md

## 快速开始

### 安装依赖

```bash
pip install requests
```

### 一键模式（推荐）

```bash
python scripts/fetch_user_data.py <用户名> --output ./output --generate
```

示例：

```bash
python scripts/fetch_user_data.py aifree --output ./skills --generate
```

执行完成后，在 `./skills/trae-aifree/` 目录下生成完整的个性化技能包。

### 分步模式

**Step 1: 提取数据**

```bash
python scripts/fetch_user_data.py <用户名> --output <输出目录> [--max-topics 50]
```

输出：`trae_user_<用户名>_<时间戳>.json`

**Step 2: 生成技能**

```bash
python scripts/generate_persona_skill.py <数据JSON文件> --output <输出目录>
```

## 输出结构

```
trae-<用户名>/
├── SKILL.md                    # 人格技能主文档（可直接使用）
├── user_data.json              # 原始提取数据（含完整风格分析）
└── references/
    └── conversation_history.md # 完整历史发言记录
```

### SKILL.md 内容结构

- **核心身份**：用户名、信任等级、注册时间、获赞统计
- **语言风格**：正式度、句长、表情使用、语气词、标点习惯、Markdown 习惯
- **关注领域**：从话题分类和标签提取的兴趣领域
- **场景差异**：发帖 vs 回复的风格对比
- **风格禁忌**：基于数据自动生成的负面约束（如「不要使用表情符号」「不要频繁使用感叹号」）
- **对话示例**：基于真实发言的 Q&A 示例

## 风格分析维度

| 维度 | 说明 |
|------|------|
| 基础统计 | 总字数、中/英文占比、句子数、段落数 |
| 句式特征 | 平均句长、平均段落长度 |
| 正式度评分 | 0-1 连续值，基于正式/非正式标记词比例 |
| 标点习惯 | 感叹号/问号/省略号/逗号/句号使用比例 |
| 语气词频率 | 14 种常见语气词（啊、呢、吧、吗等）各自计数 |
| 表情使用 | 表情数量、每百字符表情率 |
| 表达风格 | 举例/反问/强调/结构化/谦逊频率 |
| Markdown 习惯 | 代码块/列表/引用/加粗/标题检测 |
| 回复长度分布 | 短(<50字)/中(50-200字)/长(>200字)比例 |
| 高频词汇 | 中文 bigram + 英文单词 Top 15（停用词过滤） |
| 分场景分析 | 发帖 vs 回复的正式度、句长、语气词差异 |
| 负面指令 | 基于数据自动生成「不要做什么」约束 |

## 技术细节

### 数据来源（Discourse API）

- `GET /u/{username}.json` — 用户资料
- `GET /u/{username}/summary.json` — 摘要（回复列表、参与话题、获赞统计）
- `GET /t/{topic_id}.json` — 话题详情
- `GET /t/{topic_id}/posts.json?post_ids[]=...` — 按需加载帖子
- `GET /search.json?q=@{username}` — 搜索补充

### 数据量门槛

- 最少 3 条内容（话题 + 回复）
- 最少 200 字总文本量

不足时自动拒绝生成，避免低质量输出。

### 限流保护

- 请求间隔 0.5 秒
- 429 状态码自动重试（最多 3 次，指数退避）
- 5xx 错误自动重试

## 故障排除

| 问题 | 原因 | 解决 |
|------|------|------|
| 用户不存在 (404) | 用户名拼写错误 | 检查论坛用户名拼写 |
| 数据量不足 | 用户发言太少 | 需至少 3 条内容和 200 字 |
| 限流 (429) | 请求过快 | 脚本自动等待并重试 |
| requests 未安装 | 缺少依赖 | `pip install requests` |

## 项目结构

```
trae-user-distiller/
├── README.md                   # 本文档
├── SKILL.md                    # 技能定义（供 AI 使用）
└── scripts/
    ├── fetch_user_data.py      # 数据提取脚本
    └── generate_persona_skill.py # 技能生成脚本
```

## 版本历史

- **v3.0** (当前)
  - 新增一键模式 `--generate`
  - 新增分场景风格分析（发帖 vs 回复）
  - 新增负面指令自动生成
  - 优化 HTML 清理（保护代码块内容）
  - 优化正式度分析（词边界匹配）

- **v2.0**
  - 从 HTML 正则解析迁移到 Discourse JSON API
  - 新增多维风格分析（11+ 维度）
  - 新增话题缓存避免重复请求
  - 优化错误处理和限流保护

- **v1.0**
  - 初始版本，基础数据提取和技能生成

## 许可证

本项目仅供学习和研究使用。请遵守 [Trae 官方中文社区](https://forum.trae.cn/) 的使用条款，仅提取公开可见的用户数据。

---

*trae-user-distiller v3.0*
