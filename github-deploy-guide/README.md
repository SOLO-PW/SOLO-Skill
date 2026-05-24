# github-deploy-guide

**为 GitHub 开源项目自动生成面向小白的部署教程。**

你只需要提供一个 GitHub 项目链接，这个 Skill 就能自动检测项目文档、提取安装步骤，生成一篇从环境准备到部署完成的完整 Markdown 教程。

---

## 它能做什么？

把 GitHub 链接丢进去 → 拿到一份完整可用的部署教程，整个过程不需要你手动翻文档、查依赖版本、试配置项。

**核心流程：**

```
用户提供 GitHub 链接
        │
        ▼
解析链接 → 获取仓库元数据（语言/Stars/协议/最近更新）
        │
        ▼
检测文档文件（README / INSTALL / docs/ 等）
   ┌────┴────┐
  有文档      无文档
   │           │
   │           └─→ 回退链：zread.ai → Wiki → Issues → Releases
   │
   └────┬──────┘
        ▼
评估部署模式（PaaS 优先 / Docker 优先 / 本地优先）
        │
        ▼
生成部署教程 → 保存为 .md 文件
```

---

## 主要特性

### 🔍 智能文档检测
自动按优先级检测 README.md、INSTALL.md、docs/installation.md、CONTRIBUTING.md、SETUP.md 等 7 种常见的文档路径。

### 🔁 三级回退链
当项目没有 README 时，依次尝试：
1. **zread.ai** — 替换 `github.com` 为 `zread.ai` 获取 AI 总结文档
2. **GitHub Wiki** — 检查 Wiki 页面
3. **GitHub Issues** — 搜索与安装/部署相关的 Issue

如果项目有 Release 预编译二进制，还会提供快速安装方式。

### 🎯 部署模式自适应
根据项目文件自动判断推荐部署方式，环境要求按模式区分展示：

| 模式 | 适用场景 | 环境要求呈现 |
|------|---------|-------------|
| **PaaS 优先** | 纯静态/前端项目（有 vercel.json 等） | 线上部署为主，本地环境折叠为可选 |
| **Docker 优先** | 存在 Dockerfile | 本地和线上要求并列展示 |
| **云服务器优先** | 存在 nginx.conf/systemd 引用 | 本地环境可选，服务器部署为主 |
| **本地优先** | CLI 工具、桌面应用 | 本地环境为必选 |

### 🌐 多场景部署
每个教程按检测结果包含对应的部署章节：
- **本地开发**：虚拟环境、依赖安装、环境变量配置、启动命令
- **Docker**：Dockerfile 示例、docker-compose、健康检查
- **云服务器**：Nginx 反向代理、SSL 证书、systemd/PM2 进程管理
- **Kubernetes**：Deployment、Service、Ingress YAML 模板
- **PaaS**：Vercel/Netlify/Railway/Render 部署步骤

### 💻 多语言支持
覆盖 8 种主流语言的依赖安装模板和国内镜像源配置，中文教程自动使用国内镜像（清华 pip、淘宝 npm 等）。

### 📦 特殊项目类型
- **全栈项目**：前后端分别部署 + CORS 配置
- **AI/ML 项目**：GPU 驱动安装、模型下载（含国内 HF 镜像）
- **Monorepo**：pnpm workspace、Turborepo 等工具
- **数据库依赖**：Docker 一键启动数据库 + 迁移命令
- **CLI 工具**：全局安装方式 + 使用示例

### 📊 增强分析
- 项目健康度评估（活跃/降级/停止维护）
- Makefile 自动检测和命令提取
- .env.example 自动解析为配置表格
- 依赖安全检查建议

---

## 生成教程结构

```
{repo}-deploy-guide.md
├── 项目简介 + 项目信息卡片（Stars/Forks/协议/最近更新）
├── 环境准备
│   ├── 线上部署要求（PaaS 优先模式下）
│   └── 本地开发环境要求（可根据模式折叠）
├── 获取项目代码（Git 克隆 / ZIP 下载）
├── 本地开发部署（依赖安装 / 配置 / 启动 / 验证）
├── Docker 容器化部署（按需）
├── 云服务器部署（按需）
├── Kubernetes 部署（按需）
├── PaaS 一键部署（按需）
├── 依赖安全检查
└── 常见问题
```

---

## 文件结构

```
github-deploy-guide/
├── SKILL.md                              # 主文件：工作流定义 + 各场景指南
└── references/
    ├── tutorial-template.md              # 教程输出模板
    ├── lang-deps.md                      # 8 种语言的依赖安装模板和国内镜像源
    ├── deploy-examples.md                # Dockerfile/Nginx/数据库/K8s 完整配置示例
    ├── special-projects.md               # 全栈/AI-ML/Monorepo/CLI 特殊处理
    └── advanced-detection.md             # Releases/Makefile/健康度/安全检查
```

---

## 快速使用

在对话中告诉 SOLO：

```
使用 github-deploy-guide 为 https://github.com/用户名/仓库名 生成部署教程
```

Skill 会自动执行完整工作流并在工作区输出 `{仓库名}-deploy-guide.md`。

### 已有示例

用 `https://github.com/ChaseToDream/TRAE-post` 生成的教程可见同目录下的 [TRAE-post-deploy-guide.md](../TRAE-post-deploy-guide.md)。

---

## 适用场景

- 看到 GitHub 上感兴趣的开源项目，想快速部署试用
- 项目 README 写得太简略或没有安装说明
- 不熟悉某个技术栈，需要从零开始的详细指引
- 分享项目给非技术背景的团队成员，需要一份小白友好教程

---

## 注意事项

- **私有仓库**：zread.ai 和 Wiki 无法访问，需用户直接提供文档内容
- **API 速率限制**：GitHub API 受限时会直接走回退链
- **文档为空**：即使 README 存在但没有安装信息，会自动走回退链补充
- **项目停维护**：在教程开头添加醒目提示
