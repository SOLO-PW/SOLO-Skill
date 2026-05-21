# TRAE 自定义模型配置助手

<p align="center">
  <strong>让 AI 模型接入像喝水一样简单</strong><br>
  <em>支持 60+ 国内外厂商，一键生成 TRAE 标准配置</em>
</p>

<p align="center">
  <a href="#-功能特性">功能特性</a> •
  <a href="#-快速开始">快速开始</a> •
  <a href="#-支持厂商">支持厂商</a> •
  <a href="#-使用示例">使用示例</a> •
  <a href="#-自动更新">自动更新</a> •
  <a href="#-项目结构">项目结构</a>
</p>

---

## ✨ 功能特性

- 🚀 **60+ 厂商内置数据库** - 覆盖国内外主流 AI 服务商
- 🔍 **智能主动引导** - 6 步交互流程，新手也能轻松配置
- 📋 **标准配置生成** - 自动提取 Base URL、模型 ID、上下文长度
- 🔄 **自动更新机制** - 定期检查模型变更，保持信息最新
- 🛡️ **停用模型检测** - 自动识别 deprecated 模型，避免踩坑
- 📊 **质量指标追踪** - 记录更新历史，可追溯可审计

---

## 🚀 快速开始

### 安装方式

将本 Skill 文件夹拖入 SOLO 即可使用。

### 基本使用

在 SOLO 中输入以下任意关键词触发 Skill：

```
"我想在 TRAE 里配置模型"
"怎么接入 DeepSeek"
"配置硅基流动"
"智谱 GLM-5.1 怎么配"
"第三方模型 Base URL"
```

### 使用流程

1. **触发 Skill** - 输入配置需求
2. **选择厂商** - Skill 主动询问目标厂商
3. **获取配置** - 自动生成完整配置指南
4. **复制粘贴** - 将参数填入 TRAE 设置

---

## 🏢 支持厂商

### 国内厂商

| 厂商 | Base URL | 最新模型 |
|------|----------|----------|
| **硅基流动** | `https://api.siliconflow.cn/v1` | DeepSeek-V4-Pro, GLM-5-Turbo |
| **DeepSeek** | `https://api.deepseek.com` | deepseek-v4-pro, deepseek-v4-flash |
| **智谱AI** | `https://open.bigmodel.cn/api/paas/v4` | glm-5-turbo, glm-5.1 |
| **阿里云百炼** | `https://dashscope.aliyuncs.com/compatible-mode/v1` | qwen3.6-max-preview |
| **Kimi** | `https://api.kimi.com/coding/v1/messages` | kimi-k2.6 |
| **零一万物** | `https://api.lingyiwanwu.com/v1` | yi-large, yi-medium |
| **阶跃星辰** | `https://api.stepfun.com/v1` | step-3.5-flash, step-2 |
| **讯飞星火** | `https://maas-coding-api.cn-huabei-1.xf-yun.com/v2` | x1, x2, x3 |
| **百度千帆** | `https://qianfan.baidubce.com/v2` | ERNIE-4.0 |
| **百川智能** | `https://api.baichuan-ai.com/v1` | Baichuan4 |
| **商汤日日新** | `https://api.sensenova.cn/v1` | SenseChat-5 |
| **MiniMax** | `https://api.minimax.chat/v1` | abab6.5s |
| **火山方舟** | `https://ark.cn-beijing.volces.com/api/v3` | Doubao-pro |
| **腾讯云混元** | `https://hunyuan.tencentcloudapi.com/v1` | hunyuan-pro |

### 国际厂商

| 厂商 | Base URL | 最新模型 |
|------|----------|----------|
| **OpenAI** | `https://api.openai.com/v1` | gpt-5.5 |
| **Anthropic** | `https://api.anthropic.com/v1/messages` | claude-opus-4.7 |
| **Groq** | `https://api.groq.com/openai/v1` | llama-3.3-70b |
| **Together** | `https://api.together.xyz/v1` | DeepSeek-V4-Pro |
| **Mistral** | `https://api.mistral.ai/v1` | mistral-large-latest |
| **Cohere** | `https://api.cohere.ai/v1` | command-r-plus |
| **AI21** | `https://api.ai21.com/studio/v1` | jamba-1.5-large |
| **Perplexity** | `https://api.perplexity.ai/v1` | sonar-reasoning-pro |

### 聚合平台

| 平台 | Base URL | 说明 |
|------|----------|------|
| **OpenRouter** | `https://openrouter.ai/api/v1` | 聚合多家模型 |
| **302.ai** | `https://api.302.ai/v1` | 国内聚合平台 |
| **AIHubMix** | `https://aihubmix.com/v1` | 多模型接入 |

### 本地部署

| 工具 | Base URL | 说明 |
|------|----------|------|
| **Ollama** | `http://localhost:11434/v1` | 本地大模型管理 |
| **LM Studio** | `http://localhost:1234/v1` | 本地模型运行 |
| **vLLM** | `http://localhost:8000/v1` | 高性能推理引擎 |

> 📌 完整厂商列表见 [`references/providers.md`](references/providers.md)

---

## 📁 项目结构

```
trae-custom-model/
├── README.md                          # 本文件
├── SKILL.md                           # Skill 主文件（入口）
├── 【Skill 创作】*.md                  # 参赛推广帖子
├── references/
│   ├── providers.md                   # 60+ 厂商配置参考
│   ├── update_config.json             # 更新配置 & 历史记录 v2.0
│   └── model_changelog.md             # 模型变更日志
└── scripts/
    ├── search_provider.py             # 厂商查询脚本
    └── update_models.py               # 自动更新脚本 v2.0
```

---

## ⚙️ 配置参数说明

### TRAE 配置界面参数对照

| TRAE 参数 | Skill 输出字段 | 说明 |
|-----------|----------------|------|
| API格式 | 协议类型 | OpenAI / Anthropic |
| 自定义请求地址 | Base URL | 厂商 API 地址 |
| 完整URL | 是否包含 `/chat/completions` | 大多数关闭 |
| 模型ID | model_id | 厂商定义的模型标识 |
| 模型系列 | 预设模板 | DeepSeek/Claude/GPT/默认 |
| 上下文长度 | context | 输入+输出总和 |

### 常见配置错误

| 错误 | 原因 | 解决 |
|------|------|------|
| 404 | Base URL 错误 | 检查"完整URL"开关 |
| 401 | API Key 错误 | 重新获取 API Key |
| 模型不存在 | 模型ID 错误 | 核对官方文档 |
| 降智/失忆 | 上下文设置过高 | 使用官方推荐值 |

---