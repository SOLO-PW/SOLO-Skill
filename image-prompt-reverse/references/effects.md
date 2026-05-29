# 特效后期专项指南

本文档提供系统化的图像特效后期分析方法，帮助精准识别图片中的后期处理效果并转换为提示词。

---

## 目录

1. [色彩调整](#色彩调整)
2. [光影调整](#光影调整)
3. [锐化模糊](#锐化模糊)
4. [特殊效果](#特殊效果)
5. [胶片模拟](#胶片模拟)
6. [特效提示词模板](#特效提示词模板)

---

## 色彩调整

### 饱和度调整

| 效果 | 特征 | 适用场景 | 提示词 |
|------|------|----------|--------|
| 高饱和 | 色彩鲜艳浓烈 | 商业广告 | highly saturated, vivid colors, bold, vibrant |
| 低饱和 | 色彩柔和淡雅 | 文艺片 | desaturated, muted, subtle, soft colors |
| 选择性饱和 | 部分色彩突出 | 创意摄影 | selective color, color splash, accent color |
| 黑白去色 | 无彩色 | 艺术片 | black and white, monochrome, desaturated |

### 色调调整

| 效果 | 特征 | 情绪 | 提示词 |
|------|------|------|--------|
| 暖调 | 黄橙倾向 | 温馨怀旧 | warm tones, golden, amber, sepia-like |
| 冷调 | 蓝青倾向 | 冷酷现代 | cool tones, blue cast, icy, cold |
| 绿调 | 绿色倾向 | 电影感 | green tint, Matrix-style, cinematic |
| 紫调 | 紫色倾向 | 梦幻 | purple tint, violet, mystical, dreamy |

### 色彩分离

| 效果 | 特征 | 风格 | 提示词 |
|------|------|------|--------|
| 阴影偏蓝 | 暗部冷色 | 电影感 | teal shadows, blue shadows, cinematic |
| 高光偏橙 | 亮部暖色 | 电影感 | orange highlights, warm highlights, Hollywood |
| 交叉处理 | 色彩失真 | 复古 | cross-processed, color shift, vintage |
| 双色调 | 两色渐变 | 设计感 | duotone, two-tone, gradient overlay |

---

## 光影调整

### 对比度调整

| 效果 | 特征 | 氛围 | 提示词 |
|------|------|------|--------|
| 高对比 | 明暗反差大 | 戏剧性 | high contrast, dramatic, bold, punchy |
| 低对比 | 明暗反差小 | 柔和 | low contrast, flat, soft, muted |
| 中等对比 | 自然过渡 | 真实 | natural contrast, balanced, realistic |

### 曲线调整

| 效果 | 特征 | 效果 | 提示词 |
|------|------|------|--------|
| S曲线 | 增加对比 | 电影感 | S-curve, cinematic contrast, film-like |
| 提亮曲线 | 整体变亮 | 明亮 | brightened, lifted shadows, airy |
| 压暗曲线 | 整体变暗 | 暗调 | darkened, crushed blacks, moody |
| 褪色黑场 | 黑色不纯 | 复古 | faded blacks, lifted blacks, matte look |

### HDR效果

| 效果 | 特征 | 适用场景 | 提示词 |
|------|------|----------|--------|
| 自然HDR | 扩展动态范围 | 风景 | natural HDR, balanced exposure, detailed |
| 极端HDR | 超现实效果 | 艺术 | extreme HDR, surreal, hyper-realistic, painterly |
| 光晕HDR | 边缘发光 | 特殊效果 | halo HDR, glow effect, edge glow |

---

## 锐化模糊

### 锐化效果

| 效果 | 特征 | 适用场景 | 提示词 |
|------|------|----------|--------|
| 轻微锐化 | 细节增强 | 通用 | slightly sharpened, crisp, clear |
| 强力锐化 | 边缘明显 | 建筑/产品 | heavily sharpened, sharp edges, defined |
| 局部锐化 | 突出主体 | 人像 | selective sharpening, detail enhancement |

### 模糊效果

| 效果 | 特征 | 实现方式 | 提示词 |
|------|------|----------|--------|
| 高斯模糊 | 整体柔化 | 均匀模糊 | gaussian blur, soft focus, dreamy |
| 镜头模糊 | 模拟景深 | 圆形光斑 | lens blur, bokeh, depth of field |
| 运动模糊 | 动态效果 | 方向模糊 | motion blur, streaks, dynamic movement |
| 径向模糊 | 中心放射 | 速度感 | radial blur, zoom blur, speed effect |
| 倾斜模糊 | 微缩效果 | 移轴 | tilt-shift blur, miniature, selective focus |

### 景深效果

| 效果 | 特征 | 适用场景 | 提示词 |
|------|------|----------|--------|
| 浅景深 | 主体清晰背景虚 | 人像 | shallow DOF, bokeh, soft background |
| 深景深 | 全景清晰 | 风景 | deep focus, everything sharp, landscape |
| 移轴效果 | 微缩模型感 | 创意 | tilt-shift, miniature effect, toy-like |

---

## 特殊效果

### 光效

| 效果 | 特征 | 来源 | 提示词 |
|------|------|------|--------|
| 镜头光晕 | 光源入镜 | 逆光 | lens flare, sun flare, light leak |
| 光斑 | 圆形光点 | 大光圈 | bokeh, light orbs, circles of light |
| 光束 | 可见光路 | 丁达尔 | light beams, god rays, volumetric light |
| 光晕 | 边缘发光 | 后期 | glow, bloom, soft glow, luminous |
| 漏光 | 胶片漏光 | 复古 | light leak, film leak, exposure leak |

### 纹理效果

| 效果 | 特征 | 用途 | 提示词 |
|------|------|------|--------|
| 颗噪点 | 胶片颗粒 | 复古 | film grain, noise, texture, gritty |
| 划痕 | 老旧效果 | 怀旧 | scratches, vintage damage, old film |
| 灰尘 | 质感增加 | 复古 | dust, particles, vintage texture |
| 纸纹 | 纸张纹理 | 印刷 | paper texture, matte, grainy |

### 扭曲效果

| 效果 | 特征 | 实现方式 | 提示词 |
|------|------|----------|--------|
| 鱼眼 | 桶形畸变 | 镜头 | fisheye, barrel distortion, wide-angle |
| 棱镜 | 色散分离 | 后期 | prismatic, chromatic aberration, rainbow |
| 万花筒 | 重复镜像 | 后期 | kaleidoscope, mirror, symmetrical |
| 波浪 | 扭曲变形 | 后期 | wave distortion, ripple, warped |

### 颜色效果

| 效果 | 特征 | 风格 | 提示词 |
|------|------|------|--------|
| 色调分离 | 海报效果 | 设计 | posterize, limited colors, flat |
| 反转色 | 负片效果 | 艺术 | negative, inverted colors, solarized |
| 热成像 | 温度色彩 | 科技 | thermal, heat map, infrared-like |
| 单色保留 | 部分彩 | 创意 | selective color, color pop, splash |

---

## 胶片模拟

### 经典胶片

| 胶片类型 | 特征 | 氛围 | 提示词 |
|----------|------|------|--------|
| Kodak Portra | 肤色柔和 | 温暖人像 | Portra style, warm skin tones, soft, film |
| Fuji Velvia | 饱和鲜艳 | 风景 | Velvia style, vivid, saturated, rich colors |
| Kodak Tri-X | 高对比黑白 | 纪实 | Tri-X style, high contrast B&W, grainy |
| Ilford HP5 | 中等颗粒黑白 | 通用 | HP5 style, classic B&W, moderate grain |
| Kodak Ektar | 高饱和 | 风景 | Ektar style, vivid, fine grain, punchy |

### 胶片特征

| 特征 | 描述 | 提示词 |
|------|------|--------|
| 颗粒感 | 胶片噪点 | film grain, analog texture, organic noise |
| 色彩偏移 | 非精确色彩 | color shift, film tones, analog colors |
| 低对比度 | 柔和影调 | soft contrast, film look, gentle tones |
| 褪色 | 黑色不纯 | faded, lifted blacks, matte film |
| 光晕 | 高光溢出 | halation, glow, soft highlights |

### 数字胶片模拟

| 模拟 | 特征 | 提示词 |
|------|------|--------|
| VSCO风格 | 社交媒体感 | VSCO look, Instagram filter, social media style |
| 电影胶片 | 电影色调 | cinematic film, movie look, film emulation |
| 复古胶片 | 怀旧感 | vintage film, retro, nostalgic, old-school |
| 日系胶片 | 清新淡雅 | Japanese film style, light and airy, pastel |

---

## 特效提示词模板

### 色彩后期

```
[色调方向] + [饱和度] + [对比度] + [特殊效果]

示例:
Warm golden tones with slightly desaturated colors, medium contrast, subtle film grain
```

### 光影后期

```
[对比度] + [明暗调整] + [光影效果] + [氛围]

示例:
High contrast with dramatic shadows, lens flare from backlight, cinematic and moody atmosphere
```

### 胶片风格

```
[胶片类型] + [颗粒感] + [色彩特征] + [褪色程度]

示例:
Kodak Portra style with fine grain, warm skin tones, slightly faded blacks, analog film look
```

### 创意效果

```
[主要效果] + [辅助效果] + [色彩处理] + [整体风格]

示例:
Double exposure effect with light leaks, desaturated with selective color, dreamy and artistic
```

---

## 特效分析检查清单

分析图片后期效果时检查：

- [ ] 色彩倾向（暖/冷/中性）
- [ ] 饱和度（高/中/低）
- [ ] 对比度（高/中/低）
- [ ] 黑场处理（纯黑/褪色）
- [ ] 高光处理（过曝/保留）
- [ ] 锐化程度（锐利/柔和）
- [ ] 模糊类型（景深/运动/特殊）
- [ ] 特殊效果（光效/纹理/扭曲）
- [ ] 胶片感（颗粒/色彩偏移）
- [ ] 整体风格（商业/艺术/纪实）

---

## 特效关键词速查表

| 类别 | 关键词 |
|------|--------|
| 高饱和 | vivid, saturated, vibrant, bold, punchy |
| 低饱和 | desaturated, muted, subtle, soft, pastel |
| 暖调 | warm, golden, amber, orange, sepia |
| 冷调 | cool, blue, cold, icy, teal |
| 高对比 | high contrast, dramatic, bold, punchy |
| 低对比 | low contrast, flat, soft, matte |
| 锐利 | sharp, crisp, clear, detailed, defined |
| 柔和 | soft, dreamy, ethereal, gentle, diffused |
| 胶片 | film, analog, grain, vintage, retro |
| HDR | HDR, balanced, detailed, dynamic range |
| 光效 | lens flare, bokeh, glow, light leak |
| 黑白 | black and white, monochrome, B&W |
