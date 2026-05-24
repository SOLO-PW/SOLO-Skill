# 增强检测与分析能力

在基础检测之外，提供更深层次的项目分析和信息提取能力。

---

## GitHub Releases 检测

### 检测时机

当项目没有 README 或文档中缺少安装步骤时，检查 Releases 页面可能获取到预编译的二进制文件和安装说明。

### API 调用

```
GET https://api.github.com/repos/{owner}/{repo}/releases/latest
GET https://api.github.com/repos/{owner}/{repo}/releases?per_page=5
```

### 提取信息

- 最新版本号和发布日期
- 预编译二进制文件（按操作系统分类）
- Release Notes 中的安装说明
- 是否有 `latest` 标签

### 教程中的应用

如果 Release 中提供了预编译二进制文件，在教程中添加"快速安装（推荐）"章节：

```markdown
### 方法一：下载预编译版本（推荐）

1. 访问 [Releases 页面]({releases_url})
2. 下载对应操作系统的版本：
   - Windows: `{asset_name_windows}`
   - macOS: `{asset_name_macos}`
   - Linux: `{asset_name_linux}`
3. 解压并运行
```

---

## Makefile / Justfile 检测

### 检测逻辑

- 存在 `Makefile` → GNU Make
- 存在 `justfile` 或 `Justfile` → Just

### API 调用

```
GET https://raw.githubusercontent.com/{owner}/{repo}/{branch}/Makefile
GET https://raw.githubusercontent.com/{owner}/{repo}/{branch}/justfile
```

### 提取信息

从 Makefile 中提取常用 target：
- `make install` / `make setup` / `make init` → 安装依赖
- `make build` / `make compile` → 构建项目
- `make run` / `make start` / `make dev` → 启动项目
- `make test` → 运行测试
- `make clean` → 清理构建产物
- `make help` → 查看所有可用命令

### 教程中的应用

如果项目有 Makefile，在教程中优先使用 make 命令：

```markdown
### 安装依赖

```bash
make install
```

### 启动项目

```bash
make dev
```

### 查看所有可用命令

```bash
make help
```
```

---

## .env.example 自动解析

### 检测逻辑

检查是否存在以下文件：
- `.env.example`
- `.env.template`
- `.env.sample`
- `.env.local.example`

### API 调用

```
GET https://raw.githubusercontent.com/{owner}/{repo}/{branch}/.env.example
```

### 提取信息

从 .env.example 中解析每个环境变量：
- 变量名
- 注释说明（行内 `#` 注释）
- 默认值
- 是否为必填项（无默认值且无注释标记为可选）

### 教程中的应用

自动生成环境变量配置表格：

```markdown
### 环境变量配置

复制环境变量模板并填写配置：

```bash
cp .env.example .env
```

| 变量名 | 说明 | 必填 | 默认值 |
|--------|------|------|--------|
| `DATABASE_URL` | 数据库连接字符串 | ✅ | - |
| `PORT` | 服务监听端口 | ❌ | `3000` |
| `JWT_SECRET` | JWT 签名密钥 | ✅ | - |
| `LOG_LEVEL` | 日志级别 | ❌ | `info` |
```

---

## 项目健康度评估

### 评估维度

从 GitHub API 获取以下指标，在教程开头以徽章形式展示：

| 指标 | API 字段 | 说明 |
|------|---------|------|
| Stars | `stargazers_count` | 项目受欢迎程度 |
| Forks | `forks_count` | 社区参与度 |
| 最近更新 | `pushed_at` | 项目活跃度 |
| 开源协议 | `license.spdx_id` | 使用许可 |
| Issues | `open_issues_count` | 待解决问题数 |
| 语言 | `language` | 主要编程语言 |

### API 调用

```
GET https://api.github.com/repos/{owner}/{repo}
```

### 教程中的应用

在项目简介下方添加项目信息卡片：

```markdown
## 项目信息

| 指标 | 值 |
|------|-----|
| ⭐ Stars | {stars_count} |
| 🍴 Forks | {forks_count} |
| 📝 语言 | {language} |
| 📜 协议 | {license} |
| 🕐 最近更新 | {last_push_date} |
| 📦 最新版本 | {latest_release_tag} |
```

### 活跃度判断

- `pushed_at` 在 30 天内 → 🟢 活跃维护中
- `pushed_at` 在 30-180 天内 → 🟡 维护频率降低
- `pushed_at` 超过 180 天 → 🔴 可能已停止维护

在教程中添加维护状态提示：
```markdown
> ⚠️ **注意**：该项目最后一次更新是在 {date}，距今已超过 {months} 个月，可能存在依赖过时或兼容性问题。
```

---

## package.json / pyproject.toml 深度解析

### package.json 提取

从 `package.json` 中提取：
- `scripts` → 可用的 npm scripts（build、dev、start、test）
- `engines` → Node.js 版本要求
- `dependencies` / `devDependencies` → 主要依赖
- `bin` → CLI 命令（如果有）
- `type` → ES Module 或 CommonJS

### pyproject.toml 提取

从 `pyproject.toml` 中提取：
- `[project]` 下的 `requires-python` → Python 版本要求
- `[project.scripts]` → CLI 入口
- `[tool.poetry]` → Poetry 项目
- `[build-system]` → 构建系统

### go.mod 提取

- `module` → 模块路径
- `go` 指令 → Go 版本要求

### 教程中的应用

根据提取的信息精确化环境准备章节：

```markdown
### 系统要求

- **Node.js**：>= 18.0.0（项目要求）
- **npm**：>= 9.0.0
- **操作系统**：Windows 10+ / macOS 12+ / Ubuntu 20.04+
```

---

## GitHub Discussions 检测

### 检测时机

当所有文档回退均失败时，作为最后的补充信息源。

### API 调用

```
GET https://api.github.com/repos/{owner}/{repo}/discussions?per_page=5
```

注意：Discussions API 需要特殊的媒体类型头：
```
Accept: application/vnd.github+json
```

### 提取信息

搜索标题中包含 "install"、"setup"、"deploy"、"getting started"、"how to" 的讨论。

### 教程中的应用

如果从 Discussions 中找到有用信息，在教程末尾添加参考链接：

```markdown
## 参考链接

- [社区讨论：安装指南]({discussion_url})
- [社区讨论：部署经验]({discussion_url})
```

---

## 依赖安全检查提示

### 检测逻辑

在教程的"环境准备"或"安装依赖"之后，添加安全检查建议：

```markdown
### 依赖安全检查（推荐）

安装依赖后，建议运行安全检查：

```bash
# Node.js
npm audit
# 或
pnpm audit

# Python
pip audit
# 或
safety check -r requirements.txt

# Go
govulncheck ./...

# Rust
cargo audit
```

如果发现安全漏洞，根据严重程度决定是否继续。
```
