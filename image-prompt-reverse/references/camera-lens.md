# 镜头语言专项指南

本文档提供系统化的镜头语言分析方法，帮助精准提取图片中的镜头元素并转换为提示词。

---

## 目录

1. [镜头基础](#镜头基础)
2. [焦距分类](#焦距分类)
3. [景深控制](#景深控制)
4. [镜头角度](#镜头角度)
5. [镜头运动](#镜头运动)
6. [镜头提示词模板](#镜头提示词模板)

---

## 镜头基础

### 镜头参数

| 参数 | 说明 | 影响 |
|------|------|------|
| 焦距 | 视角宽窄 | 广角夸张，长焦压缩 |
| 光圈 | 进光量 | 大光圈浅景深，小光圈深景深 |
| 快门 | 曝光时间 | 高速冻结，慢速拖影 |
| ISO | 感光度 | 高ISO噪点，低ISO纯净 |

### 等效焦距参考

| 焦距范围 | 镜头类型 | 视角 | 适用场景 |
|----------|----------|------|----------|
| 8-16mm | 超广角 | 180-107° | 建筑、星空、创意 |
| 16-35mm | 广角 | 107-63° | 风景、环境、街拍 |
| 35-70mm | 标准 | 63-34° | 人文、日常、纪实 |
| 70-200mm | 中长焦 | 34-12° | 人像、运动、野生动物 |
| 200-600mm | 长焦 | 12-4° | 体育、野生动物、天文 |

---

## 焦距分类

### 超广角镜头 (8-16mm)

| 特征 | 效果 | 适用场景 | 提示词 |
|------|------|----------|--------|
| 极端透视 | 夸张近大远小 | 创意摄影 | ultra wide angle, extreme perspective, fisheye |
| 桶形畸变 | 直线弯曲 | 艺术效果 | barrel distortion, fisheye effect |
| 超大景深 | 全景清晰 | 建筑摄影 | deep focus, everything sharp |
| 夸张空间 | 空间感增强 | 室内摄影 | expanded space, dramatic interior |

### 广角镜头 (16-35mm)

| 特征 | 效果 | 适用场景 | 提示词 |
|------|------|----------|--------|
| 宽广视角 | 纳入更多场景 | 风景摄影 | wide angle, 24mm, 35mm, panoramic |
| 透视明显 | 近大远小 | 环境人像 | wide perspective, environmental portrait |
| 深景深 | 前后清晰 | 街拍 | deep depth of field, street photography |
| 环境感 | 强调环境 | 旅行摄影 | environmental, context, surroundings |

### 标准镜头 (35-70mm)

| 特征 | 效果 | 适用场景 | 提示词 |
|------|------|----------|--------|
| 自然视角 | 接近人眼 | 人文纪实 | natural perspective, 50mm, normal lens |
| 无畸变 | 真实比例 | 日常记录 | no distortion, realistic, true to life |
| 通用性 | 多场景适用 | 新闻摄影 | versatile, all-purpose, standard |
| 平衡构图 | 不夸张不压缩 | 人像 | balanced composition, natural framing |

### 中长焦镜头 (70-200mm)

| 特征 | 效果 | 适用场景 | 提示词 |
|------|------|----------|--------|
| 背景压缩 | 背景靠近主体 | 人像摄影 | telephoto compression, 85mm, 135mm |
| 浅景深 | 背景虚化 | 人像特写 | shallow depth of field, bokeh, blurred background |
| 空间压缩 | 前后景靠近 | 体育摄影 | compressed perspective, flat space |
| 远摄能力 | 拉近远景 | 野生动物 | long lens, 200mm, distant subject |

### 长焦镜头 (200mm+)

| 特征 | 效果 | 适用场景 | 提示词 |
|------|------|----------|--------|
| 极浅景深 | 极小对焦区 | 微距效果 | extremely shallow DOF, selective focus |
| 空间极压缩 | 平面感 | 创意摄影 | extreme compression, flat perspective |
| 远距拍摄 | 不干扰主体 | 野生动物 | distant shot, wildlife photography |
| 热气效果 | 空气扰动 | 远景 | heat haze, atmospheric distortion |

---

## 景深控制

### 景深类型

| 类型 | 光圈 | 效果 | 适用场景 | 提示词 |
|------|------|------|----------|--------|
| 极浅景深 | f/1.2-f/2 | 极小清晰区 | 梦幻人像 | extremely shallow DOF, dreamy, selective focus |
| 浅景深 | f/2-f/4 | 主体清晰背景虚 | 人像特写 | shallow DOF, bokeh, soft background |
| 中等景深 | f/5.6-f/8 | 主体和部分背景清晰 | 环境人像 | moderate DOF, balanced focus |
| 深景深 | f/8-f/16 | 大部分清晰 | 风景摄影 | deep DOF, sharp throughout, landscape |
| 超深景深 | f/16-f/22 | 全景清晰 | 全景摄影 | hyperfocal, infinite focus, everything sharp |

### 焦外效果 (Bokeh)

| 效果 | 特征 | 提示词 |
|------|------|--------|
| 奶油焦外 | 柔滑圆形 | creamy bokeh, smooth background blur |
| 旋转焦外 | 旋转形状 | swirly bokeh, vortex bokeh, Petzval |
| 光斑焦外 | 光点圆形 | bokeh balls, light orbs, circular highlights |
| 口径蚀 | 边缘变形 | cat's eye bokeh, optical vignetting |
| 洋葱圈 | 同心圆纹 | onion ring bokeh, concentric circles |
| 二线性 | 硬边缘 | nervous bokeh, busy background |

### 焦点控制

| 焦点 | 效果 | 提示词 |
|------|------|--------|
| 前景对焦 | 前清后虚 | focus on foreground, front focus |
| 中景对焦 | 中间清晰 | focus on middle ground, mid focus |
| 背景对焦 | 后清前虚 | focus on background, back focus |
| 追焦 | 追踪主体 | tracking focus, motion tracking |
| 移焦 | 焦点转换 | rack focus, focus pull |

---

## 镜头角度

### 垂直角度

| 角度 | 效果 | 心理暗示 | 提示词 |
|------|------|----------|--------|
| 鸟瞰 | 正上方俯拍 | 全局、渺小 | bird's eye view, top-down, overhead |
| 高角度 | 从上往下拍 | 弱小、被控制 | high angle, looking down, elevated |
| 平视 | 与主体平行 | 平等、自然 | eye level, straight on, neutral |
| 低角度 | 从下往上拍 | 强大、威严 | low angle, looking up, ground level |
| 虫眼 | 正下方仰拍 | 极端威严 | worm's eye view, extreme low angle |

### 水平角度

| 角度 | 效果 | 提示词 |
|------|------|--------|
| 正面 | 直接、对称 | front view, straight on, facing camera |
| 侧面 | 轮廓、线条 | side view, profile, silhouette |
| 3/4面 | 立体、自然 | three-quarter view, 3/4 angle |
| 背面 | 神秘、跟随 | back view, from behind, rear view |

### 荷兰角

| 角度 | 效果 | 适用场景 | 提示词 |
|------|------|----------|--------|
| 轻微倾斜 | 动感、不安 | 动作场景 | slight tilt, Dutch angle, canted |
| 中等倾斜 | 紧张、混乱 | 悬疑场景 | medium tilt, diagonal, skewed |
| 极端倾斜 | 极端不安 | 恐怖场景 | extreme tilt, very canted, disorienting |

---

## 镜头运动 (视频参考)

### 基本运动

| 运动 | 效果 | 提示词 |
|------|------|--------|
| 推镜头 | 靠近主体 | dolly in, push in, zoom in |
| 拉镜头 | 远离主体 | dolly out, pull out, zoom out |
| 摇镜头 | 水平旋转 | pan left, pan right, horizontal pan |
| 俯仰 | 垂直旋转 | tilt up, tilt down, vertical tilt |
| 移动 | 跟随主体 | tracking shot, dolly shot, following |

### 特殊运动

| 运动 | 效果 | 提示词 |
|------|------|--------|
| 旋转 | 环绕主体 | orbit shot, revolving, 360 degree |
| 升降 | 垂直移动 | crane shot, boom shot, jib |
| 手持 | 随机晃动 | handheld, shaky cam, documentary feel |
| 斯坦尼康 | 平滑移动 | steadicam, smooth tracking, floating |
| 变焦 | 焦距变化 | zoom in, zoom out, dolly zoom |

### 镜头运动情绪

| 情绪 | 运动方式 | 提示词 |
|------|----------|--------|
| 紧张 | 快速推拉 | rapid dolly, quick zoom, urgent movement |
| 平静 | 缓慢移动 | slow pan, gentle tilt, smooth glide |
| 混乱 | 手持晃动 | shaky handheld, chaotic movement |
| 神秘 | 缓慢推进 | slow push in, creeping approach |
| 震撼 | 快速拉升 | rapid pull back, dramatic reveal |

---

## 镜头提示词模板

### 焦距描述

```
[焦距]mm lens, [视角效果], [透视特点]

示例:
85mm telephoto lens, compressed background, beautiful bokeh, flattering portrait perspective
```

### 景深描述

```
[景深类型], [焦点位置], [焦外效果]

示例:
Shallow depth of field, focus on eyes, creamy smooth bokeh background
```

### 角度描述

```
[拍摄角度], [心理暗示], [构图效果]

示例:
Low angle shot looking up, conveying power and dominance, dramatic perspective
```

### 综合镜头描述

```
[焦距] + [景深] + [角度] + [特殊效果]

示例:
135mm telephoto, shallow DOF with bokeh, eye-level angle, soft natural light, cinematic look
```

---

## 镜头语言检查清单

分析图片镜头时检查：

- [ ] 估算焦距范围（广角/标准/长焦）
- [ ] 景深类型（浅/中/深）
- [ ] 焦外效果（奶油/旋转/光斑）
- [ ] 拍摄角度（俯/平/仰）
- [ ] 透视特点（夸张/自然/压缩）
- [ ] 焦点位置（前/中/后）
- [ ] 特殊效果（畸变/光晕/热气）

---

## 镜头关键词速查表

| 类别 | 关键词 |
|------|--------|
| 超广角 | ultra wide, fisheye, 8mm, extreme perspective |
| 广角 | wide angle, 24mm, 35mm, environmental |
| 标准 | 50mm, normal lens, natural perspective |
| 中焦 | 85mm, 105mm, portrait lens, moderate telephoto |
| 长焦 | 135mm, 200mm, telephoto, compressed |
| 浅景深 | shallow DOF, bokeh, soft background, f/1.4 |
| 深景深 | deep focus, sharp throughout, f/11, landscape |
| 低角度 | low angle, looking up, ground level, worm's eye |
| 高角度 | high angle, looking down, bird's eye, overhead |
| 平视 | eye level, straight on, neutral angle |
| 荷兰角 | Dutch angle, tilted, canted, diagonal |
| 电影感 | cinematic, anamorphic, film look, 2.35:1 |
