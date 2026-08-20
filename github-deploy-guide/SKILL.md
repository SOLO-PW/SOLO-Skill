---
name: github-deploy-guide
description: |
  为 GitHub 开源项目生成面向小白的部署教程。自动检测项目文档（README、INSTALL、docs/ 等），提取安装步骤，生成从环境准备到部署完成的分步 Markdown 教程。支持本地开发、Docker、云服务器、Kubernetes、PaaS 等全场景部署，覆盖 Python/Node.js/Go/Rust/Java/PHP/Ruby/Swift 等主流语言，支持全栈/AI-ML/Monorepo/CLI 等特殊项目类型。当项目无 README 时，依次回退到 zread.ai、GitHub Wiki、GitHub Issues、Releases 获取文档。当用户提供 GitHub 链接并希望部署、安装或搭建某个开源项目时触发。
---

# GitHub 开源项目部署指南

为 GitHub 开源项目生成详细的、面向小白的部署教程。

## 参考文档索引

| 文件 | 用途 | 读取时机 |
|------|------|---------|
| [references/tutorial-template.md](references/tutorial-template.md) | 教程输出模板 | 每次生成教程时 |
| [references/lang-deps.md](references/lang-deps.md) | 多语言依赖安装模板（Go/Rust/Java/PHP/Ruby/Swift + 国内镜像源） | 检测到非 Python/Node.js 语言时 |
| [references/deploy-examples.md](references/deploy-examples.md) | 各场景完整配置示例（Dockerfile/Nginx/数据库/K8s） | 生成 Docker/服务器/K8s 章节时 |
| [references/special-projects.md](references/special-projects.md) | 特殊项目类型支持（全栈/AI-ML/Monorepo/CLI/数据库依赖） | 检测到特殊项目结构时 |
| [references/advanced-detection.md](references/advanced-detection.md) | 增强检测与分析（Releases/Makefile/健康度评估/.env 解析） | 需要补充信息时 |

## 工作流程

```
用户提供 GitHub 链接
        │
        ▼
解析链接 → 提取 owner/repo
        │
        ▼
获取仓库元数据（API）
 ├─ 基本信息（语言、分支、Stars、协议）
 ├─ 部署指示文件（Dockerfile/K8s/PaaS 配置）
 ├─ 项目类型检测（全栈/AI-ML/Monorepo/CLI）
 └─ 增强分析（Releases/Makefile/.env.example）
        │
        ▼
检测用户查询语言 ──→ 设置教程语言（中文/英文）
        │
        ▼
检测文档文件 ──────────────────────────┐
(README、INSTALL、docs/、Wiki 等)        │
        │                               │
   找到？                               否
   ┌────┘                               │
   ▼                                    ▼
获取并阅读文档                   尝试回退链：
   │                             1. zread.ai
   │                             2. GitHub Wiki
   │                             3. GitHub Issues
   │                             4. GitHub Releases
   │                             5. GitHub Discussions
   │                                   │
   └──────────┬────────────────────────┘
              ▼
     检测部署场景 + 项目类型
     (本地 / Docker / 服务器 / K8s / PaaS)
     (全栈 / AI-ML / Monorepo / CLI)
              │
              ▼
     生成部署教程
     ├─ 参照 tutorial-template.md（模板）
     ├─ 参照 lang-deps.md（语言依赖）
     ├─ 参照 deploy-examples.md（配置示例）
     ├─ 参照 special-projects.md（特殊类型）
     └─ 参照 advanced-detection.md（增强信息）
              │
              ▼
     输出 .md 文件到工作区
```

## 第一步：解析 GitHub 链接

从用户提供的链接中提取 `owner` 和 `repo`。支持以下格式：

- `https://github.com/{owner}/{repo}`
- `https://github.com/{owner}/{repo}.git`
- `https://github.com/{owner}/{repo}/tree/{branch}`
- `github.com/{owner}/{repo}`（简写）

如果链接无效或不是 GitHub 链接，提示用户提供正确的链接。

## 第二步：获取仓库元数据与增强分析

使用 GitHub API 获取仓库信息：

```
GET https://api.github.com/repos/{owner}/{repo}
```

### 基本信息提取

- 语言、默认分支、主题标签、描述
- Stars、Forks、开源协议、最近更新时间（用于健康度评估）

### 部署指示文件检测

- `Dockerfile` / `docker-compose.yml` → Docker 部署
- `kubernetes/` / `k8s/` / 含 K8s 资源类型的 `*.yaml` → K8s 部署
- `vercel.json` / `netlify.toml` / `railway.toml` / `render.yaml` → PaaS 部署
- `package.json` / `requirements.txt` / `go.mod` / `pom.xml` → 语言及依赖信息

### 项目类型检测

详细检测逻辑参见 [references/special-projects.md](references/special-projects.md)：

- **全栈项目**：同时存在 `frontend/` + `backend/` 等前后端目录
- **Monorepo**：存在 `pnpm-workspace.yaml`、`lerna.json`、`nx.json`、`turbo.json`
- **AI/ML 项目**：依赖中含 `torch`/`tensorflow`/`transformers`，或引用 GPU 镜像
- **数据库依赖项目**：`docker-compose.yml` 中含数据库服务
- **CLI 工具**：`package.json` 含 `bin` 字段，或 `Cargo.toml` 含 `[[bin]]`
- **桌面/移动应用**：存在 `electron/`、`tauri.conf.json`、`android/`、`ios/`

### 增强分析

详细逻辑参见 [references/advanced-detection.md](references/advanced-detection.md)：

- **GitHub Releases**：检查是否有预编译二进制文件，提供快速安装方式
- **Makefile / Justfile**：提取常用构建 target（install、build、dev、start）
- **.env.example**：自动解析环境变量，生成配置表格
- **项目健康度**：根据 Stars、最近更新时间评估维护状态

## 第三步：检测教程语言

根据用户查询语言匹配教程输出语言：
- 中文查询 → 中文教程，优先使用国内镜像源
- 英文查询 → 英文教程，使用默认源
- 其他语言 → 跟随用户语言

国内镜像源配置参见 [references/lang-deps.md](references/lang-deps.md)。

## 第四步：检测文档

通过 GitHub API 按优先级检查以下路径：

1. `README.md` / `README.rst` / `README.txt` / `README`
2. `INSTALL.md` / `INSTALL`
3. `INSTALLATION.md`
4. `docs/installation.md` / `docs/setup.md`
5. `docs/getting-started.md`
6. `CONTRIBUTING.md`（通常包含环境搭建说明）
7. `SETUP.md`

使用 GitHub API 检查文件是否存在：
```
GET https://api.github.com/repos/{owner}/{repo}/contents/{path}
```

获取已找到文件的原始内容：
```
GET https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}
```

**判断：**
- 找到任何文档文件 → 进入第五步 A
- 未找到任何文档 → 进入第五步 B（回退链）

## 第五步 A：处理已有文档

1. 获取所有已找到文档文件的原始内容
2. 合并并分析内容，重点关注：
   - 前置条件 / 依赖要求（语言版本、操作系统、依赖项）
   - 安装步骤（克隆、安装依赖、构建）
   - 配置步骤（环境变量、配置文件）
   - 运行 / 启动应用
   - 常见问题 / 故障排除

## 第五步 B：回退链（未找到文档）

按顺序尝试每个信息源，直到获取到有用内容：

### 回退 1：zread.ai

1. 转换 GitHub 链接：将 `github.com` 替换为 `zread.ai`
2. 使用 WebFetch 获取 zread.ai 页面
3. 提取项目概述、架构、安装说明和依赖信息

### 回退 2：GitHub Wiki

1. 检查仓库是否启用了 Wiki（`has_wiki: true`）
2. 使用 WebFetch 获取 Wiki 首页内容
3. 提取安装/部署相关内容

### 回退 3：GitHub Issues

1. 搜索与安装/部署相关的 Issue（label: setup/install/deployment）
2. 从 Issue 讨论和维护者回复中提取有用的安装信息

### 回退 4：GitHub Releases

1. 获取最新 Release 信息
2. 检查是否有预编译二进制文件和安装说明
3. 详见 [references/advanced-detection.md](references/advanced-detection.md)

### 回退 5：GitHub Discussions

1. 搜索标题中包含 "install"、"setup"、"deploy" 的讨论
2. 提取有用的安装信息

**所有回退均失败时：** 提示用户并建议手动查找文档来源。

## 第六步：检测部署场景与评估部署模式

### 检测部署场景

根据仓库元数据和文档，确定需要包含哪些部署场景：

| 场景 | 检测依据 |
|------|---------|
| **本地开发** | 始终检测 |
| **Docker** | 存在 `Dockerfile`、`docker-compose.yml`，或文档提到 Docker |
| **云服务器** | 存在 `nginx.conf`、`systemd` 引用，或文档提到服务器部署 |
| **Kubernetes** | 存在 `kubernetes/`、`k8s/` 目录，或 K8s YAML 清单 |
| **PaaS** | 存在 `vercel.json`、`netlify.toml`、`railway.toml`、`render.yaml` |

### 评估部署模式

根据检测结果确定教程的**推荐部署模式**，这会直接影响教程中环境要求的呈现方式：

| 模式 | 判断条件 | 环境要求呈现方式 |
|------|---------|----------------|
| **PaaS 优先**（纯静态/前端项目） | 存在 `vercel.json`/`netlify.toml`/`railway.toml`，且无后端运行时文件（如无 `package.json` scripts 中的 build 后端、无 `Dockerfile`） | 线上部署为主推荐，本地环境要求折叠为可选章节 |
| **Docker 优先** | 存在 `Dockerfile`/`docker-compose.yml`，文档推荐 Docker 部署 | Docker 作为主场景，本地和线上各自列出环境要求 |
| **云服务器优先** | 存在 `nginx.conf`、`systemd` 引用或文档提到服务器部署 | 云服务器作为主场景，本地环境可选 |
| **本地优先** | CLI 工具、桌面应用，或上述模式均不匹配 | 本地环境为必选项，线上部署为补充选项 |

**判断优先级：** PaaS 优先 > Docker 优先 > 云服务器优先 > 本地优先

如果用户查询中提到了特定部署场景，以用户指定为准。

包含所有检测到的场景，但根据推荐模式调整顺序和环境要求的呈现方式。

## 第七步：生成部署教程

按照 [references/tutorial-template.md](references/tutorial-template.md) 中的模板生成教程。

**核心原则：**
- 面向零基础小白编写 —— 假设用户没有任何先验知识
- 包含每一步操作，即使看起来很显然（如"打开终端"）
- 在相关时同时提供 Windows 和 macOS/Linux 命令
- 在有帮助时包含预期输出 / 截图描述
- 添加常见错误的故障排除章节
- 使用项目实际的语言、框架和工具（从仓库元数据检测）
- 包含前置条件的官方安装页面链接
- 中文用户优先使用国内镜像源

**环境要求分区原则（根据部署模式调整）：**

根据第六步评估的部署模式，按以下原则组织教程中的环境准备章节：

- **PaaS 优先模式（纯静态/前端项目）：**
  - 环境准备章节开头用提示框说明"本项目推荐线上部署，无需本地开发环境"
  - 「线上部署要求」作为默认展开的主章节：仅需 GitHub 账号（和可选 PaaS 平台账号）
  - 「本地开发环境要求」作为可折叠的 `<details>` 可选章节，标为"仅当需要在本地运行时才需要"
  - 目录中环境准备只显示为一项，但正文中通过折叠区分

- **Docker / 云服务器优先模式：**
  - 「本地开发环境要求」（可选，用于调试和开发）和「线上环境要求」（服务器配置、Docker 等）并列
  - 通过小节标题区分两类要求

- **本地优先模式：**
  - 「本地开发环境要求」为必选主章节，包含详细的系统要求和工具安装
  - 「线上部署要求」作为后续独立章节存在（如果有）

**语言依赖安装：** 参见 [references/lang-deps.md](references/lang-deps.md)，根据检测到的语言选择对应的安装命令和镜像源配置。

**场景配置示例：** 参见 [references/deploy-examples.md](references/deploy-examples.md)：
- **Docker**：按语言选择 Dockerfile 示例（Python/Node.js/Go/Java/Rust），含多阶段构建、docker-compose 完整示例
- **云服务器**：Nginx 高级配置（WebSocket/HTTPS/负载均衡）、数据库配置模板
- **Kubernetes**：StatefulSet、ConfigMap、Secret 完整示例

**特殊项目类型处理：** 参见 [references/special-projects.md](references/special-projects.md)：
- **全栈项目**：分别说明前后端环境准备、CORS 配置、完整 docker-compose
- **AI/ML 项目**：GPU 驱动安装、模型下载说明（含国内镜像）、显存要求
- **Monorepo**：工作区工具安装、按包构建命令
- **数据库依赖**：Docker 一键启动数据库、迁移命令、GUI 工具推荐
- **CLI 工具**：全局安装命令、使用示例（替换浏览器验证步骤）

**增强信息集成：** 参见 [references/advanced-detection.md](references/advanced-detection.md)：
- 项目信息卡片（Stars/Forks/协议/最近更新）
- 维护状态提示（活跃/降低/停止维护）
- Makefile 命令优先使用
- .env.example 自动解析为配置表格
- Releases 预编译二进制快速安装
- 依赖安全检查建议

## 第八步：输出

将生成的教程保存为 Markdown 文件：

- 文件名：`{repo}-deploy-guide.md`
- 位置：用户的工作区文件夹
- 生成后向用户提供文件链接

## 异常处理

- **无效链接**：提示用户提供有效的 GitHub 仓库链接
- **仓库未找到（404）**：提示用户仓库可能是私有的或已删除
- **API 速率限制（403）**：直接回退到 zread.ai，然后 Wiki，然后 Issues
- **zread.ai 不可用**：继续回退链中的下一个来源
- **所有回退均失败**：提示用户并建议手动查找文档来源
- **文档内容为空**：即使 README 存在但没有安装信息，也尝试回退链作为补充
- **私有仓库**：zread.ai 和 Wiki 无法使用；提示用户是否可以直接提供文档内容
- **项目已停止维护**：在教程开头添加醒目提示，说明可能存在的兼容性风险
