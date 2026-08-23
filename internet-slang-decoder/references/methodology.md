# 互联网缩写解析方法论

> 本文档是搜索闭环和验证机制的权威定义。SKILL.md 中的关键规则引用本文档。

## 解析流程

```
用户输入 → 缩写识别 → 本地库查询
                      ├─ 命中 → 排序输出
                      └─ 未命中 → 检查缓存 → 命中 → 输出
                                           └─ 未命中 → 搜索补充 → 验证 → 回填+缓存 → 输出
```

## 缩写识别规则

- 正则模式：`[a-zA-Z]{2,10}`（纯字母）+ `[a-zA-Z][0-9][a-zA-Z0-9]{0,4}`（混合）
- 过滤：小型英文词频字典（`scripts/common_words.json`，替代原先内联硬编码的上千行停用词表；加载失败时回退到内置最小集）
- 优先级：已知缩写（在 `scripts/slang_db.json` 或 `hotwords.json` 中）优先匹配，不受词频字典过滤影响
- 上限：单次识别最多返回 20 个缩写

## 输入长度（截断提示）

- 阈值：`MAX_INPUT_LEN = 500` 字符
- **NEVER 静默截断**。输入超过阈值时：
  - 默认返回 `too_long=True` 的提示结果，交由用户决定（精简输入 / 显式截断 / 全文解析），不再偷偷丢弃尾部内容
  - `decode(..., truncate=True)` 显式按前 500 字符解析
  - `decode(..., allow_partial=True)` 全文解析，仅在结果中附带 `notice` 提示
- CLI 对应：`--truncate`、`--allow-partial`

## 搜索闭环

### 触发条件

当 `decode()` 返回 `result['unknown']` 非空时，MUST 执行搜索补充，NEVER 直接返回"未识别"。

### 搜索预算

| 未知缩写数量 | 每缩写查询数 | 策略 |
|-------------|-------------|------|
| 1-2 个 | 2 次 | 逐个或合并搜索 |
| 3-5 个 | 1 次 | 合并搜索 |
| 5+ 个 | 1 次 | 仅处理前5个，其余引导用户 |

### 搜索降级

当 WebSearch 不可用时，MUST 向用户说明并引导手动查询：
```
暂时无法联网搜索 '{缩写}'，建议您：
1. 在搜索引擎中查询 "{缩写} 是什么意思"
2. 提供更多上下文帮助我判断
```

## 准确性验证

### 置信度分级

| 置信度 | 来源 | 可信度 | 处理方式 |
|--------|------|--------|---------|
| 0.95+ | 内置库/多源验证 | 高 | 直接输出 |
| 0.85-0.94 | 内置库/单源验证 | 较高 | 直接输出，标注领域 |
| 0.70-0.84 | 搜索发现/小众 | 中 | 输出并建议确认 |
| <0.70 | 模糊搜索/猜测 | 低 | 列举可能，引导用户确认 |

### 验证规则

- 多来源一致 → 置信度 +15%
- 含义过于宽泛（含"某个""一种"）→ 置信度 -20%
- 含义过短（<3字）→ 置信度 -10%
- 含义长度合理（5-30字）→ 置信度 +5%
- 上下文领域匹配 → 置信度 +10%

## 上下文消歧

多义缩写（GG/OP/MVP/DM 等）排序不再只依赖置信度，而采用 `_disambiguate_entries()`：

- **领域一致性**：与推断领域一致的词条 +0.3 强加分（强信号）
- **词性/用法先验**：按领域的轻量动词/名词启发线索 +0.05（如游戏圈判断"太强/技能/动作"，不依赖外部 POS 工具）
- 最终按 (领域一致性, 置信度) 排序，并把最优项标记为 `recommended`（输出中显示 `★推荐`）
- 单义结果不受消歧影响

## 词条更新机制

`scripts/slang_db.json` 是主词库；为避免网络迭代导致词条过时，新增 **热词层 `scripts/hotwords.json`**：

- 通过 `python scripts/decoder.py --add <ABBR> <FULL_FORM> <MEANING> [--domain X] [--confidence N] [--notes ...]` 增量写入
- 加载时热词自动合入主词库，并覆盖同缩写+同全称的旧词条（`source` 标记为 `hotword`）
- MUST 优先用热词层做增量更新，而非直接改 `slang_db.json`（避免重跑 `build_refs.py` 引发 references 口径漂移）

## 回填格式

调用 `add_search_results()` 时，MUST 遵循以下字段要求：

```python
{
    "full_form": str,      # REQUIRED - 全称
    "meaning": str,        # REQUIRED - 含义说明
    "domain": str,         # REQUIRED - 领域枚举值
    "confidence": float,   # REQUIRED - 0.0-1.0
    "examples": list,      # OPTIONAL - 例句列表
    "source": str,         # OPTIONAL - 来源标识
    "notes": str,          # OPTIONAL - 备注（如敏感词警告）
}
```

domain 枚举值：`entertainment` / `gaming` / `lifestyle` / `tech` / `anime` / `finance` / `academic` / `unknown`
