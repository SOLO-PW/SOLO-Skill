# 各场景完整配置示例

为不同部署场景提供按语言分类的完整配置示例。根据项目检测到的语言和部署场景，选择对应示例填入教程。

---

## Docker 完整 Dockerfile 示例

### Python（Flask/Django/FastAPI）

```dockerfile
# 构建阶段
FROM python:3.12-slim AS builder
WORKDIR /app

# 先复制依赖文件，利用层缓存
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 运行阶段
FROM python:3.12-slim
WORKDIR /app

# 复制已安装的依赖
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# 复制源码
COPY . .

# 创建非 root 用户
RUN useradd -m appuser
USER appuser

EXPOSE 8000
CMD ["python", "app.py"]
# 如果是 FastAPI: CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# 如果是 Django: CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Node.js（Express/Next.js）

```dockerfile
# 构建阶段
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# 运行阶段
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./

# Next.js 特殊处理
# COPY --from=builder /app/.next/standalone ./
# COPY --from=builder /app/.next/static ./.next/static
# COPY --from=builder /app/public ./public

USER node
EXPOSE 3000
CMD ["node", "dist/index.js"]
# 如果是 Next.js standalone: CMD ["node", "server.js"]
```

### Go

```dockerfile
# 构建阶段
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o server .

# 运行阶段（最终镜像极小）
FROM alpine:3.19
RUN apk --no-cache add ca-certificates
COPY --from=builder /app/server /server
USER nobody
EXPOSE 8080
CMD ["/server"]
```

### Java（Spring Boot）

```dockerfile
# 构建阶段
FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline -B
COPY src ./src
RUN mvn package -DskipTests -B

# 运行阶段
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
USER nobody
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

### Rust

```dockerfile
# 构建阶段
FROM rust:1.78-alpine AS builder
RUN apk add --no-cache musl-dev
WORKDIR /app
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main(){}" > src/main.rs && cargo build --release && rm -rf src
COPY src ./src
RUN touch src/main.rs && cargo build --release

# 运行阶段
FROM alpine:3.19
COPY --from=builder /app/target/release/{binary_name} /app
USER nobody
EXPOSE 8080
CMD ["/app"]
```

---

## Docker Compose 完整示例

### 前后端分离 + 数据库

```yaml
version: "3.9"

services:
  # 后端 API
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgres://user:password@db:5432/mydb
      - REDIS_URL=redis://cache:6379/0
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_healthy

  # 前端
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend

  # PostgreSQL 数据库
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 5s
      timeout: 5s
      retries: 5

  # Redis 缓存
  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
```

---

## Nginx 高级配置示例

### 反向代理 + WebSocket 支持

```nginx
server {
    listen 80;
    server_name example.com;

    # 静态文件直接由 Nginx 提供
    location /static/ {
        alias /var/www/myapp/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # API 反向代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 超时设置（适合长时间请求）
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # WebSocket 支持
    location /ws/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 前端 SPA（单页应用）
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### HTTPS + SSL 完整配置

```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # SSL 安全配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # 安全头
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 负载均衡

```nginx
upstream backend {
    least_conn;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

## 数据库配置模板

### PostgreSQL

**Docker Compose 中使用：**
```yaml
db:
  image: postgres:16-alpine
  environment:
    POSTGRES_USER: myuser
    POSTGRES_PASSWORD: mypassword
    POSTGRES_DB: mydb
  volumes:
    - pgdata:/var/lib/postgresql/data
  ports:
    - "5432:5432"
```

**连接字符串格式：**
```
postgresql://myuser:mypassword@localhost:5432/mydb
```

**常用管理命令：**
```bash
# 进入数据库
docker exec -it <container_name> psql -U myuser -d mydb

# 列出所有表
\dt

# 查看表结构
\d <table_name>
```

### MySQL / MariaDB

**Docker Compose 中使用：**
```yaml
db:
  image: mysql:8.0
  environment:
    MYSQL_ROOT_PASSWORD: rootpassword
    MYSQL_DATABASE: mydb
    MYSQL_USER: myuser
    MYSQL_PASSWORD: mypassword
  volumes:
    - mysqldata:/var/lib/mysql
  ports:
    - "3306:3306"
```

**连接字符串格式：**
```
mysql://myuser:mypassword@localhost:3306/mydb
```

### MongoDB

**Docker Compose 中使用：**
```yaml
db:
  image: mongo:7
  environment:
    MONGO_INITDB_ROOT_USERNAME: myuser
    MONGO_INITDB_ROOT_PASSWORD: mypassword
  volumes:
    - mongodata:/data/db
  ports:
    - "27017:27017"
```

**连接字符串格式：**
```
mongodb://myuser:mypassword@localhost:27017/mydb?authSource=admin
```

### Redis

**Docker Compose 中使用：**
```yaml
cache:
  image: redis:7-alpine
  command: redis-server --requirepass mypassword
  volumes:
    - redisdata:/data
  ports:
    - "6379:6379"
```

**连接字符串格式：**
```
redis://:mypassword@localhost:6379/0
```

---

## K8s 数据库部署示例

### PostgreSQL StatefulSet

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:16-alpine
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_USER
          value: myuser
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: password
        - name: POSTGRES_DB
          value: mydb
        volumeMounts:
        - name: pgdata
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: pgdata
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
---
apiVersion: v1
kind: Service
metadata:
  name: postgres
spec:
  selector:
    app: postgres
  ports:
    - port: 5432
      targetPort: 5432
```

### ConfigMap 和 Secret 示例

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DATABASE_HOST: "postgres"
  DATABASE_PORT: "5432"
  DATABASE_NAME: "mydb"
  REDIS_HOST: "redis"
---
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
stringData:
  DATABASE_PASSWORD: "mypassword"
  API_SECRET_KEY: "your-secret-key"
```

在 Deployment 中引用：
```yaml
envFrom:
- configMapRef:
    name: app-config
- secretRef:
    name: app-secret
```
