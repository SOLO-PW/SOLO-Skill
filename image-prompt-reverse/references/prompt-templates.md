# 提示词生成策略与模板

本文档提供系统化的提示词生成策略和各类场景的专用模板，帮助生成更精准、可复现的AI绘图提示词。

---

## 目录

1. [提示词生成策略](#提示词生成策略)
2. [人物肖像模板](#人物肖像模板)
3. [动漫角色模板](#动漫角色模板)
4. [风景摄影模板](#风景摄影模板)
5. [城市建筑模板](#城市建筑模板)
6. [静物产品模板](#静物产品模板)
7. [幻想科幻模板](#幻想科幻模板)
8. [多模型适配策略](#多模型适配策略)

---

## 提示词生成策略

### 核心原则

**1. 结构化组织**
```
[主体] → [特征] → [环境] → [光照] → [风格] → [技术] → [质量]
```

**2. 重要性排序**
- 核心主体（最高权重）
- 关键特征（高权重）
- 环境背景（中权重）
- 风格修饰（中权重）
- 技术参数（低权重）
- 质量词（默认权重）

**3. 精准描述原则**
- 使用具体可量化的描述
- 避免主观形容词
- 使用专业术语
- 保持描述一致性

### 提示词优化流程

```
Step 1: 提取核心元素
  └─ 确定主体、风格、关键特征

Step 2: 构建基础描述
  └─ 按结构组织基础提示词

Step 3: 添加细节修饰
  └─ 补充特征细节、环境描述

Step 4: 优化权重分配
  └─ 为核心元素添加权重

Step 5: 添加质量词
  └─ 补充正向质量词和反向提示词

Step 6: 模型适配调整
  └─ 根据目标模型调整格式
```

### 权重分配策略

| 元素类型 | SD权重 | MJ权重 | 说明 |
|----------|--------|--------|------|
| 核心主体 | 1.3-1.5 | ::3-5 | 最重要的识别特征 |
| 关键特征 | 1.2-1.3 | ::2-3 | 重要的外貌/特征描述 |
| 风格词 | 1.1-1.2 | ::1-2 | 艺术风格修饰 |
| 环境词 | 0.9-1.1 | ::0.5-1 | 背景环境描述 |
| 质量词 | 1.1-1.3 | 自然融入 | 质量增强词 |

---

## 人物肖像模板

### 基础模板结构

```
[镜头] portrait of a [年龄] [性别] with [面部特征], [发型], wearing [服装], [表情], [姿态], [光照], [背景], [摄影风格], [质量词]
```

### 各模型格式

**Stable Diffusion:**
```
(85mm portrait:1.3) of a (young woman:1.2) with (symmetrical facial features:1.2), (long flowing auburn hair:1.1), wearing (elegant black dress:1.1), (gentle smile:1.1), (three-quarter view:1.0), (soft natural lighting from window:1.2), (blurred bokeh background:0.9), (professional photography:1.1), 8k, highly detailed, sharp focus, masterpiece

Negative: (worst quality:1.4), (low quality:1.4), (normal quality:1.4), bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, jpeg artifacts, signature, watermark, username, blurry
```

**Midjourney:**
```
85mm portrait of a young woman with symmetrical facial features, long flowing auburn hair, wearing elegant black dress, gentle smile, soft natural lighting from window, blurred bokeh background, professional photography, 8k, highly detailed --ar 2:3 --v 6 --s 250
```

**DALL-E 3:**
```
A professional 85mm portrait photograph of a young woman with symmetrical facial features and long flowing auburn hair. She is wearing an elegant black dress and has a gentle smile. The lighting is soft and natural, coming from a window to the side. The background is beautifully blurred with creamy bokeh. The image is shot in professional photography style with high detail and sharp focus.
```

**Flux:**
```
Professional portrait photography, 85mm lens, young woman with symmetrical features and flowing auburn hair, elegant black dress, gentle smile, soft window light, creamy bokeh background, photorealistic, 8k, highly detailed
```

### 人像细分模板

**时尚人像:**
```
[时尚风格] fashion portrait of a [模特描述], wearing [设计师服装], [夸张造型], [艺术光影], [时尚摄影风格], [杂志质感]

示例:
High fashion editorial portrait of a young Asian model, wearing avant-garde designer gown with dramatic silhouette, bold makeup with graphic eyeliner, dramatic side lighting creating strong shadows, Vogue magazine style, high-end fashion photography
```

**商业人像:**
```
Professional headshot of a [职业] [性别], wearing [商务着装], [自信表情], [专业布光], [中性背景], [企业形象风格]

示例:
Professional corporate headshot of a middle-aged businessman, wearing navy blue suit with white shirt and red tie, confident friendly smile, professional three-point lighting, neutral gray background, corporate photography style
```

---

## 动漫角色模板

### 基础模板结构

```
[风格] anime [角色类型] with [发型], [眼睛], [面部特征], wearing [服装], [表情], [姿势], [背景], [艺术风格], [质量词]
```

### 各模型格式

**Stable Diffusion:**
```
(Studio Ghibli style:1.3) anime girl with (long pink twin tails:1.2), (large expressive green eyes:1.2), (wearing school uniform with red ribbon:1.1), (cheerful expression:1.1), (standing pose:1.0), (cherry blossom background:1.0), soft pastel colors, detailed anime illustration, masterpiece, best quality

Negative: (worst quality:1.4), (low quality:1.4), bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, jpeg artifacts, signature, watermark, username, blurry, bad proportions, deformed
```

**Midjourney:**
```
Studio Ghibli style anime girl character, long pink twin tails, large expressive green eyes, wearing Japanese school uniform with red ribbon, cheerful expression, standing pose, cherry blossom petals falling in background, soft pastel colors, detailed anime illustration --ar 2:3 --niji 6 --style cute
```

**DALL-E 3:**
```
A Studio Ghibli style anime illustration of a young girl character with long pink hair styled in twin tails and large expressive green eyes. She is wearing a Japanese school uniform with a red ribbon tie. She has a cheerful expression and is standing in a relaxed pose. Cherry blossom petals are falling around her in the background. The art style features soft pastel colors and the characteristic warm, whimsical aesthetic of Studio Ghibli animation.
```

**NijiJourney:**
```
Beautiful anime girl, long pink twin tails, large green eyes, school uniform with red ribbon, cheerful smile, cherry blossom background, soft lighting, pastel colors, detailed illustration --niji 6 --ar 2:3 --style cute
```

### 动漫风格细分

**赛博朋克风格:**
```
Cyberpunk anime character with [科技特征], [霓虹光照], [未来城市背景], [科幻元素]

示例:
Cyberpunk anime girl with cybernetic eye implant and glowing blue circuit patterns on skin, short silver hair with neon blue highlights, wearing futuristic tactical outfit, serious expression, standing on rainy neon-lit street with holographic advertisements, blade runner aesthetic, neon color palette
```

**奇幻风格:**
```
Fantasy anime [角色职业] with [魔法元素], [奇幻服装], [神秘背景], [魔法效果]

示例:
Fantasy anime mage girl with long white hair and glowing purple eyes, wearing elaborate magical robes with star patterns, holding staff with glowing crystal, floating magical runes around her, mystical forest background with ethereal lighting, detailed fantasy illustration
```

---

## 风景摄影模板

### 基础模板结构

```
[时间] [季节] landscape of [地点], [天气], [前景], [中景], [背景], [光照], [色彩], [摄影风格], [质量词]
```

### 各模型格式

**Stable Diffusion:**
```
(golden hour:1.3) (autumn landscape:1.2) of (mountain lake:1.2), (clear sky with few clouds:1.0), (colorful fallen leaves in foreground:1.1), (crystal clear lake reflection:1.2), (distant snow-capped mountains:1.1), (warm side lighting:1.2), (rich orange and gold tones:1.1), panoramic view, landscape photography, 8k, photorealistic, highly detailed

Negative: (worst quality:1.4), (low quality:1.4), blurry, grainy, oversaturated, underexposed, overexposed, watermark, text
```

**Midjourney:**
```
Golden hour autumn landscape of mountain lake, clear sky with scattered clouds, colorful fallen maple leaves in foreground, crystal clear lake with perfect reflection, distant snow-capped mountains, warm golden side lighting, rich orange and gold color palette, panoramic landscape photography, 8k, photorealistic --ar 16:9 --v 6 --s 250
```

**DALL-E 3:**
```
A breathtaking golden hour autumn landscape photograph of a serene mountain lake. The foreground is covered with colorful fallen maple leaves in vibrant oranges, reds, and golds. The crystal-clear lake creates a perfect mirror reflection of the scene. In the background, majestic snow-capped mountains rise against a clear sky with scattered clouds. The warm golden side lighting creates a magical atmosphere with rich orange and gold tones throughout the scene. Shot as a panoramic landscape in photorealistic style with exceptional detail.
```

**Flux:**
```
Golden hour landscape photography, autumn mountain lake scene, colorful fallen leaves foreground, crystal clear reflective water, distant snow-capped peaks, warm golden lighting, rich autumn colors, panoramic composition, photorealistic, 8k, highly detailed
```

### 风景细分模板

**海景:**
```
[时间] seascape with [海洋状态], [天空状况], [海岸特征], [光照], [氛围]

示例:
Dramatic sunset seascape with crashing waves on rocky coastline, stormy sky with dramatic clouds breaking to reveal golden sunlight, sea spray and mist, long exposure silky water effect, powerful and moody atmosphere, professional landscape photography
```

**森林:**
```
[季节] forest scene with [树木类型], [光照条件], [地面植被], [氛围]

示例:
Misty morning forest scene with towering redwood trees, sunbeams filtering through dense canopy creating god rays, lush ferns covering forest floor, ethereal and peaceful atmosphere, soft diffused lighting, nature photography
```

---

## 城市建筑模板

### 基础模板结构

```
[时间] cityscape of [城市类型], [建筑特征], [光源], [天气/氛围], [视角], [技术], [风格], [质量词]
```

### 各模型格式

**Stable Diffusion:**
```
(night cityscape:1.3) of (cyberpunk metropolis:1.2), (towering skyscrapers with glass facades:1.2), (neon signs and street lights:1.1), (reflecting on wet pavement:1.1), (light rain creating atmospheric haze:1.0), (street level perspective:1.1), (long exposure light trails:1.0), blade runner aesthetic, cinematic composition, 8k, highly detailed

Negative: (worst quality:1.4), (low quality:1.4), blurry, grainy, oversaturated, underexposed, overexposed, watermark, text, bad architecture
```

**Midjourney:**
```
Night cityscape of cyberpunk metropolis, towering futuristic skyscrapers with illuminated glass facades, vibrant neon signs in multiple colors, wet streets reflecting city lights, light rain creating atmospheric haze and light blooms, street level perspective, long exposure light trails from passing vehicles, blade runner aesthetic, cinematic composition, dramatic lighting --ar 16:9 --v 6 --s 250
```

**DALL-E 3:**
```
A dramatic night cityscape of a futuristic cyberpunk metropolis. Towering skyscrapers with illuminated glass facades dominate the skyline, covered in vibrant neon signs displaying advertisements in multiple colors. The wet streets below reflect the kaleidoscope of city lights. Light rain creates an atmospheric haze with beautiful light blooms. Shot from street level perspective with long exposure capturing light trails from passing vehicles. The aesthetic is reminiscent of Blade Runner with cinematic composition and dramatic lighting.
```

### 建筑细分模板

**古典建筑:**
```
[角度] view of [建筑风格] [建筑类型], [建筑细节], [光照], [环境], [摄影风格]

示例:
Low angle view of Gothic cathedral architecture, intricate stone carvings and pointed arches, flying buttresses, stained glass windows, dramatic sunset lighting creating warm golden glow on stone facade, surrounded by historic European cityscape, architectural photography
```

**现代建筑:**
```
[视角] of modern [建筑类型], [材料特征], [设计特点], [环境], [摄影风格]

示例:
Dramatic upward perspective of modern glass skyscraper, reflective glass facade mirroring blue sky and clouds, sleek geometric design with clean lines, surrounded by contemporary urban plaza, minimalist architectural photography
```

---

## 静物产品模板

### 基础模板结构

```
[布光类型] product photography of [产品], [材质特征], [颜色], [背景], [构图], [摄影风格], [质量词]
```

### 各模型格式

**Stable Diffusion:**
```
(professional studio lighting:1.2) product photography of (vintage leather handbag:1.3), (rich brown textured leather:1.2), (brass hardware details:1.1), (neutral gray background:1.0), (three-quarter angle:1.1), (soft shadows:1.0), commercial photography style, 8k, highly detailed, sharp focus

Negative: (worst quality:1.4), (low quality:1.4), blurry, grainy, bad lighting, harsh shadows, overexposed, underexposed, watermark, text
```

**Midjourney:**
```
Professional studio product photography of vintage leather handbag, rich textured brown leather with natural grain, brass hardware and buckle details, neutral gray seamless background, three-quarter angle view, soft studio lighting with gentle shadows, commercial photography style, 8k, highly detailed --ar 1:1 --v 6
```

**DALL-E 3:**
```
A professional studio product photograph of a vintage leather handbag. The bag is crafted from rich textured brown leather with visible natural grain patterns. Brass hardware and buckle details add elegant accents. Shot against a neutral gray seamless background from a three-quarter angle. Soft studio lighting creates gentle shadows that emphasize the leather texture and bag structure. Commercial photography style with exceptional detail and sharp focus.
```

### 静物细分模板

**食物摄影:**
```
[风格] food photography of [菜品], [摆盘], [光线], [背景], [氛围]

示例:
Rustic food photography of gourmet burger with melted cheese and fresh vegetables, artisanal wooden board presentation, natural window light from side, dark textured background, steam rising from hot food, appetizing and delicious appearance, professional food photography
```

**珠宝摄影:**
```
[布光] jewelry photography of [珠宝类型], [材质], [设计], [背景], [效果]

示例:
Dramatic jewelry photography of diamond necklace, sparkling brilliant-cut diamonds in platinum setting, black reflective background creating mirror effect, focused lighting creating spectacular fire and brilliance, luxury jewelry advertisement style
```

---

## 幻想科幻模板

### 科幻场景模板

**赛博朋克:**
```
Cyberpunk [场景类型] with [科技元素], [光照], [氛围], [细节]

SD:
(cyberpunk street scene:1.3) with (flying vehicles:1.2), (holographic advertisements:1.1), (neon lights in pink and blue:1.2), (rainy night:1.1), (steam rising from vents:1.0), (distant futuristic skyline:1.1), blade runner aesthetic, cinematic lighting, 8k, highly detailed

MJ:
Cyberpunk street scene with flying vehicles and hovering drones, massive holographic advertisements covering buildings, vibrant neon lights in pink and cyan, rainy night with wet streets reflecting lights, steam rising from street vents, distant futuristic skyline with towering skyscrapers, blade runner aesthetic, cinematic lighting --ar 16:9 --v 6
```

**太空科幻:**
```
[类型] space scene with [天体], [飞船/空间站], [光照], [氛围]

SD:
(epic space scene:1.3) with (distant galaxy and nebula:1.2), (massive space station:1.2), (Earth visible in background:1.1), (dramatic rim lighting:1.2), (stars and cosmic dust:1.0), sci-fi concept art style, cinematic composition, 8k, highly detailed

MJ:
Epic space scene with colorful distant galaxy and purple nebula, massive ring-shaped space station in foreground, Earth visible in background with atmosphere glow, dramatic rim lighting from distant star, countless stars and cosmic dust, sci-fi concept art style, cinematic composition --ar 21:9 --v 6
```

### 奇幻场景模板

**西方奇幻:**
```
Fantasy [场景] with [魔法元素], [生物], [环境], [氛围]

SD:
(epic fantasy landscape:1.3) with (floating islands:1.2), (ancient magical castle:1.2), (dragons flying in sky:1.1), (waterfalls flowing upward:1.1), (magical aurora in sky:1.0), (lush impossible vegetation:1.0), fantasy concept art, dramatic lighting, 8k, masterpiece

MJ:
Epic fantasy landscape with floating islands connected by rope bridges, ancient magical castle perched on largest island, dragons flying between islands, waterfalls flowing upward defying gravity, magical aurora lighting the sky, lush impossible vegetation with giant flowers, fantasy concept art style --ar 16:9 --v 6
```

---

## 多模型适配策略

### 模型特性对比

| 特性 | Stable Diffusion | Midjourney | DALL-E 3 | Flux | NijiJourney |
|------|------------------|------------|----------|------|-------------|
| 语法 | 权重语法 | 自然+参数 | 纯自然语言 | 自然+风格 | 自然+参数 |
| 长度 | 50-150 tokens | 30-80 words | 100-400 words | 50-150 words | 30-80 words |
| 质量词 | 必需 | 可选 | 内置 | 可选 | 可选 |
| 反向提示 | 必需 | --no参数 | 不支持 | 可选 | --no参数 |
| 风格控制 | 权重调节 | --s参数 | 描述控制 | 风格词 | --style参数 |

### 自动适配规则

**从SD格式转换:**

1. **转Midjourney:**
   - 移除权重语法
   - 保留核心描述词
   - 添加--ar、--v、--s参数
   - 反向提示转为--no

2. **转DALL-E 3:**
   - 展开为完整句子
   - 添加连接词和修饰语
   - 保持自然语言流畅性
   - 详细描述视觉效果

3. **转Flux:**
   - 简化权重语法
   - 保留关键风格词
   - 自然语言为主
   - 适当添加质量词

4. **转NijiJourney:**
   - 添加--niji参数
   - 选择合适--style
   - 优化动漫相关描述
   - 简化复杂修饰

### 提示词优化检查清单

生成提示词后检查：

- [ ] 核心主体描述是否清晰具体
- [ ] 关键特征是否包含足够细节
- [ ] 权重分配是否合理（核心>次要）
- [ ] 质量词是否适合目标模型
- [ ] 反向提示词是否针对性强
- [ ] 整体长度是否符合模型建议
- [ ] 描述是否存在矛盾
- [ ] 是否避免了主观形容词

---

## 提示词解释功能指南（并入自 prompt-explanation.md）

> 提示词编写方法与术语解释同属「提示词」主题，故合并至此文档。本节提供提示词解释的工作流程和方法，帮助理解每个提示词的作用和意义。

### 功能概述

#### 什么是提示词解释

提示词解释是指在输出提示词的同时，为每个关键提示词提供：
- **含义说明**: 这个词具体指什么
- **作用解释**: 为什么要用这个词
- **视觉效果**: 这个词会产生什么视觉效果
- **权重建议**: 这个词应该给多少权重

#### 适用场景

| 场景 | 说明 |
|------|------|
| 学习阶段 | 帮助新手理解提示词含义 |
| 精调阶段 | 理解每个词的作用以便调整 |
| 复现阶段 | 理解关键元素以便在其他平台复现 |
| 优化阶段 | 理解权重分配的原因 |

### 解释维度

#### 单词解释维度

| 维度 | 说明 | 示例 |
|------|------|------|
| 含义 | 这个词是什么意思 | "bokeh: 焦外虚化效果" |
| 作用 | 为什么用这个词 | "用于突出主体，模糊背景" |
| 效果 | 产生什么视觉效果 | "使背景光点变成柔和的圆形光斑" |
| 权重 | 建议权重及原因 | "权重1.1-1.3，因为它增强氛围但不是核心元素" |

#### 组合解释维度

| 维度 | 说明 | 示例 |
|------|------|------|
| 整体结构 | 提示词的组织逻辑 | "按主体→特征→环境→光照→风格组织" |
| 元素关系 | 各元素之间的关联 | "服装与风格相呼应，光照与氛围配合" |
| 权重逻辑 | 权重分配的原因 | "核心主体权重最高，背景最低" |
| 风格统一 | 风格描述的一致性 | "所有风格词都指向电影感写实风格" |

### 解释格式

#### 行内解释格式

在提示词后面直接添加解释：

```
提示词: beautiful woman (美丽女性), long silver hair (银色长发), wearing elegant dress (穿着优雅连衣裙)
```

#### 分段解释格式

将提示词拆解后逐段解释：

```
### 主体描述
- **beautiful woman**: 核心主体，描述人物性别和外貌
- **long silver hair**: 关键特征，银色长发增加视觉辨识度

### 服装描述
- **wearing elegant dress**: 服装风格，优雅连衣裙定义整体气质
```

#### 表格解释格式

用表格展示每个词的解释：

| 提示词 | 中文 | 类型 | 作用 | 建议权重 |
|--------|------|------|------|----------|
| beautiful woman | 美丽女性 | 主体 | 核心主体描述 | 1.3-1.5 |
| long silver hair | 银色长发 | 特征 | 增加视觉辨识度 | 1.2-1.3 |
| elegant dress | 优雅连衣裙 | 服装 | 定义整体风格 | 1.1-1.2 |

### 常用提示词解释库

#### 主体描述词

| 提示词 | 含义 | 作用 | 视觉效果 |
|--------|------|------|----------|
| beautiful | 美丽的 | 描述外貌吸引力 | 面容姣好，五官协调 |
| handsome | 英俊的 | 男性外貌吸引力 | 面部轮廓分明，气质佳 |
| young | 年轻的 | 年龄特征 | 皮肤光滑，面部饱满 |
| elegant | 优雅的 | 气质描述 | 姿态端庄，举止优雅 |
| mysterious | 神秘的 | 氛围描述 | 表情深邃，氛围神秘 |

#### 发型描述词

| 提示词 | 含义 | 作用 | 视觉效果 |
|--------|------|------|----------|
| flowing | 飘逸的 | 头发动态 | 头发随风飘动，有动感 |
| silky | 丝滑的 | 头发质感 | 头发光泽柔顺 |
| wavy | 波浪卷 | 发型形状 | 自然的波浪卷发 |
| braided | 编织的 | 发型样式 | 辫子或编发造型 |
| twin tails | 双马尾 | 发型样式 | 两边扎起的马尾 |

#### 服装描述词

| 提示词 | 含义 | 作用 | 视觉效果 |
|--------|------|------|----------|
| elegant | 优雅的 | 服装风格 | 剪裁得体，面料高档 |
| intricate | 精致的 | 服装细节 | 细节丰富，工艺精湛 |
| flowing | 飘逸的 | 服装动态 | 衣物随风飘动 |
| form-fitting | 合身的 | 服装剪裁 | 贴合身体曲线 |
| ornate | 华丽的 | 装饰程度 | 装饰繁复，细节丰富 |

#### 光照描述词

| 提示词 | 含义 | 作用 | 视觉效果 |
|--------|------|------|----------|
| cinematic | 电影级 | 光照风格 | 光影对比强烈，有电影质感 |
| dramatic | 戏剧性 | 光照效果 | 强烈的明暗对比 |
| soft | 柔和的 | 光线质感 | 光线均匀，阴影柔和 |
| rim light | 轮廓光 | 光源类型 | 主体边缘有光晕 |
| backlit | 逆光 | 光源方向 | 光源在主体背后，轮廓发光 |
| golden hour | 黄金时刻 | 时间光线 | 日落时的温暖金色光线 |
| volumetric | 体积光 | 光线效果 | 光线可见光束，有体积感 |
| chiaroscuro | 明暗对照 | 光影技法 | 强烈的明暗对比，文艺复兴风格 |

#### 风格描述词

| 提示词 | 含义 | 作用 | 视觉效果 |
|--------|------|------|----------|
| photorealistic | 照片写实 | 风格类型 | 高度写实，像真实照片 |
| hyperrealistic | 超写实 | 风格类型 | 比照片更精细的写实 |
| oil painting | 油画 | 艺术媒介 | 油画笔触和质感 |
| watercolor | 水彩 | 艺术媒介 | 水彩透明和晕染效果 |
| anime | 动漫 | 风格类型 | 日式动漫画风 |
| illustration | 插画 | 艺术类型 | 插画风格，可以是各种风格 |
| concept art | 概念艺术 | 艺术类型 | 游戏/电影概念设计风格 |
| editorial | 编辑级 | 摄影风格 | 杂志级别的专业摄影 |

#### 质量描述词

| 提示词 | 含义 | 作用 | 视觉效果 |
|--------|------|------|----------|
| masterpiece | 杰作 | 质量标记 | 提升整体质量 |
| best quality | 最佳品质 | 质量标记 | 追求最高质量 |
| highly detailed | 高度详细 | 细节程度 | 细节丰富，纹理清晰 |
| sharp focus | 锐利对焦 | 清晰度 | 主体清晰锐利 |
| 8k | 8K分辨率 | 分辨率 | 超高分辨率输出 |
| intricate details | 精致细节 | 细节程度 | 细节精致入微 |

#### 负面提示词

| 提示词 | 含义 | 作用 | 避免的效果 |
|--------|------|------|------------|
| ugly | 丑陋的 | 排除差质量 | 避免面部变形 |
| deformed | 变形的 | 排除变形 | 避免身体比例错误 |
| blurry | 模糊的 | 排除模糊 | 避免画面不清晰 |
| bad anatomy | 错误解剖 | 排除解剖错误 | 避免手指、肢体错误 |
| watermark | 水印 | 排除水印 | 避免出现水印文字 |
| text | 文字 | 排除文字 | 避免出现不需要的文字 |

### 解释输出模板

#### 标准解释输出

```markdown
## 提示词解释

### 核心主体
- **[主体词]**: [含义]，[作用]，[视觉效果]
  - 建议权重: [权重范围]，[原因]

### 关键特征
- **[特征词]**: [含义]，[作用]，[视觉效果]
  - 建议权重: [权重范围]，[原因]

### 环境背景
- **[环境词]**: [含义]，[作用]，[视觉效果]
  - 建议权重: [权重范围]，[原因]

### 光影氛围
- **[光影词]**: [含义]，[作用]，[视觉效果]
  - 建议权重: [权重范围]，[原因]

### 风格修饰
- **[风格词]**: [含义]，[作用]，[视觉效果]
  - 建议权重: [权重范围]，[原因]
```

#### 表格解释输出

```markdown
## 提示词解释

| 提示词 | 中文 | 类型 | 作用 | 视觉效果 | 权重 |
|--------|------|------|------|----------|------|
| [词1] | [中文] | [类型] | [作用] | [效果] | [权重] |
| [词2] | [中文] | [类型] | [作用] | [效果] | [权重] |
```

#### 详细解释输出

```markdown
## 提示词详解

### 1. [提示词] ([中文])

**含义**: [详细含义说明]

**为什么使用**: [使用原因和目的]

**视觉效果**: [产生的具体视觉效果]

**权重建议**: [建议权重范围]
- 原因: [为什么给这个权重]

**相关词汇**: [可以替换或补充的词汇]
```

### 解释最佳实践

#### 1. 分层解释

按提示词结构分层解释，帮助理解整体逻辑：
- 主体层 → 特征层 → 环境层 → 光影层 → 风格层

#### 2. 重点标注

对核心词汇重点标注，帮助识别关键元素：
- 核心主体（最重要）
- 关键特征（重要）
- 风格修饰（辅助）

#### 3. 对比说明

对比不同词汇的差异，帮助理解选择原因：
- "flowing" vs "straight": 飘逸感 vs 利落感
- "cinematic" vs "dramatic": 电影感 vs 戏剧性

#### 4. 提供替代

为每个词提供替代选项，增加灵活性：
- "beautiful" 可替换为: attractive, gorgeous, stunning, pretty

#### 5. 权重解释

解释权重分配的原因，帮助用户理解：
- 为什么主体权重高：是画面的核心焦点
- 为什么背景权重低：是辅助元素，不应喧宾夺主
