# SOLO-Skill

SOLO 技能创作赛的个人 skill 集合。仓库内共 16 个独立 skill，每个 skill 位于独立目录，包含 SKILL.md（执行规范）、README.md（说明文档）、references/（进阶参考）以及可选的 scripts/（脚本工具）。

## Skill 索引

| 目录 | SKILL.md | 说明 |
|------|----------|------|
| [bilibili-up-analyzer](bilibili-up-analyzer/SKILL.md) | [SKILL.md](bilibili-up-analyzer/SKILL.md) | Bilibili UP主视频数据分析与报告生成 |
| [break-up](break-up/SKILL.md) | [SKILL.md](break-up/SKILL.md) | 基于聊天记录的阻抗式分手话术生成 |
| [career-analysis](career-analysis/SKILL.md) | [SKILL.md](career-analysis/SKILL.md) | 就业方向分析与发展路径规划 |
| [classical-poetry-composer](classical-poetry-composer/SKILL.md) | [SKILL.md](classical-poetry-composer/SKILL.md) | 标准唐诗宋词创作与格律校验 |
| [girlfriend-emotion-advisor](girlfriend-emotion-advisor/SKILL.md) | [SKILL.md](girlfriend-emotion-advisor/SKILL.md) | 女友话术分析与情绪解读 |
| [github-deploy-guide](github-deploy-guide/SKILL.md) | [SKILL.md](github-deploy-guide/SKILL.md) | GitHub 开源项目小白部署教程生成 |
| [github-repo-summarizer](github-repo-summarizer/SKILL.md) | [SKILL.md](github-repo-summarizer/SKILL.md) | 开源项目通俗推荐介绍文生成 |
| [image-prompt-reverse](image-prompt-reverse/SKILL.md) | [SKILL.md](image-prompt-reverse/SKILL.md) | AI 绘图提示词反推工具 |
| [internet-nonsense-generator](internet-nonsense-generator/SKILL.md) | [SKILL.md](internet-nonsense-generator/SKILL.md) | 互联网废话文学生成器 |
| [internet-slang-decoder](internet-slang-decoder/SKILL.md) | [SKILL.md](internet-slang-decoder/SKILL.md) | 网络缩写与网络用语解析器 |
| [poetry-match](poetry-match/SKILL.md) | [SKILL.md](poetry-match/SKILL.md) | 古诗词意境匹配推荐 |
| [skill-fusion](skill-fusion/SKILL.md) | [SKILL.md](skill-fusion/SKILL.md) | 多 Skill 融合器 |
| [skill-post-writer](skill-post-writer/SKILL.md) | [SKILL.md](skill-post-writer/SKILL.md) | SOLO 技能创作赛推广帖撰写 |
| [trae-custom-model](trae-custom-model/SKILL.md) | [SKILL.md](trae-custom-model/SKILL.md) | TRAE/SOLO 自定义模型配置助手 |
| [trae-user-distiller](trae-user-distiller/SKILL.md) | [SKILL.md](trae-user-distiller/SKILL.md) | Trae 论坛用户数字人格蒸馏 |
| [turtle-soup-creator](turtle-soup-creator/SKILL.md) | [SKILL.md](turtle-soup-creator/SKILL.md) | 海龟汤文案创作 |

## 目录规范（全仓库统一约定）

为保证一致性并避免文档失同步，所有 skill 目录遵循以下约定：

- **SKILL.md = 执行规范**：即模型执行该技能时读取的指令 prompt，包含 frontmatter、概述、工作流程、规则、references 索引。运行时的操作细节一律只在此文件。
- **README.md = 说明文档**：面向人的简介，包含技能是什么、能做什么、适用场景、目录结构、快速使用示例。不复制 SKILL.md 的执行细节。
- **references/ = 进阶参考**：示例、模板、长表格、领域知识等非核心流程内容，由 SKILL.md 按需引用，避免主文件臃肿。
- **scripts/ = 脚本工具**：可执行脚本需配套 `requirements.txt` 声明第三方依赖；仅用标准库的脚本在 requirements.txt 中注明即可。
- **frontmatter**：统一使用 YAML 块引号（`description: |`）规范，`name` 与目录名强一致且不加引号。

## 渐进式披露

内容型 skill 应保持主文件克制：笼统规则与流程留在 SKILL.md，大量示例/模板/领域资料下沉到 references。主文件建议控制在 300 行以内，超过时优先抽取 references。

## FAQ

**Q1：技能脚本用到哪些第三方依赖？**
A：含 `scripts/` 的目录均提供 `requirements.txt`。目前仅 bilibili-up-analyzer（requests、matplotlib）与 trae-user-distiller（requests、urllib3）有第三方依赖；其余脚本仅使用 Python 标准库。

**Q2：SKILL.md 与 README.md 内容为什么不一样？**
A：SKILL.md 是模型执行时的指令（执行规范），README.md 面向人类读者（说明文档）。两者职责边界见上文「目录规范」，避免重复与失同步。

**Q3：技能主文件太长怎么办？**
A：按「渐进式披露」原则，将示例、模板、长表格抽到 `references/`，在 SKILL.md 中仅保留流程与引用链接。

**Q4：为什么 frontmatter 统一用 `|`？**
A：多行描述统一使用 YAML 块引号（literal block scalar）规范，避免纯文本/双引号/折叠等混用造成的解析与维护不一致；`name` 保持与目录名强一致。

**Q5：如何为一个 skill 新增脚本？**
A：将脚本放入 `scripts/`，同步新增/更新 `requirements.txt`，并在 SKILL.md 的脚本使用章节补充调用示例。