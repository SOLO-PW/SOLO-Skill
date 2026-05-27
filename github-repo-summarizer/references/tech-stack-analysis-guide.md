# 技术栈分析指南

## 概述

本文档详细说明如何分析GitHub仓库的技术栈，包括编程语言、框架、工具、数据库等。

## 分析维度

### 1. 编程语言识别

#### 数据来源
- GitHub API `/repos/{owner}/{repo}/languages`
- 返回各语言的字节数，按降序排列

#### 常见语言映射
| API返回值 | 显示名称 | 用途 |
|-----------|----------|------|
| JavaScript | JavaScript | 前端/全栈 |
| TypeScript | TypeScript | 类型安全的前端 |
| Python | Python | 后端/数据科学 |
| Java | Java | 企业级应用 |
| Go | Go | 高性能后端 |
| Rust | Rust | 系统编程 |
| C++ | C++ | 系统/游戏 |
| Ruby | Ruby | Web开发 |
| PHP | PHP | Web开发 |
| Swift | Swift | iOS开发 |
| Kotlin | Kotlin | Android开发 |
| Dart | Dart | Flutter开发 |

#### 语言占比计算
```
语言占比 = (语言字节数 / 总字节数) × 100%
```

**示例**：
- JavaScript: 60%
- TypeScript: 30%
- HTML: 5%
- CSS: 5%

### 2. 框架识别

#### 识别方法
1. **配置文件识别**：检查项目中的框架配置文件
2. **依赖文件识别**：分析package.json、requirements.txt等
3. **关键词匹配**：从README和Topics中提取

#### 前端框架识别

| 配置文件 | 框架 | 版本检查 |
|----------|------|----------|
| `next.config.js` | Next.js | package.json中的next版本 |
| `nuxt.config.js` | Nuxt.js | package.json中的nuxt版本 |
| `angular.json` | Angular | package.json中的@angular/core版本 |
| `svelte.config.js` | Svelte | package.json中的svelte版本 |
| `vite.config.js` | Vite | package.json中的vite版本 |

**React项目识别**：
- package.json中包含`react`依赖
- 文件扩展名`.jsx`或`.tsx`
- README中提到React

**Vue.js项目识别**：
- package.json中包含`vue`依赖
- 文件扩展名`.vue`
- README中提到Vue

#### 后端框架识别

| 语言 | 框架 | 识别特征 |
|------|------|----------|
| Python | Django | settings.py文件、django依赖 |
| Python | Flask | app.py文件、flask依赖 |
| Python | FastAPI | main.py文件、fastapi依赖 |
| Node.js | Express | express依赖、app.js文件 |
| Node.js | NestJS | @nestjs/core依赖 |
| Java | Spring Boot | pom.xml中的spring-boot依赖 |
| Ruby | Rails | Gemfile中的rails依赖 |
| PHP | Laravel | composer.json中的laravel依赖 |

#### 移动端框架识别

| 框架 | 识别特征 |
|------|----------|
| React Native | react-native依赖、android/ios目录 |
| Flutter | pubspec.yaml文件、lib/目录 |
| Ionic | @ionic/angular或@ionic/react依赖 |

#### 桌面应用框架识别

| 框架 | 识别特征 |
|------|----------|
| Electron | electron依赖、main.js文件 |
| Tauri | src-tauri/目录、tauri依赖 |

### 3. 数据库识别

#### 关系型数据库
| 数据库 | 识别特征 |
|--------|----------|
| MySQL | mysql依赖、mysql连接字符串 |
| PostgreSQL | pg/psycopg2依赖、postgres连接字符串 |
| SQLite | sqlite3依赖、.db文件 |
| MariaDB | mariadb依赖 |

#### NoSQL数据库
| 数据库 | 识别特征 |
|--------|----------|
| MongoDB | mongoose/mongodb依赖、mongo连接字符串 |
| Redis | redis/ioredis依赖 |
| Elasticsearch | elasticsearch依赖 |
| Firebase | firebase依赖 |

#### ORM框架识别
| 语言 | ORM | 识别特征 |
|------|-----|----------|
| Python | SQLAlchemy | sqlalchemy依赖 |
| Python | Django ORM | django依赖 |
| Node.js | Sequelize | sequelize依赖 |
| Node.js | Prisma | prisma依赖、prisma/目录 |
| Node.js | TypeORM | typeorm依赖 |
| Java | Hibernate | hibernate依赖 |

### 4. 构建工具识别

#### 前端构建工具
| 工具 | 配置文件 | 说明 |
|------|----------|------|
| Webpack | webpack.config.js | 模块打包器 |
| Vite | vite.config.js | 快速构建工具 |
| Rollup | rollup.config.js | 库打包工具 |
| Parcel | .parcelrc | 零配置打包器 |
| esbuild | esbuild配置 | 极速打包器 |

#### CSS工具
| 工具 | 配置文件 | 说明 |
|------|----------|------|
| PostCSS | postcss.config.js | CSS转换工具 |
| Tailwind CSS | tailwind.config.js | 实用优先的CSS框架 |
| Sass | .scss文件 | CSS预处理器 |
| Less | .less文件 | CSS预处理器 |

### 5. 测试工具识别

#### 单元测试
| 工具 | 识别特征 |
|------|----------|
| Jest | jest依赖、jest.config.js |
| Mocha | mocha依赖、.mocharc.yml |
| Vitest | vitest依赖、vitest.config.js |
| pytest | pytest依赖、conftest.py |

#### E2E测试
| 工具 | 识别特征 |
|------|----------|
| Cypress | cypress依赖、cypress/目录 |
| Playwright | playwright依赖、playwright.config.js |
| Selenium | selenium依赖 |

### 6. CI/CD工具识别

| 工具 | 配置文件 | 说明 |
|------|----------|------|
| GitHub Actions | .github/workflows/*.yml | GitHub内置CI/CD |
| GitLab CI | .gitlab-ci.yml | GitLab CI/CD |
| Jenkins | Jenkinsfile | Jenkins流水线 |
| Travis CI | .travis.yml | Travis CI |
| CircleCI | .circleci/config.yml | CircleCI |

### 7. 部署平台识别

| 平台 | 配置文件 | 说明 |
|------|----------|------|
| Docker | Dockerfile, docker-compose.yml | 容器化部署 |
| Kubernetes | k8s/*.yaml | 容器编排 |
| Vercel | vercel.json | 前端部署平台 |
| Netlify | netlify.toml | 前端部署平台 |
| AWS | serverless.yml, SAM模板 | 云服务部署 |
| Heroku | Procfile | PaaS平台 |

### 8. 包管理器识别

| 语言 | 包管理器 | 锁文件 |
|------|----------|--------|
| JavaScript | npm | package-lock.json |
| JavaScript | Yarn | yarn.lock |
| JavaScript | pnpm | pnpm-lock.yaml |
| Python | pip | requirements.txt |
| Python | Poetry | poetry.lock |
| Python | Pipenv | Pipfile.lock |
| Ruby | Bundler | Gemfile.lock |
| PHP | Composer | composer.lock |
| Rust | Cargo | Cargo.lock |
| Go | Go Modules | go.sum |
| Java | Maven | pom.xml |
| Java | Gradle | build.gradle |

## 分析流程

### 步骤1：获取文件树
```
调用 GitHub API: GET /repos/{owner}/{repo}/git/trees/{branch}?recursive=1
```

### 步骤2：识别配置文件
遍历文件树，识别以下配置文件：
- package.json, requirements.txt, pom.xml等依赖文件
- webpack.config.js, vite.config.js等构建配置
- Dockerfile, docker-compose.yml等部署配置
- .github/workflows/*.yml等CI/CD配置

### 步骤3：分析依赖文件
读取依赖文件内容，提取：
- 生产依赖（dependencies）
- 开发依赖（devDependencies）
- 版本信息

### 步骤4：关键词匹配
从README和Topics中提取技术关键词，匹配已知的框架和工具。

### 步骤5：生成技术栈报告
将识别结果整理为结构化的技术栈信息。

## 技术栈分类模板

### 前端项目
```yaml
编程语言: [JavaScript, TypeScript]
前端框架: [React, Vue.js, Angular]
UI框架: [Ant Design, Element UI, Material-UI]
状态管理: [Redux, Vuex, MobX]
构建工具: [Webpack, Vite]
CSS工具: [Tailwind CSS, Sass]
测试工具: [Jest, Cypress]
包管理器: [npm, Yarn]
```

### 后端项目
```yaml
编程语言: [Python, Java, Go, Node.js]
后端框架: [Django, Flask, FastAPI, Express, Spring Boot]
数据库: [MySQL, PostgreSQL, MongoDB, Redis]
ORM: [SQLAlchemy, Prisma, Hibernate]
API风格: [REST, GraphQL, gRPC]
测试工具: [pytest, JUnit]
包管理器: [pip, Maven, Go Modules]
```

### 全栈项目
```yaml
前端:
  语言: [JavaScript, TypeScript]
  框架: [React, Vue.js]
  构建: [Vite, Webpack]

后端:
  语言: [Node.js, Python]
  框架: [Express, FastAPI]
  数据库: [PostgreSQL, MongoDB]

部署:
  容器: [Docker]
  CI/CD: [GitHub Actions]
  平台: [Vercel, AWS]
```

### 机器学习项目
```yaml
编程语言: [Python]
深度学习框架: [TensorFlow, PyTorch, Keras]
机器学习库: [scikit-learn, XGBoost]
数据处理: [Pandas, NumPy]
可视化: [Matplotlib, Seaborn]
部署: [Flask API, FastAPI]
```

## 示例分析

### React项目识别
```
文件特征:
- package.json包含react依赖
- src/目录下有.jsx或.tsx文件
- public/index.html文件

技术栈结果:
- 编程语言: JavaScript, TypeScript
- 前端框架: React
- 构建工具: Webpack (react-scripts)
- 包管理器: npm
```

### Python机器学习项目识别
```
文件特征:
- requirements.txt或pyproject.toml
- .py文件
- Jupyter notebook (.ipynb)
- model/目录

技术栈结果:
- 编程语言: Python
- ML框架: TensorFlow/PyTorch
- 数据处理: Pandas, NumPy
- 包管理器: pip
```

### Go微服务项目识别
```
文件特征:
- go.mod文件
- main.go文件
- Dockerfile
- k8s/目录

技术栈结果:
- 编程语言: Go
- 框架: Gin/Echo
- 部署: Docker, Kubernetes
- 包管理器: Go Modules
```