# 快速参考卡片

## GitHub仓库URL格式

### 支持的格式
```
https://github.com/用户名/仓库名
https://github.com/用户名/仓库名.git
git@github.com:用户名/仓库名.git
github.com/用户名/仓库名
```

### URL解析正则
```regex
github\.com/([^/]+)/([^/]+?)(?:\.git)?$
```

## WebFetch访问地址

### 仓库主页
```
https://github.com/{owner}/{repo}
```

### README文件
```
https://raw.githubusercontent.com/{owner}/{repo}/main/README.md
https://raw.githubusercontent.com/{owner}/{repo}/master/README.md
```

### package.json（Node.js项目）
```
https://raw.githubusercontent.com/{owner}/{repo}/main/package.json
```

### requirements.txt（Python项目）
```
https://raw.githubusercontent.com/{owner}/{repo}/main/requirements.txt
```

## 信息提取清单

### 基础信息
- [ ] 项目名称（name）
- [ ] 项目描述（description）
- [ ] Star数量（stargazers_count）
- [ ] Fork数量（forks_count）
- [ ] 最后更新时间（updated_at）
- [ ] 开源许可证（license）
- [ ] 主题标签（topics）

### README信息
- [ ] 项目简介
- [ ] 功能特性列表
- [ ] 安装说明
- [ ] 使用示例
- [ ] 图片/截图链接
- [ ] 技术栈说明

### 技术栈信息
- [ ] 编程语言
- [ ] 框架/库
- [ ] 数据库
- [ ] 构建工具
- [ ] 包管理器
- [ ] 部署平台

## 技术栈识别关键词

### 前端框架
| 关键词 | 框架 |
|--------|------|
| react | React |
| vue | Vue.js |
| angular | Angular |
| svelte | Svelte |
| next | Next.js |
| nuxt | Nuxt.js |

### 后端框架
| 关键词 | 框架 |
|--------|------|
| express | Express.js |
| django | Django |
| flask | Flask |
| fastapi | FastAPI |
| spring | Spring Boot |
| laravel | Laravel |
| nest | NestJS |

### 数据库
| 关键词 | 数据库 |
|--------|--------|
| mysql | MySQL |
| postgres | PostgreSQL |
| mongo | MongoDB |
| redis | Redis |
| sqlite | SQLite |
| elasticsearch | Elasticsearch |

### 构建工具
| 关键词 | 工具 |
|--------|------|
| webpack | Webpack |
| vite | Vite |
| rollup | Rollup |
| babel | Babel |
| eslint | ESLint |
| prettier | Prettier |

### 部署工具
| 关键词 | 工具 |
|--------|------|
| docker | Docker |
| kubernetes | Kubernetes |
| k8s | Kubernetes |
| vercel | Vercel |
| netlify | Netlify |
| aws | AWS |

## 快速开始命令模板

### JavaScript/TypeScript项目
```bash
# 克隆项目
git clone https://github.com/{owner}/{repo}.git
cd {repo}

# 安装依赖（选择一种）
npm install
yarn install
pnpm install

# 启动项目
npm start
yarn start
pnpm start
```

### Python项目
```bash
# 克隆项目
git clone https://github.com/{owner}/{repo}.git
cd {repo}

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖（选择一种）
pip install -r requirements.txt
poetry install
pipenv install

# 运行项目
python main.py
python app.py
```

### Go项目
```bash
# 克隆项目
git clone https://github.com/{owner}/{repo}.git
cd {repo}

# 下载依赖
go mod download

# 运行项目
go run main.go
go run .
```

### Rust项目
```bash
# 克隆项目
git clone https://github.com/{owner}/{repo}.git
cd {repo}

# 编译项目
cargo build --release

# 运行项目
cargo run
```

### Java项目
```bash
# 克隆项目
git clone https://github.com/{owner}/{repo}.git
cd {repo}

# Maven构建
mvn clean install
mvn spring-boot:run

# Gradle构建
./gradlew build
./gradlew bootRun
```

## 数字格式化规则

### Star/Fork数量
```
< 1000    → 直接显示，如：999
1000-9999 → 使用千位分隔符，如：1,234
>= 10000  → 使用万为单位，如：1.2万
```

### 日期格式
```
原始格式：2024-01-15T10:30:00Z
显示格式：2024年01月15日
```

## 活跃度评估标准

### 根据最后更新时间
```
<= 7天   → 非常活跃 🔥
<= 30天  → 活跃
<= 90天  → 一般
> 90天   → 不太活跃
```

### 根据Star数量
```
> 10000  → 社区认可度高
> 1000   → 有一定社区基础
> 100    → 新兴项目
< 100    → 小众项目
```

## 文档质量评估

### 评分标准
```
>= 80分  → 优秀
>= 60分  → 良好
>= 40分  → 一般
>= 20分  → 较差
< 20分   → 很差
```

### 检查项
- 项目描述（5分）
- 安装说明（5分）
- 使用说明（5分）
- 功能特性（5分）
- 代码示例（5分）
- 标题结构（5分）
- 图片/截图（5分）
- 许可证（5分）

## 适用场景推断

### 前端项目
- 前端单页应用(SPA)开发
- 服务端渲染(SSR)应用开发
- 静态网站开发
- 移动端H5开发

### 后端项目
- 后端API服务开发
- 微服务架构开发
- RESTful API开发
- GraphQL API开发

### 移动端项目
- 跨平台移动应用开发
- iOS应用开发
- Android应用开发

### 数据科学项目
- 机器学习模型开发
- 数据分析和处理
- 深度学习研究

### DevOps项目
- 容器化部署和编排
- CI/CD流水线搭建
- 自动化运维

## 交互式提问模板

### 需求确认
```
为了生成更符合您需求的文章，想确认几个问题：
1. 这篇文章的主要目的是什么？（推荐/介绍/分析）
2. 目标读者是谁？（开发者/产品经理/普通用户）
3. 您希望重点介绍哪些方面？
```

### 信息补充
```
这个仓库的信息比较简洁，为了生成更丰富的文章，您能否提供：
1. 项目的主要使用场景？
2. 与其他类似项目相比的优势？
3. 是否有实际应用案例可以分享？
```

### 后续优化
```
文章已生成完成！您是否需要：
1. 补充更多技术细节？
2. 添加使用案例或代码示例？
3. 与其他类似项目进行对比？
4. 调整文章风格或重点？
```

## 文章结构模板

### 标准结构
```markdown
# [项目名称]：[一句话描述]

![项目截图](图片URL)

## 📋 项目简介
[项目描述]

## 🎯 主要功能
- 功能1
- 功能2
- 功能3

## 🛠️ 技术栈
| 类别 | 技术 |
|------|------|
| 语言 | ... |
| 框架 | ... |

## 🚀 快速开始
```bash
[安装命令]
```

## 📊 项目数据
- ⭐ Star：数量
- 🍴 Fork：数量

## 💡 适用场景
- 场景1
- 场景2

## 🔗 相关链接
- [仓库](URL)
- [文档](URL)

## 📝 总结
[推荐理由]
```

## 错误处理

### 常见错误
```
仓库不存在 → 检查URL是否正确
私有仓库   → 需要访问权限
网络错误   → 检查网络连接
README缺失 → 使用项目描述
```

### 占位符文本
```
[待补充：项目简介]
[待补充：主要功能]
[待补充：技术栈详情]
[待补充：快速开始指南]
[待补充：适用场景]
```