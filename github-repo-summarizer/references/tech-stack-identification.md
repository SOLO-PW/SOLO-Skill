# 技术栈识别规则

## 识别方法

### 1. 文件扩展名分析
通过项目中的文件扩展名识别编程语言和技术栈：

| 扩展名 | 技术栈 | 识别特征 |
|--------|--------|----------|
| `.js`, `.jsx` | JavaScript/React | 前端/全栈开发 |
| `.ts`, `.tsx` | TypeScript/React | 类型安全的前端开发 |
| `.vue` | Vue.js | Vue前端框架 |
| `.py` | Python | 后端/数据科学/机器学习 |
| `.java` | Java | 企业级应用/Android |
| `.go` | Go | 高性能后端服务 |
| `.rs` | Rust | 系统编程/高性能应用 |
| `.rb` | Ruby | Web开发(Rails) |
| `.php` | PHP | Web开发(Laravel) |
| `.swift` | Swift | iOS/macOS开发 |
| `.kt` | Kotlin | Android开发 |
| `.dart` | Dart/Flutter | 跨平台移动开发 |

### 2. 配置文件分析
通过配置文件识别框架和工具：

| 配置文件 | 技术栈 | 说明 |
|----------|--------|------|
| `package.json` | Node.js | JavaScript运行时和依赖管理 |
| `requirements.txt` | Python | Python依赖管理 |
| `Pipfile` | Python(Pipenv) | Python依赖管理 |
| `pyproject.toml` | Python(Poetry) | Python依赖管理 |
| `pom.xml` | Java(Maven) | Java项目构建 |
| `build.gradle` | Java(Gradle) | Java项目构建 |
| `Cargo.toml` | Rust | Rust项目构建 |
| `go.mod` | Go | Go模块管理 |
| `Gemfile` | Ruby | Ruby依赖管理 |
| `composer.json` | PHP | PHP依赖管理 |

### 3. 框架特征文件识别
通过框架特有的文件识别具体框架：

| 特征文件 | 框架 | 说明 |
|----------|------|------|
| `next.config.js` | Next.js | React全栈框架 |
| `nuxt.config.js` | Nuxt.js | Vue全栈框架 |
| `angular.json` | Angular | 前端框架 |
| `svelte.config.js` | Svelte | 前端编译器 |
| `vite.config.js` | Vite | 前端构建工具 |
| `webpack.config.js` | Webpack | 前端构建工具 |
| `tailwind.config.js` | Tailwind CSS | CSS框架 |
| `postcss.config.js` | PostCSS | CSS处理工具 |
| `.babelrc` | Babel | JavaScript编译器 |
| `tsconfig.json` | TypeScript | TypeScript配置 |

### 4. 容器和部署文件识别
通过部署相关文件识别部署技术：

| 文件 | 技术 | 说明 |
|------|------|------|
| `Dockerfile` | Docker | 容器化部署 |
| `docker-compose.yml` | Docker Compose | 多容器编排 |
| `k8s/` 或 `kubernetes/` | Kubernetes | 容器编排平台 |
| `.github/workflows/` | GitHub Actions | CI/CD流水线 |
| `.gitlab-ci.yml` | GitLab CI | GitLab CI/CD |
| `Jenkinsfile` | Jenkins | CI/CD流水线 |
| `serverless.yml` | Serverless Framework | 无服务器部署 |
| `vercel.json` | Vercel | 前端部署平台 |
| `netlify.toml` | Netlify | 前端部署平台 |

## 技术栈分类

### 前端技术栈
```
前端框架：
- React (Facebook)
- Vue.js (尤雨溪)
- Angular (Google)
- Svelte (Rich Harris)

构建工具：
- Vite
- Webpack
- Rollup
- Parcel

UI框架：
- Ant Design
- Element UI
- Material-UI
- Bootstrap
- Tailwind CSS

状态管理：
- Redux
- Vuex/Pinia
- MobX
- Zustand
```

### 后端技术栈
```
Node.js生态：
- Express.js
- Koa.js
- NestJS
- Fastify

Python生态：
- Django
- Flask
- FastAPI
- Tornado

Java生态：
- Spring Boot
- Spring Cloud
- MyBatis

Go生态：
- Gin
- Echo
- Beego
- Fiber
```

### 数据库技术栈
```
关系型数据库：
- MySQL
- PostgreSQL
- SQLite
- Oracle
- SQL Server

NoSQL数据库：
- MongoDB (文档型)
- Redis (键值型)
- Elasticsearch (搜索引擎)
- Cassandra (列存储)
- Neo4j (图数据库)

ORM框架：
- SQLAlchemy (Python)
- Hibernate (Java)
- Sequelize (Node.js)
- Prisma (Node.js)
- TypeORM (Node.js)
```

### 云服务和基础设施
```
云平台：
- AWS (Amazon Web Services)
- Google Cloud Platform
- Microsoft Azure
- 阿里云
- 腾讯云

容器和编排：
- Docker
- Kubernetes
- Docker Swarm

服务网格：
- Istio
- Linkerd
- Consul
```

### 机器学习/人工智能
```
深度学习框架：
- TensorFlow
- PyTorch
- Keras
- PaddlePaddle

机器学习库：
- scikit-learn
- XGBoost
- LightGBM
- CatBoost

数据处理：
- Pandas
- NumPy
- Apache Spark
- Dask

计算机视觉：
- OpenCV
- Pillow
- torchvision

自然语言处理：
- NLTK
- spaCy
- Transformers (Hugging Face)
```

## 识别优先级

### 主要技术栈识别
1. **核心语言**：通过文件扩展名和配置文件确定
2. **主要框架**：通过框架特征文件确定
3. **构建工具**：通过配置文件确定
4. **部署方式**：通过部署文件确定

### 次要技术栈识别
1. **开发工具**：ESLint、Prettier、Jest等
2. **辅助库**：工具库、UI组件库等
3. **文档工具**：Storybook、Docusaurus等

## 技术栈描述模板

### 简洁描述
```
技术栈：[语言] + [框架] + [数据库] + [部署]
示例：JavaScript + React + Node.js + MongoDB + Docker
```

### 详细描述
```
前端：React 18 + TypeScript + Ant Design
后端：Node.js + Express + MongoDB
构建：Vite + ESLint + Prettier
测试：Jest + React Testing Library
部署：Docker + Nginx + AWS
```

### 表格描述
| 层级 | 技术 | 版本 | 说明 |
|------|------|------|------|
| 前端 | React | 18.x | UI框架 |
| 后端 | Node.js | 18.x | 运行时 |
| 数据库 | MongoDB | 6.x | 文档数据库 |
| 部署 | Docker | 24.x | 容器化 |

## 常见技术栈组合

### MERN Stack
- **M**ongoDB
- **E**xpress.js
- **R**eact
- **N**ode.js

### MEVN Stack
- **M**ongoDB
- **E**xpress.js
- **V**ue.js
- **N**ode.js

### LAMP Stack
- **L**inux
- **A**pache
- **M**ySQL
- **P**HP

### JAMstack
- **J**avaScript
- **A**PIs
- **M**arkup

### Django Stack
- Python
- Django
- PostgreSQL
- Redis
- Celery

### Spring Boot Stack
- Java
- Spring Boot
- MySQL/PostgreSQL
- Redis
- RabbitMQ