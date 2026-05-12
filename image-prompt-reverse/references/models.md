# AI绘图模型提示词格式规范

本文档详细说明各主流AI绘图模型的提示词格式、语法特点和最佳实践。

---

## 目录

1. [Stable Diffusion (SD/SDXL)](#stable-diffusion-sdsdxl)
2. [Midjourney](#midjourney)
3. [DALL-E 3](#dall-e-3)
4. [ComfyUI / Automatic1111](#comfyui--automatic1111)
5. [Flux](#flux)
6. [NijiJourney](#nijijourney)
7. [Leonardo.ai](#leonardoai)
8. [InvokeAI](#invokeai)
9. [Playground AI](#playground-ai)
10. [Ideogram](#ideogram)
11. [通用提示词结构](#通用提示词结构)

---

## Stable Diffusion (SD/SDXL)

### 基本格式

```
正向提示词: <主体描述>, <风格描述>, <质量词>, <技术参数>
反向提示词: <排除内容>, <负面质量词>
```

### 语法特点

- **权重语法**: `(word:1.2)` 增强权重, `(word:0.8)` 降低权重
- **嵌套权重**: `((word))` 或 `{{{word}}}` 多层增强
- **交替词**: `[word1|word2]` 在步数间交替
- **组合词**: `[word1::0.3]` 前30%步数使用, `[word1:word2:0.5]` 50%步数切换

### SD 1.5 特点

- 推荐768x512或512x768分辨率
- 需要较多质量修饰词
- 对负面提示词敏感

### SDXL 特点

- 推荐1024x1024分辨率
- 原生支持更自然的描述
- refiner可增强细节

### 示例

```
正向: a beautiful woman with long silver hair, intricate fantasy armor, glowing blue eyes, standing in enchanted forest, magical particles floating, cinematic lighting, 8k, highly detailed, masterpiece, best quality, sharp focus

反向: ugly, deformed, noisy, blurry, low contrast, bad anatomy, extra limbs, poorly drawn face, mutation, watermark, text
```

---

## Midjourney

### 基本格式

```
<主体描述>, <风格描述>, <参数>
```

### 参数语法

| 参数 | 说明 | 示例 |
|------|------|------|
| `--ar` | 宽高比 | `--ar 16:9` |
| `--s` | 风格化程度 (0-1000) | `--s 250` |
| `--c` | 混乱度 (0-100) | `--c 50` |
| `--q` | 质量 (.25/.5/1) | `--q 2` |
| `--v` | 版本号 | `--v 6` |
| `--niji` | 动漫风格 | `--niji 6` |
| `--no` | 负面提示 | `--no text, watermark` |
| `--style` | 风格变体 | `--style raw` |
| `--iw` | 图片权重 (0-2) | `--iw 1.5` |
| `--seed` | 种子值 | `--seed 12345` |
| `--tile` | 无缝纹理 | `--tile` |
| `--video` | 生成视频 | `--video` |

### 语法特点

- 使用逗号分隔描述词
- 支持URL作为参考图
- `::` 语法设置词权重: `sunset::2, ocean::1`
- `--no` 作为负面提示

### 示例

```
a majestic dragon soaring through clouds at sunset, scales shimmering with golden light, epic fantasy art, dramatic lighting, highly detailed, cinematic composition --ar 16:9 --v 6 --s 250 --no text, watermark
```

---

## DALL-E 3

### 基本格式

```
<完整的自然语言描述>
```

### 语法特点

- **自然语言优先**: 支持完整句子描述
- **自动优化**: 系统会自动优化提示词
- **无需质量词**: 内置高质量输出
- **长度限制**: 约4000字符

### 最佳实践

- 使用描述性、具体的语言
- 说明艺术风格和媒介
- 描述构图和视角
- 避免模糊或抽象描述

### 示例

```
A photorealistic image of a serene Japanese garden at dawn, with cherry blossoms gently falling onto a crystal-clear koi pond. Traditional wooden bridges arch over the water, and soft morning mist rises between carefully pruned pine trees. The scene is captured with a wide-angle lens, creating a sense of peaceful tranquility. Golden sunlight filters through the branches, creating dappled light patterns on the moss-covered stone lanterns.
```

---

## ComfyUI / Automatic1111

### 基本格式

与Stable Diffusion相同，但支持更多扩展语法。

### 扩展语法

- **区域控制**: 使用Regional Prompter扩展
- **ControlNet提示**: 结合ControlNet条件
- **LoRA触发词**: `<lora:name:weight>` 后跟触发词
- **Embedding**: `(embedding:name:weight)` 负面提示嵌入

### 示例

```
正向: masterpiece, best quality, ultra highres, 1girl, solo, white dress, standing in flower field, sunlight, soft lighting, intricate details, <lora:add_detail:0.5>

反向: (worst quality:1.4), (low quality:1.4), (normal quality:1.4), lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, jpeg artifacts, signature, watermark, username, blurry, (ng_deepnegative_v1_75t:1.2)
```

---

## Flux

### 基本格式

```
<自然语言描述>, <风格关键词>
```

### 语法特点

- 支持自然语言描述
- 对提示词理解能力强
- 原生高分辨率输出
- 较少需要质量修饰词
- 支持简单权重语法

### 最佳实践

- 详细描述主体和场景
- 明确指定艺术风格
- 描述光照和氛围
- 可适当添加质量词增强效果

### 示例

```
A professional portrait photograph of a young woman with auburn hair, wearing an elegant black dress, standing in a modern art gallery. Soft diffused lighting from large windows, shallow depth of field, shot on medium format camera, editorial style, highly detailed, photorealistic
```

---

## NijiJourney

### 基本格式

```
<动漫风格描述>, --niji <版本> [参数]
```

### 语法特点

- 专为动漫/插画风格优化
- 支持Midjourney大部分参数
- `--style` 参数控制风格变体

### 风格变体

| 参数 | 说明 |
|------|------|
| `--style cute` | 可爱风格，适合萌系角色 |
| `--style scenic` | 风景风格，适合场景插画 |
| `--style expressive` | 表现风格，适合情感表达 |
| `--style original` | 原始风格，MJ V5类似效果 |

### 示例

```
anime girl with pink hair, wearing school uniform, cherry blossoms background, soft pastel colors, detailed illustration, studio ghibli style --niji 6 --ar 2:3 --style cute
```

---

## Leonardo.ai

### 基本格式

```
<主体描述>, <风格描述>, <质量词>
```

### 语法特点

- 支持自然语言和标签混合
- 内置多种预设风格
- 支持负面提示词
- 支持Alchemy高清增强

### 内置风格预设

| 风格 | 关键词 |
|------|--------|
| Dynamic | 动态风格，适合动作场景 |
| Cinematic | 电影感，适合场景和氛围 |
| Vibrant | 鲜艳风格，高饱和度 |
| Creative | 创意风格，艺术化表现 |
| Photography | 摄影风格，写实感 |

### 示例

```
正向: cinematic portrait of a warrior princess, intricate armor design, dramatic lighting, epic fantasy atmosphere, highly detailed, 8k, masterpiece

反向: blurry, low quality, distorted, bad anatomy, watermark
```

---

## InvokeAI

### 基本格式

```
<主体描述>, <风格描述>, <质量词>
```

### 语法特点

- 基于Stable Diffusion
- 支持权重语法 `(word:1.2)`
- 支持负面提示词
- 支持ControlNet
- 支持模型融合

### 特殊功能

- **Unified Canvas**: 统一画布编辑
- **Node Editor**: 节点式工作流
- **Model Manager**: 模型管理

### 示例

```
正向: (masterpiece:1.2), (best quality:1.2), detailed fantasy landscape, floating islands, waterfalls, magical atmosphere, ethereal lighting

反向: (worst quality:1.4), (low quality:1.4), blurry, bad anatomy
```

---

## Playground AI

### 基本格式

```
<主体描述>, <风格描述>, <质量词>
```

### 语法特点

- 支持自然语言描述
- 内置多种滤镜风格
- 支持负面提示词
- 支持图像混合

### 滤镜风格

| 滤镜 | 效果 |
|------|------|
| Cinematic | 电影感 |
| Analogue | 胶片感 |
| Volumetric | 体积光效果 |
| Epic | 史诗感 |
| Line Art | 线稿风格 |

### 示例

```
正向: cinematic portrait of a cyberpunk character, neon lights, futuristic city background, highly detailed, 8k

反向: blurry, low quality, distorted
```

---

## Ideogram

### 基本格式

```
<主体描述>, <风格描述>, <质量词>
```

### 语法特点

- **擅长文字渲染**: 在图片中生成清晰文字
- 支持自然语言描述
- 支持多种风格预设
- 支持负面提示词

### 风格预设

| 风格 | 说明 |
|------|------|
| Auto | 自动选择 |
| Design | 设计风格 |
| Realistic | 写实风格 |
| 3D | 3D渲染风格 |
| Anime | 动漫风格 |

### 示例

```
正向: Typography poster design with text "DREAM BIG", modern minimalist style, gradient background, professional graphic design

反向: blurry text, distorted letters, low quality
```

---

## 通用提示词结构

### 标准结构模板

```
[主体] + [动作/姿态] + [服装/外观] + [环境/背景] + [光照] + [风格] + [质量词]
```

### 描述顺序建议

1. **主体** (Subject): 人物、物体、场景焦点
2. **特征** (Features): 外观、服装、表情
3. **动作** (Action): 姿态、运动状态
4. **环境** (Environment): 背景、场景元素
5. **氛围** (Atmosphere): 光照、天气、情绪
6. **风格** (Style): 艺术风格、媒介
7. **技术** (Technical): 质量、分辨率、视角

### 权重分配原则

| 模型 | 核心主体 | 风格词 | 质量词 | 背景 |
|------|----------|--------|--------|------|
| SD/SDXL | 1.3-1.5 | 1.1-1.2 | 1.1-1.3 | 0.8-1.0 |
| Midjourney | ::3-5 | ::1-2 | 自然融入 | ::0.5-1 |
| DALL-E 3 | 详细描述 | 详细描述 | 可选 | 详细描述 |
| Flux | 详细描述 | 明确指定 | 可选 | 详细描述 |
| NijiJourney | ::3-5 | ::1-2 | 自然融入 | ::0.5-1 |
| Leonardo.ai | 1.2-1.4 | 1.1-1.2 | 1.1-1.3 | 0.9-1.1 |
| InvokeAI | 1.3-1.5 | 1.1-1.2 | 1.1-1.3 | 0.8-1.0 |
| Playground | 详细描述 | 滤镜选择 | 可选 | 详细描述 |
| Ideogram | 详细描述 | 风格选择 | 可选 | 详细描述 |

### 模型选择建议

| 需求 | 推荐模型 |
|------|----------|
| 写实人像 | SDXL, Midjourney V6, Flux |
| 动漫插画 | NijiJourney, SD+动漫模型 |
| 风景摄影 | Midjourney, SDXL, Leonardo.ai |
| 概念艺术 | Midjourney, SDXL, InvokeAI |
| 商业产品 | DALL-E 3, Flux, SDXL |
| 文字设计 | Ideogram |
| 快速原型 | Playground AI, Leonardo.ai |
| 精细控制 | ComfyUI, Automatic1111 |
