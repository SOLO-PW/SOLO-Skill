---
name: image-prompt-reverse
description: |
  AI图像提示词反推工具。分析用户上传的图片，生成精准的描述性提示词，支持输出多种主流AI绘图模型格式（Stable Diffusion、Midjourney、DALL-E 3、Flux、NijiJourney等），具备IP/品牌识别能力，支持交互式精调。当用户需要"反推图片提示词"、"分析图片生成提示词"、"图片转提示词"、"提取图片描述词"、"生成AI绘图提示词"时触发此技能。
---

# Image Prompt Reverse

## 概述

本技能用于分析用户上传的图片，生成精准、全面的AI绘图提示词。采用系统化分析方法，支持10+种主流AI绘图模型格式输出，具备IP/品牌识别能力，支持交互式精调，帮助用户在不同AI平台上复现类似效果的图像。

## 核心能力

1. **图片深度分析** - 系统化提取图片中的视觉元素，使用分层检查清单确保全面性
2. **场景专项识别** - 针对人物、动漫、风景、城市、静物、幻想等场景的专项分析
3. **多模型格式输出** - 适配10+种主流AI绘图模型的提示词格式
4. **智能提示词生成** - 基于场景类型自动生成最优提示词结构
5. **角色与IP识别** - 识别常见动漫角色、明星和知名IP品牌
6. **质量词推荐** - 自动推荐正向质量词和反向提示词
7. **交互式精调** - 支持用户指定区域重点分析和提示词微调

## 支持的AI绘图模型

| 模型 | 特点 | 适用场景 |
|------|------|----------|
| Stable Diffusion | 权重语法，高度可控 | 精细调整、专业创作 |
| Midjourney | 自然语言+参数 | 艺术风格、概念设计 |
| DALL-E 3 | 纯自然语言 | 商业应用、文字理解 |
| Flux | 自然语言+风格词 | 写实人像、高质量输出 |
| NijiJourney | 动漫专用 | 二次元、插画创作 |
| Leonardo.ai | 内置风格预设 | 快速原型、多种风格 |
| InvokeAI | 节点工作流 | 专业工作流、精细控制 |
| Playground AI | 滤镜风格 | 快速生成、风格探索 |
| Ideogram | 文字渲染 | 文字设计、海报创作 |

详细格式规范参见 [models.md](references/models.md)。

---

## 工作流程

### 快速流程（30秒）

```
1. 识别场景类型 → 2. 提取主体特征 → 3. 分析光影色彩 → 4. 生成提示词
```

### 完整流程

#### 步骤1: 接收图片

确认用户已上传图片。如果用户未上传图片，提示用户提供。

#### 步骤2: 场景类型识别

首先识别图片的场景类型，以确定分析重点：

| 场景类型 | 判断标准 | 分析重点 | 参考文档 |
|----------|----------|----------|----------|
| 人物肖像 | 人物占比>50% | 面部/表情/服装 | [pose.md](references/pose.md) |
| 动漫/二次元 | 线条清晰，大眼睛 | 角色/画风 | [character-recognition.md](references/character-recognition.md) |
| 风景/自然 | 自然景观为主 | 天气/光线/季节 | [nature.md](references/nature.md) |
| 城市/建筑 | 建筑结构 | 风格/材质/构图 | [architecture.md](references/architecture.md) |
| 静物/产品 | 单一物体 | 材质/光影/设计 | [material.md](references/material.md) |
| 美食 | 食物为主 | 摆盘/质感/氛围 | [food-photography.md](references/food-photography.md) |
| 动物 | 动物为主 | 品种/姿态/环境 | [animals.md](references/animals.md) |
| 车辆 | 车辆为主 | 类型/品牌/风格 | [vehicles.md](references/vehicles.md) |
| 科技产品 | 电子产品 | 设计/材质/风格 | [tech-products.md](references/tech-products.md) |
| 游戏 | 游戏相关 | 场景/角色/风格 | [gaming.md](references/gaming.md) |

详细场景识别参见 [scene-recognition.md](references/scene-recognition.md)。

#### 步骤3: 主体识别

根据场景类型，进行专项识别：

**人物图片**:
- 动漫角色识别 → [character-recognition.md](references/character-recognition.md)
- 明星/名人识别 → [celebrity-recognition.md](references/celebrity-recognition.md)
- IP/品牌识别 → [ip-brand-recognition.md](references/ip-brand-recognition.md)

**识别置信度**:

| 置信度 | 输出方式 |
|--------|----------|
| 高 | 直接说出角色/明星名 |
| 中 | "疑似为XX" |
| 低 | 不猜测，详细描述可见特征 |

#### 步骤4: 深度分析

使用五层分析法系统化分析：

```
第一层: 整体印象 - 风格、氛围、情绪基调
第二层: 主体内容 - 人物/物体特征、数量、位置
第三层: 环境背景 - 场景、地点、背景元素
第四层: 技术细节 - 光照、视角、构图、景深
第五层: 质量特征 - 分辨率、细节程度、画面质感
```

**分析参考文档**:

| 分析维度 | 参考文档 |
|----------|----------|
| 构图 | [composition.md](references/composition.md) |
| 色彩 | [color-palette.md](references/color-palette.md) |
| 光影 | [lighting.md](references/lighting.md) |
| 材质 | [material.md](references/material.md) |
| 镜头 | [camera-lens.md](references/camera-lens.md) |
| 天气 | [weather.md](references/weather.md) |
| 情绪 | [emotion.md](references/emotion.md) |
| 姿态 | [pose.md](references/pose.md) |
| 特效 | [effects.md](references/effects.md) |

**使用检查清单确保全面性**:

分析时必须参照 [precision-checklist.md](references/precision-checklist.md) 逐项检查。

#### 步骤5: 验证分析结果

**交叉验证规则**:
- 性别验证: 必须满足 服装特征 + (发型特征 或 面部特征)
- 风格验证: 必须满足至少2个风格特征一致
- 光照验证: 阴影方向 + 高光位置 + 光源方向必须一致

详细验证方法参见 [analysis-method.md](references/analysis-method.md)。

#### 步骤6: 生成提示词

**基于场景类型选择模板**:

根据识别的场景类型，使用 [prompt-templates.md](references/prompt-templates.md) 中的对应模板。

**提示词生成原则**:

```
[主体] → [特征] → [环境] → [光照] → [风格] → [技术] → [质量]
```

- 具体优于抽象: "flowing silver hair" > "nice hair"
- 可量化优于模糊: "35mm lens" > "normal lens"
- 按重要性排序，核心主体权重最高

**权重分配策略**:

| 元素类型 | SD权重 | MJ权重 | 说明 |
|----------|--------|--------|------|
| 核心主体 | 1.3-1.5 | ::3-5 | 最重要的识别特征 |
| 关键特征 | 1.2-1.3 | ::2-3 | 重要的外貌/特征描述 |
| 风格词 | 1.1-1.2 | ::1-2 | 艺术风格修饰 |
| 环境词 | 0.9-1.1 | ::0.5-1 | 背景环境描述 |
| 质量词 | 1.1-1.3 | 自然融入 | 质量增强词 |

#### 步骤7: 模型适配输出

**询问用户需要哪些模型的提示词格式**，或默认输出以下常用模型：

| 模型 | 特点 |
|------|------|
| Stable Diffusion | 权重语法，需质量词 |
| Midjourney | 参数语法，自然描述 |
| DALL-E 3 | 纯自然语言描述 |
| Flux | 自然语言+风格词 |
| NijiJourney | 动漫风格专用 |

**自动适配规则**:
1. **SD → Midjourney**: 移除权重语法，保留核心描述，添加参数
2. **SD → DALL-E 3**: 展开为完整句子，添加连接词，详细描述
3. **SD → Flux**: 简化权重，保留风格词，自然语言为主
4. **SD → NijiJourney**: 添加--niji参数，优化动漫描述

详细格式规范参见 [models.md](references/models.md)。

#### 步骤8: 输出质量词

自动生成配套的质量增强词和反向提示词。参见 [quality-words.md](references/quality-words.md)。

#### 步骤9: 交互式精调（可选）

初始提示词生成后，支持用户进行交互式精调：

**精调选项**:
- **区域指定分析**: 用户指定图片中的特定区域重点分析
- **元素精调**: 调整特定元素的描述方式
- **风格微调**: 调整整体风格方向
- **权重调整**: 修改元素权重分配
- **格式优化**: 针对特定模型优化输出格式

详细精调方法参见 [interactive-refinement.md](references/interactive-refinement.md)。

---

## 输出格式

### 标准输出模板

```markdown
## 📷 图片分析结果

### 整体描述
[一句话概括图片内容]

### 场景类型
[识别的场景类型]

### 详细分析
- **主体**: [主体描述]
- **角色/IP**: [识别到的角色名/明星名/IP品牌，或"未识别到"]
- **风格**: [艺术风格]
- **光照**: [光照类型]
- **视角**: [视角构图]
- **氛围**: [情绪氛围]

---

## 🎨 提示词输出

### Stable Diffusion
**正向提示词:**
```
[SD格式提示词]
```

**反向提示词:**
```
[反向提示词]
```

### Midjourney
```
[Midjourney格式提示词]
```

### DALL-E 3
```
[自然语言描述]
```

### Flux
```
[Flux格式提示词]
```

### NijiJourney
```
[NijiJourney格式提示词]
```

---

## ✨ 质量词推荐

### 正向质量词
```
[推荐的质量增强词]
```

### 反向提示词模板
```
[通用反向提示词]
```
```

---

## 提示词编写原则

### 精准描述

- **具体优于抽象**: 使用"flowing silver hair"而非"nice hair"
- **可量化优于模糊**: 使用"35mm lens"而非"normal lens"
- **专业术语**: 使用"chiaroscuro lighting"而非"dramatic lighting"
- **避免主观**: 不描述"beautiful"，而是描述"symmetrical facial features"

### 长度建议

| 模型 | 推荐长度 |
|------|----------|
| Stable Diffusion | 50-150 tokens |
| Midjourney | 30-80 words |
| DALL-E 3 | 100-400 words |
| Flux | 50-150 words |
| NijiJourney | 30-80 words |

### 不确定性处理

当无法确定某些特征时：
- **性别不确定**: 使用"a person"或"androgynous appearance"
- **年龄不确定**: 使用"young adult"
- **细节不清**: 标注"细节模糊，可能为..."
- **遮挡严重**: 标注"部分被遮挡，可见..."

---

## 常见错误预防

### 性别误认预防

**高风险场景**: 动漫风格人物、中性服装、背影/侧影

**预防措施**:
1. 优先查看服装（裙子/西装等决定性特征）
2. 多重特征交叉验证（服装+发型+配饰）
3. 不确定时使用中性描述（"a person"）

详细指南参见 [gender-identification.md](references/gender-identification.md)。

### 风格误判预防

**易混淆风格**: 3D渲染vs照片写实、油画vs数字绘画、动漫vs卡通

**预防措施**:
1. 查看纹理细节（笔触、像素、光滑度）
2. 检查边缘处理方式
3. 观察光影的物理准确性

详细指南参见 [art-styles.md](references/art-styles.md)。

---

## 参考资源快速索引

### 按分析阶段

| 阶段 | 文档 | 说明 |
|------|------|------|
| 场景识别 | [scene-recognition.md](references/scene-recognition.md) | 场景类型判断 |
| 主体识别 | [character-recognition.md](references/character-recognition.md) | 动漫角色识别 |
| 主体识别 | [celebrity-recognition.md](references/celebrity-recognition.md) | 明星名人识别 |
| 主体识别 | [ip-brand-recognition.md](references/ip-brand-recognition.md) | IP品牌识别 |
| 深度分析 | [analysis-method.md](references/analysis-method.md) | 分析方法论 |
| 深度分析 | [precision-checklist.md](references/precision-checklist.md) | 检查清单 |
| 提示词生成 | [prompt-templates.md](references/prompt-templates.md) | 提示词模板 |
| 模型适配 | [models.md](references/models.md) | 模型格式规范 |
| 质量优化 | [quality-words.md](references/quality-words.md) | 质量词库 |

### 按视觉元素

| 元素 | 文档 | 说明 |
|------|------|------|
| 构图 | [composition.md](references/composition.md) | 构图法则分析 |
| 色彩 | [color-palette.md](references/color-palette.md) | 色彩搭配分析 |
| 光影 | [lighting.md](references/lighting.md) | 光影效果分析 |
| 材质 | [material.md](references/material.md) | 材质纹理识别 |
| 镜头 | [camera-lens.md](references/camera-lens.md) | 镜头语言分析 |
| 天气 | [weather.md](references/weather.md) | 天气氛围分析 |
| 情绪 | [emotion.md](references/emotion.md) | 情绪氛围分析 |
| 姿态 | [pose.md](references/pose.md) | 人物姿态分析 |
| 特效 | [effects.md](references/effects.md) | 后期特效分析 |

### 按专业领域

| 领域 | 文档 | 说明 |
|------|------|------|
| 人像 | [fashion.md](references/fashion.md) | 时尚穿搭分析 |
| 人像 | [gender-identification.md](references/gender-identification.md) | 性别识别指南 |
| 美食 | [food-photography.md](references/food-photography.md) | 美食摄影分析 |
| 室内 | [interior-design.md](references/interior-design.md) | 室内设计分析 |
| 建筑 | [architecture.md](references/architecture.md) | 建筑风格分析 |
| 风景 | [nature.md](references/nature.md) | 自然景观分析 |
| 动物 | [animals.md](references/animals.md) | 宠物动物分析 |
| 车辆 | [vehicles.md](references/vehicles.md) | 车辆交通分析 |
| 运动 | [sports.md](references/sports.md) | 运动场景分析 |
| 音乐 | [music.md](references/music.md) | 音乐乐器分析 |
| 演出 | [performance.md](references/performance.md) | 舞台演出分析 |
| 游戏 | [gaming.md](references/gaming.md) | 游戏场景分析 |
| 科技 | [tech-products.md](references/tech-products.md) | 科技产品分析 |
| 艺术 | [art-styles.md](references/art-styles.md) | 艺术风格分析 |

### 辅助功能

| 功能 | 文档 | 说明 |
|------|------|------|
| 提示词解释 | [prompt-explanation.md](references/prompt-explanation.md) | 解释提示词含义 |
| 交互精调 | [interactive-refinement.md](references/interactive-refinement.md) | 提示词微调 |
