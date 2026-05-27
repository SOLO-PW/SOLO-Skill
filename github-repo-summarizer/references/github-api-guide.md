# GitHub API 使用指南

## 概述

本文档说明如何使用GitHub API获取仓库信息，用于生成推荐文章。

## API端点

### 1. 仓库基本信息

**端点**：`GET /repos/{owner}/{repo}`

**返回数据**：
```json
{
  "name": "仓库名称",
  "full_name": "所有者/仓库名",
  "description": "项目描述",
  "homepage": "项目主页URL",
  "stargazers_count": 12345,
  "forks_count": 678,
  "watchers_count": 12345,
  "open_issues_count": 42,
  "created_at": "2020-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "pushed_at": "2024-01-01T00:00:00Z",
  "license": {
    "name": "MIT License"
  },
  "default_branch": "main",
  "topics": ["javascript", "react", "frontend"],
  "size": 12345,
  "archived": false,
  "disabled": false
}
```

### 2. 编程语言

**端点**：`GET /repos/{owner}/{repo}/languages`

**返回数据**：
```json
{
  "JavaScript": 1234567,
  "TypeScript": 987654,
  "HTML": 45678,
  "CSS": 23456
}
```

**说明**：返回的语言按字节数排序，可以识别主要编程语言。

### 3. README内容

**端点**：`GET /repos/{owner}/{repo}/readme`

**返回数据**：
```json
{
  "content": "Base64编码的README内容",
  "encoding": "base64"
}
```

**解码方法**：
```python
import base64
content = base64.b64decode(data["content"]).decode("utf-8")
```

### 4. 主题标签

**端点**：`GET /repos/{owner}/{repo}/topics`

**返回数据**：
```json
{
  "names": ["javascript", "react", "frontend", "ui"]
}
```

### 5. 贡献者列表

**端点**：`GET /repos/{owner}/{repo}/contributors`

**返回数据**：
```json
[
  {
    "login": "用户名",
    "contributions": 123,
    "avatar_url": "https://avatars.githubusercontent.com/u/123456"
  }
]
```

**说明**：默认返回30位贡献者，按贡献数量排序。

### 6. 版本发布

**端点**：`GET /repos/{owner}/{repo}/releases`

**返回数据**：
```json
[
  {
    "tag_name": "v1.0.0",
    "name": "Release v1.0.0",
    "published_at": "2024-01-01T00:00:00Z",
    "body": "版本说明内容"
  }
]
```

### 7. 文件树

**端点**：`GET /repos/{owner}/{repo}/git/trees/{branch}?recursive=1`

**返回数据**：
```json
{
  "tree": [
    {
      "path": "package.json",
      "type": "blob"
    },
    {
      "path": "src/index.js",
      "type": "blob"
    }
  ]
}
```

**说明**：用于分析项目结构和识别配置文件。

## 请求头设置

### 基本请求头
```python
headers = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "GitHub-Repo-Analyzer"
}
```

### 带访问令牌的请求头
```python
headers = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "GitHub-Repo-Analyzer",
    "Authorization": "token ghp_xxxxxxxxxxxx"
}
```

## 访问令牌

### 何时需要访问令牌
- 访问私有仓库
- 提高API速率限制（未认证：60次/小时，认证：5000次/小时）

### 获取访问令牌
1. 登录GitHub
2. 进入 Settings → Developer settings → Personal access tokens
3. 生成新令牌，选择适当的权限（repo权限用于私有仓库）

## 错误处理

### 常见错误码

| 状态码 | 含义 | 处理方法 |
|--------|------|----------|
| 200 | 成功 | 正常处理 |
| 404 | 仓库不存在 | 检查URL或提示私有仓库 |
| 403 | 速率限制 | 等待或使用访问令牌 |
| 500 | 服务器错误 | 稍后重试 |

### 速率限制检查
```python
response.headers.get("X-RateLimit-Remaining")  # 剩余请求次数
response.headers.get("X-RateLimit-Reset")       # 重置时间
```

## 信息提取流程

### 步骤1：获取基础信息
1. 调用 `/repos/{owner}/{repo}` 获取仓库基本信息
2. 提取名称、描述、Star数、Fork数等

### 步骤2：分析技术栈
1. 调用 `/repos/{owner}/{repo}/languages` 获取语言信息
2. 调用 `/repos/{owner}/{repo}/git/trees/{branch}` 获取文件树
3. 识别配置文件（package.json、requirements.txt等）
4. 从README和Topics中提取技术关键词

### 步骤3：提取功能特性
1. 调用 `/repos/{owner}/{repo}/readme` 获取README内容
2. 解析功能特性章节
3. 提取功能列表

### 步骤4：收集社区数据
1. 调用 `/repos/{owner}/{repo}/contributors` 获取贡献者
2. 调用 `/repos/{owner}/{repo}/releases` 获取版本信息
3. 统计社区活跃度

## 数据处理示例

### 语言占比计算
```python
languages = {"JavaScript": 100000, "TypeScript": 50000, "HTML": 10000}
total = sum(languages.values())
percentages = {lang: (bytes/total)*100 for lang, bytes in languages.items()}
# 结果：{"JavaScript": 62.5, "TypeScript": 31.25, "HTML": 6.25}
```

### 日期格式化
```python
from datetime import datetime

def format_date(iso_date):
    dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    return dt.strftime("%Y年%m月%d日")

# 示例：2024-01-01T00:00:00Z → 2024年01月01日
```

### 数字格式化
```python
def format_number(num):
    if num >= 10000:
        return f"{num/10000:.1f}万"
    return f"{num:,}"

# 示例：12345 → 1.2万，1234 → 1,234
```

## 最佳实践

### 1. 缓存API响应
- 避免重复请求相同数据
- 使用本地缓存减少API调用

### 2. 处理分页
- 贡献者列表默认30条
- 使用 `?per_page=100` 增加每页数量
- 使用 `?page=2` 获取下一页

### 3. 错误重试
- 网络错误时自动重试
- 速率限制时等待并重试

### 4. 批量处理
- 并行请求独立的API端点
- 使用异步请求提高效率