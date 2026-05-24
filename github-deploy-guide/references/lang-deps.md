# 多语言依赖安装模板

根据项目语言自动选择对应的依赖安装命令。检测依据：仓库根目录的包管理文件。

## 语言检测映射

| 语言 | 检测文件 | 包管理器 |
|------|---------|---------|
| Python | `requirements.txt`、`pyproject.toml`、`setup.py`、`Pipfile` | pip / poetry / pipenv |
| Node.js | `package.json` | npm / yarn / pnpm |
| Go | `go.mod` | go modules |
| Rust | `Cargo.toml` | cargo |
| Java | `pom.xml`、`build.gradle`、`build.gradle.kts` | Maven / Gradle |
| PHP | `composer.json` | composer |
| Ruby | `Gemfile` | bundler |
| Swift | `Package.swift` | swift package manager |

---

## Python

### 检测文件

- `requirements.txt` → pip
- `pyproject.toml` → 可能是 pip 或 poetry
- `Pipfile` → pipenv
- `setup.py` → pip（旧式）

### 安装命令

**pip（标准方式）：**
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

**poetry：**
```bash
# 安装 poetry（如未安装）
pip install poetry

# 安装依赖
poetry install

# 进入虚拟环境
poetry shell
```

**pipenv：**
```bash
# 安装 pipenv（如未安装）
pip install pipenv

# 安装依赖
pipenv install

# 激活虚拟环境
pipenv shell
```

### 国内镜像源

```bash
# pip 临时使用清华镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# pip 永久配置（推荐）
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# poetry 配置镜像
poetry config repositories.tsinghua https://pypi.tuna.tsinghua.edu.cn/simple/
poetry source add tsinghua https://pypi.tuna.tsinghua.edu.cn/simple/ --priority=primary
```

### 常见问题

- **Python 版本不兼容**：检查 `pyproject.toml` 中的 `requires-python` 或 `.python-version` 文件
- **pip 版本过旧**：`pip install --upgrade pip`
- **权限问题（Linux/Mac）**：始终使用虚拟环境，不要 `sudo pip install`

---

## Node.js

### 检测文件

- `package.json` → npm / yarn / pnpm
- `pnpm-lock.yaml` → pnpm
- `yarn.lock` → yarn
- `package-lock.json` → npm

### 安装命令

**npm：**
```bash
npm install
```

**yarn：**
```bash
# 安装 yarn（如未安装）
npm install -g yarn

yarn install
```

**pnpm：**
```bash
# 安装 pnpm（如未安装）
npm install -g pnpm

pnpm install
```

### 国内镜像源

```bash
# npm 临时使用淘宝镜像
npm install --registry=https://registry.npmmirror.com

# npm 永久配置
npm config set registry https://registry.npmmirror.com

# yarn 配置
yarn config set registry https://registry.npmmirror.com

# pnpm 配置
pnpm config set registry https://registry.npmmirror.com
```

### 常见问题

- **Node.js 版本不匹配**：检查 `package.json` 中的 `engines` 字段；推荐使用 nvm 管理版本
- **node-gyp 编译失败（Windows）**：需要安装 `npm install -g windows-build-tools` 或 Visual Studio Build Tools
- **依赖冲突**：删除 `node_modules` 和锁文件后重新安装

---

## Go

### 检测文件

- `go.mod`

### 安装命令

```bash
# 下载依赖
go mod download

# 编译项目
go build -o {binary_name} .

# 或直接运行
go run .
```

### 国内镜像源

```bash
# 设置 GOPROXY（七牛云镜像）
go env -w GOPROXY=https://goproxy.cn,direct

# 验证
go env GOPROXY
```

### 常见问题

- **Go 版本不兼容**：检查 `go.mod` 中的 `go` 指令版本
- **CGO 相关错误**：Windows 上需要 MinGW-w64 或 TDM-GCC
- **私有模块**：配置 `GOPRIVATE` 环境变量

---

## Rust

### 检测文件

- `Cargo.toml`

### 安装命令

```bash
# 编译项目
cargo build --release

# 运行项目
cargo run

# 仅编译（不运行）
cargo build
```

### 国内镜像源

在 `~/.cargo/config.toml`（Windows: `%USERPROFILE%\.cargo\config.toml`）中配置：

```toml
[source.crates-io]
replace-with = 'ustc'

[source.ustc]
registry = "sparse+https://mirrors.ustc.edu.cn/crates.io-index/"
```

### 常见问题

- **编译时间过长**：Rust 首次编译较慢，后续增量编译会快很多
- **Rust 工具链版本**：使用 `rustup update` 更新到最新稳定版
- **OpenSSL 链接错误（Windows）**：安装 vcpkg 并设置环境变量

---

## Java

### 检测文件

- `pom.xml` → Maven
- `build.gradle` / `build.gradle.kts` → Gradle

### 安装命令

**Maven：**
```bash
# 编译并打包
mvn clean package -DskipTests

# 运行
java -jar target/{jar_name}.jar
```

**Gradle：**
```bash
# 使用 Gradle Wrapper（推荐，项目通常自带）
./gradlew build -x test

# 运行
./gradlew bootRun    # Spring Boot 项目
# 或
java -jar build/libs/{jar_name}.jar
```

### 国内镜像源

**Maven**（修改 `~/.m2/settings.xml`）：
```xml
<mirrors>
  <mirror>
    <id>aliyun</id>
    <mirrorOf>central</mirrorOf>
    <url>https://maven.aliyun.com/repository/central</url>
  </mirror>
</mirrors>
```

**Gradle**（修改 `build.gradle` 或 `settings.gradle`）：
```groovy
repositories {
    maven { url 'https://maven.aliyun.com/repository/central' }
    maven { url 'https://maven.aliyun.com/repository/public' }
}
```

### 常见问题

- **Java 版本不匹配**：检查 `pom.xml` 中的 `<java.version>` 或 `build.gradle` 中的 `sourceCompatibility`
- **Maven 下载慢**：配置阿里云镜像
- **Gradle Wrapper 不存在**：运行 `gradle wrapper` 生成

---

## PHP

### 检测文件

- `composer.json`

### 安装命令

```bash
# 安装依赖
composer install

# 或不安装开发依赖（生产环境）
composer install --no-dev --optimize-autoloader
```

### 国内镜像源

```bash
# 配置阿里云镜像（全局）
composer config -g repo.packagist composer https://mirrors.aliyun.com/composer/

# 或项目级别
composer config repo.packagist composer https://mirrors.aliyun.com/composer/
```

### 常见问题

- **PHP 版本不兼容**：检查 `composer.json` 中的 `require.php`
- **PHP 扩展缺失**：根据 `composer.json` 的 `require` 中列出的扩展安装（如 `ext-pdo`、`ext-mbstring`）
- **权限问题（Linux）**：避免 `sudo composer`，修复目录权限

---

## Ruby

### 检测文件

- `Gemfile`

### 安装命令

```bash
# 安装依赖
bundle install
```

### 国内镜像源

```bash
# 配置清华镜像
bundle config mirror.https://rubygems.org https://mirrors.tuna.tsinghua.edu.cn/rubygems/
```

### 常见问题

- **Ruby 版本不兼容**：检查 `Gemfile` 中的 `ruby` 指令；推荐使用 rbenv 或 rvm 管理版本
- **Bundler 未安装**：`gem install bundler`
- **原生扩展编译失败**：安装 build-essential（Linux）或 Xcode Command Line Tools（macOS）

---

## Swift

### 检测文件

- `Package.swift`

### 安装命令

```bash
# 构建项目
swift build

# 运行项目
swift run

# 或使用 Xcode 打开
swift package generate-xcodeproj
```

### 常见问题

- **仅限 macOS**：Swift 服务端项目在 Linux 上也可运行，但开发通常在 macOS 上
- **Xcode 版本**：确保 Xcode 版本与 Swift 版本匹配
- **依赖解析失败**：删除 `.build` 目录后重新 `swift package resolve`
