# Bilibili UP主分析技能 - 接口设计文档

## 概述

本文档描述Bilibili UP主分析技能中使用的数据接口设计。技能通过调用Bilibili公开API获取UP主和视频数据。

## 数据源说明

技能使用Bilibili官方公开API作为数据源，主要包括以下接口：

### 1. UP主信息接口

**接口地址**: `https://api.bilibili.com/x/space/acc/info`

**请求方法**: GET

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| mid | string | 是 | UP主UID |

**响应示例**:

```json
{
  "code": 0,
  "message": "0",
  "ttl": 1,
  "data": {
    "mid": 123456,
    "name": "UP主名称",
    "sex": "男",
    "face": "头像URL",
    "sign": "个性签名",
    "level": 6,
    "follower": 100000,
    "following": 100,
    "archive_count": 500,
    "article_count": 10,
    "like_num": 500000
  }
}
```

**字段说明**:

| 字段 | 类型 | 说明 |
|------|------|------|
| mid | int | UP主UID |
| name | string | 昵称 |
| face | string | 头像URL |
| sign | string | 个性签名 |
| level | int | 账号等级(0-6) |
| follower | int | 粉丝数 |
| following | int | 关注数 |
| archive_count | int | 视频投稿数 |
| article_count | int | 专栏投稿数 |
| like_num | int | 获赞数 |

### 2. 视频列表接口

**接口地址**: `https://api.bilibili.com/x/space/arc/search`

**请求方法**: GET

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| mid | string | 是 | UP主UID |
| pn | int | 否 | 页码，默认1 |
| ps | int | 否 | 每页数量，默认30，最大50 |
| order | string | 否 | 排序方式：pubdate(发布时间), click(播放量), stow(收藏) |

**响应示例**:

```json
{
  "code": 0,
  "message": "0",
  "ttl": 1,
  "data": {
    "list": {
      "vlist": [
        {
          "bvid": "BV1xx411c7mD",
          "title": "视频标题",
          "description": "视频简介",
          "created": 1609459200,
          "length": "10:30",
          "pic": "封面URL",
          "play": 10000,
          "comment": 100,
          "typeid": 36,
          "typename": "知识",
          "video_review": 500
        }
      ]
    },
    "page": {
      "pn": 1,
      "ps": 30,
      "count": 100
    }
  }
}
```

**字段说明**:

| 字段 | 类型 | 说明 |
|------|------|------|
| bvid | string | 视频BV号 |
| title | string | 视频标题 |
| description | string | 视频简介 |
| created | int | 发布时间戳 |
| length | string | 视频时长 |
| pic | string | 封面URL |
| play | int | 播放量 |
| comment | int | 评论数 |
| typeid | int | 分区ID |
| typename | string | 分区名称 |
| video_review | int | 弹幕数 |

### 3. 视频详情接口

**接口地址**: `https://api.bilibili.com/x/web-interface/view`

**请求方法**: GET

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| bvid | string | 是 | 视频BV号 |

**响应示例**:

```json
{
  "code": 0,
  "message": "0",
  "ttl": 1,
  "data": {
    "bvid": "BV1xx411c7mD",
    "aid": 12345678,
    "title": "视频标题",
    "desc": "视频描述",
    "duration": 630,
    "pubdate": 1609459200,
    "owner": {
      "mid": 123456,
      "name": "UP主名称"
    },
    "stat": {
      "view": 10000,
      "danmaku": 500,
      "reply": 100,
      "favorite": 1000,
      "coin": 500,
      "share": 200,
      "like": 2000,
      "dislike": 10
    },
    "tname": "知识",
    "tid": 36
  }
}
```

**字段说明**:

| 字段 | 类型 | 说明 |
|------|------|------|
| bvid | string | 视频BV号 |
| aid | int | 视频AV号 |
| title | string | 视频标题 |
| desc | string | 视频描述 |
| duration | int | 视频时长(秒) |
| pubdate | int | 发布时间戳 |
| owner.mid | int | UP主UID |
| owner.name | string | UP主昵称 |
| stat.view | int | 播放量 |
| stat.danmaku | int | 弹幕数 |
| stat.reply | int | 评论数 |
| stat.favorite | int | 收藏数 |
| stat.coin | int | 投币数 |
| stat.share | int | 分享数 |
| stat.like | int | 点赞数 |
| stat.dislike | int | 点踩数 |
| tname | string | 分区名称 |
| tid | int | 分区ID |

## 数据模型

### UP主信息模型 (UpInfo)

```python
{
    "uid": str,              # UP主UID
    "name": str,             # 昵称
    "face": str,             # 头像URL
    "sign": str,             # 个性签名
    "level": int,            # 账号等级
    "follower": int,         # 粉丝数
    "following": int,        # 关注数
    "archive_count": int,    # 视频投稿数
    "article_count": int,    # 专栏投稿数
    "like_num": int,         # 获赞数
}
```

### 视频基础信息模型 (VideoBase)

```python
{
    "bvid": str,             # 视频BV号
    "title": str,            # 视频标题
    "description": str,      # 视频简介
    "created": int,          # 发布时间戳
    "length": str,           # 视频时长(字符串)
    "pic": str,              # 封面URL
    "play": int,             # 播放量
    "comment": int,          # 评论数
    "typeid": int,           # 分区ID
    "typename": str,         # 分区名称
    "video_review": int,     # 弹幕数
}
```

### 视频详细信息模型 (VideoDetail)

```python
{
    "bvid": str,             # 视频BV号
    "aid": int,              # 视频AV号
    "title": str,            # 视频标题
    "description": str,      # 视频描述
    "duration": int,         # 视频时长(秒)
    "pubdate": int,          # 发布时间戳
    "owner": {
        "mid": int,          # UP主UID
        "name": str,         # UP主昵称
    },
    "stat": {
        "view": int,         # 播放量
        "danmaku": int,      # 弹幕数
        "reply": int,        # 评论数
        "favorite": int,     # 收藏数
        "coin": int,         # 投币数
        "share": int,        # 分享数
        "like": int,         # 点赞数
        "dislike": int,      # 点踩数
    },
    "tname": str,            # 分区名称
    "tid": int,              # 分区ID
}
```

## 错误处理

### 错误码说明

| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| 0 | 成功 | - |
| -400 | 请求错误 | 检查请求参数 |
| -403 | 访问被拒绝 | 可能是频率限制，稍后重试 |
| -404 | 资源不存在 | 检查UID或BV号是否正确 |
| -500 | 服务器错误 | 稍后重试 |
| -503 | 服务暂不可用 | 稍后重试 |

### 网络错误处理

技能内置以下网络错误处理机制：

1. **自动重试**: 请求失败时自动重试3次
2. **指数退避**: 每次重试间隔1秒
3. **超时设置**: 单次请求超时10秒
4. **异常捕获**: 捕获所有网络异常并返回友好提示

## 频率限制

### 限制策略

Bilibili API存在频率限制，技能采用以下策略应对：

1. **请求间隔**: 分页请求间隔0.5秒
2. **缓存机制**: 数据缓存24小时，减少重复请求
3. **增量更新**: 优先使用缓存，仅获取新数据

### 建议

- 启用缓存功能 (`--cache`)
- 避免频繁分析同一UP主
- 大量数据分析时选择非高峰时段

## 数据安全

### 数据使用规范

1. 仅获取公开可见的数据
2. 不存储用户隐私信息
3. 遵守Bilibili用户协议
4. 数据仅用于分析目的，不用于商业用途

### 缓存安全

- 缓存数据存储在本地
- 缓存文件使用哈希命名，避免信息泄露
- 支持手动清除缓存

## 扩展接口

如需使用第三方数据服务，可实现以下接口：

### 自定义数据获取器

```python
class CustomDataFetcher:
    def get_up_info(self, uid: str) -> Dict[str, Any]:
        """获取UP主信息"""
        pass
    
    def get_video_list(self, uid: str, page: int, page_size: int) -> List[Dict[str, Any]]:
        """获取视频列表"""
        pass
    
    def get_video_detail(self, bvid: str) -> Dict[str, Any]:
        """获取视频详情"""
        pass
```

### 接口适配器

```python
class DataFetcherAdapter:
    def __init__(self, fetcher):
        self.fetcher = fetcher
    
    def adapt_up_info(self, raw_data: Dict) -> Dict[str, Any]:
        """适配UP主信息格式"""
        return {
            "uid": str(raw_data.get("mid", "")),
            "name": raw_data.get("name", ""),
            # ... 其他字段映射
        }
```

## 更新日志

### v1.0.0

- 初始版本
- 支持基础UP主信息获取
- 支持视频列表和详情获取
- 实现数据缓存机制
