# 常见厂商配置参考

本文档汇总了常见AI模型服务商在TRAE中的配置参数，供快速参考。

> ⚠️ **模型信息可能随时间变化，建议定期更新本文档**

---

## 目录

- [OpenAI 官方](#openai-官方)
- [Anthropic (Claude)](#anthropic-claude)
- [DeepSeek 官方](#deepseek-官方)
- [智谱AI (BigModel)](#智谱ai-bigmodel)
- [通义千问 (阿里云百炼)](#通义千问-阿里云百炼)
- [Kimi (月之暗面)](#kimi-月之暗面)
- [硅基流动](#硅基流动)
- [其他厂商](#其他厂商)

---

## OpenAI 官方

| 参数 | 值 |
|------|-----|
| API格式 | OpenAI |
| Base URL | `https://api.openai.com/v1` |
| 完整URL | 关闭 |

**⭐ 最新模型 (2026年4月23日):**
- `gpt-5.5` - **GPT-5.5** (最新旗舰) - 1M上下文

**注意:** 
- ⚠️ GPT-5.5于2026年4月23日发布，支持100万上下文
- ⚠️ 旧模型(gpt-4o、gpt-4o-mini、gpt-4-turbo、o1等)已于2026年2月停用

---

## Anthropic (Claude)

| 参数 | 值 |
|------|-----|
| API格式 | Anthropic |
| Base URL | `https://api.anthropic.com/v1/messages` |
| 完整URL | **开启** |

**⭐ 最新模型 (2026年4月16日):**
- `claude-opus-4.7` - **Claude Opus 4.7** (最新旗舰) - 200K上下文
- `claude-sonnet-4.8` - Claude Sonnet 4.8 (高性能) - 200K上下文

**其他模型:**
- `claude-opus-4` - Claude Opus 4 (旧版旗舰) - 200K上下文
- `claude-sonnet-4` - Claude Sonnet 4 - 200K上下文
- `claude-haiku-4` - Claude Haiku 4 (轻量) - 200K上下文

**说明:** Claude Opus 4.7于2026年4月16日发布，编程能力提升13%，视觉能力提升3倍

---

## DeepSeek 官方

| 参数 | 值 |
|------|-----|
| API格式 | OpenAI |
| Base URL | `https://api.deepseek.com` |
| 完整URL | 关闭 |

**⭐ 最新模型 (2026年4月24日):**
- `deepseek-v4-pro` - **DeepSeek-V4-Pro** (最新旗舰) - 1M上下文
- `deepseek-v4-flash` - DeepSeek-V4-Flash (轻量) - 1M上下文

**⚠️ 停用提醒:**
- `deepseek-chat` 和 `deepseek-reasoner` 将于 **2026-07-24** 停用
- 请尽快迁移到 `deepseek-v4-pro` 或 `deepseek-v4-flash`

**说明:** V4系列于2026年4月24日发布，支持100万token上下文

---

## 智谱AI (BigModel)

| 参数 | 值 |
|------|-----|
| API格式 | OpenAI |
| Base URL | `https://open.bigmodel.cn/api/paas/v4` |
| 完整URL | 关闭 |

**⭐ 最新模型:**
- `glm-5-turbo` - **GLM-5-Turbo** (最新闭源旗舰) - 256K上下文
- `glm-5.1` - GLM-5.1 (最新开源旗舰) - 256K上下文
- `glm-5` - GLM-5 - 256K上下文

**其他模型:**
- `glm-4-plus` - GLM-4 Plus - 128K上下文
- `glm-4-flash` - GLM-4 Flash (免费额度) - 128K上下文
- `glm-4-long` - GLM-4 Long (超长上下文) - 1M上下文
- `glm-4v-plus` - GLM-4V Plus (多模态) - 8K上下文
- `glm-4-alltools` - GLM-4 All Tools (工具调用) - 128K上下文

**说明:** GLM-5于2026年2月发布，GLM-5-Turbo为最新闭源旗舰模型

---

## 通义千问 (阿里云百炼)

| 参数 | 值 |
|------|-----|
| API格式 | OpenAI |
| Base URL | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 完整URL | 关闭 |

**⭐ 最新模型 (2026年):**
- `qwen3.6-max-preview` - **Qwen3.6-Max-Preview** (最新旗舰) - 256K上下文
- `qwen3.6-plus` - Qwen3.6-Plus - 128K上下文
- `qwen3.6-flash` - Qwen3.6-Flash - 128K上下文

**代码专用模型:**
- `qwen3-coder-plus` - Qwen3-Coder-Plus - 256K上下文
- `qwen3-coder-turbo` - Qwen3-Coder-Turbo - 128K上下文

**多模态模型:**
- `qwen3-vl-max` - Qwen3-VL-Max - 128K上下文
- `qwen3-vl-plus` - Qwen3-VL-Plus - 128K上下文

**其他模型:**
- `qwen-max` - Qwen-Max (旧版旗舰) - 32K上下文
- `qwen-long` - Qwen-Long (超长上下文) - 1M上下文

**百炼支持的第三方模型:**
- `deepseek-v4-pro` / `deepseek-v4-flash`
- `kimi-k2.6`
- `glm-5.1`
- `MiniMax/MiniMax-M2.7`

---

## Kimi (月之暗面)

**特殊配置！**

| 参数 | 值 |
|------|-----|
| API格式 | Anthropic |
| Base URL | `https://api.kimi.com/coding/v1/messages` |
| 完整URL | **开启** |

**⭐ 最新模型 (2026年4月20日):**
- `kimi-k2.6` - **Kimi K2.6** (最新旗舰代码模型) - 256K上下文
- `kimi-k2.5` - Kimi K2.5 - 256K上下文
- `kimi-k2` - Kimi K2 - 200K上下文

**说明:** K2.6官方称其为迄今最强代码模型，性能对标GPT-5.4

---

## 硅基流动

| 参数 | 值 |
|------|-----|
| API格式 | OpenAI |
| Base URL | `https://api.siliconflow.cn/v1` |
| 完整URL | 关闭 |

**热门模型:**
- `deepseek-ai/DeepSeek-V4-Pro` - DeepSeek-V4-Pro (最新旗舰) - 1M上下文
- `deepseek-ai/DeepSeek-V4-Flash` - DeepSeek-V4-Flash - 1M上下文
- `THUDM/GLM-5-Turbo` - GLM-5-Turbo (最新旗舰) - 256K上下文
- `THUDM/GLM-5.1` - GLM-5.1 - 256K上下文
- `Qwen/Qwen3.6-Max-Preview` - Qwen3.6-Max-Preview - 256K上下文
- `Qwen/Qwen2.5-72B-Instruct` - Qwen2.5 72B - 128K上下文
- `meta-llama/Llama-3.3-70B-Instruct` - Llama 3.3 70B - 128K上下文

**说明:** 硅基流动提供150+模型，以上为热门模型，完整列表请查看官网

---

## 其他厂商

### Google Gemini

| 参数 | 值 |
|------|-----|
| API格式 | OpenAI |
| Base URL | `https://generativelanguage.googleapis.com/v1beta/openai` |
| 完整URL | 关闭 |

**热门模型:**
- `gemini-2.0-flash` - Gemini 2.0 Flash - 1M上下文
- `gemini-1.5-pro` - Gemini 1.5 Pro - 2M上下文
- `gemini-1.5-flash` - Gemini 1.5 Flash - 1M上下文

---

### Groq

| 参数 | 值 |
|------|-----|
| API格式 | OpenAI |
| Base URL | `https://api.groq.com/openai/v1` |
| 完整URL | 关闭 |

**热门模型:**
- `llama-3.3-70b-versatile` - Llama 3.3 70B - 128K上下文
- `llama-3.1-8b-instant` - Llama 3.1 8B - 128K上下文
- `deepseek-r1-distill-llama-70b` - DeepSeek R1 Distill - 128K上下文

**说明:** Groq主打超快推理速度

---

### Mistral AI

| 参数 | 值 |
|------|-----|
| API格式 | OpenAI |
| Base URL | `https://api.mistral.ai/v1` |
| 完整URL | 关闭 |

**热门模型:**
- `mistral-large-latest` - Mistral Large - 128K上下文
- `mistral-small-latest` - Mistral Small - 128K上下文
- `codestral-latest` - Codestral (代码专用) - 256K上下文

---

### Together AI

| 参数 | 值 |
|------|-----|
| API格式 | OpenAI |
| Base URL | `https://api.together.xyz/v1` |
| 完整URL | 关闭 |

**热门模型:**
- `deepseek-ai/DeepSeek-V4-Pro` - DeepSeek-V4-Pro - 1M上下文
- `deepseek-ai/DeepSeek-V4-Flash` - DeepSeek-V4-Flash - 1M上下文
- `meta-llama/Llama-3.3-70B-Instruct-Turbo` - Llama 3.3 70B - 128K上下文

---

## 已停用模型清单

| 厂商 | 停用模型 | 替代方案 |
|------|----------|----------|
| **DeepSeek** | `deepseek-chat` | 使用 `deepseek-v4-pro` 或 `deepseek-v4-flash` |
| **DeepSeek** | `deepseek-reasoner` | 使用 `deepseek-v4-pro` 或 `deepseek-v4-flash` |
| **OpenAI** | `gpt-4o` | 使用 `gpt-5.5` |
| **OpenAI** | `gpt-4o-mini` | 使用 `gpt-5.5` |
| **OpenAI** | `gpt-4-turbo` | 使用 `gpt-5.5` |
| **OpenAI** | `o1-preview` | 使用 `gpt-5.5` |
| **OpenAI** | `o1-mini` | 使用 `gpt-5.5` |
| **Anthropic** | `claude-3-5-sonnet-*` | 使用 `claude-opus-4.7` |
| **Anthropic** | `claude-3-opus-*` | 使用 `claude-opus-4.7` |
| **Kimi** | `kimi-for-coding` | 使用 `kimi-k2.6` |

---

## 上下文长度参考

| 模型 | 官方上下文 | 建议配置 |
|------|-----------|----------|
| GPT-5.5 | 1M | 1M |
| DeepSeek-V4-Pro | 1M | 1M |
| DeepSeek-V4-Flash | 1M | 1M |
| Claude Opus 4.7 | 200K | 200K |
| GLM-5-Turbo | 256K | 256K |
| Qwen3.6-Max-Preview | 256K | 256K |
| Kimi K2.6 | 256K | 256K |

**重要提醒:**
- TRAE的上下文配置 = 输入 + 输出的总和
- 不要盲目调高上下文，会导致降智和失忆

---

*最后更新: 2026-05-21*
