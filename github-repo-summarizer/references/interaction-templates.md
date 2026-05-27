# 交互式提问模板

## 概述

本文档提供各种场景下的交互式提问模板，用于在生成文章过程中与用户进行有效沟通。

## 使用说明

使用AskUserQuestion工具时，按照以下格式组织问题：
- **question**：完整的问题描述
- **header**：简短的标签（最多12字符）
- **options**：2-4个选项
- **multiSelect**：是否允许多选

## 第一阶段：需求确认

### 场景1：用户只提供URL，没有说明需求

**触发条件**：用户输入只包含GitHub仓库URL，没有其他说明

```json
{
  "question": "我注意到您提供了一个GitHub仓库链接，为了生成更符合您需求的文章，想确认一下您的具体需求是什么？",
  "header": "文章目的",
  "options": [
    {
      "label": "项目推荐",
      "description": "生成适合技术博客分享的推荐文章，突出项目亮点和价值"
    },
    {
      "label": "技术分析",
      "description": "深入分析技术实现细节，适合技术团队评估"
    },
    {
      "label": "项目介绍",
      "description": "简洁的功能概述，快速了解项目"
    },
    {
      "label": "对比评测",
      "description": "与同类项目进行对比分析"
    }
  ],
  "multiSelect": false
}
```

### 场景2：确认目标读者

**触发条件**：用户说明了文章目的，但未明确目标读者

```json
{
  "question": "这篇文章主要面向哪类读者？不同读者的关注点会有所不同。",
  "header": "目标读者",
  "options": [
    {
      "label": "开发者",
      "description": "包含技术细节、代码示例、架构设计等"
    },
    {
      "label": "技术管理者",
      "description": "侧重技术选型、团队协作、项目价值"
    },
    {
      "label": "产品经理",
      "description": "侧重功能特性、用户体验、业务价值"
    },
    {
      "label": "普通用户",
      "description": "通俗易懂，侧重使用场景和效果"
    }
  ],
  "multiSelect": false
}
```

### 场景3：确认内容重点

**触发条件**：用户已说明目的和读者，需要确认重点内容

```json
{
  "question": "您希望文章重点介绍哪些方面？",
  "header": "内容重点",
  "options": [
    {
      "label": "核心功能",
      "description": "详细介绍项目的主要功能和特性"
    },
    {
      "label": "技术架构",
      "description": "深入分析技术实现和架构设计"
    },
    {
      "label": "使用场景",
      "description": "重点介绍适用场景和实际应用案例"
    },
    {
      "label": "快速上手",
      "description": "侧重安装配置和快速开始指南"
    }
  ],
  "multiSelect": true
}
```

## 第二阶段：信息补充

### 场景4：README内容较少

**触发条件**：仓库README内容较少，无法提取足够信息

```json
{
  "question": "这个仓库的README内容比较简洁，为了生成更丰富的文章，您能否补充一些信息？",
  "header": "信息补充",
  "options": [
    {
      "label": "我来补充",
      "description": "我会提供项目的更多详细信息"
    },
    {
      "label": "使用默认",
      "description": "基于现有信息生成文章，缺少的部分用占位符"
    },
    {
      "label": "查看Wiki",
      "description": "尝试从项目的Wiki或其他文档获取信息"
    },
    {
      "label": "参考Issues",
      "description": "从项目的Issues和讨论中提取信息"
    }
  ],
  "multiSelect": false
}
```

### 场景5：技术栈复杂

**触发条件**：项目使用多种技术栈，需要确认重点

```json
{
  "question": "这个项目使用了多种技术栈，您希望文章重点介绍哪些技术？",
  "header": "技术重点",
  "options": [
    {
      "label": "前端技术",
      "description": "重点介绍前端框架、UI组件等"
    },
    {
      "label": "后端技术",
      "description": "重点介绍后端架构、API设计等"
    },
    {
      "label": "全栈概览",
      "description": "全面介绍前后端技术栈"
    },
    {
      "label": "核心技术",
      "description": "只介绍项目的核心创新技术"
    }
  ],
  "multiSelect": false
}
```

### 场景6：缺少图片资源

**触发条件**：仓库中没有找到合适的图片

```json
{
  "question": "这个仓库没有找到项目截图或Logo，您希望如何处理？",
  "header": "图片处理",
  "options": [
    {
      "label": "使用占位符",
      "description": "使用占位符图片，后续手动替换"
    },
    {
      "label": "不添加图片",
      "description": "文章中不包含图片部分"
    },
    {
      "label": "我提供图片",
      "description": "我会提供项目的截图或Logo"
    },
    {
      "label": "从官网获取",
      "description": "尝试从项目官网获取图片"
    }
  ],
  "multiSelect": false
}
```

## 第三阶段：内容确认

### 场景7：确认文章风格

**触发条件**：生成文章前确认写作风格

```json
{
  "question": "您希望文章采用什么样的风格？",
  "header": "文章风格",
  "options": [
    {
      "label": "专业严谨",
      "description": "使用专业术语，结构化表达，适合技术文档"
    },
    {
      "label": "轻松易读",
      "description": "使用通俗语言，增加emoji，适合博客分享"
    },
    {
      "label": "简洁明了",
      "description": "精简内容，突出重点，适合快速阅读"
    },
    {
      "label": "详细全面",
      "description": "包含尽可能多的信息，适合深度了解"
    }
  ],
  "multiSelect": false
}
```

### 场景8：确认技术深度

**触发条件**：技术类文章需要确认技术深度

```json
{
  "question": "技术细节应该深入到什么程度？",
  "header": "技术深度",
  "options": [
    {
      "label": "概览级别",
      "description": "简单介绍使用的技术，不涉及实现细节"
    },
    {
      "label": "应用级别",
      "description": "介绍如何使用，包含基本示例"
    },
    {
      "label": "原理级别",
      "description": "深入分析技术原理和实现机制"
    },
    {
      "label": "源码级别",
      "description": "分析源码实现，适合深度学习"
    }
  ],
  "multiSelect": false
}
```

## 第四阶段：后续优化

### 场景9：文章生成后的优化需求

**触发条件**：文章已生成，询问用户是否需要进一步优化

```json
{
  "question": "文章已生成完成！您是否需要进一步优化？",
  "header": "后续优化",
  "options": [
    {
      "label": "补充技术细节",
      "description": "添加更多技术实现细节和代码示例"
    },
    {
      "label": "添加使用案例",
      "description": "补充实际应用案例和最佳实践"
    },
    {
      "label": "对比分析",
      "description": "与同类项目进行对比分析"
    },
    {
      "label": "调整风格",
      "description": "调整文章风格或内容重点"
    }
  ],
  "multiSelect": true
}
```

### 场景10：确认输出格式

**触发条件**：用户可能需要不同格式的输出

```json
{
  "question": "您希望文章以什么格式输出？",
  "header": "输出格式",
  "options": [
    {
      "label": "Markdown",
      "description": "标准Markdown格式，适合博客和文档"
    },
    {
      "label": "HTML",
      "description": "HTML格式，适合网页展示"
    },
    {
      "label": "纯文本",
      "description": "纯文本格式，适合邮件或聊天分享"
    },
    {
      "label": "保持默认",
      "description": "使用默认的Markdown格式"
    }
  ],
  "multiSelect": false
}
```

## 特殊场景

### 场景11：批量分析确认

**触发条件**：用户提供多个仓库URL

```json
{
  "question": "您提供了多个仓库，希望如何处理？",
  "header": "批量处理",
  "options": [
    {
      "label": "分别生成",
      "description": "为每个仓库生成独立的推荐文章"
    },
    {
      "label": "对比分析",
      "description": "生成一篇对比分析文章"
    },
    {
      "label": "技术栈报告",
      "description": "生成整体技术栈分析报告"
    },
    {
      "label": "逐个处理",
      "description": "逐个处理，每个都询问详细需求"
    }
  ],
  "multiSelect": false
}
```

### 场景12：私有仓库处理

**触发条件**：用户提供的仓库是私有的

```json
{
  "question": "这个仓库似乎是私有的，无法直接访问。您希望如何处理？",
  "header": "私有仓库",
  "options": [
    {
      "label": "我提供信息",
      "description": "我会手动提供仓库的相关信息"
    },
    {
      "label": "使用公开信息",
      "description": "仅使用公开可访问的信息生成文章"
    },
    {
      "label": "跳过此仓库",
      "description": "跳过这个仓库，处理其他仓库"
    },
    {
      "label": "稍后重试",
      "description": "等我设置好访问权限后再试"
    }
  ],
  "multiSelect": false
}
```

## 提问最佳实践

### 1. 问题设计原则
- **清晰明确**：问题描述要清晰，避免歧义
- **选项互斥**：单选题的选项要互斥
- **覆盖全面**：选项要覆盖主要可能性
- **描述详细**：每个选项要有清晰的说明

### 2. 提问时机
- **需求不明确时**：在开始工作前确认需求
- **信息不足时**：在遇到信息缺失时及时询问
- **有多种选择时**：在有多种处理方式时让用户选择
- **完成后确认**：在完成阶段性工作后确认是否满足需求

### 3. 避免过度提问
- **批量问题**：将相关问题合并到一个问题中
- **默认选项**：提供合理的默认选项
- **跳过机制**：允许用户跳过非必要问题
- **智能推断**：能推断的就不要问

### 4. 问题顺序
1. 先问目的和受众（影响整体方向）
2. 再问内容重点（影响具体内容）
3. 最后问格式和风格（影响输出形式）

## 回答处理

### 单选回答处理
```python
if answer == "项目推荐":
    # 设置文章类型为推荐文章
    article_type = "recommendation"
elif answer == "技术分析":
    # 设置文章类型为技术分析
    article_type = "technical_analysis"
```

### 多选回答处理
```python
if "核心功能" in answers:
    # 添加功能特性章节
    include_features = True
if "技术架构" in answers:
    # 添加技术架构章节
    include_architecture = True
```

### 自定义回答处理
```python
if answer == "Other":
    # 获取用户自定义输入
    custom_input = user_custom_text
    # 处理自定义需求
```

## 提问示例对话

### 完整对话流程

**用户**：`https://github.com/facebook/react`

**系统**：
```
我注意到您提供了一个GitHub仓库链接，为了生成更符合您需求的文章，想确认一下您的具体需求是什么？

选项：
1. 项目推荐 - 生成适合技术博客分享的推荐文章
2. 技术分析 - 深入分析技术实现细节
3. 项目介绍 - 简洁的功能概述
4. 对比评测 - 与同类项目进行对比分析
```

**用户**：选择"项目推荐"

**系统**：
```
这篇文章主要面向哪类读者？

选项：
1. 开发者 - 包含技术细节、代码示例
2. 技术管理者 - 侧重技术选型、项目价值
3. 产品经理 - 侧重功能特性、业务价值
4. 普通用户 - 通俗易懂，侧重使用场景
```

**用户**：选择"开发者"

**系统**：
```
您希望文章重点介绍哪些方面？（可多选）

选项：
1. 核心功能 - 详细介绍主要功能和特性
2. 技术架构 - 深入分析技术实现
3. 使用场景 - 重点介绍适用场景
4. 快速上手 - 侧重安装配置指南
```

**用户**：选择"核心功能"和"快速上手"

**系统**：开始生成文章...