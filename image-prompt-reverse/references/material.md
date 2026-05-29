# 材质识别专项指南

本文档提供系统化的材质识别方法，帮助精准提取图片中的材质元素并转换为提示词。

---

## 目录

1. [材质基础](#材质基础)
2. [自然材质](#自然材质)
3. [人造材质](#人造材质)
4. [织物材质](#织物材质)
5. [表面处理](#表面处理)
6. [材质提示词模板](#材质提示词模板)

---

## 材质基础

### 材质三要素

| 要素 | 说明 | 提示词关联 |
|------|------|------------|
| 质地 | 表面纹理特征 | smooth, rough, grainy, textured |
| 光泽 | 反光程度 | glossy, matte, shiny, dull |
| 触感 | 视觉触感 | soft, hard, silky, coarse |

### 材质分类

| 类别 | 包含材质 | 特点 |
|------|----------|------|
| 自然材质 | 木、石、皮、毛 | 有机纹理，不规则 |
| 人造材质 | 金属、玻璃、塑料 | 规则纹理，均匀 |
| 织物材质 | 棉、丝、羊毛、皮革 | 编织纹理，柔软 |
| 复合材质 | 碳纤维、混凝土 | 混合特征 |

---

## 自然材质

### 木材

| 木材类型 | 纹理特征 | 适用场景 | 提示词 |
|----------|----------|----------|--------|
| 原木 | 粗糙树皮，明显年轮 | 乡村风格 | raw wood, rustic timber, bark texture |
| 抛光木 | 光滑，细腻木纹 | 家具 | polished wood, smooth timber, wood grain |
| 旧木 | 风化痕迹，裂纹 | 复古风格 | weathered wood, aged timber, distressed |
| 竹子 | 细长纹理，节状 | 东方风格 | bamboo, bamboo texture, bamboo grain |

### 石材

| 石材类型 | 纹理特征 | 适用场景 | 提示词 |
|----------|----------|----------|--------|
| 大理石 | 流动纹理，光泽 | 高端装饰 | marble, marble texture, veined marble |
| 花岗岩 | 颗粒状，坚硬 | 建筑外墙 | granite, speckled stone, granite texture |
| 砂岩 | 粗糙，颗粒感 | 园林景观 | sandstone, rough stone, sandy texture |
| 板岩 | 层状，暗色 | 屋顶地板 | slate, layered stone, dark slate |
| 鹅卵石 | 光滑，圆形 | 河边场景 | pebbles, river stones, smooth rocks |

### 皮革

| 皮革类型 | 纹理特征 | 适用场景 | 提示词 |
|----------|----------|----------|--------|
| 光面皮 | 光滑，细腻 | 时尚配饰 | smooth leather, polished leather |
| 磨砂皮 | 哑光，柔软 | 休闲风格 | suede, nubuck, matte leather |
| 鳄鱼皮 | 方块纹理，昂贵 | 奢侈品 | crocodile leather, exotic skin, scaled |
| 蛇皮 | 细密鳞片，光泽 | 时尚前卫 | snakeskin, reptile skin, scaled texture |
| 旧皮 | 磨损痕迹，复古 | 复古风格 | aged leather, worn leather, patina |

### 毛发

| 毛发类型 | 特征 | 适用场景 | 提示词 |
|----------|------|----------|--------|
| 人类毛发 | 丝滑，有光泽 | 人像摄影 | silky hair, shiny hair, flowing hair |
| 动物毛皮 | 浓密，柔软 | 动物摄影 | fur, fluffy fur, animal fur |
| 羊毛 | 卷曲，蓬松 | 服装面料 | wool, woolly texture, sheep wool |
| 羽毛 | 轻盈，层叠 | 装饰元素 | feathers, plumage, soft feathers |

---

## 人造材质

### 金属

| 金属类型 | 特征 | 适用场景 | 提示词 |
|----------|------|----------|--------|
| 黄金 | 金黄色，高贵 | 珠宝首饰 | gold, golden, golden metallic |
| 白银 | 银白色，冷调 | 现代设计 | silver, silver metallic, polished silver |
| 铜 | 红棕色，复古 | 复古装饰 | copper, bronze, brass, patina copper |
| 钢铁 | 冷灰色，工业 | 工业风格 | steel, stainless steel, chrome |
| 铝 | 浅灰，轻盈 | 现代产品 | aluminum, brushed aluminum, matte metal |
| 钛 | 深灰，高端 | 高端产品 | titanium, dark metal, aerospace metal |

### 金属表面处理

| 处理方式 | 效果 | 提示词 |
|----------|------|--------|
| 抛光 | 镜面反射 | polished, mirror finish, reflective |
| 拉丝 | 细密纹理 | brushed, satin finish, directional grain |
| 磨砂 | 哑光质感 | matte, frosted, sandblasted |
| 电镀 | 光亮表面 | chrome plated, electroplated, shiny |
| 氧化 | 古旧效果 | oxidized, patina, aged metal |

### 玻璃

| 玻璃类型 | 特征 | 适用场景 | 提示词 |
|----------|------|----------|--------|
| 透明玻璃 | 完全透明 | 窗户器皿 | clear glass, transparent, see-through |
| 磨砂玻璃 | 半透明 | 隐私隔断 | frosted glass, translucent, obscured |
| 彩色玻璃 | 色彩丰富 | 教堂装饰 | stained glass, colored glass, mosaic |
| 钢化玻璃 | 坚硬，安全 | 建筑幕墙 | tempered glass, safety glass, toughened |
| 碎裂玻璃 | 裂纹效果 | 艺术效果 | cracked glass, shattered, broken glass |

### 塑料

| 塑料类型 | 特征 | 适用场景 | 提示词 |
|----------|------|----------|--------|
| 光面塑料 | 光滑，反光 | 电子产品 | glossy plastic, smooth plastic, shiny |
| 磨砂塑料 | 哑光，细腻 | 家用品 | matte plastic, soft-touch plastic |
| 透明塑料 | 半透明 | 包装材料 | transparent plastic, clear plastic |
| 橡胶 | 柔软，防滑 | 手柄握把 | rubber, rubbery texture, soft grip |

---

## 织物材质

### 天然纤维

| 织物类型 | 特征 | 适用场景 | 提示词 |
|----------|------|----------|--------|
| 棉布 | 柔软，透气 | 日常服装 | cotton, cotton fabric, soft cotton |
| 亚麻 | 粗糙纹理，自然 | 夏季服装 | linen, linen fabric, natural linen |
| 丝绸 | 光滑，光泽 | 高端服装 | silk, silky smooth, lustrous silk |
| 羊毛 | 温暖，柔软 | 冬季服装 | wool, woolen, warm wool |
| 羊绒 | 极致柔软 | 奢侈品 | cashmere, soft cashmere, luxurious |

### 人造纤维

| 织物类型 | 特征 | 适用场景 | 提示词 |
|----------|------|----------|--------|
| 涤纶 | 耐用，挺括 | 运动服装 | polyester, synthetic fabric |
| 尼龙 | 光滑，轻盈 | 户外装备 | nylon, nylon fabric, smooth nylon |
| 雪纺 | 轻薄，透明 | 礼服裙装 | chiffon, sheer fabric, flowing chiffon |
| 蕾丝 | 镂空，精致 | 婚纱内衣 | lace, delicate lace, intricate lacework |
| 天鹅绒 | 柔软，光泽 | 高端装饰 | velvet, plush velvet, velvety |

### 特殊织物

| 织物类型 | 特征 | 适用场景 | 提示词 |
|----------|------|----------|--------|
| 牛仔布 | 厚实，蓝色 | 休闲服装 | denim, jeans fabric, blue denim |
| 灯芯绒 | 纵向条纹 | 复古风格 | corduroy, ribbed fabric, corded |
| 皮革 | 光滑，坚韧 | 机车风格 | leather, leather texture, faux leather |
| 毛皮 | 浓密，保暖 | 冬季配饰 | fur, faux fur, fluffy fur |
| 金属丝 | 闪亮，硬挺 | 舞台服装 | metallic fabric, shimmer, sequined |

---

## 表面处理

### 光泽度

| 光泽类型 | 效果 | 提示词 |
|----------|------|--------|
| 高光 | 强烈反射 | high gloss, mirror-like, ultra shiny |
| 半光 | 温和反射 | semi-gloss, satin finish, soft sheen |
| 哑光 | 无反射 | matte, flat finish, no shine |
| 丝光 | 柔和光泽 | silky, lustrous, soft glow |

### 纹理效果

| 纹理类型 | 效果 | 提示词 |
|----------|------|--------|
| 光滑 | 无纹理 | smooth, silky, glass-like |
| 粗糙 | 明显纹理 | rough, coarse, gritty |
| 颗粒 | 细小凸起 | grainy, sandy, speckled |
| 凹凸 | 不规则起伏 | bumpy, uneven, textured |
| 编织 | 交叉纹理 | woven, braided, interlaced |

### 特殊效果

| 效果类型 | 描述 | 提示词 |
|----------|------|--------|
| 生锈 | 氧化腐蚀 | rusty, corroded, oxidized |
| 风化 | 自然老化 | weathered, aged, worn |
| 碎裂 | 裂纹效果 | cracked, fractured, crazed |
| 剥落 | 涂层脱落 | peeling, flaking, chipped |
| 烧焦 | 火烧痕迹 | burnt, charred, scorched |

---

## 材质提示词模板

### 单材质描述

```
[材质类型], [表面处理], [光泽度], [颜色]

示例:
polished marble, smooth surface, high gloss, white with gray veins
```

### 多材质组合

```
[主体材质] with [装饰材质], [对比效果]

示例:
smooth wooden table with metal legs, warm wood contrasting cool steel
```

### 材质特写

```
[材质] close-up, [纹理细节], [光照效果]

示例:
leather close-up, detailed grain texture, soft side lighting highlighting texture
```

### 材质氛围

```
[材质] creating [氛围], [整体效果]

示例:
rough exposed brick creating industrial atmosphere, raw and authentic feel
```

---

## 材质识别检查清单

分析图片材质时检查：

- [ ] 主要材质类型（自然/人造/织物）
- [ ] 表面处理方式（抛光/磨砂/氧化等）
- [ ] 光泽度（高光/半光/哑光）
- [ ] 纹理特征（光滑/粗糙/编织等）
- [ ] 颜色和色调
- [ ] 材质组合方式
- [ ] 特殊效果（生锈/风化/碎裂等）
- [ ] 材质与整体风格的协调性

---

## 材质关键词速查表

| 类别 | 关键词 |
|------|--------|
| 光滑 | smooth, sleek, polished, glass-like, silky |
| 粗糙 | rough, coarse, gritty, textured, grainy |
| 金属 | metallic, chrome, gold, silver, copper, steel |
| 玻璃 | glass, transparent, frosted, crystal, clear |
| 木材 | wood, timber, wooden, oak, bamboo, rustic |
| 石材 | stone, marble, granite, slate, pebble |
| 皮革 | leather, suede, nubuck, faux leather, worn |
| 织物 | fabric, cotton, silk, wool, velvet, linen |
| 塑料 | plastic, glossy, matte, rubber, synthetic |
| 特殊 | rusty, weathered, cracked, aged, patina |
