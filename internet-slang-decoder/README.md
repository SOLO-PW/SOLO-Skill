# Internet Slang Decoder

互联网缩写和网络用语解析 Skill，覆盖 7 大领域、490+ 词条。

## 支持领域

| 领域 | 示例缩写 | 词条数 |
|------|---------|--------|
| 娱乐圈/饭圈 | yyds, xswl, awsl, kswl, u1s1 | 55 |
| 游戏圈 | gg, op, mvp, afk, gank, carry | 76 |
| 生活/网络 | btw, lol, omg, ngl, fr, bruh | 108 |
| 科技/互联网 | api, pr, k8s, grpc, lgtm, ci/cd | 152 |
| 动漫/二次元 | tsundere, isekai, otaku, gacha | 33 |
| 金融/商业 | nft, defi, hodl, fomo, whale | 46 |
| 学术/教育 | gpa, sci, phd, mba, toefl, ielts | 23 |

## 文件结构

```
internet-slang-decoder/
├── SKILL.md                    # Skill 入口（触发条件 + 工作流 + 规则）
├── README.md                   # 本文件
├── scripts/
│   ├── decoder.py              # 核心解析器
│   ├── search_slang.py         # 搜索验证工具
│   ├── build_refs.py           # JSON → MD 生成器
│   └── slang_db.json           # 词条数据源（493条）
└── references/
    ├── methodology.md          # 方法论（搜索闭环、验证机制）
    ├── result-schema.md        # 输出格式规范
    ├── templates.md            # 交互话术模板
    ├── ambiguous-abbreviations.md
    ├── entertainment.md        # 各领域词典（自动生成）
    ├── gaming.md
    ├── lifestyle.md
    ├── tech.md
    ├── anime.md
    ├── finance.md
    └── academic.md
```

## 使用示例

### 文本输出
```
$ python scripts/decoder.py "yyds 这个太op了，xswl"

原文：yyds 这个太op了，xswl

✓ 识别到 3 个缩写：

【xswl】→ 笑死我了 | 娱乐圈 | 95%
【yyds】→ 永远的神 | 娱乐圈 | 95%
【op】  → overpowered / opening（多义）
```

### JSON 输出
```bash
python scripts/decoder.py "gg wp" --format json
```

### Markdown 输出
```bash
python scripts/decoder.py "api ui ux" --format markdown
```

### 带上下文
```bash
python scripts/decoder.py "gg" --context "游戏"
```

## 数据维护

词条数据存储在 `scripts/slang_db.json`，是唯一的权威数据源。

```bash
# 编辑 slang_db.json 后，重新生成 references/*.md
python scripts/build_refs.py
```
