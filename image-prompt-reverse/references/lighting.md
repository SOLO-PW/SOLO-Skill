# 光影效果专项指南

本文档提供系统化的光影效果分析方法，帮助精准提取图片中的光影元素并转换为提示词。

---

## 目录

1. [光影基础](#光影基础)
2. [光源类型](#光源类型)
3. [光照方向](#光照方向)
4. [光影质量](#光影质量)
5. [特殊光影效果](#特殊光影效果)
6. [光影提示词模板](#光影提示词模板)

---

## 光影基础

### 光影三要素

| 要素 | 说明 | 提示词关联 |
|------|------|------------|
| 光源 | 光线来源 | natural light, artificial light, sunlight |
| 方向 | 光线角度 | front light, side light, backlit |
| 质量 | 光线软硬 | soft light, hard light, diffused |

### 光影基本概念

| 概念 | 说明 | 视觉效果 |
|------|------|----------|
| 高光 | 最亮区域 | 物体表面反射光线的亮点 |
| 阴影 | 最暗区域 | 光线被遮挡形成的暗区 |
| 中间调 | 过渡区域 | 高光和阴影之间的过渡 |
| 反光 | 环境反射 | 周围环境在物体上的反射 |

---

## 光源类型

### 自然光源

| 光源 | 特征 | 时间 | 提示词 |
|------|------|------|--------|
| 正午阳光 | 强烈，顶光 | 12:00 | midday sun, overhead sunlight, harsh noon light |
| 黄金时刻 | 温暖，柔和 | 日出日落 | golden hour, warm sunset light, magic hour |
| 蓝色时刻 | 冷调，柔和 | 日出前/日落后 | blue hour, twilight, pre-dawn light |
| 阴天光 | 柔和，均匀 | 阴天 | overcast light, cloudy sky, diffused daylight |
| 月光 | 冷调，柔和 | 夜晚 | moonlight, lunar glow, soft night light |
| 星光 | 微弱，点状 | 深夜 | starlight, starry sky, dim star glow |

### 人造光源

| 光源 | 特征 | 场景 | 提示词 |
|------|------|------|--------|
| 钨丝灯 | 暖黄光 | 室内 | tungsten light, warm incandescent, yellow bulb |
| 荧光灯 | 冷白光 | 办公室 | fluorescent light, cool white, office lighting |
| LED灯 | 可调色温 | 现代空间 | LED light, adjustable color temperature |
| 蜡烛 | 暖黄，闪烁 | 浪漫场景 | candlelight, flickering flame, warm glow |
| 霓虹灯 | 彩色，鲜艳 | 城市夜景 | neon lights, neon glow, colorful neon |
| 壁炉 | 暖橙，温暖 | 冬季室内 | fireplace, warm fire, glowing embers |

### 特殊光源

| 光源 | 特征 | 场景 | 提示词 |
|------|------|------|--------|
| 屏幕光 | 冷蓝光 | 科技场景 | screen glow, monitor light, digital illumination |
| 车灯 | 强烈，白色 | 街道 | headlights, car lights, beam of light |
| 舞台灯 | 彩色，戏剧 | 演出 | stage lighting, spot light, theatrical light |
| 烟火 | 彩色，闪烁 | 节日 | fireworks, sparkling lights, pyrotechnic |
| 激光 | 单色，细线 | 派对 | laser light, beam, neon laser |

---

## 光照方向

### 基本方向

| 方向 | 效果 | 适用场景 | 提示词 |
|------|------|----------|--------|
| 正面光 | 均匀照明，少阴影 | 证件照 | front lighting, flat light, even illumination |
| 侧光 | 立体感，纹理突出 | 人像艺术 | side lighting, Rembrandt lighting, dramatic side light |
| 逆光 | 轮廓发光，剪影 | 氛围人像 | backlit, backlighting, rim light, silhouette |
| 顶光 | 眼窝阴影 | 特殊效果 | overhead lighting, top light, harsh overhead |
| 底光 | 恐怖效果 | 恐怖题材 | under lighting, uplighting, horror lighting |

### 侧光细分

| 角度 | 效果 | 专业术语 | 提示词 |
|------|------|----------|--------|
| 45度侧光 | 经典人像光 | 伦勃朗光 | Rembrandt lighting, 45-degree side light |
| 90度侧光 | 强烈明暗对比 | 分割光 | split lighting, half-face shadow |
| 135度侧光 | 轮廓光 | 逆侧光 | rim light, edge light, back-side light |

### 逆光效果

| 效果 | 描述 | 提示词 |
|------|------|--------|
| 轮廓光 | 边缘发光 | rim light, edge glow, halo effect |
| 剪影 | 完全暗部 | silhouette, dark outline, backlit silhouette |
| 透射光 | 穿过物体 | translucency, light through, backlit transparency |
| 光晕 | 光芒四射 | lens flare, sun flare, light burst |

---

## 光影质量

### 硬光与软光

| 类型 | 特征 | 阴影 | 适用场景 | 提示词 |
|------|------|------|----------|--------|
| 硬光 | 方向性强 | 边缘清晰 | 戏剧效果 | hard light, harsh light, sharp shadows |
| 软光 | 散射均匀 | 边缘模糊 | 柔美人像 | soft light, diffused light, gentle shadows |

### 软光程度

| 程度 | 效果 | 提示词 |
|------|------|--------|
| 极软光 | 几乎无阴影 | very soft light, overcast, cloud-like diffusion |
| 中等软光 | 柔和阴影 | soft diffused light, window light, shade |
| 微软光 | 轻微阴影 | slightly soft, gentle diffusion, light haze |

### 硬光程度

| 程度 | 效果 | 提示词 |
|------|------|--------|
| 极硬光 | 强烈对比 | harsh direct light, midday sun, bare bulb |
| 中等硬光 | 明显阴影 | hard light, focused beam, directional light |
| 微硬光 | 轻微对比 | slightly hard, crisp light, clear shadows |

---

## 特殊光影效果

### 自然光效

| 效果 | 描述 | 触发条件 | 提示词 |
|------|------|----------|--------|
| 丁达尔效应 | 光束可见 | 空气中有微粒 | Tyndall effect, god rays, light beams, volumetric light |
| 彩虹 | 色散光谱 | 水雾+阳光 | rainbow, double rainbow, prismatic colors |
| 光斑 | 圆形光点 | 大光圈 | bokeh, light orbs, soft circles of light |
| 透射光 | 穿过透明体 | 玻璃/水 | light transmission, backlit, through glass |
| 反射光 | 镜面反射 | 水面/镜面 | reflection, mirror reflection, light bounce |

### 人造光效

| 效果 | 描述 | 场景 | 提示词 |
|------|------|------|--------|
| 镜头光晕 | 光源入镜 | 逆光拍摄 | lens flare, sun flare, anamorphic flare |
| 光绘 | 光线轨迹 | 长曝光 | light painting, light trails, long exposure |
| 星芒 | 光芒放射 | 小光圈 | starburst, sun star, light star pattern |
| 霓虹反射 | 彩色反射 | 雨夜城市 | neon reflection, wet pavement glow, colorful lights |
| 烛光闪烁 | 温暖摇曳 | 室内 | candlelight, flickering, warm glow |

### 戏剧光效

| 效果 | 描述 | 风格 | 提示词 |
|------|------|------|--------|
| 明暗对照 | 强烈对比 | 巴洛克 | chiaroscuro, dramatic contrast, Caravaggio lighting |
| 低调光 | 大面积暗部 | 黑色电影 | low key, dark moody, noir lighting |
| 高调光 | 大面积亮部 | 清新风格 | high key, bright, overexposed look |
| 色彩光 | 彩色光源 | 现代艺术 | colored lighting, gel lights, color wash |
| 剪影光 | 完全逆光 | 氛围 | silhouette lighting, backlit, dark outline |

---

## 光影情绪

### 情绪对应

| 情绪 | 光影特征 | 提示词 |
|------|----------|--------|
| 温馨 | 暖色软光 | warm soft light, cozy lighting, gentle glow |
| 神秘 | 低调硬光 | mysterious lighting, dark shadows, moody |
| 浪漫 | 柔和暖光 | romantic lighting, soft warm glow, dreamy |
| 紧张 | 高对比硬光 | tense lighting, harsh shadows, dramatic |
| 忧郁 | 冷调低光 | melancholic lighting, cool dim light, somber |
| 活力 | 明亮高调 | energetic lighting, bright vibrant, lively |
| 恐怖 | 底光/顶光 | horror lighting, eerie glow, unsettling shadows |

### 电影风格光影

| 风格 | 特征 | 代表导演/摄影师 | 提示词 |
|------|------|-----------------|--------|
| 黑色电影 | 高对比，阴影 | 雷诺阿 | film noir, high contrast, venetian blinds shadow |
| 新现实主义 | 自然光 | 德西卡 | neorealist, natural lighting, documentary style |
| 德国表现主义 | 极端阴影 | 朗格 | expressionist, distorted shadows, angular lighting |
| 好莱坞黄金时代 | 柔光，魅力 | 赫伦 | Hollywood glamour, soft focus, butterfly lighting |
| 现代数字 | 清晰，干净 | 芬奇 | modern digital, clean lighting, clinical |

---

## 光影提示词模板

### 基础光影描述

```
[光源类型] + [光照方向] + [光影质量] + [色温]

示例:
Warm natural sunlight from window, soft side lighting, diffused quality, golden tones
```

### 戏剧光影描述

```
[光影风格] + [对比度] + [阴影特征] + [情绪]

示例:
Dramatic chiaroscuro lighting, high contrast, deep shadows creating mysterious mood
```

### 氛围光影描述

```
[光源] + [效果] + [氛围] + [时间]

示例:
Golden hour sunlight with lens flare, warm and romantic atmosphere, sunset time
```

### 特殊光效描述

```
[光效类型] + [触发条件] + [视觉效果]

示例:
Tyndall effect through morning mist, visible light beams, ethereal atmosphere
```

---

## 光影识别检查清单

分析图片光影时检查：

- [ ] 主光源类型（自然/人造）
- [ ] 光照方向（正面/侧面/逆光）
- [ ] 光影质量（硬光/软光）
- [ ] 色温（暖/冷/中性）
- [ ] 阴影特征（边缘/深度/方向）
- [ ] 特殊光效（光晕/光束/反射）
- [ ] 整体对比度
- [ ] 光影与情绪的匹配

---

## 光影关键词速查表

| 类别 | 关键词 |
|------|--------|
| 自然光 | sunlight, daylight, natural light, sun, sky |
| 人造光 | artificial light, lamp, bulb, LED, neon |
| 暖光 | warm light, golden, amber, tungsten, sunset |
| 冷光 | cool light, blue, daylight, moonlight, icy |
| 软光 | soft light, diffused, overcast, gentle, subtle |
| 硬光 | hard light, harsh, direct, focused, sharp |
| 侧光 | side lighting, Rembrandt, split, dramatic |
| 逆光 | backlit, rim light, silhouette, halo, glow |
| 顶光 | overhead, top light, harsh noon, downlight |
| 低调 | low key, dark, moody, shadows, noir |
| 高调 | high key, bright, airy, overexposed, clean |
| 戏剧 | dramatic, chiaroscuro, contrast, theatrical |
| 光效 | lens flare, bokeh, god rays, light beams |
