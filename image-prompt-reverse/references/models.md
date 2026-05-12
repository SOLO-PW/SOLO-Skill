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
7. [通用提示词结构](#通用提示词结构)

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

### 示例

```
正向: masterpiece, best quality, ultra highres, 1girl, solo, white dress, standing in flower field, sunlight, soft lighting, intricate details, <lora:add_detail:0.5>

反向: (worst quality:1.4), (low quality:1.4), (normal quality:1.4), lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, jpeg artifacts, signature, watermark, username, blurry
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

### 示例

```
A professional portrait photograph of a young woman with auburn hair, wearing an elegant black dress, standing in a modern art gallery. Soft diffused lighting from large windows, shallow depth of field, shot on medium format camera, editorial style
```

---

## NijiJourney

### 基本格式

```
<动漫风格描述>, --niji <版本>
```

### 语法特点

- 专为动漫/插画风格优化
- 支持Midjourney大部分参数
- `--style cute` 或 `--style scenic` 风格变体

### 示例

```
anime girl with pink hair, wearing school uniform, cherry blossoms background, soft pastel colors, detailed illustration, studio ghibli style --niji 6 --ar 2:3 --style cute
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

- 核心元素权重最高: `(main subject:1.3)`
- 风格词中等权重: `(art style:1.1)`
- 质量词默认或略高: `(masterpiece:1.2)`
- 背景元素可降低: `(background:0.9)`
