# 部署教程模板

使用此模板生成最终的部署教程。将所有 `{占位符}` 替换为实际项目信息。标记为 `[可选]` 的章节可根据情况省略。仅包含在仓库中检测到的部署场景。

---

```markdown
# {project_name} 部署教程

> 本教程将手把手教你从零开始部署 **{project_name}**，适合完全没有经验的初学者。
>
> - 项目地址：{github_url}
> - 项目语言：{language}
> - 难度等级：{beginner | intermediate | advanced}
> - 覆盖场景：{列出检测到的部署场景，如 本地开发 / Docker / 云服务器 / K8s / PaaS}

## 目录

- [项目简介](#项目简介)
- [项目信息](#项目信息)
{仅当项目停止维护时: - [维护状态提示](#维护状态提示)}
- [环境准备](#环境准备)
- [获取项目代码](#获取项目代码)
{仅当项目有 Makefile 时: - [使用 Makefile（推荐）](#使用-makefile推荐)}
{仅当项目有数据库依赖时: - [数据库准备](#数据库准备)}
- [本地开发部署](#本地开发部署)
{仅当检测到 Docker 时: - [Docker 容器化部署](#docker-容器化部署)}
{仅当检测到裸机部署时: - [云服务器部署](#云服务器部署)}
{仅当检测到 K8s 时: - [Kubernetes 部署](#kubernetes-部署)}
{仅当检测到 PaaS 时: - [PaaS 一键部署](#paas-一键部署)}
- [依赖安全检查](#依赖安全检查)
- [常见问题](#常见问题)

## 项目简介

{2-3 句话介绍项目是什么、做什么用、为什么值得部署。基于 README 或 zread.ai 的项目概述生成。}

**技术栈：** {列出主要技术栈，如 Python 3.10+、Node.js 18+、Docker、PostgreSQL 等}

## 项目信息

| 指标 | 值 |
|------|-----|
| ⭐ Stars | {stars_count} |
| 🍴 Forks | {forks_count} |
| 📝 语言 | {language} |
| 📜 协议 | {license} |
| 🕐 最近更新 | {last_push_date} |
{仅当有 Release 时: | 📦 最新版本 | {latest_release_tag} |}

{仅当项目停止维护时:
## 维护状态提示

> ⚠️ **注意**：该项目最后一次更新是在 {date}，距今已超过 {months} 个月，可能存在依赖过时或兼容性问题。建议在部署前检查 Issues 中是否有未解决的依赖冲突问题。
}

## 环境准备

{根据部署模式选择以下三个版本之一}

{===== 版本 A：PaaS 优先模式（纯静态/前端项目，无需本地环境） =====}

{仅当 PaaS 优先模式时:
> 💡 **推荐方式**：本项目推荐直接部署到线上平台，你**无需在本地安装任何开发环境**。
> 仅需一个 GitHub 账号即可完成部署。本地开发环境为可选步骤，仅当你想在本地测试修改时才需要。

### 线上部署要求

- **GitHub 账号**：免费注册于 [github.com](https://github.com/)
{仅当特定平台账号时: - **{platform} 账号**：{platform_url}}
- 无需安装任何本地工具或开发环境
- 所有构建和部署流程在云端自动完成

### 本地开发环境要求（可选）

<details>
<summary>点击展开 — 仅当需要在本地运行时才需要</summary>

{根据项目实际依赖列出，以下为示例}

#### 安装 {tool_1}（如 Python / Node.js / Go 等）

**Windows：**
1. 访问 {official_download_url}
2. 下载安装包并运行
3. 安装时勾选 "Add to PATH"
4. 打开终端验证安装：
   ```bash
   {tool_1} --version
   ```
   预期输出：`{version_string}`

**macOS：**
```bash
brew install {tool_1}
```

**Linux (Ubuntu/Debian)：**
```bash
sudo apt install {package_name}
```

#### 安装 Git [可选]

{如果用户只需要线上部署，Git 不是必需的，可以跳过}

</details>
}

{===== 版本 B：Docker / 云服务器优先模式 =====}

{仅当 Docker 或云服务器优先模式时:
本项目的部署需要准备本地开发环境和线上运行环境，两者要求不同，请根据你的需求参考对应章节。

### 本地开发环境要求

如果你想在本地修改代码或调试，请准备以下环境。

#### 系统要求

- 操作系统：{Windows 10+ / macOS 12+ / Ubuntu 20.04+}
- 磁盘空间：至少 {X} GB 可用空间
- 内存：建议 {X} GB 以上

#### 安装必要工具

{根据项目实际依赖列出，以下为示例}

##### 1. 安装 {tool_1}（如 Python / Node.js / Go 等）

**Windows：**
1. 访问 {official_download_url}
2. 下载安装包并运行
3. 安装时勾选 "Add to PATH"
4. 打开终端验证安装：
   ```bash
   {tool_1} --version
   ```
   预期输出：`{version_string}`

**macOS：**
```bash
brew install {tool_1}
```

**Linux (Ubuntu/Debian)：**
```bash
sudo apt install {package_name}
```

##### 2. 安装 Git

所有平台均可从 [git-scm.com](https://git-scm.com/) 下载安装，安装后验证：
```bash
git --version
```

### 线上部署环境要求

若要将项目部署到服务器，还需要以下准备（详见对应部署章节）：

{仅当检测到 Docker 时: - **Docker**：用于容器化部署}
{仅当检测到云服务器时: - **云服务器**（推荐 Ubuntu 22.04 LTS）}
{仅当检测到 Docker 时: - 额外**磁盘空间**：至少 {X} GB（用于存储 Docker 镜像和数据）}
}

{===== 版本 C：本地优先模式（默认） =====}

{仅当本地优先模式时:
在开始之前，请确保你的电脑满足以下要求。

#### 系统要求

- 操作系统：{Windows 10+ / macOS 12+ / Ubuntu 20.04+}
- 磁盘空间：至少 {X} GB 可用空间
- 内存：建议 {X} GB 以上

#### 安装必要工具

{根据项目实际依赖列出，以下为示例}

##### 1. 安装 {tool_1}（如 Python / Node.js / Go 等）

**Windows：**
1. 访问 {official_download_url}
2. 下载安装包并运行
3. 安装时勾选 "Add to PATH"
4. 打开终端验证安装：
   ```bash
   {tool_1} --version
   ```
   预期输出：`{version_string}`

**macOS：**
```bash
brew install {tool_1}
```

**Linux (Ubuntu/Debian)：**
```bash
sudo apt install {package_name}
```

##### 2. 安装 Git

所有平台均可从 [git-scm.com](https://git-scm.com/) 下载安装，安装后验证：
```bash
git --version
```
}

## 获取项目代码

### 方法一：使用 Git 克隆（推荐）

打开终端，执行以下命令：

```bash
git clone {clone_url}
cd {repo_name}
```

### 方法二：直接下载 ZIP

1. 访问 {github_url}
2. 点击绿色 "Code" 按钮
3. 选择 "Download ZIP"
4. 解压到任意目录
5. 在终端中进入该目录：
   ```bash
   cd {repo_name}
   ```

---

{仅当项目有 Makefile 时:
## 使用 Makefile（推荐）

本项目提供了 Makefile，可以简化常用操作：

```bash
make help    # 查看所有可用命令
```

常用命令：

| 命令 | 说明 |
|------|------|
| `make install` | 安装项目依赖 |
| `make build` | 构建项目 |
| `make dev` | 启动开发服务器 |
| `make start` | 启动生产服务 |
| `make test` | 运行测试 |
| `make clean` | 清理构建产物 |

{如果 Makefile 中没有上述 target，根据实际 Makefile 内容替换}
}

{仅当项目有数据库依赖时:
## 数据库准备

本项目依赖 {database_type} 数据库。最简单的方式是使用 Docker 启动：

```bash
docker run -d \
  --name {repo_name}-db \
  {database_docker_command}
```

验证数据库是否启动成功：
```bash
docker logs {repo_name}-db
```

{仅当项目有数据库迁移时:
### 数据库迁移

```bash
{migration_command}
```
}

### 数据库管理工具推荐

- DBeaver（免费，支持所有数据库）：https://dbeaver.io/
{仅当使用 PostgreSQL 时: - pgAdmin（PostgreSQL 专用）：https://www.pgadmin.org/}
{仅当使用 MySQL 时: - MySQL Workbench（MySQL 专用）：https://dev.mysql.com/downloads/workbench/}
}

---

## 本地开发部署

### 安装依赖

{根据项目包管理器选择对应格式}

#### {如果使用 pip (Python)}

```bash
# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

{中文用户可补充: 国内用户可使用清华镜像加速：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
}

#### {如果使用 npm (Node.js)}

```bash
npm install
```

{中文用户可补充: 国内用户可使用淘宝镜像：
```bash
npm install --registry=https://registry.npmmirror.com
```
}

#### {如果使用其他包管理器}

```bash
{install_command}
```

### 项目配置

{根据项目实际配置需求填写}

#### 配置环境变量

1. 复制环境变量模板：
   ```bash
   cp .env.example .env
   ```
   {如果没有 .env.example，手动创建 .env 文件}

2. 编辑 `.env` 文件，填写必要配置：

   ```env
   # {配置项说明}
   {KEY}={value}
   ```

### 启动项目

```bash
{start_command}
```

启动成功后，终端应显示类似：
```
{expected_output}
```

### 验证部署

打开浏览器，访问：{local_url}（如 http://localhost:3000）

---

{以下章节仅当检测到对应部署方式时包含}

---

## Docker 容器化部署

> 适用场景：需要在任何环境中一致运行，或准备部署到服务器。

### 前置条件

确保已安装 Docker 和 Docker Compose：
- Docker: https://docs.docker.com/get-docker/
- Docker Compose: 通常随 Docker Desktop 一起安装

验证安装：
```bash
docker --version
docker compose version
```

### 构建镜像

1. 进入项目根目录
2. 检查项目是否已有 `Dockerfile` 和 `docker-compose.yml`
3. 构建镜像：
   ```bash
   docker build -t {repo_name}:latest .
   ```

{如果项目没有 Dockerfile，提供以下最小示例并说明如何创建：}

**创建 .dockerignore（避免将不必要的文件复制到镜像中）：**
```
node_modules
.git
__pycache__
*.pyc
.env
dist
```

{根据项目语言提供对应的 Dockerfile 示例，参考 SKILL.md 中的场景指南}

### 使用 Docker Compose 启动（推荐）

{如果项目有 docker-compose.yml：}
```bash
docker compose up -d
```

{如果项目没有 docker-compose.yml，提供最小示例：}
```yaml
version: "3.9"
services:
  app:
    build: .
    ports:
      - "{port}:{port}"
    environment:
      - {ENV_KEY}={value}
    volumes:
      - ./{data_dir}:/{container_data_dir}
```

### 常用 Docker 命令

```bash
docker compose up -d          # 后台启动所有服务
docker compose logs -f        # 查看实时日志
docker compose down           # 停止并移除所有容器
docker compose ps             # 查看运行状态
docker system prune -a        # 清理无用镜像和缓存（磁盘空间不足时使用）
```

### 验证

打开浏览器，访问：http://localhost:{port}

---

## 云服务器部署

> 适用场景：需要将项目部署到公网服务器，供外部用户访问。

### 前置条件

- 一台云服务器（推荐 Ubuntu 22.04 LTS，2核4G 起步）
- 已绑定域名（可选，用于 HTTPS）
- 通过 SSH 连接到服务器：
  ```bash
  ssh root@{server_ip}
  ```

### 1. 安装基础环境

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装必要工具
sudo apt install -y git nginx certbot python3-certbot-nginx
```

### 2. 上传项目代码

```bash
# 方法一：直接克隆
git clone {clone_url}
cd {repo_name}

# 方法二：从本地上传（在本地电脑执行）
scp -r ./{repo_name} root@{server_ip}:/var/www/{repo_name}
```

### 3. 安装项目依赖

{根据项目语言提供对应命令，如：}

```bash
# Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Node.js
npm ci --production
```

### 4. 配置 Nginx 反向代理

创建 Nginx 配置文件：

```bash
sudo nano /etc/nginx/sites-available/{repo_name}
```

写入以下内容：

```nginx
server {
    listen 80;
    server_name {domain_or_ip};

    location / {
        proxy_pass http://127.0.0.1:{port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用站点并测试：
```bash
sudo ln -s /etc/nginx/sites-available/{repo_name} /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5. 配置进程管理

{根据项目语言选择：}

**Python（使用 systemd）：**
```bash
sudo nano /etc/systemd/system/{repo_name}.service
```
```ini
[Unit]
Description={project_name}
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/{repo_name}
ExecStart=/var/www/{repo_name}/venv/bin/python app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl enable {repo_name}
sudo systemctl start {repo_name}
```

**Node.js（使用 PM2）：**
```bash
npm install -g pm2
pm2 start {entry_file} --name {repo_name}
pm2 save
pm2 startup    # 设置开机自启
```

### 6. 配置 SSL 证书（可选但推荐）

```bash
sudo certbot --nginx -d {domain} -d www.{domain}
```

Certbot 会自动修改 Nginx 配置并设置自动续期。

### 7. 开放防火墙端口

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow {port}/tcp    # 如果应用需要直接暴露端口
sudo ufw enable
```

### 验证

打开浏览器，访问：http://{domain_or_ip}

---

## Kubernetes 部署

> 适用场景：需要自动扩缩容、高可用、多副本部署的生产环境。
>
> ⚠️ 前提：你已经有可用的 Kubernetes 集群（本地可用 minikube，云端可用 EKS/GKE/ACK）。

### 前置条件

- 已安装 kubectl 并连接到集群
- 已安装 Ingress Controller（如 nginx-ingress-controller）

验证：
```bash
kubectl cluster-info
kubectl get nodes
```

### 1. 创建命名空间

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: {repo_name}
```

```bash
kubectl apply -f namespace.yaml
```

### 2. 创建 Deployment

{如果项目已有 K8s 配置文件，直接引用；否则提供以下模板：}

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {repo_name}
  namespace: {repo_name}
spec:
  replicas: 2
  selector:
    matchLabels:
      app: {repo_name}
  template:
    metadata:
      labels:
        app: {repo_name}
    spec:
      containers:
      - name: {repo_name}
        image: {image_name}:{tag}
        ports:
        - containerPort: {port}
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        env:
        - name: {ENV_KEY}
          value: "{ENV_VALUE}"
```

### 3. 创建 Service

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: {repo_name}-service
  namespace: {repo_name}
spec:
  selector:
    app: {repo_name}
  ports:
    - protocol: TCP
      port: 80
      targetPort: {port}
  type: ClusterIP
```

### 4. 创建 Ingress

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {repo_name}-ingress
  namespace: {repo_name}
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: {domain}
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: {repo_name}-service
            port:
              number: 80
```

### 5. 部署所有资源

```bash
kubectl apply -f namespace.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml
```

### 常用 kubectl 命令

```bash
kubectl get pods -n {repo_name}                    # 查看 Pod 状态
kubectl get svc,deploy -n {repo_name}              # 查看服务和部署
kubectl logs -f deployment/{repo_name} -n {repo_name}  # 查看日志
kubectl rollout status deployment/{repo_name} -n {repo_name}  # 查看更新状态
kubectl scale deployment/{repo_name} --replicas=5 -n {repo_name}  # 手动扩容
```

### 验证

```bash
kubectl get ingress -n {repo_name}
```

打开浏览器，访问：http://{domain}

---

## PaaS 一键部署

> 适用场景：不想管理服务器，快速上线。推荐个人项目和快速验证使用。

{根据项目检测到的 PaaS 配置文件，仅包含相关平台}

### {Platform_1}（如 Vercel / Netlify / Railway / Render）

{如果项目有对应的配置文件，直接引用并说明部署步骤}

#### 部署步骤

1. 将代码推送到 GitHub
2. 访问 {platform_url}，使用 GitHub 账号登录
3. 点击 "New Project" / "Import Repository"
4. 选择对应的 GitHub 仓库
5. 平台会自动检测框架和构建配置
6. 配置环境变量（如有需要）：
   - 在 Settings → Environment Variables 中添加
7. 点击 "Deploy"

#### 配置文件说明

{引用项目中已有的配置文件内容并逐项解释}

#### 常用命令

```bash
# {平台 CLI 安装和部署命令}
```

#### 注意事项

- 免费额度限制：{说明该平台的免费层限制}
- 环境变量在平台控制台中设置，不要硬编码在代码中
- 端口通过环境变量注入，应用应监听 `process.env.PORT`

---

## 依赖安全检查

安装依赖后，建议运行安全检查以发现已知漏洞：

{根据项目语言选择对应命令，参见 references/lang-deps.md}

```bash
{security_check_command}
```

如果发现安全漏洞，根据严重程度决定是否继续：
- **低危**：可以暂时忽略，不影响本地开发
- **中危**：建议更新相关依赖后再继续
- **高危/严重**：强烈建议修复后再部署到生产环境

---

## 常见问题

### Q1: {常见错误1描述}

**错误信息：**
```
{error_message}
```

**解决方法：**
{逐步排查方案}

### Q2: {常见错误2描述}

**解决方法：**
{解决方案}

### Q3: 端口被占用

**解决方法：**
{如何更换端口或释放端口}

### Q4: Docker 构建失败

**解决方法：**
{常见 Docker 构建问题排查}

### Q5: 服务器上无法访问

**排查步骤：**
1. 检查应用是否正在运行
2. 检查防火墙是否开放端口
3. 检查 Nginx 配置是否正确
4. 检查云服务商的安全组规则

---

> 本教程基于 {project_name} 的 {documentation_source} 生成。
> 如遇到教程未覆盖的问题，请查阅项目官方文档或提交 Issue。
```

---

## 模板使用说明（供 AI Agent 参考，不包含在输出中）

- 所有章节必须填充具体、可操作的内容 —— 最终输出中不得留有任何占位符
- 根据仓库元数据检测实际技术栈，相应调整工具安装章节
- 仅包含在仓库中检测到的部署场景章节（存在 Dockerfile → 包含 Docker，存在 k8s/ → 包含 K8s 等）
- **环境准备章节三选一**：根据 SKILL.md 第六步评估的部署模式，从版本 A/B/C 中选择一个生成：
  - **版本 A（PaaS 优先）**：项目是纯静态/前端项目，存在 PaaS 配置文件 → 本地环境折叠为可选 `<details>`
  - **版本 B（Docker/服务器优先）**：存在 Dockerfile 或文档指向服务器部署 → 本地和线上要求并列展示
  - **版本 C（本地优先）**：CLI 工具、桌面应用等 → 本地环境为必选主章节
- 如果项目以 Docker 为主要部署方式，优先展示 Docker 说明
- 如果项目有 Web UI，包含浏览器验证步骤
- 如果项目是 CLI 工具，包含示例命令
- 如果项目需要 API 密钥或账号，明确说明需要什么以及从哪里获取
- 中文用户优先使用国内镜像源（pip 清华源、npm 淘宝源）
- 教程语言与用户查询语言保持一致
- 云服务器部署时，根据项目语言选择进程管理器（Python → systemd，Node.js → PM2，Go → systemd）
- K8s 部署时，提醒用户需要单独安装 Ingress Controller
- PaaS 部署时，说明各平台的免费额度限制
- 当未找到特定部署配置文件时，提供最小可用的示例供用户自定义
