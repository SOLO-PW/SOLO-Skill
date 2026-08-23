# Skill Fusion — 智能技能融合器

将多个 AI Agent Skill 融合为统一的新 Skill，通过结构化分析、冲突解决和内容合成完成。

## 功能概览

- **三种工作模式**：预览分析（preview）、完整融合（full）、增量融合（incremental）
- **六阶段融合流程**：收集验证 → 深度解析 → 关系分析 → 冲突解决 → 设计合成 → 验证输出
- **智能冲突解决**：四级冲突分类 + 交互式决策协议
- **批量融合支持**：3+ 个 Skill 的两阶段聚合策略
- **低交叉度智能分析**：自动评估融合价值，避免强行合并

## 快速开始

| 你的需求 | 模式 | 说明 |
|----------|------|------|
| 先看看能不能融合 | `preview` | 仅输出分析报告，不生成 Skill |
| 融合两个 Skill | `full` | 完整六阶段融合流程 |
| 在已融合 Skill 上加新能力 | `incremental` | 以已有结果为基准增量扩展 |
| 融合 3+ 个 Skill | `full` + 批量 | 两两分组聚合 |

## 目录结构

```
skill-fusion/
├── SKILL.md                           # 核心工作流与操作指引
└── references/
    ├── fusion-algorithm.md            # 六阶段融合算法详细方法论
    ├── conflict-resolution.md         # 冲突分类体系与解决协议
    ├── incremental-fusion.md          # 增量融合的完整流程
    ├── preview-analysis.md            # 预览模式的分析框架与报告模板
    ├── output-template.md             # 融合输出结构模板与命名规范
    ├── fusion-config.md               # 可配置规则阈值、默认值与覆盖机制
    ├── script-dependency-check.md     # 跨 Skill 脚本依赖解析与冲突检测
    └── examples.md                    # 8 个融合案例（含失败案例）
```

## 核心概念

### 交叉度评估

融合前必须评估 Skill 之间的功能交叉度：

| 交叉度 | 处理方式 |
|--------|----------|
| 高（>50%） | 直接融合，合并重叠部分 |
| 中（20-50%） | 智能整合，保留特色能力 |
| 低（<20%） | 深度分析后决定是否融合 |

### 冲突解决

| 级别 | 类型 | 处理方式 |
|------|------|----------|
| 严重 | 矛盾 | 交互式：向用户展示选项，等待决策 |
| 高 | 重叠 | 交互式：向用户展示选项，等待决策 |
| 中 | 模糊 | 提出智能合并方案，经用户确认 |
| 低 | 冗余 | 自动去重 |

### 融合输出

融合后的 Skill 包含：
- 合成后的 `SKILL.md`（含融合日志）
- 合并去重后的 `references/`
- 如输入含脚本或资源，输出创建对应目录

## 参考文档索引

| 文档 | 内容 | 何时阅读 |
|------|------|----------|
| [fusion-algorithm.md](references/fusion-algorithm.md) | 六阶段流程的详细方法论、低交叉度策略 | 需要理解融合算法细节时 |
| [conflict-resolution.md](references/conflict-resolution.md) | 冲突分类、解决策略、交互式模板 | 遇到冲突需要解决时 |
| [incremental-fusion.md](references/incremental-fusion.md) | 增量融合流程、回溯冲突、边界检查 | 使用增量融合模式时 |
| [preview-analysis.md](references/preview-analysis.md) | 预览分析框架、报告模板 | 使用预览模式时 |
| [output-template.md](references/output-template.md) | 输出结构模板、融合日志规范、命名规范 | 生成融合 Skill 时 |
| [fusion-config.md](references/fusion-config.md) | 可配置规则阈值、默认值与覆盖机制 | 需要调整融合规模或规则阈值时 |
| [script-dependency-check.md](references/script-dependency-check.md) | 跨 Skill 脚本依赖解析与冲突检测 | 融合含 scripts 的 Skill 时 |
| [examples.md](references/examples.md) | 8 个完整案例（互补/重叠/多领域/资源冲突/失败/低交叉高价值/增量/预览） | 需要参考实际案例时 |
