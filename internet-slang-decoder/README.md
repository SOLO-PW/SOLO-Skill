# Internet Slang Decoder

互联网缩写和网络用语解析工具，覆盖娱乐圈、游戏圈、生活网络、科技互联网、动漫、金融等多个领域。

## 功能

- **多领域缩写解析**：内置 150+ 常见缩写，覆盖 6 大领域
- **多义性处理**：同一缩写多种含义时，按置信度排序展示
- **上下文感知**：自动从文本关键词推断领域，提升匹配精度
- **网络搜索补充**：对未知缩写自动调用 WebSearch 搜索并回填
- **准确性验证**：多源交叉验证，置信度分级标注

## 触发示例

| 用户输入 | 触发 |
|---------|------|
| "yyds 是什么意思" | ✅ |
| "这句话里的缩写帮我看看" | ✅ |
| "游戏术语 op 是什么" | ✅ |
| "什么是人工智能" | ❌ 非缩写类 |

## 文件结构

```
internet-slang-decoder/
├── SKILL.md                              # Skill 主文档
├── scripts/
│   ├── decoder.py                        # 核心解析器
│   └── search_slang.py                   # 搜索验证工具
└── references/
    ├── methodology.md                    # 解析方法论
    ├── ambiguous-abbreviations.md        # 多义缩写对照表
    ├── templates.md                      # 交互话术模板
    ├── entertainment.md                  # 娱乐圈词典
    ├── gaming.md                         # 游戏圈词典
    ├── lifestyle.md                      # 生活/网络词典
    └── tech.md                           # 科技/互联网词典
```

## 快速使用

```bash
# 解析文本中的缩写
python scripts/decoder.py "yyds，这波操作太op了"

# 带上下文解析（提升准确度）
python scripts/decoder.py "gg wp" --context "游戏"

# JSON 输出
python scripts/decoder.py "xswl" --json

# 搜索未知缩写
python scripts/search_slang.py "xdd" --context "娱乐"
```

## 覆盖领域

| 领域 | 示例缩写 |
|------|---------|
| 娱乐圈/饭圈 | yyds, xswl, awsl, zqsg, kswl, u1s1 |
| 游戏圈 | gg, op, mvp, afk, buff, nerf, gank |
| 生活/网络 | btw, fyi, asap, tbh, dm, lol, ngl |
| 科技/互联网 | api, ui, pr, lgtm, wip, k8s, ci/cd |
| 动漫/二次元 | （通过搜索补充） |
| 金融/商业 | （通过搜索补充） |

## 工作原理

```
用户输入 → 本地库查询 → 命中 → 排序输出
                     → 未命中 → WebSearch → 解析验证 → 回填 → 输出
```

## 依赖

- Python 3.6+
- 无第三方依赖
