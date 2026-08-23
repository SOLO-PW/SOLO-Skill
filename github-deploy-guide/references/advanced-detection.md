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

---

## 不同仓库形态下的健壮性处理（边界情况）

上述增强检测（Releases / Makefile / .env 解析 / 健康度）在**多种仓库形态**下都需保持健壮，不因某项缺失而中断整体生成。以下为常见边界情况与建议降级策略：

### Releases 检测

| 边界情况 | 处理方式 |
|---------|----------|
| 仓库没有任何 Release | 检测 `gh release list` 或 Releases API 返回空 → 跳过「快速安装」章节，提示用户改用源码构建 |
| 有 Release 但无预编译二进制（仅源码 tag） | 不展示二进制下载表格，仅标注版本号与发布时间，提示「本版本为源码包，请使用源码构建方式」 |
| Release 资产未按 OS 命名 / 命名无法识别 | 不要把文件名强行套进 Windows/macOS/Linux 分类；列出全部资产文件名，标注「请根据文件名判断对应平台」 |
| 单仓库只有 `latest` 而无可追溯旧版 | 引用 `latest` 即可，避免虚构版本历史；版本号缺失时写「最新版」占位 |

### Makefile / Justfile 检测

| 边界情况 | 处理方式 |
|---------|----------|
| 仓库没有 Makefile / justfile | 跳过 make 优先方案，直接使用语言原生命令（如 npm/pip/cargo） |
| Makefile 中缺少某个 target（如没有 `make dev`） | 只展示实际存在的 target；不要凭空补写不存在的 `make dev`，可给 `make help` 或建议用户查看 `Makefile` 里可用的 target |
| target 相互依赖 / 有复杂前置项 | 照原文推荐 `make <target>`，必要时补充其依赖说明，不要简化导致命令失效 |
| 同时存在 Makefile 与多个子 Makefile（monorepo） | 优先根目录 Makefile；若根目录无目标 target，提示切换到对应子目录后再执行 `make` |

### .env.example 自动解析

| 边界情况 | 处理方式 |
|---------|----------|
| 仓库没有 .env.example / .env.template 等 | 跳过环境变量表格，并提示「本项目未提供环境变量模板，请参考源码或文档」 |
| monorepo 下 .env 分散在多个包/子目录 | 分别探测各子目录，为每个含模板的目录生成一张表格，并说明对应的工作目录 |
| .env.example 中含注释说明 | 以行内 `#` 注释作为变量说明；无注释、无默认值的变量标为「必填但说明未知」 |
| 变量含敏感默认值或占位明文 | 在表格备注强调「默认值仅供本地开发，生产环境务必替换」 |
| 文件解析失败（非标准 key=value 格式） | 不回滚、不报错：提示「无法自动解析，请手动参照 .env.example 配置」，并将原文贴出供用户参考 |

### 项目健康度评估

| 边界情况 | 处理方式 |
|---------|----------|
| 活跃度以外的字段缺失（如无 license / 无 issues 数据） | 对缺失字段用「—」占位，不阻塞信息卡片展示 |
| `pushed_at` 缺失 | 默认按「未知更新状态」处理，不给出误导性的活跃/停止判断 |
| 通过 gh/MCP 通道拿数据时字段名不同 | 按通道字段映射归一化（如 `stargazerCount` 与 `stargazers_count`），取不到则回落到 REST 或跳过 |

> **总原则**：所有增强检测一律「结果驱动、缺失降级」——某项信息缺失时，跳过对应章节并用占位或提示替代，绝不因单个字段缺失而中断教程生成，也不虚构不存在的命令/资产/变量。
