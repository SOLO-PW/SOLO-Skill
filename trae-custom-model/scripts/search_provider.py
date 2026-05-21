#!/usr/bin/env python3
"""
TRAE 自定义模型厂商配置搜索脚本

用法:
    python search_provider.py <厂商名称>
    
示例:
    python search_provider.py 硅基流动
    python search_provider.py DeepSeek
"""

import sys
import json

# 已知厂商配置数据库
# 注意：模型信息可能随时间变化，建议定期更新
KNOWN_PROVIDERS = {
    "硅基流动": {
        "name": "硅基流动 (SiliconFlow)",
        "protocol": "OpenAI",
        "base_url": "https://api.siliconflow.cn/v1",
        "full_url": False,
        "models": [
            {"id": "deepseek-ai/DeepSeek-V4-Pro", "name": "DeepSeek-V4-Pro (最新旗舰)", "context": "1M"},
            {"id": "deepseek-ai/DeepSeek-V4-Flash", "name": "DeepSeek-V4-Flash", "context": "1M"},
            {"id": "THUDM/GLM-5-Turbo", "name": "GLM-5-Turbo (最新旗舰)", "context": "256K"},
            {"id": "THUDM/GLM-5.1", "name": "GLM-5.1", "context": "256K"},
            {"id": "THUDM/GLM-4-9B-Chat", "name": "GLM-4 9B", "context": "128K"},
            {"id": "Qwen/Qwen3.6-Max-Preview", "name": "Qwen3.6-Max-Preview", "context": "256K"},
            {"id": "Qwen/Qwen2.5-72B-Instruct", "name": "Qwen2.5 72B", "context": "128K"},
            {"id": "meta-llama/Llama-3.3-70B-Instruct", "name": "Llama 3.3 70B", "context": "128K"},
        ],
        "docs_url": "https://docs.siliconflow.cn/",
        "note": "硅基流动提供150+模型，以上为热门模型，完整列表请查看官网"
    },
    "siliconflow": {
        "name": "硅基流动 (SiliconFlow)",
        "protocol": "OpenAI",
        "base_url": "https://api.siliconflow.cn/v1",
        "full_url": False,
        "models": [
            {"id": "deepseek-ai/DeepSeek-V3", "name": "DeepSeek V3", "context": "64K"},
            {"id": "deepseek-ai/DeepSeek-R1", "name": "DeepSeek R1", "context": "64K"},
        ],
        "docs_url": "https://docs.siliconflow.cn/"
    },
    "deepseek": {
        "name": "DeepSeek 官方",
        "protocol": "OpenAI",
        "base_url": "https://api.deepseek.com",
        "full_url": False,
        "models": [
            {"id": "deepseek-v4-pro", "name": "DeepSeek-V4-Pro (最新旗舰)", "context": "1M", "recommended": True},
            {"id": "deepseek-v4-flash", "name": "DeepSeek-V4-Flash (轻量)", "context": "1M"},
        ],
        "docs_url": "https://platform.deepseek.com/",
        "note": "V4系列于2026年4月24日发布，支持100万token上下文。旧模型 deepseek-chat/deepseek-reasoner 将于2026-07-24停用"
    },
    "智谱": {
        "name": "智谱AI (BigModel)",
        "protocol": "OpenAI",
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "full_url": False,
        "models": [
            {"id": "glm-5-turbo", "name": "GLM-5-Turbo (最新闭源旗舰)", "context": "256K", "recommended": True},
            {"id": "glm-5.1", "name": "GLM-5.1 (最新开源旗舰)", "context": "256K"},
            {"id": "glm-5", "name": "GLM-5", "context": "256K"},
            {"id": "glm-4-plus", "name": "GLM-4 Plus", "context": "128K"},
            {"id": "glm-4-air", "name": "GLM-4 Air (高性价比)", "context": "128K"},
            {"id": "glm-4-flash", "name": "GLM-4 Flash (免费额度)", "context": "128K"},
            {"id": "glm-4-long", "name": "GLM-4 Long (超长上下文)", "context": "1M"},
            {"id": "glm-4v-plus", "name": "GLM-4V Plus (多模态)", "context": "8K", "vision": True},
            {"id": "glm-4-alltools", "name": "GLM-4 All Tools (工具调用)", "context": "128K"},
        ],
        "docs_url": "https://open.bigmodel.cn/dev/howuse/glm-4",
        "note": "GLM-5于2026年2月发布，GLM-5-Turbo为最新闭源旗舰模型"
    },
    "bigmodel": {
        "name": "智谱AI (BigModel)",
        "protocol": "OpenAI",
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "full_url": False,
        "models": [
            {"id": "glm-5-turbo", "name": "GLM-5-Turbo (最新闭源旗舰)", "context": "256K", "recommended": True},
        ],
        "docs_url": "https://open.bigmodel.cn/dev/howuse/glm-4"
    },
    "百度": {
        "name": "百度千帆",
        "protocol": "OpenAI",
        "base_url": "https://qianfan.baidubce.com/v2",
        "full_url": False,
        "models": [
            {"id": "ernie-4.0-8k-latest", "name": "文心4.0 (最新)", "context": "8K", "recommended": True},
            {"id": "ernie-4.0-8k", "name": "文心4.0", "context": "8K"},
            {"id": "ernie-4.0-turbo-8k", "name": "文心4.0 Turbo", "context": "8K"},
            {"id": "ernie-3.5-8k", "name": "文心3.5", "context": "8K"},
            {"id": "ernie-speed-128k", "name": "文心Speed 128K", "context": "128K"},
            {"id": "ernie-speed-8k", "name": "文心Speed 8K", "context": "8K"},
            {"id": "ernie-lite-8k", "name": "文心Lite", "context": "8K"},
            {"id": "ernie-tiny-8k", "name": "文心Tiny", "context": "8K"},
        ],
        "docs_url": "https://qianfan.baidu.com/"
    },
    "千帆": {
        "name": "百度千帆",
        "protocol": "OpenAI",
        "base_url": "https://qianfan.baidubce.com/v2",
        "full_url": False,
        "models": [
            {"id": "ernie-4.0-8k-latest", "name": "文心4.0 (最新)", "context": "8K", "recommended": True},
        ],
        "docs_url": "https://qianfan.baidu.com/"
    },
    "讯飞": {
        "name": "讯飞星火 (讯飞星辰Maas)",
        "protocol": "OpenAI",
        "base_url": "https://maas-coding-api.cn-huabei-1.xf-yun.com/v2",
        "full_url": False,
        "models": [
            {"id": "x1", "name": "星火X1 (深度思考)", "context": "32K", "recommended": True},
            {"id": "x2", "name": "星火X2 (多模态)", "context": "32K", "vision": True},
            {"id": "x3", "name": "星火X3 (标准)", "context": "32K"},
            {"id": "lite", "name": "星火Lite (轻量)", "context": "32K"},
            {"id": "pro-128k", "name": "星火Pro 128K", "context": "128K"},
            {"id": "max-32k", "name": "星火Max 32K", "context": "32K"},
        ],
        "docs_url": "https://xinghuo.xfyun.cn/",
        "note": "讯飞同时支持OpenAI和Anthropic协议"
    },
    "火山": {
        "name": "火山方舟 (Volcengine)",
        "protocol": "OpenAI",
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        "full_url": False,
        "models": [],
        "note": "需要在火山方舟控制台创建推理接入点，使用接入点ID作为模型ID。支持DeepSeek、豆包、GLM等模型",
        "docs_url": "https://www.volcengine.com/product/ark"
    },
    "302": {
        "name": "302.ai",
        "protocol": "OpenAI",
        "base_url": "https://api.302.ai/v1",
        "full_url": False,
        "models": [],
        "note": "聚合平台，支持GPT-4o、Claude、DeepSeek等众多模型",
        "docs_url": "https://302.ai/"
    },
    "openrouter": {
        "name": "OpenRouter",
        "protocol": "OpenAI",
        "base_url": "https://openrouter.ai/api/v1",
        "full_url": False,
        "models": [
            {"id": "deepseek/deepseek-chat", "name": "DeepSeek V3", "context": "64K"},
            {"id": "deepseek/deepseek-r1", "name": "DeepSeek R1", "context": "64K"},
            {"id": "anthropic/claude-3.5-sonnet", "name": "Claude 3.5 Sonnet", "context": "200K"},
            {"id": "anthropic/claude-3-opus", "name": "Claude 3 Opus", "context": "200K"},
            {"id": "openai/gpt-4o", "name": "GPT-4o", "context": "128K"},
            {"id": "openai/gpt-4o-mini", "name": "GPT-4o Mini", "context": "128K"},
            {"id": "google/gemini-2.0-flash-001", "name": "Gemini 2.0 Flash", "context": "1M"},
            {"id": "meta-llama/llama-3.3-70b-instruct", "name": "Llama 3.3 70B", "context": "128K"},
        ],
        "docs_url": "https://openrouter.ai/docs",
        "note": "OpenRouter提供100+模型，以上为热门模型"
    },
    "kimi": {
        "name": "Kimi (月之暗面)",
        "protocol": "Anthropic",
        "base_url": "https://api.kimi.com/coding/v1/messages",
        "full_url": True,
        "models": [
            {"id": "kimi-k2.6", "name": "Kimi K2.6 (最新旗舰代码模型)", "context": "256K", "recommended": True},
            {"id": "kimi-k2.5", "name": "Kimi K2.5", "context": "256K"},
            {"id": "kimi-k2", "name": "Kimi K2", "context": "200K"},
        ],
        "note": "K2.6于2026年4月20日发布，官方称其为迄今最强代码模型，支持256K上下文",
        "docs_url": "https://platform.moonshot.cn/"
    },
    "小米": {
        "name": "小米 Mimo",
        "protocol": "OpenAI",
        "base_url": "https://api.xiaomimimo.com/v1",
        "full_url": False,
        "models": [],
        "docs_url": "https://mimo.ai/"
    },
    "minimax": {
        "name": "MiniMax",
        "protocol": "Anthropic",
        "base_url": "https://api.minimaxi.com/anthropic/chat/completions",
        "full_url": True,
        "models": [
            {"id": "abab6.5s", "name": "abab6.5s", "context": "245K"},
            {"id": "abab6.5g", "name": "abab6.5g", "context": "8K"},
            {"id": "abab6.5t", "name": "abab6.5t", "context": "8K"},
        ],
        "docs_url": "https://www.minimaxi.com/"
    },
    "通义": {
        "name": "阿里云百炼 (通义千问)",
        "protocol": "OpenAI",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "full_url": False,
        "models": [
            {"id": "qwen3.6-max-preview", "name": "Qwen3.6-Max-Preview (最新旗舰)", "context": "256K", "recommended": True},
            {"id": "qwen3.6-plus", "name": "Qwen3.6-Plus", "context": "128K"},
            {"id": "qwen3.6-flash", "name": "Qwen3.6-Flash", "context": "128K"},
            {"id": "qwen3-coder-plus", "name": "Qwen3-Coder-Plus (代码专用)", "context": "256K"},
            {"id": "qwen3-coder-turbo", "name": "Qwen3-Coder-Turbo (代码轻量)", "context": "128K"},
            {"id": "qwen3-vl-plus", "name": "Qwen3-VL-Plus (多模态)", "context": "128K", "vision": True},
            {"id": "qwen3-vl-max", "name": "Qwen3-VL-Max (多模态旗舰)", "context": "128K", "vision": True},
            {"id": "qwen-max", "name": "Qwen-Max (旧版旗舰)", "context": "32K"},
            {"id": "qwen-plus", "name": "Qwen-Plus (旧版)", "context": "128K"},
            {"id": "qwen-long", "name": "Qwen-Long (超长上下文)", "context": "1M"},
        ],
        "note": "数据来源: 阿里云百炼官方文档 (2026-05-11)",
        "docs_url": "https://help.aliyun.com/zh/model-studio/getting-started/models"
    },
    "阿里云": {
        "name": "阿里云百炼 (通义千问)",
        "protocol": "OpenAI",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "full_url": False,
        "models": [
            {"id": "qwen3.6-max-preview", "name": "Qwen3.6-Max-Preview (最新旗舰)", "context": "256K", "recommended": True},
            {"id": "qwen3.6-plus", "name": "Qwen3.6-Plus", "context": "128K"},
            {"id": "qwen3.6-flash", "name": "Qwen3.6-Flash", "context": "128K"},
        ],
        "docs_url": "https://help.aliyun.com/zh/model-studio/getting-started/models"
    },
    "dashscope": {
        "name": "阿里云百炼 (DashScope)",
        "protocol": "OpenAI",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "full_url": False,
        "models": [
            {"id": "qwen3.6-max-preview", "name": "Qwen3.6-Max-Preview (最新旗舰)", "context": "256K", "recommended": True},
        ],
        "docs_url": "https://help.aliyun.com/zh/model-studio/getting-started/models"
    },
    "qwen": {
        "name": "通义千问 (Qwen)",
        "protocol": "OpenAI",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "full_url": False,
        "models": [
            {"id": "qwen3.6-max-preview", "name": "Qwen3.6-Max-Preview (最新旗舰)", "context": "256K", "recommended": True},
        ],
        "docs_url": "https://help.aliyun.com/zh/model-studio/getting-started/models"
    },
    "零一万物": {
        "name": "零一万物 (01.AI)",
        "protocol": "OpenAI",
        "base_url": "https://api.lingyiwanwu.com/v1",
        "full_url": False,
        "models": [
            {"id": "yi-large", "name": "Yi-Large (旗舰)", "context": "32K", "recommended": True},
            {"id": "yi-medium", "name": "Yi-Medium", "context": "16K"},
            {"id": "yi-spark", "name": "Yi-Spark (轻量)", "context": "16K"},
            {"id": "yi-large-rag", "name": "Yi-Large-RAG", "context": "32K"},
            {"id": "yi-vision", "name": "Yi-Vision (多模态)", "context": "16K", "vision": True},
        ],
        "docs_url": "https://platform.lingyiwanwu.com/docs"
    },
    "lingyi": {
        "name": "零一万物 (01.AI)",
        "protocol": "OpenAI",
        "base_url": "https://api.lingyiwanwu.com/v1",
        "full_url": False,
        "models": [
            {"id": "yi-large", "name": "Yi-Large", "context": "32K", "recommended": True},
        ],
        "docs_url": "https://platform.lingyiwanwu.com/docs"
    },
    "商汤": {
        "name": "商汤日日新 (SenseNova)",
        "protocol": "OpenAI",
        "base_url": "https://api.sensenova.cn/v1",
        "full_url": False,
        "models": [
            {"id": "SenseChat-5", "name": "日日新5.0 (最新)", "context": "128K", "recommended": True},
            {"id": "SenseChat-4", "name": "日日新4.0", "context": "128K"},
            {"id": "SenseChat-Turbo", "name": "日日新Turbo", "context": "128K"},
            {"id": "SenseChat-5-Vision", "name": "日日新5.0 Vision (多模态)", "context": "32K", "vision": True},
        ],
        "docs_url": "https://platform.sensenova.cn/doc"
    },
    "sensenova": {
        "name": "商汤日日新 (SenseNova)",
        "protocol": "OpenAI",
        "base_url": "https://api.sensenova.cn/v1",
        "full_url": False,
        "models": [],
        "docs_url": "https://platform.sensenova.cn/doc"
    },
    "百川": {
        "name": "百川智能 (Baichuan)",
        "protocol": "OpenAI",
        "base_url": "https://api.baichuan-ai.com/v1",
        "full_url": False,
        "models": [
            {"id": "Baichuan4", "name": "Baichuan 4 (最新)", "context": "128K", "recommended": True},
            {"id": "Baichuan3-Turbo", "name": "Baichuan 3 Turbo", "context": "128K"},
            {"id": "Baichuan3-Turbo-128k", "name": "Baichuan 3 Turbo 128K", "context": "128K"},
            {"id": "Baichuan2-Turbo", "name": "Baichuan 2 Turbo", "context": "32K"},
        ],
        "docs_url": "https://platform.baichuan-ai.com/docs"
    },
    "baichuan": {
        "name": "百川智能 (Baichuan)",
        "protocol": "OpenAI",
        "base_url": "https://api.baichuan-ai.com/v1",
        "full_url": False,
        "models": [
            {"id": "Baichuan4", "name": "Baichuan 4", "context": "128K", "recommended": True},
        ],
        "docs_url": "https://platform.baichuan-ai.com/docs"
    },
    "阶跃星辰": {
        "name": "阶跃星辰 (StepFun)",
        "protocol": "OpenAI",
        "base_url": "https://api.stepfun.com/v1",
        "full_url": False,
        "models": [
            {"id": "step-3.5-flash", "name": "Step-3.5 Flash (最新轻量)", "context": "32K", "recommended": True},
            {"id": "step-3.5-large", "name": "Step-3.5 Large", "context": "32K"},
            {"id": "step-3.5-turbo", "name": "Step-3.5 Turbo", "context": "32K"},
            {"id": "step-3.5-vision", "name": "Step-3.5 Vision (多模态)", "context": "32K", "vision": True},
            {"id": "step-2-16k", "name": "Step-2 16K", "context": "16K"},
            {"id": "step-2-32k", "name": "Step-2 32K", "context": "32K"},
            {"id": "step-1-8k", "name": "Step-1 8K", "context": "8K"},
            {"id": "step-1-32k", "name": "Step-1 32K", "context": "32K"},
            {"id": "step-1-128k", "name": "Step-1 128K", "context": "128K"},
            {"id": "step-1-256k", "name": "Step-1 256K", "context": "256K"},
        ],
        "docs_url": "https://platform.stepfun.com/docs"
    },
    "stepfun": {
        "name": "阶跃星辰 (StepFun)",
        "protocol": "OpenAI",
        "base_url": "https://api.stepfun.com/v1",
        "full_url": False,
        "models": [],
        "docs_url": "https://platform.stepfun.com/docs"
    },
    "月之暗面": {
        "name": "Kimi (月之暗面)",
        "protocol": "Anthropic",
        "base_url": "https://api.kimi.com/coding/v1/messages",
        "full_url": True,
        "models": [
            {"id": "kimi-k2.6", "name": "Kimi K2.6 (最新旗舰)", "context": "256K", "recommended": True},
        ],
        "note": "K2.6于2026年4月20日发布，官方称其为迄今最强代码模型，支持256K上下文",
        "docs_url": "https://platform.moonshot.cn/"
    },
    "moonshot": {
        "name": "Kimi (月之暗面)",
        "protocol": "Anthropic",
        "base_url": "https://api.kimi.com/coding/v1/messages",
        "full_url": True,
        "models": [
            {"id": "kimi-k2.6", "name": "Kimi K2.6", "context": "256K", "recommended": True},
        ],
        "docs_url": "https://platform.moonshot.cn/"
    },
    "together": {
        "name": "Together AI",
        "protocol": "OpenAI",
        "base_url": "https://api.together.xyz/v1",
        "full_url": False,
        "models": [
            {"id": "deepseek-ai/DeepSeek-V3", "name": "DeepSeek V3", "context": "64K"},
            {"id": "deepseek-ai/DeepSeek-R1", "name": "DeepSeek R1", "context": "64K"},
            {"id": "meta-llama/Llama-3.3-70B-Instruct-Turbo", "name": "Llama 3.3 70B", "context": "128K"},
            {"id": "meta-llama/Llama-3.3-8B-Instruct-Turbo", "name": "Llama 3.3 8B", "context": "128K"},
            {"id": "Qwen/Qwen2.5-72B-Instruct-Turbo", "name": "Qwen2.5 72B", "context": "128K"},
            {"id": "google/gemma-2-27b-it", "name": "Gemma 2 27B", "context": "128K"},
        ],
        "docs_url": "https://docs.together.ai/"
    },
    "groq": {
        "name": "Groq",
        "protocol": "OpenAI",
        "base_url": "https://api.groq.com/openai/v1",
        "full_url": False,
        "models": [
            {"id": "llama-3.3-70b-versatile", "name": "Llama 3.3 70B", "context": "128K"},
            {"id": "llama-3.1-8b-instant", "name": "Llama 3.1 8B", "context": "128K"},
            {"id": "mixtral-8x7b-32768", "name": "Mixtral 8x7B", "context": "32K"},
            {"id": "gemma2-9b-it", "name": "Gemma 2 9B", "context": "8K"},
            {"id": "deepseek-r1-distill-llama-70b", "name": "DeepSeek R1 Distill (Llama 70B)", "context": "128K"},
        ],
        "docs_url": "https://console.groq.com/docs"
    },
    "azure": {
        "name": "Azure OpenAI",
        "protocol": "OpenAI",
        "base_url": "https://{your-resource-name}.openai.azure.com/openai/deployments/{deployment-id}",
        "full_url": True,
        "models": [],
        "note": "需要替换为自己的资源名称和部署ID，API版本建议使用 2024-10-21",
        "docs_url": "https://learn.microsoft.com/zh-cn/azure/ai-services/openai/"
    },
    "azureopenai": {
        "name": "Azure OpenAI",
        "protocol": "OpenAI",
        "base_url": "https://{your-resource-name}.openai.azure.com/openai/deployments/{deployment-id}",
        "full_url": True,
        "models": [],
        "note": "需要替换为自己的资源名称和部署ID",
        "docs_url": "https://learn.microsoft.com/zh-cn/azure/ai-services/openai/"
    },
    "openai": {
        "name": "OpenAI 官方",
        "protocol": "OpenAI",
        "base_url": "https://api.openai.com/v1",
        "full_url": False,
        "models": [
            {"id": "gpt-5.5", "name": "GPT-5.5 (最新旗舰)", "context": "1M", "recommended": True},
            {"id": "gpt-5.5-2026-04-23", "name": "GPT-5.5 快照版", "context": "1M"},
        ],
        "docs_url": "https://platform.openai.com/docs",
        "note": "GPT-5.5于2026年4月23日发布，支持100万上下文。旧模型(gpt-4o、gpt-4o-mini、gpt-4-turbo、o1等)已于2026年2月停用"
    },
    "anthropic": {
        "name": "Anthropic (Claude)",
        "protocol": "Anthropic",
        "base_url": "https://api.anthropic.com/v1/messages",
        "full_url": True,
        "models": [
            {"id": "claude-opus-4.7", "name": "Claude Opus 4.7 (最新旗舰)", "context": "200K", "recommended": True},
            {"id": "claude-sonnet-4.8", "name": "Claude Sonnet 4.8 (高性能)", "context": "200K"},
            {"id": "claude-opus-4", "name": "Claude Opus 4 (旧版旗舰)", "context": "200K"},
            {"id": "claude-sonnet-4", "name": "Claude Sonnet 4", "context": "200K"},
            {"id": "claude-haiku-4", "name": "Claude Haiku 4 (轻量)", "context": "200K"},
        ],
        "docs_url": "https://docs.anthropic.com/",
        "note": "Claude Opus 4.7于2026年4月16日发布，编程能力提升13%，视觉能力提升3倍"
    },
    "claude": {
        "name": "Anthropic (Claude)",
        "protocol": "Anthropic",
        "base_url": "https://api.anthropic.com/v1/messages",
        "full_url": True,
        "models": [
            {"id": "claude-opus-4.7", "name": "Claude Opus 4.7 (最新旗舰)", "context": "200K", "recommended": True},
        ],
        "docs_url": "https://docs.anthropic.com/"
    },
    "cohere": {
        "name": "Cohere",
        "protocol": "OpenAI",
        "base_url": "https://api.cohere.com/v1",
        "full_url": False,
        "models": [
            {"id": "command-r-plus", "name": "Command R+", "context": "128K"},
            {"id": "command-r", "name": "Command R", "context": "128K"},
            {"id": "command", "name": "Command", "context": "128K"},
        ],
        "docs_url": "https://docs.cohere.com/"
    },
    "perplexity": {
        "name": "Perplexity",
        "protocol": "OpenAI",
        "base_url": "https://api.perplexity.ai",
        "full_url": False,
        "models": [
            {"id": "sonar-reasoning-pro", "name": "Sonar Reasoning Pro", "context": "128K"},
            {"id": "sonar-reasoning", "name": "Sonar Reasoning", "context": "128K"},
            {"id": "sonar-pro", "name": "Sonar Pro", "context": "200K"},
            {"id": "sonar", "name": "Sonar", "context": "128K"},
        ],
        "docs_url": "https://docs.perplexity.ai/"
    },
    "mistral": {
        "name": "Mistral AI",
        "protocol": "OpenAI",
        "base_url": "https://api.mistral.ai/v1",
        "full_url": False,
        "models": [
            {"id": "mistral-large-latest", "name": "Mistral Large (最新)", "context": "128K", "recommended": True},
            {"id": "mistral-medium-latest", "name": "Mistral Medium", "context": "128K"},
            {"id": "mistral-small-latest", "name": "Mistral Small", "context": "128K"},
            {"id": "codestral-latest", "name": "Codestral (代码)", "context": "256K"},
            {"id": "pixtral-large-latest", "name": "Pixtral Large (多模态)", "context": "128K", "vision": True},
        ],
        "docs_url": "https://docs.mistral.ai/"
    },
    "ai21": {
        "name": "AI21 Labs",
        "protocol": "OpenAI",
        "base_url": "https://api.ai21.com/studio/v1",
        "full_url": False,
        "models": [
            {"id": "jamba-1.5-large", "name": "Jamba 1.5 Large", "context": "256K"},
            {"id": "jamba-1.5-mini", "name": "Jamba 1.5 Mini", "context": "256K"},
        ],
        "docs_url": "https://studio.ai21.com/"
    },
    "fireworks": {
        "name": "Fireworks AI",
        "protocol": "OpenAI",
        "base_url": "https://api.fireworks.ai/inference/v1",
        "full_url": False,
        "models": [
            {"id": "accounts/fireworks/models/deepseek-v3", "name": "DeepSeek V3", "context": "64K"},
            {"id": "accounts/fireworks/models/deepseek-r1", "name": "DeepSeek R1", "context": "64K"},
            {"id": "accounts/fireworks/models/llama-v3p3-70b-instruct", "name": "Llama 3.3 70B", "context": "128K"},
            {"id": "accounts/fireworks/models/qwen2p5-72b-instruct", "name": "Qwen2.5 72B", "context": "128K"},
        ],
        "docs_url": "https://docs.fireworks.ai/"
    },
    "novita": {
        "name": "Novita AI",
        "protocol": "OpenAI",
        "base_url": "https://api.novita.ai/v3/openai",
        "full_url": False,
        "models": [
            {"id": "deepseek/deepseek_v3", "name": "DeepSeek V3", "context": "64K"},
            {"id": "meta-llama/llama-3.3-70b-instruct", "name": "Llama 3.3 70B", "context": "128K"},
        ],
        "docs_url": "https://novita.ai/docs"
    },
    "hyperbolic": {
        "name": "Hyperbolic",
        "protocol": "OpenAI",
        "base_url": "https://api.hyperbolic.xyz/v1",
        "full_url": False,
        "models": [
            {"id": "deepseek-ai/DeepSeek-V3", "name": "DeepSeek V3", "context": "64K"},
            {"id": "meta-llama/Llama-3.3-70B-Instruct", "name": "Llama 3.3 70B", "context": "128K"},
        ],
        "docs_url": "https://docs.hyperbolic.xyz/"
    },
    "replicate": {
        "name": "Replicate",
        "protocol": "OpenAI",
        "base_url": "https://openai-proxy.replicate.com/v1",
        "full_url": False,
        "models": [],
        "docs_url": "https://replicate.com/docs"
    },
    "poe": {
        "name": "Poe",
        "protocol": "OpenAI",
        "base_url": "https://api.poe.com/chat/completions",
        "full_url": True,
        "models": [],
        "docs_url": "https://creator.poe.com/docs/quick-start"
    },
    "腾讯云": {
        "name": "腾讯云大模型知识引擎",
        "protocol": "OpenAI",
        "base_url": "https://api.lke.tencent-cloud.com/v1",
        "full_url": False,
        "models": [
            {"id": "hunyuan-pro", "name": "混元Pro", "context": "32K"},
            {"id": "hunyuan-standard", "name": "混元Standard", "context": "32K"},
            {"id": "hunyuan-standard-256K", "name": "混元Standard 256K", "context": "256K"},
            {"id": "hunyuan-lite", "name": "混元Lite", "context": "8K"},
            {"id": "hunyuan-vision", "name": "混元Vision (多模态)", "context": "32K", "vision": True},
        ],
        "docs_url": "https://cloud.tencent.com/document/product/1759"
    },
    "tencent": {
        "name": "腾讯云大模型知识引擎",
        "protocol": "OpenAI",
        "base_url": "https://api.lke.tencent-cloud.com/v1",
        "full_url": False,
        "models": [],
        "docs_url": "https://cloud.tencent.com/document/product/1759"
    },
    "华为云": {
        "name": "华为云盘古大模型",
        "protocol": "OpenAI",
        "base_url": "https://infer-modelarts-cn-southwest-2.myhuaweicloud.com/v1",
        "full_url": False,
        "models": [],
        "note": "需要在华为云ModelArts平台创建推理服务",
        "docs_url": "https://support.huaweicloud.com/productdesc-modelarts/"
    },
    "huawei": {
        "name": "华为云盘古大模型",
        "protocol": "OpenAI",
        "base_url": "https://infer-modelarts-cn-southwest-2.myhuaweicloud.com/v1",
        "full_url": False,
        "models": [],
        "docs_url": "https://support.huaweicloud.com/productdesc-modelarts/"
    },
    "京东": {
        "name": "京东言犀大模型",
        "protocol": "OpenAI",
        "base_url": "https://api.yanxi.jd.com/v1",
        "full_url": False,
        "models": [
            {"id": "yanxi-chat", "name": "言犀Chat", "context": "32K"},
        ],
        "docs_url": "https://yanxi.jd.com/"
    },
    "京东云": {
        "name": "京东言犀大模型",
        "protocol": "OpenAI",
        "base_url": "https://api.yanxi.jd.com/v1",
        "full_url": False,
        "models": [],
        "docs_url": "https://yanxi.jd.com/"
    },
    "网易": {
        "name": "网易伏羲",
        "protocol": "OpenAI",
        "base_url": "https://openapi.163.com/v1",
        "full_url": False,
        "models": [],
        "docs_url": "https://fuxi.163.com/"
    },
    "昆仑万维": {
        "name": "昆仑万维天工大模型",
        "protocol": "OpenAI",
        "base_url": "https://api.tiangong.kunlun.com/v1",
        "full_url": False,
        "models": [
            {"id": "tiangong-pro", "name": "天工Pro", "context": "32K"},
        ],
        "docs_url": "https://tiangong.kunlun.com/"
    },
    "天工": {
        "name": "昆仑万维天工大模型",
        "protocol": "OpenAI",
        "base_url": "https://api.tiangong.kunlun.com/v1",
        "full_url": False,
        "models": [],
        "docs_url": "https://tiangong.kunlun.com/"
    },
    "xai": {
        "name": "xAI (Grok)",
        "protocol": "OpenAI",
        "base_url": "https://api.x.ai/v1",
        "full_url": False,
        "models": [
            {"id": "grok-2-1212", "name": "Grok 2", "context": "128K"},
            {"id": "grok-2-vision-1212", "name": "Grok 2 Vision", "context": "32K", "vision": True},
            {"id": "grok-beta", "name": "Grok Beta", "context": "128K"},
        ],
        "docs_url": "https://docs.x.ai/"
    },
    "grok": {
        "name": "xAI (Grok)",
        "protocol": "OpenAI",
        "base_url": "https://api.x.ai/v1",
        "full_url": False,
        "models": [
            {"id": "grok-2-1212", "name": "Grok 2", "context": "128K"},
        ],
        "docs_url": "https://docs.x.ai/"
    },
    "gemini": {
        "name": "Google Gemini",
        "protocol": "OpenAI",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "full_url": False,
        "models": [
            {"id": "gemini-2.0-flash", "name": "Gemini 2.0 Flash (最新)", "context": "1M", "recommended": True},
            {"id": "gemini-2.0-flash-lite", "name": "Gemini 2.0 Flash Lite", "context": "1M"},
            {"id": "gemini-1.5-pro", "name": "Gemini 1.5 Pro", "context": "2M"},
            {"id": "gemini-1.5-flash", "name": "Gemini 1.5 Flash", "context": "1M"},
            {"id": "gemini-1.5-flash-8b", "name": "Gemini 1.5 Flash 8B", "context": "1M"},
        ],
        "note": "Google Gemini 支持 OpenAI 兼容接口",
        "docs_url": "https://ai.google.dev/gemini-api/docs/openai"
    },
    "google": {
        "name": "Google Gemini",
        "protocol": "OpenAI",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "full_url": False,
        "models": [
            {"id": "gemini-2.0-flash", "name": "Gemini 2.0 Flash", "context": "1M", "recommended": True},
        ],
        "docs_url": "https://ai.google.dev/gemini-api/docs/openai"
    },
    "vertex": {
        "name": "Google Vertex AI",
        "protocol": "OpenAI",
        "base_url": "https://{region}-aiplatform.googleapis.com/v1/projects/{project-id}/locations/{region}/endpoints/openapi",
        "full_url": False,
        "models": [],
        "note": "需要替换 region 和 project-id",
        "docs_url": "https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/openai"
    },
    "huggingface": {
        "name": "Hugging Face",
        "protocol": "OpenAI",
        "base_url": "https://api-inference.huggingface.co/v1",
        "full_url": False,
        "models": [],
        "note": "使用 Inference API 或 Dedicated Endpoints",
        "docs_url": "https://huggingface.co/docs/api-inference/index"
    },
    "ollama": {
        "name": "Ollama (本地部署)",
        "protocol": "OpenAI",
        "base_url": "http://localhost:11434/v1",
        "full_url": False,
        "models": [],
        "note": "本地部署，默认端口11434，需先安装Ollama",
        "docs_url": "https://ollama.com/"
    },
    "lmstudio": {
        "name": "LM Studio (本地部署)",
        "protocol": "OpenAI",
        "base_url": "http://localhost:1234/v1",
        "full_url": False,
        "models": [],
        "note": "本地部署，默认端口1234，需先启动LM Studio服务器",
        "docs_url": "https://lmstudio.ai/"
    },
    "vllm": {
        "name": "vLLM (本地/自托管)",
        "protocol": "OpenAI",
        "base_url": "http://localhost:8000/v1",
        "full_url": False,
        "models": [],
        "note": "自托管部署，默认端口8000，需先启动vLLM服务",
        "docs_url": "https://docs.vllm.ai/"
    },
    "sglang": {
        "name": "SGLang (本地/自托管)",
        "protocol": "OpenAI",
        "base_url": "http://localhost:30000/v1",
        "full_url": False,
        "models": [],
        "note": "自托管部署，默认端口30000",
        "docs_url": "https://sgl-project.github.io/"
    },
    "oneapi": {
        "name": "One API (聚合中转)",
        "protocol": "OpenAI",
        "base_url": "https://api.oneapi.com/v1",
        "full_url": False,
        "models": [],
        "note": "开源API聚合中转平台，支持多种模型",
        "docs_url": "https://github.com/songquanpeng/one-api"
    },
    "newapi": {
        "name": "New API (聚合中转)",
        "protocol": "OpenAI",
        "base_url": "https://api.newapi.com/v1",
        "full_url": False,
        "models": [],
        "note": "One API的衍生版本，支持更多功能",
        "docs_url": "https://github.com/Calcium-Ion/new-api"
    },
    "lobe": {
        "name": "Lobe Chat (聚合)",
        "protocol": "OpenAI",
        "base_url": "https://api.lobehub.com/v1",
        "full_url": False,
        "models": [],
        "docs_url": "https://lobehub.com/"
    },
    "aihubmix": {
        "name": "AI Hub Mix (聚合)",
        "protocol": "OpenAI",
        "base_url": "https://aihubmix.com/v1",
        "full_url": False,
        "models": [],
        "docs_url": "https://aihubmix.com/"
    },
    "api2d": {
        "name": "API2D (OpenAI代理)",
        "protocol": "OpenAI",
        "base_url": "https://openai.api2d.net/v1",
        "full_url": False,
        "models": [],
        "note": "国内OpenAI API代理服务",
        "docs_url": "https://api2d.com/"
    },
    "closeai": {
        "name": "CloseAI (OpenAI代理)",
        "protocol": "OpenAI",
        "base_url": "https://api.closeai-proxy.com/v1",
        "full_url": False,
        "models": [],
        "note": "国内OpenAI API代理服务",
        "docs_url": "https://closeai.com/"
    },
}


def search_provider(query: str) -> dict:
    """
    搜索厂商配置信息
    
    Args:
        query: 厂商名称关键词
        
    Returns:
        厂商配置信息字典，未找到返回None
    """
    query = query.lower().strip()
    
    # 直接匹配
    if query in KNOWN_PROVIDERS:
        return KNOWN_PROVIDERS[query]
    
    # 模糊匹配
    for key, config in KNOWN_PROVIDERS.items():
        if query in key or key in query:
            return config
        if query in config["name"].lower():
            return config
    
    return None


def format_output(config: dict) -> str:
    """格式化输出厂商配置信息"""
    if not config:
        return json.dumps({"error": "未找到该厂商的配置信息"}, ensure_ascii=False, indent=2)
    
    return json.dumps(config, ensure_ascii=False, indent=2)


def main():
    if len(sys.argv) < 2:
        print("用法: python search_provider.py <厂商名称>")
        print("\n支持的厂商:")
        providers = set()
        for key, config in KNOWN_PROVIDERS.items():
            providers.add(config["name"])
        for name in sorted(providers):
            print(f"  - {name}")
        sys.exit(1)
    
    query = sys.argv[1]
    config = search_provider(query)
    print(format_output(config))


if __name__ == "__main__":
    main()
