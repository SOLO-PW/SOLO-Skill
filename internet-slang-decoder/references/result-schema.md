# 输出格式规范

## decode() 返回结构

```json
{
  "original_text": "用户原始输入",
  "context": "用户指定的上下文（可为 null）",
  "inferred_domain": "推断的领域（可为 null）",
  "truncated": false,
  "too_long": false,
  "notice": "可有可无，输入超长时的提示信息（可为 null）",
  "found": [
    {
      "abbreviation": "缩写",
      "matches": [
        {
          "full_form": "全称",
          "meaning": "含义说明",
          "domain": "领域枚举值",
          "confidence": 0.85,
          "examples": ["例句"],
          "source": "builtin|web_search|cache|hotword",
          "notes": "备注（可为 null）",
          "recommended": true
        }
      ]
    }
  ],
  "unknown": ["未识别的缩写"],
  "total_found": 3,
  "total_unknown": 1,
  "search_queries": [
    {
      "abbreviation": "未知缩写",
      "queries": ["推荐的搜索查询"]
    }
  ]
}
```

> - `too_long=True`：输入超过 500 字符且未显式处理时的提示结果，`found`/`unknown` 为空，交由用户决定。
> - `recommended`：上下文消歧后标注的最优多义项（`matches` 中为 true 的条目标记 ★推荐）。

## 领域枚举值

| 值 | 中文 |
|---|------|
| entertainment | 娱乐圈 |
| gaming | 游戏圈 |
| lifestyle | 生活/网络 |
| tech | 科技/互联网 |
| anime | 动漫/二次元 |
| finance | 金融/商业 |
| academic | 学术/教育 |
| unknown | 未知 |

## 置信度分级

| 范围 | 可信度 | 处理 |
|------|--------|------|
| 0.95+ | 高 | 直接输出 |
| 0.85-0.94 | 较高 | 直接输出，标注领域 |
| 0.70-0.84 | 中 | 输出并建议确认 |
| <0.70 | 低 | 列举可能，引导确认 |
