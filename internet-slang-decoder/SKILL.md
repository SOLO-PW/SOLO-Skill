---
name: internet-slang-decoder
description: |
  解析互联网缩写和网络用语的专业工具。覆盖娱乐圈（饭圈）、游戏圈、生活网络用语、科技互联网、动漫、金融、学术等领域。内置 490+ 词条，数据存储在 scripts/slang_db.json。
  
  ## 触发条件（满足任一即触发）
  
  ### 直接询问类（中文）
  - "xxx是什么意思" / "xxx是啥意思" / "xxx什么梗"
  - "xxx代表什么" / "xxx是什么缩写"
  - "xxx啥意思" / "xxx什么意思"
  - "yyds是什么" / "gg是什么"
  - "绝绝子什么意思" / "泰裤辣是什么"
  
  ### 直接询问类（英文）
  - "what does xxx mean" / "what is xxx"
  - "xxx meaning" / "xxx stands for"
  - "what is xxx short for" / "decode xxx"
  - "xxx slang" / "xxx abbreviation"
  
  ### 解析请求类
  - "解析这句话里的缩写" / "这句话里的网络用语什么意思"
  - "帮我看看这句话" / "翻译一下这个缩写"
  - "这句话怎么理解" / "这段话里的术语"
  - "parse this text" / "explain this slang"
  
  ### 网络用语/词典类
  - "网络用语xxx" / "饭圈用语xxx" / "游戏术语xxx"
  - "缩写xxx" / "xxx缩写" / "xxx梗" / "xxx网络梗"
  - "动漫用语xxx" / "金融术语xxx" / "币圈xxx"
  - "slang dictionary" / "internet slang" / "abbreviation lookup"
  - "有没有缩写词典" / "网络用语大全" / "黑话词典"
  
  ### 特定缩写识别
  - 2-6个字母的连续英文单词（如yyds, xswl, gg, op, api）
  - 混合数字字母的短词（如u1s1, b2b, k8s）
  - 中文语境中出现的英文缩写
  - 中文拼音缩写（如jjz, tkl, wyz, hjj, yjjc, bdjw）
  
  ### 上下文线索
  - 用户提到"缩写"、"简称"、"术语"、"黑话"
  - 用户说"看不懂"、"不明白"、"啥意思"
  - 用户询问特定圈子用语（游戏/饭圈/科技/动漫/金融/学术）
  
  ## 不触发的情况
  - 普通英文单词（hello, world, python等常见词）
  - 专业术语全称解释（如"什么是人工智能"）
  - 非缩写类词汇解释（如"什么是区块链"）
  - 超过6个字母的英文单词
  - 纯翻译请求（如"翻译一下这段英文"、"translate this to Chinese"）
  
  ## 功能特性
  - 内置 490+ 词条，覆盖 7 大领域
  - 支持多义性处理（如GG可以是good game或哥哥）
  - 置信度排序和上下文感知
  - 对未知缩写自动调用WebSearch搜索补充
  - 搜索结果缓存（30天有效期）
  - 多源交叉验证确保准确性
  - 支持 text/json/markdown 三种输出格式
---

# 互联网缩写解析器

## 核心工作流（Agent MUST READ）

```
用户输入 → decoder.decode() → 检查 unknown 列表
                                    ├─ 空 → 直接输出结果
                                    └─ 非空 → 检查缓存 → 命中 → 输出
                                                        └─ 未命中 → WebSearch → 解析验证 → add_search_results() 回填 → 输出
```

### CRITICAL 规则

1. **MUST** 当 `result['unknown']` 非空且缓存未命中时，执行搜索补充，NEVER 直接返回"未识别"
2. **MUST** 搜索结果回填时遵循 methodology.md 中定义的字段格式
3. **MUST** 优先读取缓存，避免重复搜索
4. **NEVER** 单次会话搜索超过 5 次（搜索预算硬上限）
5. **NEVER** 对置信度 < 0.50 的结果直接输出，MUST 标注"不确定"并引导用户确认
6. **MUST** 输入超过 500 字符时截断处理，提示用户精简输入

## 快速判断指南

收到用户查询时，快速检查：

1. **包含2-6字母缩写？** → 可能是（如yyds, gg, op, api）
2. **询问"什么意思/是什么/meaning"？** → 可能是
3. **提到"缩写/简称/术语/黑话/slang"？** → 可能是
4. **请求"解析/翻译缩写/解释"？** → 可能是
5. **特定圈子语境？**（游戏/饭圈/科技/动漫/金融）→ 可能是

**排除**：普通英文单词、非缩写类概念解释、纯翻译请求

## 搜索闭环执行步骤

### Step 1：本地解析

```python
from scripts.decoder import SlangDecoder
decoder = SlangDecoder()
result = decoder.decode("用户输入的文本", context="可选上下文")
```

### Step 2：检查是否需要搜索

```python
if result['unknown']:
    search_queries = result['search_queries']
```

### Step 3：执行 WebSearch

对未知缩写执行搜索。**多个缩写应合并为一次搜索**：

```
WebSearch('"缩写A" "缩写B" 网络用语 缩写 含义')
```

如果 `result['inferred_domain']` 有值，添加领域限定词。

### Step 4：解析搜索结果并回填

从搜索片段中提取含义，然后回填。回填字段 MUST 遵循 methodology.md 定义的格式。

### Step 5：输出结果

向用户呈现所有解析结果，标注来源（内置库/网络搜索/缓存）。

## 搜索预算

详见 [methodology.md](references/methodology.md) - 搜索闭环章节。

## 上下文感知

| 关键词 | 推断领域 |
|--------|---------|
| 游戏/电竞/开黑/排位 | 游戏圈 |
| 娱乐/饭圈/明星/追星 | 娱乐圈 |
| 科技/编程/开发/代码 | 科技/互联网 |
| 动漫/二次元/番剧 | 动漫/二次元 |
| 金融/股票/投资/币圈 | 金融/商业 |
| 学术/论文/考试/大学 | 学术/教育 |
| 生活/日常/聊天 | 生活/网络 |

## 多义缩写处理

遇到 GG、OP、MVP、DM 等多义缩写时：
1. 列举所有可能含义
2. 按置信度排序
3. 根据上下文提升相关领域权重
4. 引导用户确认

完整多义表见 [ambiguous-abbreviations.md](references/ambiguous-abbreviations.md)

## 搜索降级策略

当 WebSearch 不可用时，MUST 向用户说明情况并引导手动查询，NEVER 静默失败。

## 参考文档

- [methodology.md](references/methodology.md) - 完整方法论（搜索闭环、验证机制、回填格式）
- [result-schema.md](references/result-schema.md) - 输出格式规范
- [ambiguous-abbreviations.md](references/ambiguous-abbreviations.md) - 多义缩写对照表（自动生成）
- [templates.md](references/templates.md) - 用户交互话术模板（自动生成）
- [entertainment.md](references/entertainment.md) - 娱乐圈词典（自动生成）
- [gaming.md](references/gaming.md) - 游戏圈词典（自动生成）
- [lifestyle.md](references/lifestyle.md) - 生活/网络词典（自动生成）
- [tech.md](references/tech.md) - 科技/互联网词典（自动生成）
- [anime.md](references/anime.md) - 动漫/二次元词典（自动生成）
- [finance.md](references/finance.md) - 金融/商业词典（自动生成）
- [academic.md](references/academic.md) - 学术/教育词典（自动生成）

## 工具脚本

- `scripts/decoder.py` - 核心解析器（从 slang_db.json 加载 + 搜索回填 + 缓存）
- `scripts/search_slang.py` - 搜索工具（查询生成 + 结果解析 + 准确性验证）
- `scripts/build_refs.py` - 从 JSON 生成 references/ 下的 .md 词典文件
- `scripts/slang_db.json` - 词条数据源（Single Source of Truth，493条）
