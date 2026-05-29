# 构图分析专项指南

本文档提供系统化的构图分析方法，帮助精准提取图片中的构图元素并转换为提示词。

---

## 目录

1. [构图基础](#构图基础)
2. [经典构图法则](#经典构图法则)
3. [视角与角度](#视角与角度)
4. [景深与焦距](#景深与焦距)
5. [空间与层次](#空间与层次)
6. [构图提示词模板](#构图提示词模板)

---

## 构图基础

### 构图三要素

| 要素 | 说明 | 提示词关联 |
|------|------|------------|
| 主体 | 画面的视觉焦点 | subject, focal point, main element |
| 陪体 | 辅助主体的元素 | supporting elements, secondary objects |
| 背景 | 主体后面的环境 | background, backdrop, environment |

### 构图原则

1. **简洁性** - 去除干扰元素，突出主体
2. **平衡性** - 视觉重量的均衡分布
3. **引导性** - 引导视线流动
4. **对比性** - 通过对比突出主体

---

## 经典构图法则

### 三分法 (Rule of Thirds)

将画面分成3×3网格，主体放在交叉点或线上。

```
┌─────┬─────┬─────┐
│     │     │     │
├─────┼─────┼─────┤
│     │     │     │
├─────┼─────┼─────┤
│     │     │     │
└─────┴─────┴─────┘
```

**识别特征**:
- 主体位于网格线交叉点
- 地平线位于上1/3或下1/3线
- 留白在主体朝向一侧

**提示词**: `rule of thirds composition`, `subject placed at intersection point`

### 黄金分割 (Golden Ratio)

比三分法更精确的比例关系（约1:1.618）。

**识别特征**:
- 主体位于黄金分割点
- 螺旋线引导视线
- 比例和谐优美

**提示词**: `golden ratio composition`, `fibonacci spiral`, `harmonious proportions`

### 对称构图 (Symmetry)

画面左右或上下对称。

**类型**:
| 对称类型 | 说明 | 示例 |
|----------|------|------|
| 左右对称 | 垂直轴对称 | 建筑正面、倒影 |
| 上下对称 | 水平轴对称 | 水面倒影 |
| 辐射对称 | 中心点对称 | 花朵、穹顶 |

**提示词**: `symmetrical composition`, `perfect symmetry`, `mirror reflection`

### 对角线构图 (Diagonal)

主体沿对角线排列，增加动感。

**识别特征**:
- 主要线条沿对角线分布
- 画面有动态感
- 视线沿对角线移动

**提示词**: `diagonal composition`, `dynamic diagonal lines`, `sense of movement`

### 框架构图 (Framing)

用前景元素框住主体。

**常见框架**:
| 框架类型 | 示例 |
|----------|------|
| 自然框架 | 树枝、拱门、洞穴 |
| 建筑框架 | 门窗、走廊、拱廊 |
| 人工框架 | 镜框、相框 |

**提示词**: `natural framing`, `frame within frame`, `architectural framing`

### 引导线构图 (Leading Lines)

用线条引导视线到主体。

**常见引导线**:
| 线条类型 | 示例 |
|----------|------|
| 直线 | 道路、铁轨、栏杆 |
| 曲线 | 河流、小径、海岸线 |
| 汇聚线 | 透视消失点 |

**提示词**: `leading lines`, `converging lines`, `path leading to subject`

### 前景兴趣点 (Foreground Interest)

在前景添加元素增加层次感。

**识别特征**:
- 前景有明确的视觉元素
- 增加画面深度感
- 引导视线进入画面

**提示词**: `foreground interest`, `strong foreground element`, `depth through foreground`

---

## 视角与角度

### 拍摄角度

| 角度 | 说明 | 效果 | 提示词 |
|------|------|------|--------|
| 平视 | 与主体平行 | 自然、亲切 | `eye level`, `straight on` |
| 仰视 | 从下往上拍 | 威严、高大 | `low angle`, `looking up`, `worm's eye view` |
| 俯视 | 从上往下拍 | 渺小、全局 | `high angle`, `looking down`, `bird's eye view` |
| 鸟瞰 | 正上方俯拍 | 地图感、全局 | `overhead`, `top-down view`, `aerial view` |
| 虫眼 | 正下方仰拍 | 极端仰视 | `worm's eye view`, `extreme low angle` |

### 拍摄距离

| 距离 | 说明 | 提示词 |
|------|------|--------|
| 特写 | 面部/细节 | `close-up`, `extreme close-up`, `macro` |
| 近景 | 胸部以上 | `medium close-up`, `head and shoulders` |
| 中景 | 腰部以上 | `medium shot`, `waist up` |
| 全身 | 完整人物 | `full body shot`, `full length` |
| 远景 | 人物在环境中 | `long shot`, `wide shot`, `establishing shot` |

### 镜头类型

| 镜头 | 焦距 | 效果 | 提示词 |
|------|------|------|--------|
| 超广角 | 14-24mm | 夸张透视，大场景 | `ultra wide angle`, `fisheye` |
| 广角 | 24-35mm | 场景感，透视明显 | `wide angle lens`, `24mm`, `35mm` |
| 标准 | 50mm | 自然视角 | `50mm lens`, `standard lens` |
| 中长焦 | 85-135mm | 人像，背景虚化 | `85mm portrait`, `135mm telephoto` |
| 长焦 | 200mm+ | 压缩透视，远摄 | `telephoto lens`, `200mm`, `compression` |

---

## 景深与焦距

### 景深类型

| 类型 | 说明 | 效果 | 提示词 |
|------|------|------|--------|
| 浅景深 | 只有主体清晰 | 突出主体，背景虚化 | `shallow depth of field`, `bokeh`, `blurred background` |
| 深景深 | 前后都清晰 | 全景清晰，场景感 | `deep depth of field`, `everything in focus` |
| 移轴 | 微缩效果 | 玩具感 | `tilt-shift`, `miniature effect` |

### 焦外效果 (Bokeh)

| 焦外类型 | 说明 | 提示词 |
|----------|------|--------|
| 奶油焦外 | 柔滑圆形 | `creamy bokeh`, `smooth bokeh` |
| 旋转焦外 | 旋转形状 | `swirly bokeh`, `vintage bokeh` |
| 光斑焦外 | 光点形状 | `bokeh balls`, `light orbs` |
| 口径蚀 | 边缘变形 | `cat's eye bokeh`, `optical vignetting` |

### 焦点控制

| 焦点位置 | 效果 | 提示词 |
|----------|------|--------|
| 前景对焦 | 前景清晰，背景虚化 | `focus on foreground`, `front focus` |
| 中景对焦 | 中间清晰 | `focus on middle ground` |
| 背景对焦 | 背景清晰，前景虚化 | `focus on background`, `back focus` |
| 追焦 | 追踪运动主体 | `tracking focus`, `motion tracking` |

---

## 空间与层次

### 画面层次

```
前景 (Foreground)
  │
  ├─ 引导元素
  ├─ 框架元素
  └─ 增加深度
  │
中景 (Middle Ground)
  │
  ├─ 主体
  ├─ 陪体
  └─ 主要活动
  │
背景 (Background)
  │
  ├─ 环境信息
  ├─ 氛围营造
  └─ 空间延伸
```

### 空间深度技巧

| 技巧 | 说明 | 提示词 |
|------|------|--------|
| 空气透视 | 远处偏蓝偏淡 | `atmospheric perspective`, `aerial perspective` |
| 大小对比 | 近大远小 | `size contrast`, `scale reference` |
| 重叠遮挡 | 前景遮挡背景 | `overlapping elements`, `depth through overlap` |
| 线条透视 | 平行线汇聚 | `linear perspective`, `converging lines` |
| 色彩透视 | 远处色彩变淡 | `color perspective`, `distant colors fade` |

### 画面空间感

| 空间感 | 说明 | 提示词 |
|--------|------|--------|
| 开放空间 | 大量留白，呼吸感 | `open space`, `negative space`, `breathing room` |
| 封闭空间 | 充满画面，压迫感 | `tight framing`, `filled frame` |
| 纵深空间 | 强烈深度感 | `deep space`, `receding planes` |
| 平面空间 | 弱化深度 | `flat space`, `graphic composition` |

---

## 构图提示词模板

### 人像构图模板

```
[构图类型] portrait, [视角], [景深], [焦点], [留白方向]

示例:
Rule of thirds portrait, eye level angle, shallow depth of field with creamy bokeh, focus on eyes, subject looking into space with negative space on right side
```

### 风景构图模板

```
[构图类型] landscape, [视角], [层次描述], [引导线], [空间感]

示例:
Leading lines landscape, low angle view, strong foreground rock formation, middle ground lake, distant mountains, river leading eye to horizon, deep space with atmospheric perspective
```

### 建筑构图模板

```
[构图类型] architecture, [视角], [对称性], [透视], [框架]

示例:
Symmetrical architectural shot, looking up at cathedral ceiling, perfect vertical symmetry, strong converging lines, ornate Gothic arches framing the space
```

### 动态构图模板

```
[构图类型], [运动方向], [留白], [动感元素]

示例:
Dynamic diagonal composition, car moving from left to right, negative space in front of vehicle, motion blur on wheels, sense of speed and movement
```

---

## 构图分析检查清单

分析图片构图时检查：

- [ ] 主体位置（三分点/中心/偏离中心）
- [ ] 画面层次（前景/中景/背景）
- [ ] 视角角度（平视/仰视/俯视）
- [ ] 景深控制（浅景深/深景深）
- [ ] 引导线条（是否存在，方向如何）
- [ ] 对称性（是否对称，对称类型）
- [ ] 框架元素（是否有前景框架）
- [ ] 空间感（开放/封闭/纵深）
- [ ] 焦点位置（前景/中景/背景）
- [ ] 留白方向（主体朝向哪侧留白）

---

## 构图关键词速查表

| 构图类型 | 关键词 |
|----------|--------|
| 三分法 | rule of thirds, grid composition |
| 黄金分割 | golden ratio, fibonacci, golden spiral |
| 对称 | symmetrical, mirror, balanced |
| 对角线 | diagonal, dynamic, angular |
| 框架 | framing, frame within frame |
| 引导线 | leading lines, converging lines |
| 中心 | centered, central composition |
| 极简 | minimal, negative space, simple |
| 填满 | fill frame, tight crop |
| 层次 | layered, depth, foreground interest |
