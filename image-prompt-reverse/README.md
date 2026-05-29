# Image Prompt Reverse — AI 图像提示词反推工具

> 分析用户上传的图片，生成精准、可复现的 AI 绘图提示词，支持 10+ 种主流模型格式输出。

---

## 功能特性

- **图片深度分析** — 采用五层分析法，从整体印象到技术细节系统化提取视觉元素
- **场景专项识别** — 针对人物、动漫、风景、城市、静物、美食、动物等场景的专项分析
- **多模型格式输出** — 一键适配 Stable Diffusion、Midjourney、DALL-E 3、Flux、NijiJourney 等 10+ 种主流 AI 绘图模型
- **角色与IP识别** — 识别常见动漫角色、明星和知名IP品牌
- **构图分析** — 深度分析三分法、黄金分割、对称性等构图细节
- **色彩分析** — 提取主色调、配色方案、色彩和谐度
- **交互式精调** — 支持用户指定区域重点分析和提示词微调
- **提示词解释** — 为每个关键提示词提供含义、作用和视觉效果解释
- **质量词推荐** — 自动生成配套正向质量词和反向提示词

---

## 支持的 AI 模型

| 模型 | 特点 | 适用场景 |
|------|------|----------|
| Stable Diffusion | 权重语法，高度可控 | 精细调整、专业创作 |
| Stable Diffusion 3 | 自然语言，T5编码器 | 高质量写实，复杂场景 |
| Midjourney | 自然语言 + 参数 | 艺术风格、概念设计 |
| DALL-E 3 | 纯自然语言 | 商业应用、文字理解 |
| Flux | 自然语言 + 风格词 | 写实人像、高质量输出 |
| NijiJourney | 动漫专用 | 二次元、插画创作 |
| Leonardo.ai | 内置风格预设 | 快速原型、多种风格 |
| InvokeAI | 节点工作流 | 专业工作流、精细控制 |
| Playground AI | 滤镜风格 | 快速生成、风格探索 |
| Ideogram | 文字渲染 | 文字设计、海报创作 |

---

## 快速开始

### 基本用法

直接上传图片并告诉 Agent 你的需求：

> "帮我反推这张图片的提示词"

> "分析这张图，生成 Stable Diffusion 和 Midjourney 的提示词"

> "提取这张动漫图的角色描述词"

### 工作流程

```
上传图片 → 场景识别 → 主体分析 → 深度分析 → 生成提示词 → 模型适配 → 质量词推荐
```

**30秒快速流程**:
1. 识别场景类型（人物/风景/动漫/产品等）
2. 提取主体特征（外观/姿态/表情）
3. 分析光影色彩（光源/色调/氛围）
4. 生成提示词（按模板组织）

---

## 支持的场景类型

| 场景类型 | 分析重点 | 参考文档 |
|----------|----------|----------|
| 人物肖像 | 面部/表情/服装/姿态 | [pose.md](references/pose.md) |
| 动漫/二次元 | 角色/画风/特征 | [character-recognition.md](references/character-recognition.md) |
| 风景/自然 | 天气/光线/季节 | [nature.md](references/nature.md) |
| 城市/建筑 | 风格/材质/构图 | [architecture.md](references/architecture.md) |
| 美食 | 摆盘/质感/氛围 | [food-photography.md](references/food-photography.md) |
| 动物 | 品种/姿态/环境 | [animals.md](references/animals.md) |
| 车辆 | 类型/品牌/风格 | [vehicles.md](references/vehicles.md) |
| 科技产品 | 设计/材质/风格 | [tech-products.md](references/tech-products.md) |
| 游戏 | 场景/角色/风格 | [gaming.md](references/gaming.md) |
| 音乐 | 乐器/演奏/氛围 | [music.md](references/music.md) |
| 演出 | 舞台/灯光/表演 | [performance.md](references/performance.md) |
| 时尚 | 服装/配饰/风格 | [fashion.md](references/fashion.md) |
| 室内 | 设计/家具/软装 | [interior-design.md](references/interior-design.md) |

---

## 参考文档

### 核心分析方法

| 文档 | 说明 |
|------|------|
| [SKILL.md](SKILL.md) | 技能主定义文件，包含完整工作流程和触发条件 |
| [references/analysis-method.md](references/analysis-method.md) | 图片分析方法论（五层分析法、描述词选择原则） |
| [references/precision-checklist.md](references/precision-checklist.md) | 精准分析检查清单 |
| [references/gender-identification.md](references/gender-identification.md) | 性别识别精准指南 |

### 场景与主体识别

| 文档 | 说明 |
|------|------|
| [references/scene-recognition.md](references/scene-recognition.md) | 场景识别专项指南 |
| [references/character-recognition.md](references/character-recognition.md) | 动漫角色识别指南（含2023-2025热门角色） |
| [references/celebrity-recognition.md](references/celebrity-recognition.md) | 明星/名人识别指南 |
| [references/ip-brand-recognition.md](references/ip-brand-recognition.md) | IP/品牌识别指南 |
| [references/animals.md](references/animals.md) | 宠物动物分析专项指南 |
| [references/vehicles.md](references/vehicles.md) | 车辆交通分析专项指南 |

### 视觉元素分析

| 文档 | 说明 |
|------|------|
| [references/composition.md](references/composition.md) | 构图分析专项指南 |
| [references/color-palette.md](references/color-palette.md) | 色彩分析专项指南 |
| [references/lighting.md](references/lighting.md) | 光影效果专项指南 |
| [references/material.md](references/material.md) | 材质识别专项指南 |
| [references/camera-lens.md](references/camera-lens.md) | 镜头语言专项指南 |
| [references/weather.md](references/weather.md) | 天气氛围专项指南 |
| [references/emotion.md](references/emotion.md) | 情绪氛围专项指南 |
| [references/pose.md](references/pose.md) | 人物姿态专项指南 |
| [references/effects.md](references/effects.md) | 特效后期专项指南 |

### 专业领域分析

| 文档 | 说明 |
|------|------|
| [references/food-photography.md](references/food-photography.md) | 美食摄影分析专项指南 |
| [references/interior-design.md](references/interior-design.md) | 室内设计分析专项指南 |
| [references/fashion.md](references/fashion.md) | 时尚穿搭分析专项指南 |
| [references/sports.md](references/sports.md) | 运动场景分析专项指南 |
| [references/architecture.md](references/architecture.md) | 建筑风格分析专项指南 |
| [references/art-styles.md](references/art-styles.md) | 艺术风格分析专项指南 |
| [references/nature.md](references/nature.md) | 自然景观分析专项指南 |
| [references/tech-products.md](references/tech-products.md) | 科技产品分析专项指南 |
| [references/music.md](references/music.md) | 音乐乐器分析专项指南 |
| [references/performance.md](references/performance.md) | 舞台演出分析专项指南 |
| [references/gaming.md](references/gaming.md) | 游戏场景分析专项指南 |

### 提示词生成

| 文档 | 说明 |
|------|------|
| [references/prompt-templates.md](references/prompt-templates.md) | 提示词生成策略与模板 |
| [references/models.md](references/models.md) | 各模型提示词格式详细规范（含SD3） |
| [references/quality-words.md](references/quality-words.md) | 质量词库和反向提示词 |
| [references/prompt-explanation.md](references/prompt-explanation.md) | 提示词解释功能指南 |
| [references/interactive-refinement.md](references/interactive-refinement.md) | 交互式精调功能指南 |

---

## 提示词编写原则

- **具体优于抽象**："flowing silver hair" > "nice hair"
- **可量化优于模糊**："35mm lens" > "normal lens"
- **专业术语增强准确性**："chiaroscuro lighting" > "dramatic lighting"
- **避免主观描述**：不描述 "beautiful"，而是描述 "symmetrical facial features"

### 权重分配建议

| 元素类型 | SD权重 | MJ权重 | 说明 |
|----------|--------|--------|------|
| 核心主体 | 1.3-1.5 | ::3-5 | 最重要的识别特征 |
| 关键特征 | 1.2-1.3 | ::2-3 | 重要的外貌/特征描述 |
| 风格词 | 1.1-1.2 | ::1-2 | 艺术风格修饰 |
| 环境词 | 0.9-1.1 | ::0.5-1 | 背景环境描述 |
| 质量词 | 1.1-1.3 | 自然融入 | 质量增强词 |

### 提示词长度建议

| 模型 | 推荐长度 |
|------|----------|
| Stable Diffusion | 50-150 tokens |
| Midjourney | 30-80 words |
| DALL-E 3 | 100-400 words |
| Flux | 50-150 words |
| NijiJourney | 30-80 words |

---

## 常见问题

### 如何提高提示词准确性？

1. **使用具体描述**：避免"beautiful"等主观词汇，使用"symmetrical facial features"等客观描述
2. **交叉验证特征**：确保描述的特征在图片中都能看到
3. **参考检查清单**：使用 [precision-checklist.md](references/precision-checklist.md) 确保全面性

### 如何处理不确定的特征？

- **性别不确定**：使用"a person"或"androgynous appearance"
- **年龄不确定**：使用"young adult"
- **细节不清**：标注"细节模糊，可能为..."
- **遮挡严重**：标注"部分被遮挡，可见..."

### 如何针对特定模型优化？

- **Stable Diffusion**：使用权重语法`(word:1.2)`，添加反向提示词
- **Midjourney**：添加参数`--ar 16:9 --v 6 --s 250`
- **DALL-E 3**：使用自然语言，详细描述场景
- **Flux**：简化权重，保留风格词

---

*本技能遵循系统化分析方法，通过分层检查清单确保分析全面性，具备IP/品牌识别能力，支持交互式精调，帮助用户在不同AI平台上复现类似效果的图像。*
