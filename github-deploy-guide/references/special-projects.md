# 特殊项目类型支持

针对非标准项目结构提供专门的检测逻辑和教程模板。

---

## 项目类型检测

| 类型 | 检测依据 |
|------|---------|
| **全栈项目** | 同时存在 `frontend/` + `backend/` 或 `client/` + `server/` 目录 |
| **Monorepo** | 存在 `pnpm-workspace.yaml`、`lerna.json`、`nx.json`、`turbo.json` |
| **AI/ML 项目** | 存在 `requirements.txt` 中含 `torch`/`tensorflow`/`transformers`，或 `Dockerfile` 含 GPU 关键字 |
| **数据库依赖项目** | `docker-compose.yml` 中含数据库服务，或文档提到数据库配置 |
| **桌面应用** | 存在 `electron/`、`tauri.conf.json`、`.pro`（Qt） |
| **移动应用** | 存在 `android/`、`ios/`、`app.json`（Expo） |
| **CLI 工具** | `package.json` 中含 `bin` 字段，或 `Cargo.toml` 中含 `[[bin]]` |

---

## 全栈项目（前后端分离）

### 检测逻辑

检查是否存在以下目录结构之一：
- `frontend/` + `backend/`
- `client/` + `server/`
- `web/` + `api/`
- `app/` + `server/`

或 `docker-compose.yml` 中定义了多个 build 服务。

### 教程补充要点

1. **分别说明前后端的环境准备和依赖安装**
2. **说明前后端如何通信**（API 地址、CORS 配置）
3. **提供完整的 docker-compose.yml**（包含前端、后端、数据库）
4. **说明开发模式下的端口分配**（如前端 3000，后端 8000）

### 环境变量配置模板

**后端 `.env`：**
```env
# 数据库
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
# Redis
REDIS_URL=redis://localhost:6379/0
# JWT 密钥
JWT_SECRET=your-secret-key-change-in-production
# 允许的前端地址（CORS）
ALLOWED_ORIGINS=http://localhost:3000
```

**前端 `.env`：**
```env
# 后端 API 地址
VITE_API_URL=http://localhost:8000/api
# 或 Next.js
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

---

## AI / ML 项目

### 检测逻辑

- `requirements.txt` 包含 `torch`、`tensorflow`、`transformers`、`diffusers`、`accelerate` 等
- 存在 `model/`、`models/`、`weights/`、`checkpoints/` 目录
- `Dockerfile` 中引用 GPU 基础镜像（如 `nvidia/cuda`）
- 文档提到 CUDA、GPU、模型下载

### 教程补充要点

1. **GPU 驱动安装**（如需要）
   - NVIDIA 驱动：https://www.nvidia.com/Download/index.aspx
   - CUDA Toolkit：https://developer.nvidia.com/cuda-downloads
   - 验证：`nvidia-smi`

2. **模型下载说明**
   - Hugging Face 模型：说明需要 `huggingface-cli login` 或设置 `HF_TOKEN`
   - 国内用户镜像：`export HF_ENDPOINT=https://hf-mirror.com`
   - 大模型可能需要几十 GB 磁盘空间

3. **内存/显存要求**
   - 明确标注最低显存要求（如 "至少需要 8GB 显存"）
   - CPU 模式下的性能警告

4. **Docker GPU 支持**
   ```bash
   # 安装 NVIDIA Container Toolkit
   # Ubuntu:
   curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
   # （完整安装步骤参考官方文档）

   # 运行 GPU 容器
   docker run --gpus all myapp:latest
   ```

### Dockerfile 示例（GPU）

```dockerfile
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python3", "app.py"]
```

---

## Monorepo 项目

### 检测逻辑

- 存在 `pnpm-workspace.yaml` → pnpm workspace
- 存在 `lerna.json` → Lerna
- 存在 `nx.json` → Nx
- 存在 `turbo.json` → Turborepo

### 教程补充要点

1. **说明 Monorepo 工具的安装**
   ```bash
   # pnpm workspace（最常见）
   npm install -g pnpm
   pnpm install

   # Turborepo
   npm install -g turbo
   ```

2. **说明如何构建特定包**
   ```bash
   # pnpm workspace
   pnpm --filter {package_name} build
   pnpm --filter {package_name} dev

   # Turborepo
   turbo run build --filter={package_name}
   turbo run dev --filter={package_name}
   ```

3. **说明包之间的依赖关系**

---

## 数据库依赖项目

### 检测逻辑

- `docker-compose.yml` 中包含数据库服务（postgres、mysql、mongo、redis）
- `.env.example` 中包含数据库连接字符串
- 文档提到数据库配置

### 教程补充要点

1. **在"本地开发部署"章节之前，插入"数据库准备"章节**
2. **提供 Docker 一键启动数据库的命令**（即使项目不以 Docker 为主部署方式）
3. **说明数据库 GUI 工具**（如 DBeaver、Navicat、DataGrip、pgAdmin）
4. **说明数据库初始化**（迁移命令、种子数据）

### 数据库准备章节模板

```markdown
## 数据库准备

本项目依赖 PostgreSQL 数据库。最简单的方式是使用 Docker 启动：

```bash
docker run -d \
  --name mydb \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=mypassword \
  -e POSTGRES_DB=mydb \
  -p 5432:5432 \
  postgres:16-alpine
```

验证数据库是否启动成功：
```bash
docker logs mydb
```

### 数据库迁移

```bash
# 如果使用 Alembic（Python）
alembic upgrade head

# 如果使用 Prisma（Node.js）
npx prisma migrate dev

# 如果使用 Flyway（Java）
mvn flyway:migrate
```

### 数据库管理工具推荐

- DBeaver（免费，支持所有数据库）：https://dbeaver.io/
- pgAdmin（PostgreSQL 专用）：https://www.pgadmin.org/
```

---

## CLI 工具项目

### 检测逻辑

- `package.json` 中存在 `bin` 字段
- `Cargo.toml` 中存在 `[[bin]]`
- `setup.py` 中存在 `console_scripts`
- 项目描述中提到 "CLI"、"command-line"、"命令行"

### 教程补充要点

1. **安装到全局**
   ```bash
   # Node.js
   npm install -g .

   # Python
   pip install -e .

   # Go
   go install .

   # Rust
   cargo install --path .
   ```

2. **验证安装**
   ```bash
   {command_name} --help
   {command_name} --version
   ```

3. **提供常用命令示例**（从 README 或帮助文档中提取）

4. **不需要"验证部署 - 打开浏览器"步骤**，替换为 CLI 使用示例
