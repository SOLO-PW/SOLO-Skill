---
name: skill-fusion
description: |
  智能融合多个 Skill 为统一新 Skill。当用户需要合并、整合、重组 Skill，或构建复合能力工作流时使用。触发词：融合 Skill、合并 Skill、整合 Skill、组合 Skill、Skill 合并、Skill 整合、把两个 Skill 合成一个、在已有 Skill 上加新能力、预览融合可行性、批量融合。支持三种模式：preview（仅分析不生成）、full（完整融合）、incremental（增量融合）。
---

# Skill 融合器

将多个 Skill 融合为统一的新 Skill，通过结构化分析、冲突解决和内容合成完成。

---

## 快速判断

| 用户意图 | 模式 | 关键动作 |
|----------|------|----------|
| "先看看能不能融合" | `preview` | 输出分析报告，不生成 Skill |
| "融合 A 和 B" | `full` | 完整六阶段融合流程 |
| "在已融合的 X 上加 Y" | `incremental` | 以 X 为基准增量融合 Y |
| "融合 A B C D" | `full` + 批量 | 两两分组 → 结果融合 |

---

## 融合工作流

### 模式一：full（完整融合）

```
步骤 1: 收集验证 → 步骤 2: 深度解析 → 步骤 3: 关系分析 → 步骤 4: 冲突解决 → 步骤 5: 设计合成 → 步骤 6: 验证输出
```

#### 步骤 1：收集验证

对每个输入 Skill 目录：
1. 读取 `SKILL.md`，验证 frontmatter 包含 `name` 和 `description`
2. 清点目录结构：`scripts/`、`references/`、`assets/` 及其内容
3. 标记缺失或格式错误的文件，向用户报告

**前置检查**：
- 至少提供 2 个 Skill 目录
- 每个 SKILL.md 的 frontmatter 格式有效
- 如验证失败，列出具体问题并终止

#### 步骤 2：深度解析

对每个 Skill 构建能力画像：

| 提取维度 | 来源 | 产出 |
|----------|------|------|
| 名称、描述、触发模式 | frontmatter | 元数据对象 |
| 语义块（工作流/工具指令/领域知识/约束/示例） | SKILL.md body | 语义块列表 |
| 脚本用途、依赖、接口 | `scripts/` | 脚本清单 |
| 参考文件主题和关键章节 | `references/` | 参考清单 |
| 资源格式和使用场景 | `assets/` | 资源清单 |
| 核心能力、领域标签、触发条件、依赖项、复杂度 | 综合分析 | 能力画像 |

详细方法论参见 [references/fusion-algorithm.md](references/fusion-algorithm.md)。

#### 步骤 3：关系分析

对所有 Skill 执行交叉分析：

1. **功能重叠检测** — 分类为 `identical`（完全相同）、`equivalent`（等效）、`adjacent`（相邻）
2. **互补性映射** — 识别独特能力、自然流水线序列、协同效应
3. **冲突检测** — 不兼容依赖、矛盾指令、互斥约束
4. **缺口分析** — 融合后应补充的缺失能力
5. **交叉度评估** — 计算功能重叠百分比

**交叉度分支**：

| 交叉度 | 处理 |
|--------|------|
| 高（>50%） | 直接融合，合并重叠部分 |
| 中（20-50%） | 智能整合，保留特色能力 |
| 低（<20%） | 进入扩展分析流程（见下方） |

**低交叉度扩展分析**：
1. 深度理解每个 Skill 的用户意图、使用场景、能力边界
2. 寻找融合价值点：场景串联、能力互补、知识复用、用户体验
3. 决策融合方向：深度整合 / 轻量整合 / 编排整合 / 建议不融合
4. 如决策为"建议不融合"，输出分析报告并终止

详见 [references/fusion-algorithm.md](references/fusion-algorithm.md) 的"低交叉度 Skill 的智能融合策略"章节。

向用户呈现结构化分析摘要后再继续。

#### 步骤 4：冲突解决

对每个冲突按严重级别处理：

| 级别 | 类型 | 处理方式 |
|------|------|----------|
| 严重 | 矛盾（指令直接对立） | 交互式：向用户展示冲突和选项，等待决策 |
| 高 | 重叠（相同能力不同实现） | 交互式：向用户展示冲突和选项，等待决策 |
| 中 | 模糊（适用范围不清） | 提出智能合并方案，经用户确认 |
| 低 | 冗余（重复内容） | 自动去重，保留更全面版本 |

交互式解决时，为每个冲突提供 4 个选项：
- **选项 A**：使用 Skill X 的方法（附理由）
- **选项 B**：使用 Skill Y 的方法（附理由）
- **选项 C**：合并两种方法为统一方案（如可行）
- **选项 D**：保留两种作为条件分支（由上下文决定）

详见 [references/conflict-resolution.md](references/conflict-resolution.md)。

#### 步骤 5：设计合成

**结构设计**：
1. 确定范围：单领域（深度）或多领域（广度）
2. 设计 SKILL.md 结构：合成 frontmatter + 合并 body（渐进式披露）
3. 设计资源整合方案：scripts 保留最健壮版本 / references 按主题合并去重 / assets 用命名空间前缀解决冲突

**内容合成**：
1. 编写 SKILL.md frontmatter（复合名称 + 全面描述）
2. 编写 SKILL.md body（合并工作流 + 条件分支 + 领域章节）
3. 合并参考文件，保持连贯叙述
4. 整合脚本，保留最佳实现
5. 嵌入融合日志（HTML 注释记录所有合并决策）

输出模板参见 [references/output-template.md](references/output-template.md)。

#### 步骤 6：验证输出

**必须通过**：
- [ ] frontmatter 包含 `name` 和 `description`
- [ ] 描述覆盖所有原始 Skill 的触发场景
- [ ] 工作流单一连贯，非独立指令拼接
- [ ] 所有资源引用路径正确
- [ ] 融合日志已嵌入
- [ ] 无内部矛盾或未解决冲突
- [ ] SKILL.md body < 500 行（超出则拆分到 references）

**建议通过**：
- [ ] 模块边界清晰（低交叉度融合时）
- [ ] 冲突解决有明确记录
- [ ] 渐进式披露应用得当

验证失败则修复后重新验证。

---

### 模式二：incremental（增量融合）

在已融合的 Skill 基础上，融合新的 Skill。

与 full 模式的差异：
- 步骤 1：基准 Skill 为已融合 Skill，验证其融合日志完整性
- 步骤 3：交叉度分析仅在新 Skill 与基准之间进行
- 步骤 5：在基准结构上扩展，而非从零设计
- 新增：检查增量融合是否会破坏已有模块边界

详见 [references/incremental-fusion.md](references/incremental-fusion.md)。

---

### 模式三：preview（预览分析）

仅输出分析报告，不生成 Skill。用于融合前评估可行性。

执行步骤 1-3（收集验证 → 深度解析 → 关系分析），然后输出分析报告。

报告包含：
- 各 Skill 能力画像
- 功能重叠与互补性分析
- 冲突检测清单（含严重级别）
- 交叉度评估
- 融合建议与风险评估
- 预估融合复杂度

详见 [references/preview-analysis.md](references/preview-analysis.md)。

---

## 批量融合（3+ Skill）

采用两阶段聚合策略：

```
Skill A + B + C + D
  ├─ 第一轮：(A+B) → Temp-AB，(C+D) → Temp-CD
  └─ 第二轮：(Temp-AB + Temp-CD) → Final
```

**分组策略**：

| 策略 | 适用场景 | 逻辑 |
|------|----------|------|
| 高交叉优先 | 存在明显聚类 | 高交叉度先融合，降低冲突 |
| 领域聚类 | 跨多领域 | 按领域分组，先组内再跨组 |
| 流水线顺序 | 存在输入输出链 | 按数据流顺序逐步融合 |

**每轮检查点**：
- 中间产物 SKILL.md < 500 行
- 无能力稀释（核心能力被弱化）
- 用户可终止并输出当前状态

**复杂度预警**：

| 信号 | 阈值 | 建议 |
|------|------|------|
| 领域数量 | >4 | 拆分为多个融合任务 |
| 严重/高冲突 | >10 | 先解决冲突再融合 |
| 互斥依赖 | 存在 | 建议不融合或重构依赖 |

---

## 交互式调优

融合完成后支持微调，可调优项：

| 调优项 | 说明 |
|--------|------|
| 名称调整 | 修改融合 Skill 名称 |
| 描述优化 | 补充遗漏的触发场景 |
| 工作流重组 | 调整步骤顺序或分组 |
| 模块边界 | 重新分配模块职责 |
| 冲突重解 | 重新选择冲突解决方案 |
| 内容删减 | 移除冗余内容 |

**限制**：不能添加原始 Skill 不存在的新能力；不能改变核心决策（如建议不融合的不能强制融合）；调优不超过 3 轮。

---

## 输入输出规范

### 输入

| 输入项 | 必需 | 说明 |
|--------|------|------|
| Skill 目录路径（≥2 个） | 是 | 待融合的 Skill 目录 |
| 工作模式 | 否 | `preview`/`full`/`incremental`，默认 `full` |
| 批量策略 | 否 | `pairwise`/`cluster`/`pipeline`，默认自动 |
| 基准 Skill 路径 | 增量模式必需 | 已融合的 Skill 目录 |
| 融合意图说明 | 否（推荐） | 帮助理解融合目标 |
| 优先级顺序 | 否 | 冲突时的优先级，默认提供顺序 |

### 输出

**preview 模式**：融合分析报告（Markdown）

**full / incremental 模式**：
```
<融合-skill-名称>/
├── SKILL.md              # 融合的 frontmatter + body + 融合日志
└── references/           # 合并去重后的参考文件
```

如输入含 scripts 或 assets，输出创建相应目录。

---

## 参考文档

- **融合算法**：[references/fusion-algorithm.md](references/fusion-algorithm.md) — 六阶段流程详细方法论 + 低交叉度策略
- **冲突解决**：[references/conflict-resolution.md](references/conflict-resolution.md) — 分类体系、策略和交互式协议
- **增量融合**：[references/incremental-fusion.md](references/incremental-fusion.md) — 增量融合的详细算法和注意事项
- **预览分析**：[references/preview-analysis.md](references/preview-analysis.md) — 预览模式的详细分析框架
- **输出模板**：[references/output-template.md](references/output-template.md) — 融合 Skill 的输出结构模板
- **示例**：[references/examples.md](references/examples.md) — 六个融合案例（含失败案例和增量融合）
