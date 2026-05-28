# GitHub 开源项目推荐文章生成器

将 GitHub 仓库转化为通俗易懂的推荐文章，面向普通群众，用轻松有趣的语言介绍开源项目。

## ✨ 功能特点

- **零技术门槛**：自动将技术术语转化为日常用语
- **轻松有趣**：像朋友推荐好物一样自然亲切
- **视觉友好**：多用 emoji、结构清晰、易于阅读
- **智能分析**：自动提取项目亮点、使用场景、社区数据

## 🎯 使用场景

- 向非技术朋友介绍有趣的开源项目
- 为技术博客生成通俗易懂的项目推荐
- 快速了解一个 GitHub 仓库的核心价值

## 📝 使用方法

只需提供 GitHub 仓库链接，即可生成推荐文章：

```
用户：帮我介绍一下 https://github.com/xxx/xxx
```

支持的 URL 格式：
- `https://github.com/用户名/仓库名`
- `https://github.com/用户名/仓库名.git`
- `git@github.com:用户名/仓库名.git`

## 📊 数据解读

| 指标 | 通俗解读 |
|------|----------|
| Star > 10000 | 🔥 超火项目，大家都在用！ |
| Star > 1000 | ⭐ 很受欢迎，社区活跃 |
| 更新 < 7 天 | 🚀 维护超积极 |
| 更新 < 30 天 | ✅ 定期更新，稳定可靠 |
| MIT 许可 | 🎉 随便用，很自由 |

## 📁 文件结构

```
github-repo-summarizer/
├── SKILL.md                           # 核心技能定义
├── README.md                          # 本文件
└── references/
    ├── article-generation-guide.md    # 文章生成详细指南
    ├── article-templates.md           # 文章模板库
    ├── quick-reference.md             # 快速参考卡片
    ├── interaction-templates.md       # 交互式提问模板
    ├── troubleshooting-guide.md       # 常见问题处理指南
    ├── tech-stack-analysis-guide.md   # 技术栈分析指南
    ├── tech-stack-identification.md   # 技术栈识别规则
    ├── quality-assessment.md          # 质量评估标准
    ├── readme-quality-assessment.md   # README 质量评估
    └── github-api-guide.md            # GitHub API 使用指南
```

## 💡 示例输出

```markdown
# TailwindCSS：让你的网页颜值瞬间拉满！

![TailwindCSS 示例](https://tailwindcss.com/...)

## 🌟 这是什么？
TailwindCSS 是一个超实用的 CSS 框架，让你不用写一行 CSS 代码，
就能做出超好看的网页！

## ✨ 有什么亮点？
- **零配置**：开箱即用，不用折腾
- **颜值在线**：自带现代感设计
- **手机电脑都能用**：自动适配各种屏幕

## 🎯 能用来做什么？
- **个人博客**：5分钟做出专业级博客
- **公司官网**：快速搭建漂亮的企业网站
- **产品原型**：快速验证设计想法
```

## ⚠️ 注意事项

- 仅支持公开仓库，私有仓库需要访问权限
- 建议提供完整的仓库链接（包含 `https://`）
- 生成的文章会自动保存为 Markdown 文件

## 📚 相关资源

- [SKILL.md](./SKILL.md) - 核心技能定义
- [references/article-templates.md](./references/article-templates.md) - 更多文章模板
- [references/troubleshooting-guide.md](./references/troubleshooting-guide.md) - 问题排查指南
