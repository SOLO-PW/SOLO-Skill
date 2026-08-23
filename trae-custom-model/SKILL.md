---
name: trae-custom-model
description: |
  帮助用户在TRAE/SOLO中配置自定义AI模型。当用户提到"TRAE自定义模型"、"添加模型"、"配置API"、"base URL"、"模型ID"、"接入模型"、"第三方模型"、"厂商配置"等关键词时触发。支持自动搜索厂商API文档，提取base URL、模型ID、上下文长度等配置信息，生成标准的TRAE配置指南。
---

# TRAE 自定义模型配置助手

帮助用户在TRAE IDE或SOLO桌面端中配置第三方AI模型服务商的自定义模型。

## 使用方式

**当用户触发此skill后，必须按以下流程主动引导用户：**

### Step 1: 主动询问厂商信息

**不要等待用户提问，立即主动询问：**

> "你好！我可以帮你在TRAE中配置自定义模型。请告诉我你想接入哪个厂商的模型？"
>
> "支持的厂商包括：硅基流动、DeepSeek、智谱AI、百度千帆、讯飞星火、火山方舟、阿里云百炼(通义千问)、零一万物，商汤日日新、百川智能、阶跃星辰、Kimi、MiniMax、腾讯云混元、OpenRouter、Together、Groq等40+厂商。"
>
> "你也可以直接告诉我厂商名称，我会帮你查找配置信息。"

### Step 2: 如果用户不确定厂商

**提供选择建议：**

> "如果你不确定选择哪个厂商，可以告诉我："
> "1. 你主要使用什么模型？（如DeepSeek、GPT、Claude、通义千问等）"
> "2. 你更看重什么？（价格/速度/中文能力/代码能力）"
> "3. 是国内还是海外服务商？"

### Step 3: 获取厂商信息后

**执行以下操作：**

1. **首先查询内置数据库**：运行 `python scripts/search_provider.py <厂商名>`
2. **如果内置数据库有该厂商**：直接展示配置信息
3. **如果内置数据库没有**：使用 WebSearch 搜索该厂商的API文档

### Step 4: 搜索厂商API文档

**搜索关键词组合：**
- `{厂商名} API 文档 base URL OpenAI`
- `{厂商名} 模型列表 model id`
- `{厂商名} OpenAI compatible API endpoint`

### Step 5: 提取并展示配置

**输出格式必须包含：**

```markdown
## {厂商名} 模型配置指南

### 基础配置
| 参数 | 填写值 | 说明 |
|------|--------|------|
| API格式 | OpenAI/Anthropic | 协议类型 |
| 自定义请求地址 | `https://api.xxx.com/v1` | Base URL |
| 完整URL | 关闭/开启 | 是否包含/chat/completions |
| 模型ID | `xxx` | 从下方选择 |

### 推荐模型列表
- `model-id-1` - {模型名称} - 上下文: {长度}
- `model-id-2` - {模型名称} - 上下文: {长度}

### 进阶配置建议
| 参数 | 建议值 | 说明 |
|------|--------|------|
| 模型系列 | 默认/DeepSeek/Claude/GPT | 根据模型选择 |
| 上下文长度 | {官方值} | 不建议修改 |
| 多模态 | 开启/关闭 | 根据模型能力 |

### 配置步骤
1. **TRAE IDE**: 设置 → 模型 → 添加模型 → 自定义配置
2. **SOLO桌面端**: 左下角头像 → 设置 → 模型 → 添加模型
3. 填写上述参数
4. 添加API Key
5. 点击确认

### 注意事项
- ⚠️ 模型ID区分大小写，务必准确填写
- ⚠️ 上下文长度建议使用官方值，过高会导致降智
- ⚠️ 如连接失败，检查"完整URL"开关是否正确
```

### Step 6: 询问是否需要更多帮助

**配置展示后，主动询问：**

> "配置信息已生成。你还需要："
> "1. 查看其他厂商的配置对比？"
> "2. 了解如何获取API Key？"
> "3. 排查连接问题？"
> "4. 配置其他模型？"

## 核心功能

1. **自动搜索厂商API文档** - 根据用户提供的厂商名称，搜索官方API文档
2. **提取关键配置信息**:
   - Base URL / API Endpoint
   - 支持的模型ID列表
   - 官方上下文长度配置
   - 支持的API协议 (OpenAI/Anthropic)
   - 多模态支持情况
3. **生成配置指南** - 输出符合TRAE要求的配置步骤和参数

## 模型清单自动更新机制

### 更新频率配置

| 频率 | 说明 | 适用场景 |
|------|------|----------|
| `weekly` | 每周更新一次 | 推荐大多数用户 |
| `monthly` | 每月更新一次 | 变化较少的厂商 |
| `manual` | 手动更新 | 需要完全控制 |

**配置文件**: `references/update_config.json`

### 更新脚本

**基本用法:**
```bash
# 官方接口探测（直接校验模型ID真实性，推荐先用）
python scripts/update_models.py --probe-only

# 检查更新（推荐首次使用，含官方接口核验 + 停用同步摘要）
python scripts/update_models.py --check-only

# 模拟运行（查看将要进行的更改）
python scripts/update_models.py --dry-run

# 执行更新
python scripts/update_models.py

# 交互式向导
python scripts/update_models.py --wizard
```

**参数说明:**
| 参数 | 说明 |
|------|------|
| `--check-only` | 只检查不修改，输出停用/变更同步摘要（供定时任务主动通知用户） |
| `--dry-run` | 模拟运行 |
| `--wizard` | 交互式向导 |
| `--auto-search` | 自动搜索最新模型（需要网络） |
| `--probe` | 开启官方接口探测（默认开启） |
| `--no-probe` | 关闭官方接口探测（离线场景） |
| `--probe-only` | 仅执行官方接口探测，输出模型核验报告 |

**动态年份：** 搜索关键词不再硬编码年份，运行时自动替换为当前年份，避免逐年过期。

**模型真实性核验：** 脚本会对厂商 `GET /v1/models` 接口做直接探测，命中官方清单的模型标记为 `verified`；需鉴权的标记 `🔑`；探测未命中的标记为疑似杜撰。可通过设置 `OPENAI_API_KEY`、`DEEPSEEK_API_KEY` 等环境变量进行带 Key 的完整探测。

### 定时任务设置

#### 方法1: Windows 任务计划程序

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器: 每周一 09:00
4. 操作: 启动程序
5. 程序/脚本: `python`
6. 参数: `scripts\update_models.py --check-only`
7. 起始位置: `D:\codeFile\SOLO-Skill\trae-custom-model`

#### 方法2: SOLO 定时任务

使用 SOLO 的 Schedule 工具创建自动化任务：

```
创建每周定时任务，每周一上午9点检查模型更新
任务内容:
1. 运行 python scripts/update_models.py --check-only
2. 解析输出中的「SYNC SUMMARY」部分
3. 对 [DEPRECATED] 停用模型，通知用户立即替换为替代方案
4. 对 [UNVERIFIED] 疑似杜撰/未核验模型，提示用户以官方文档为准
5. 如有新模型建议 [SUGGESTION]，更新 references/update_config.json
```

#### 方法3: GitHub Actions (可选)

在 skill 仓库创建 `.github/workflows/update-models.yml`:

```yaml
name: Weekly Model Update Check

on:
  schedule:
    - cron: '0 1 * * 1'  # 每周一 09:00 北京时间
  workflow_dispatch:       # 手动触发

jobs:
  update-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Check updates
        run: python scripts/update_models.py --check-only
```

### 更新内容

脚本会自动:
1. ✅ 官方接口探测（`GET /models`）校验模型ID真实性
2. ✅ 检查已知停用模型状态
3. ✅ 检测新增/变更模型
4. ✅ 更新 `references/providers.md`
5. ✅ 更新 `references/model_changelog.md`
6. ✅ 记录更新历史到 `references/update_config.json`
7. ✅ 记录检查历史和统计信息
8. ✅ `--check-only` 输出「SYNC SUMMARY」供定时任务同步停用/变更给用户

### 查看更新日志

| 文件 | 说明 |
|------|------|
| `references/model_changelog.md` | 模型变更历史记录 |
| `references/update_config.json` | 完整配置和历史 |
| 控制台输出 | 实时更新进度 |

### 质量保证

- **检查次数统计**: 记录总检查次数和成功更新数
- **厂商状态追踪**: 每个厂商单独记录状态
- **问题记录**: 记录检查中发现的问题
- **置信度评估**: 模型ID的可信度分级（high/medium/low）
- **真实性核验**: 通过官方接口探测标记 `verified` / `requires_auth` / `unverified`，疑似杜撰模型会单列提示

### 交互式向导

运行 `python scripts/update_models.py --wizard` 可进入交互式模式:

```
🎯 TRAE 模型配置更新向导

请选择操作:
1. 立即检查更新
2. 设置更新频率
3. 查看更新历史
4. 查看统计信息
5. 重置配置
0. 退出
```

### 最佳实践

1. **首次使用**: 先用 `--check-only` 了解当前状态
2. **定期检查**: 设置每周定时任务自动检查
3. **查看日志**: 每次更新后查看 `model_changelog.md`
4. **备份配置**: `update_config.json` 包含所有历史记录

---

## TRAE配置界面说明

### 添加位置

**TRAE IDE:**
- 设置 → 模型 → 添加模型
- 或对话框模型清单 → 添加模型

**SOLO桌面端:**
- 左下角头像 → 设置 → 模型 → 添加模型

### 基础配置要点

1. **选择自定义配置**，API格式选择OpenAI（兼容性最好）
2. **自定义请求地址**：
   - 大部分厂商URL不含 `/chat/completions` 尾缀，关闭"完整URL"按钮
   - 少数厂商（如Kimi、MiniMax）有特殊路径，需开启并填写完整URL
3. **模型ID**：必须从官方文档查询，每家厂商命名规则不同
4. **多模态**：根据模型实际能力开启，不要强行开启

### 进阶配置要点

1. **模型系列**：选择预设模板（DeepSeek/Claude/GPT）或默认
2. **上下文长度**：设置为模型官方配置值，不是越高越好
   - 过高会导致降智和失忆
   - 格式：输入+输出总和
3. **工具调用轮次**：非专业人士保持默认200次

## 常见厂商速查

### 国内热门厂商

| 厂商 | Base URL | 协议 | 最新模型 |
|------|----------|------|----------|
| 硅基流动 | `https://api.siliconflow.cn/v1` | OpenAI | DeepSeek-V4-Pro, GLM-5-Turbo |
| DeepSeek官方 | `https://api.deepseek.com` | OpenAI | deepseek-v4-pro, deepseek-v4-flash |
| 智谱AI | `https://open.bigmodel.cn/api/paas/v4` | OpenAI | glm-5-turbo, glm-5.1 |
| 阿里云百炼 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | OpenAI | qwen3.6-max-preview |
| 零一万物 | `https://api.lingyiwanwu.com/v1` | OpenAI | yi-large, yi-medium |
| 阶跃星辰 | `https://api.stepfun.com/v1` | OpenAI | step-3.5-flash, step-2 |
| Kimi | `https://api.kimi.com/coding/v1/messages` | Anthropic | kimi-k2.6 |
| 讯飞星火 | `https://maas-coding-api.cn-huabei-1.xf-yun.com/v2` | OpenAI | x1, x2, x3 |

### 国际热门厂商

| 厂商 | Base URL | 协议 | 最新模型 |
|------|----------|------|----------|
| OpenAI | `https://api.openai.com/v1` | OpenAI | gpt-5.5 |
| Anthropic | `https://api.anthropic.com/v1/messages` | Anthropic | claude-opus-4.7 |
| Groq | `https://api.groq.com/openai/v1` | OpenAI | llama-3.3-70b |
| Together | `https://api.together.xyz/v1` | OpenAI | DeepSeek-V4-Pro |

### 聚合平台

| 平台 | Base URL | 说明 |
|------|----------|------|
| OpenRouter | `https://openrouter.ai/api/v1` | 聚合多家模型 |
| 302.ai | `https://api.302.ai/v1` | 国内聚合平台 |

## 重要提醒

1. **模型ID必须准确**：每家厂商命名规则不同，务必查询官方文档
2. **Base URL格式**：
   - 标准格式：`https://api.xxx.com/v1`（不含尾缀）
   - 完整格式：`https://api.xxx.com/v1/chat/completions`
3. **上下文长度**：使用官方推荐值，盲目调高会导致性能下降
4. **协议选择**：优先使用OpenAI协议，兼容性最好

## 故障排查

### 连接失败排查清单

1. ✅ API Key 是否正确？
2. ✅ Base URL 是否完整？（检查"完整URL"开关）
3. ✅ 模型ID 是否准确？（区分大小写）
4. ✅ 协议选择是否正确？（OpenAI vs Anthropic）
5. ✅ 网络是否能访问该API地址？

### 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| 404 | Base URL错误 | 检查"完整URL"开关 |
| 401 | API Key错误 | 重新获取API Key |
| 模型不存在 | 模型ID错误 | 核对官方文档 |
| 降智/失忆 | 上下文设置过高 | 使用官方推荐值 |

## 资源参考

| 文件 | 说明 |
|------|------|
| `references/providers.md` | 详细厂商配置参考 |
| `references/update_config.json` | 更新配置、厂商状态、历史记录 |
| `references/model_changelog.md` | 模型变更日志 |
| `scripts/search_provider.py` | 厂商配置查询脚本 |
| `scripts/update_models.py` | 模型清单更新脚本 v2.0 |

**厂商配置查询:**
```bash
python scripts/search_provider.py <厂商名>
```

**模型更新检查:**
```bash
python scripts/update_models.py --check-only
```

**交互式更新向导:**
```bash
python scripts/update_models.py --wizard
```

## 交互示例

**用户**: "我想在TRAE里加个模型"

**助手**: "你好！我可以帮你在TRAE中配置自定义模型。请告诉我你想接入哪个厂商的模型？

支持的厂商包括：硅基流动、DeepSeek、智谱AI、百度千帆、讯飞星火、火山方舟、阿里云百炼(通义千问)、零一万物，商汤日日新、百川智能、阶跃星辰、Kimi、MiniMax、腾讯云混元、OpenRouter、Together、Groq等40+厂商。

你也可以直接告诉我厂商名称，我会帮你查找配置信息。"

---

**用户**: "硅基流动"

**助手**: [查询内置数据库] → [展示硅基流动配置] → [询问是否需要其他帮助]

---

**用户**: "有个叫XXX的厂商"

**助手**: [内置数据库无该厂商] → [WebSearch搜索] → [提取配置] → [展示结果]

---

**用户**: "更新模型清单"

**助手**: [运行 update_models.py] → [检查更新] → [展示更新结果]
