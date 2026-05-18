---
name: internet-slang-decoder
description: |
  解析互联网缩写和网络用语的专业工具。覆盖娱乐圈（饭圈）、游戏圈、生活网络用语、科技互联网、动漫、金融等多个领域。
  
  ## 触发条件（满足任一即触发）
  
  ### 直接询问类
  - "xxx是什么意思" / "xxx是啥意思" / "xxx什么梗"
  - "xxx代表什么" / "xxx是什么缩写"
  - "xxx啥意思" / "xxx什么意思"
  - "yyds是什么" / "gg是什么"
  
  ### 解析请求类
  - "解析这句话" / "这句话什么意思" / "这段话里的缩写"
  - "帮我看看这句话" / "翻译一下"
  - "这句话怎么理解"
  
  ### 网络用语类
  - "网络用语xxx" / "饭圈用语xxx" / "游戏术语xxx"
  - "缩写xxx" / "xxx缩写"
  - "xxx梗" / "xxx网络梗"
  
  ### 特定缩写识别
  - 2-6个字母的连续英文单词（如yyds, xswl, gg, op, api）
  - 混合数字字母的短词（如u1s1, b2b）
  - 中文语境中出现的英文缩写
  
  ### 上下文线索
  - 用户提到"缩写"、"简称"、"术语"、"黑话"
  - 用户说"看不懂"、"不明白"、"啥意思"
  - 用户询问特定圈子用语（游戏/饭圈/科技）
  
  ## 不触发的情况
  - 普通英文单词（hello, world, python等常见词）
  - 专业术语全称解释（如"什么是人工智能"）
  - 非缩写类词汇解释（如"什么是区块链"）
  - 超过6个字母的英文单词
  
  ## 功能特性
  - 支持多义性处理（如GG可以是good game或哥哥）
  - 置信度排序和上下文感知
  - 对未知缩写自动调用WebSearch搜索补充
  - 多源交叉验证确保准确性
---

# 互联网缩写解析器

## 核心工作流（Agent 必读）

```
用户输入 → decoder.decode() → 检查 unknown 列表
                                    ├─ 空 → 直接输出结果
                                    └─ 非空 → WebSearch 搜索 → 解析结果 → add_search_results() 回填 → 输出
```

**关键规则：当 `result['unknown']` 非空时，必须执行搜索补充，不能直接返回"未识别"。**

## 快速判断指南

收到用户查询时，快速检查：

1. **包含2-6字母缩写？** → 可能是（如yyds, gg, op, api）
2. **询问"什么意思/是什么"？** → 可能是
3. **提到"缩写/简称/术语"？** → 可能是
4. **请求"解析/翻译/解释"？** → 可能是
5. **特定圈子语境？**（游戏/饭圈/科技）→ 可能是

**排除**：普通英文单词、非缩写类概念解释

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
    # 需要搜索补充
    search_queries = result['search_queries']
    # search_queries 包含为每个未知缩写推荐的搜索查询
```

### Step 3：执行 WebSearch

对未知缩写执行搜索。**多个缩写应合并为一次搜索**：

```
WebSearch('"缩写A" "缩写B" 网络用语 缩写 含义')
```

如果 `result['inferred_domain']` 有值，添加领域限定词：
```
WebSearch('"缩写A" "缩写B" 游戏术语 含义')
```

### Step 4：解析搜索结果

从 WebSearch 返回的片段中提取含义，然后回填：

```python
# 手动分析搜索结果后，构造 findings 回填
decoder.add_search_results("缩写", [
    {
        "full_form": "全称",
        "meaning": "含义说明",
        "domain": "gaming",  # entertainment/gaming/lifestyle/tech/anime/finance/unknown
        "confidence": 0.8,
        "examples": ["例句"],
        "source": "知乎/百度百科/..."
    }
])
```

### Step 5：输出结果

向用户呈现所有解析结果，标注来源（内置库/网络搜索）。

## 搜索预算

| 未知缩写数量 | 最大搜索次数 | 策略 |
|-------------|-------------|------|
| 1-2 个 | 2 次 | 逐个或合并搜索 |
| 3-5 个 | 3 次 | 合并搜索 + 补充搜索 |
| 5+ 个 | 3 次 | 合并搜索，其余引导用户 |

## 准确性验证

搜索结果的置信度评估：
- **多个来源一致** → 置信度 0.85+
- **单一权威来源**（知乎高赞/百度百科）→ 置信度 0.80
- **单一普通来源** → 置信度 0.70
- **含义模糊/宽泛** → 置信度 0.50-0.60，标注"不确定"

## 上下文感知

自动从文本关键词推断领域，也支持手动指定：

| 关键词 | 推断领域 |
|--------|---------|
| 游戏/电竞/开黑/排位 | 游戏圈 |
| 娱乐/饭圈/明星/追星 | 娱乐圈 |
| 科技/编程/开发/代码 | 科技/互联网 |
| 动漫/二次元/番剧 | 动漫/二次元 |
| 金融/股票/投资 | 金融/商业 |
| 生活/日常/聊天 | 生活/网络 |

## 多义缩写处理

遇到 GG、OP、MVP、DM 等多义缩写时：
1. 列举所有可能含义
2. 按置信度排序
3. 根据上下文提升相关领域权重
4. 引导用户确认

完整多义表见 [ambiguous-abbreviations.md](references/ambiguous-abbreviations.md)

## 用户引导

### 搜索无结果时
```
我搜索了缩写 '{缩写}'，但没有找到明确的含义。

请问：
1. 这是在什么场景下看到的？（游戏/娱乐/工作/其他）
2. 能否提供完整句子？
```

### 搜索结果矛盾时
```
关于 '{缩写}'，不同来源说法不一：
- 来源A：{含义A}
- 来源B：{含义B}

请问您是在什么场景下看到的？
```

### 置信度低时
```
'{缩写}' 可能是 {含义}（置信度较低）。
建议您向对方确认，或提供更多上下文。
```

更多话术模板见 [templates.md](references/templates.md)

## 参考文档

- [methodology.md](references/methodology.md) - 完整方法论（搜索闭环、验证机制）
- [ambiguous-abbreviations.md](references/ambiguous-abbreviations.md) - 多义缩写对照表
- [templates.md](references/templates.md) - 用户交互话术模板
- [entertainment.md](references/entertainment.md) - 娱乐圈缩写词典
- [gaming.md](references/gaming.md) - 游戏圈缩写词典
- [lifestyle.md](references/lifestyle.md) - 生活/网络用语词典
- [tech.md](references/tech.md) - 科技/互联网缩写词典

## 工具脚本

- `scripts/decoder.py` - 核心解析器（本地库 + 搜索回填）
- `scripts/search_slang.py` - 搜索工具（查询生成 + 结果解析 + 准确性验证）
