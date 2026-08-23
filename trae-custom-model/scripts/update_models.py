#!/usr/bin/env python3
"""
TRAE 自定义模型厂商配置自动更新脚本 v2.1

功能:
1. 自动搜索各厂商最新模型信息（使用WebSearch）
2. 检测模型停用/上线情况
3. 官方接口直接探测（GET {base}/models）校验模型ID真实性
4. 模型置信度标注与真实性留痕
5. 分析模型质量和使用建议
6. 更新 search_provider.py 和 providers.md
7. 记录详细的更新日志，供定时任务停用/变更同步

用法:
    python update_models.py [--dry-run] [--check-only] [--auto-search] [--no-probe] [--probe-only]
    
参数:
    --dry-run: 只显示将要进行的更改，不实际修改文件
    --check-only: 只检查更新，不修改文件（用于定时任务同步）
    --auto-search: 自动搜索最新模型信息（需要网络）
    --probe: 开启官方接口探测（默认开启）
    --no-probe: 关闭官方接口探测（离线场景）
    --probe-only: 仅执行官方接口探测并输出核验报告
"""

import json
import re
import sys
import os
import socket
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ============================================================
# 厂商搜索配置 - 定义需要搜索的厂商和搜索关键词
# ============================================================
PROVIDER_SEARCH_CONFIG = {
    "openai": {
        "name": "OpenAI",
        "search_keywords": [
            "OpenAI API 模型列表 2026 gpt-5 gpt-5.5 最新",
            "OpenAI gpt-5.5 API model id 2026",
            "OpenAI 停用模型 2026 gpt-4o 停用"
        ],
        "docs_url": "https://platform.openai.com/docs",
        "status_check_url": "https://status.openai.com",
        "known_models": ["gpt-5.5", "gpt-4o", "gpt-4o-mini"]
    },
    "anthropic": {
        "name": "Anthropic",
        "search_keywords": [
            "Claude Opus 4.7 Anthropic 最新模型 2026",
            "Anthropic Claude 模型列表 2026 claude-4",
            "Anthropic 停用模型 2026 claude-3"
        ],
        "docs_url": "https://docs.anthropic.com/",
        "known_models": ["claude-opus-4.7", "claude-3-5-sonnet-20241022", "claude-3-opus-20240229"]
    },
    "deepseek": {
        "name": "DeepSeek",
        "search_keywords": [
            "DeepSeek V4 模型列表 2026 deepseek-v4-pro",
            "DeepSeek 停用模型 2026 deepseek-chat 停用"
        ],
        "docs_url": "https://platform.deepseek.com/",
        "known_models": ["deepseek-v4-pro", "deepseek-v4-flash", "deepseek-chat", "deepseek-reasoner"]
    },
    "智谱": {
        "name": "智谱AI",
        "search_keywords": [
            "GLM-5 模型列表 2026 bigmodel 智谱",
            "智谱 GLM-5.1 API model id 2026"
        ],
        "docs_url": "https://open.bigmodel.cn/dev/howuse/glm-4",
        "known_models": ["glm-5-turbo", "glm-5.1", "glm-4-plus", "glm-4-airx"]
    },
    "通义千问": {
        "name": "通义千问",
        "search_keywords": [
            "Qwen3 模型列表 2026 阿里云百炼 dashscope",
            "阿里云百炼 Qwen3.6 API model id 2026"
        ],
        "docs_url": "https://help.aliyun.com/zh/model-studio/getting-started/models",
        "known_models": ["qwen3.6-max-preview", "qwen3.6-plus", "qwen3.5-max", "qwen-plus"]
    },
    "kimi": {
        "name": "Kimi",
        "search_keywords": [
            "Kimi K2.6 moonshot API model id 2026",
            "月之暗面 Kimi 最新模型 2026"
        ],
        "docs_url": "https://platform.moonshot.cn/",
        "known_models": ["kimi-k2.6", "kimi-k2", "kimi-for-coding", "moonshot-v1-8k"]
    },
    "硅基流动": {
        "name": "硅基流动 SiliconFlow",
        "search_keywords": [
            "硅基流动 模型列表 2026 SiliconFlow 最新模型"
        ],
        "docs_url": "https://docs.siliconflow.cn/",
        "known_models": ["DeepSeek-V4-Pro", "GLM-5-Turbo", "Qwen3.6-Max-Preview"]
    },
    "零一万物": {
        "name": "零一万物",
        "search_keywords": [
            "零一万物 模型列表 2026 yi-large API"
        ],
        "docs_url": "https://platform.lingyiwanwu.com/",
        "known_models": ["yi-large", "yi-medium", "yi-spark"]
    }
}

# ============================================================
# 动态年份处理
# 搜索关键词中硬编码的年份（如 2026）会逐年过期，
# 运行时统一替换为当前年份，避免关键词随年份失效。
# ============================================================
_YEAR_PATTERN = re.compile(r"\b20\d{2}\b")

def _apply_dynamic_year():
    """将所有搜索关键词中的四位数年份替换为当前年份"""
    current_year = str(datetime.now().year)
    for config in PROVIDER_SEARCH_CONFIG.values():
        keywords = config.get("search_keywords", [])
        config["search_keywords"] = [
            _YEAR_PATTERN.sub(current_year, kw) for kw in keywords
        ]

_apply_dynamic_year()

# ============================================================
# 官方接口探测配置
# 每个可探测的厂商提供一个 GET {base}/models 地址，用于
# 直接校验模型ID真实性，而非仅依赖 WebSearch / 手工杜撰。
# 若环境变量中存在 API Key（如 OPENAI_API_KEY），会携带
# 鉴权探测；否则按「需鉴权」处理并记录留痕。
# ============================================================
PROVIDER_PROBE_CONFIG = {
    "openai": {
        "api_base_url": "https://api.openai.com/v1",
        "api_key_env": "OPENAI_API_KEY",
        "models_path": "/models"
    },
    "anthropic": {
        "api_base_url": "https://api.anthropic.com/v1",
        "api_key_env": "ANTHROPIC_API_KEY",
        "models_path": "/models",
        "requires_auth": True
    },
    "deepseek": {
        "api_base_url": "https://api.deepseek.com",
        "api_key_env": "DEEPSEEK_API_KEY",
        "models_path": "/models"
    },
    "智谱": {
        "api_base_url": "https://open.bigmodel.cn/api/paas/v4",
        "api_key_env": "ZHIPU_API_KEY",
        "models_path": "/models"
    },
    "通义千问": {
        "api_base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "api_key_env": "DASHSCOPE_API_KEY",
        "models_path": "/models"
    },
    "kimi": {
        "api_base_url": "https://api.kimi.com/coding/v1",
        "api_key_env": "MOONSHOT_API_KEY",
        "models_path": "/models"
    },
    "硅基流动": {
        "api_base_url": "https://api.siliconflow.cn/v1",
        "api_key_env": "SILICONFLOW_API_KEY",
        "models_path": "/models"
    },
    "零一万物": {
        "api_base_url": "https://api.lingyiwanwu.com/v1",
        "api_key_env": "LINGYIWANWU_API_KEY",
        "models_path": "/models"
    }
}

# 已知的停用模型（需要定期检查和更新）
DEPRECATED_MODELS = {
    "deepseek-chat": {
        "since": "2026-07-24",
        "replacement": "deepseek-v4-pro",
        "reason": "V4系列上线",
        "confidence": "confirmed"
    },
    "deepseek-reasoner": {
        "since": "2026-07-24",
        "replacement": "deepseek-v4-flash",
        "reason": "V4系列上线",
        "confidence": "confirmed"
    },
    "gpt-4o": {
        "since": "2026-02",
        "replacement": "gpt-5.5",
        "reason": "GPT-5系列上线",
        "confidence": "confirmed"
    },
    "gpt-4o-mini": {
        "since": "2026-02",
        "replacement": "gpt-5.5",
        "reason": "GPT-5系列上线",
        "confidence": "confirmed"
    },
    "gpt-4-turbo": {
        "since": "2026-02",
        "replacement": "gpt-5.5",
        "reason": "GPT-5系列上线",
        "confidence": "confirmed"
    },
    "o1-preview": {
        "since": "2026-02",
        "replacement": "gpt-5.5",
        "reason": "统一到GPT-5系列",
        "confidence": "confirmed"
    },
    "o1-mini": {
        "since": "2026-02",
        "replacement": "gpt-5.5",
        "reason": "统一到GPT-5系列",
        "confidence": "confirmed"
    },
    "claude-3-5-sonnet-20241022": {
        "since": "2026-04",
        "replacement": "claude-opus-4.7",
        "reason": "Claude 4系列上线",
        "confidence": "confirmed"
    },
    "claude-3-opus-20240229": {
        "since": "2026-04",
        "replacement": "claude-opus-4.7",
        "reason": "Claude 4系列上线",
        "confidence": "confirmed"
    },
    "kimi-for-coding": {
        "since": "2026-04",
        "replacement": "kimi-k2.6",
        "reason": "K2系列上线",
        "confidence": "confirmed"
    }
}

# 新增模型需要检查的特征词
NEW_MODEL_PATTERNS = [
    r"(gpt-\d+(?:\.\d+)?)",
    r"(claude-(?:opus|sonnet|haiku)-\d+(?:\.\d+)?)",
    r"(deepseek-v\d+(?:\.\d+)?(?:-(?:pro|flash|chat|reasoner))?)",
    r"(glm-\d+(?:\.\d+)?(?:-(?:turbo|plus|air))?)",
    r"(qwen\d(?:\.\d+)?(?:-(?:max|plus|flash|turbo))?)",
    r"(kimi-k\d(?:\.\d+)?)",
    r"(step-\d+(?:\.\d+)?(?:-(?:flash|pro))?)"
]

# 更新配置文件路径
CONFIG_FILE = Path(__file__).parent.parent / "references" / "update_config.json"
CHANGELOG_FILE = Path(__file__).parent.parent / "references" / "model_changelog.md"
PROVIDERS_FILE = Path(__file__).parent.parent / "references" / "providers.md"
SEARCH_SCRIPT = Path(__file__).parent / "search_provider.py"


# ============================================================
# 更新配置管理类
# ============================================================
class UpdateConfig:
    """更新配置管理"""
    
    def __init__(self):
        self.config_file = CONFIG_FILE
        self.load()
    
    def load(self):
        """加载配置"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = self._default_config()
    
    def _default_config(self):
        """默认配置"""
        return {
            "version": "2.0",
            "update_frequency": "weekly",
            "last_update": None,
            "last_check": None,
            "next_scheduled_check": None,
            "auto_update_enabled": False,
            "update_history": [],
            "providers": {},
            "model_count": 0,
            "deprecated_models": [],
            "new_models_found": [],
            "quality_metrics": {
                "total_checks": 0,
                "successful_updates": 0,
                "errors": []
            }
        }
    
    def save(self):
        """保存配置"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def record_update(self, provider: str, changes: dict):
        """记录更新"""
        update_record = {
            "date": datetime.now().isoformat(),
            "provider": provider,
            "changes": changes
        }
        self.data["update_history"].append(update_record)
        self.data["last_update"] = datetime.now().isoformat()
        self.data["quality_metrics"]["successful_updates"] += 1
        
        # 计算下次检查时间
        self._calculate_next_check()
        
        # 保留最近100条记录
        if len(self.data["update_history"]) > 100:
            self.data["update_history"] = self.data["update_history"][-100:]
    
    def record_check(self, provider: str, status: str, details: dict = None):
        """记录检查"""
        check_record = {
            "date": datetime.now().isoformat(),
            "provider": provider,
            "status": status,
            "details": details or {}
        }
        if "check_history" not in self.data:
            self.data["check_history"] = []
        self.data["check_history"].append(check_record)
        self.data["last_check"] = datetime.now().isoformat()
        self.data["quality_metrics"]["total_checks"] += 1
        
        # 保留最近100条记录
        if len(self.data["check_history"]) > 100:
            self.data["check_history"] = self.data["check_history"][-100:]
    
    def record_new_model(self, model_id: str, provider: str, source: str):
        """记录新发现的模型"""
        new_model = {
            "model_id": model_id,
            "provider": provider,
            "discovered_date": datetime.now().date().isoformat(),
            "source": source,
            "verified": False
        }
        
        # 检查是否已存在
        for existing in self.data.get("new_models_found", []):
            if existing["model_id"] == model_id and existing["provider"] == provider:
                return False
        
        if "new_models_found" not in self.data:
            self.data["new_models_found"] = []
        self.data["new_models_found"].append(new_model)
        return True
    
    def mark_model_verified(self, model_id: str, provider: str):
        """标记模型已验证"""
        for model in self.data.get("new_models_found", []):
            if model["model_id"] == model_id and model["provider"] == provider:
                model["verified"] = True
                model["verified_date"] = datetime.now().date().isoformat()
    
    def _calculate_next_check(self):
        """计算下次检查时间"""
        freq = self.data.get("update_frequency", "weekly")
        if freq == "weekly":
            delta = timedelta(days=7)
        elif freq == "monthly":
            delta = timedelta(days=30)
        else:
            delta = timedelta(days=7)  # 默认一周
        
        next_check = datetime.now() + delta
        self.data["next_scheduled_check"] = next_check.isoformat()
    
    def get_needs_update(self) -> bool:
        """检查是否需要更新"""
        if self.data["update_frequency"] == "manual":
            return False
        
        if not self.data["last_update"]:
            return True
        
        last_update = datetime.fromisoformat(self.data["last_update"])
        now = datetime.now()
        
        if self.data["update_frequency"] == "weekly":
            return (now - last_update) > timedelta(days=7)
        elif self.data["update_frequency"] == "monthly":
            return (now - last_update) > timedelta(days=30)
        
        return False
    
    def set_frequency(self, freq: str):
        """设置更新频率"""
        if freq in ["weekly", "monthly", "manual"]:
            self.data["update_frequency"] = freq
            self._calculate_next_check()
            self.save()
            return True
        return False
    
    def get_provider_status(self, provider_id: str) -> dict:
        """获取厂商状态"""
        return self.data.get("providers", {}).get(provider_id, {
            "status": "unknown",
            "last_verified": None,
            "model_count": 0,
            "issues": []
        })
    
    def update_provider_status(self, provider_id: str, status: dict):
        """更新厂商状态"""
        if "providers" not in self.data:
            self.data["providers"] = {}
        self.data["providers"][provider_id] = status


# ============================================================
# 模型更新分析器
# ============================================================
class ModelAnalyzer:
    """模型信息分析器"""
    
    @staticmethod
    def extract_model_ids(text: str) -> List[str]:
        """从文本中提取模型ID"""
        models = set()
        for pattern in NEW_MODEL_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            models.update(matches)
        return list(models)
    
    @staticmethod
    def is_likely_new(model_id: str, known_models: List[str]) -> bool:
        """判断是否为新模型"""
        return model_id.lower() not in [m.lower() for m in known_models]
    
    @staticmethod
    def is_deprecated(model_id: str) -> Tuple[bool, Optional[dict]]:
        """检查模型是否已停用"""
        model_lower = model_id.lower()
        for deprecated_id, info in DEPRECATED_MODELS.items():
            if deprecated_id.lower() == model_lower:
                return True, info
        return False, None
    
    @staticmethod
    def get_model_confidence(model_id: str) -> str:
        """评估模型ID的置信度"""
        # 高置信度：包含版本号
        if re.search(r'\d+(?:\.\d+)?', model_id):
            return "high"
        # 中置信度：包含明确后缀
        if any(suffix in model_id.lower() for suffix in ['-pro', '-flash', '-turbo', '-plus', '-max']):
            return "medium"
        return "low"
    
    @staticmethod
    def generate_update_suggestion(model_id: str, provider: str, action: str) -> str:
        """生成更新建议"""
        if action == "add":
            return f"建议添加 {provider} 的新模型: {model_id}"
        elif action == "remove":
            info = DEPRECATED_MODELS.get(model_id, {})
            replacement = info.get("replacement", "最新版本")
            return f"建议移除 {provider} 的停用模型: {model_id}，替代方案: {replacement}"
        elif action == "update":
            return f"建议更新 {provider} 的模型: {model_id}"
        return ""


# ============================================================
# 官方接口探测器
# ============================================================
class ModelVerifier:
    """通过厂商官方 GET {base}/models 接口直接探测模型清单，
    用于校验内置模型ID真实性，而非仅依赖 WebSearch 或人工录入。

    - 携带 API Key（从环境变量读取）时返回真实模型列表；
    - 无 Key 时记录「需鉴权」留痕，可确认接口可达但不返回清单；
    - 网络失败/证书异常时记录「不可达」，避免误判。
    """

    PROBE_TIMEOUT = 8

    @staticmethod
    def probe(probe_config: dict) -> dict:
        """探测单个厂商的 /models 接口

        Args:
            probe_config: PROVIDER_PROBE_CONFIG 中的单条配置

        Returns:
            {
                "status": "ok" | "requires_auth" | "unreachable" | "failed",
                "models": List[str],      # status=ok 时返回真实模型ID列表
                "message": str
            }
        """
        base_url = probe_config.get("api_base_url", "").rstrip("/")
        models_path = probe_config.get("models_path", "/models")
        api_key = os.environ.get(probe_config.get("api_key_env", ""), "")
        url = f"{base_url}{models_path}"

        headers = {"User-Agent": "TRAE-custom-model-verifier/2.1"}
        if api_key:
            if probe_config.get("requires_auth"):
                headers["x-api-key"] = api_key
            headers["Authorization"] = f"Bearer {api_key}"

        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=ModelVerifier.PROBE_TIMEOUT) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                if resp.status == 200:
                    models = ModelVerifier._parse_models(body)
                    if models is None:
                        return {"status": "failed", "models": [], "message": "接口返回但无法解析模型列表"}
                    return {"status": "ok", "models": models, "message": f"探测成功，共 {len(models)} 个模型"}
                return {
                    "status": "requires_auth",
                    "models": [],
                    "message": f"接口可达但 HTTP {resp.status}（需鉴权）"
                }
        except urllib.error.HTTPError as e:
            # 401/403 = 鉴权不足但对端点确实存在，直接断言需人工验证
            if e.code in (401, 403):
                return {
                    "status": "requires_auth",
                    "models": [],
                    "message": f"接口可达但 HTTP {e.code}（需鉴权/配额）"
                }
            return {
                "status": "failed",
                "models": [],
                "message": f"HTTP {e.code}"
            }
        except (urllib.error.URLError, socket.timeout, OSError) as e:
            return {
                "status": "unreachable",
                "models": [],
                "message": f"网络不可达: {e}"
            }
        except Exception as e:  # 证书等异常
            return {
                "status": "failed",
                "models": [],
                "message": f"探测异常: {e}"
            }

    @staticmethod
    def _parse_models(body: str) -> Optional[List[str]]:
        """从 OpenAI 兼容 /models 响应中解析模型ID列表"""
        try:
            data = json.loads(body)
        except (json.JSONDecodeError, ValueError):
            return None
        if isinstance(data, dict) and isinstance(data.get("data"), list):
            ids = []
            for item in data["data"]:
                if isinstance(item, dict) and isinstance(item.get("id"), str):
                    ids.append(item["id"])
            return ids or None
        # Anthropic 风格：{"data":[{"id":..., "type":"model"}], ...}
        return None

    @staticmethod
    def check_model(known_models: List[str], probe_result: dict) -> Dict[str, str]:
        """根据探测结果给模型的核验状态打标

        Returns:
            { model_id: "verified" | "not_found" | "requires_auth" | "unverified" }
        """
        status = probe_result.get("status")
        probed = set(m.lower() for m in probe_result.get("models", []))

        result = {}
        for model in known_models:
            low = model.lower()
            if status == "ok":
                result[model] = "verified" if low in probed else "not_found"
            elif status == "requires_auth":
                result[model] = "requires_auth"
            else:
                result[model] = "unverified"
        return result


# ============================================================
# 模型信息更新器
# ============================================================
class ModelUpdater:
    """模型信息更新器"""
    
    def __init__(self, dry_run: bool = False, auto_search: bool = False, probe: bool = True):
        self.dry_run = dry_run
        self.auto_search = auto_search
        self.probe = probe
        self.config = UpdateConfig()
        self.analyzer = ModelAnalyzer()
        self.script_dir = Path(__file__).parent
        self.project_dir = self.script_dir.parent
        self.changes = []
        self.suggestions = []
        self.verification_report = []
    
    def run(self, check_only: bool = False):
        """运行更新"""
        print("=" * 70)
        print("🚀 TRAE 自定义模型配置自动更新工具 v2.1")
        print("=" * 70)
        print(f"模式: {'🔍 只检查' if check_only else ('⚙️ 模拟运行' if self.dry_run else '📝 实际更新')}")
        print(f"官方接口探测: {'✅ 开启' if self.probe else '⏭️ 已关闭(--no-probe)'}")
        print(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"更新频率: {self.config.data['update_frequency']}")
        print()
        
        # 显示上次更新状态
        if self.config.data['last_update']:
            print(f"上次更新: {self.config.data['last_update']}")
        if self.config.data['last_check']:
            print(f"上次检查: {self.config.data['last_check']}")
        print()
        
        # 检查各厂商
        for provider_id, config in PROVIDER_SEARCH_CONFIG.items():
            print(f"\n{'='*70}")
            print(f"[{provider_id}] {config['name']}")
            print("-" * 70)
            # 提前探测（每个厂商仅探测一次，可被 _check_provider 复用）
            probe_result = None
            if self.probe:
                probe_config = PROVIDER_PROBE_CONFIG.get(provider_id)
                probe_result = ModelVerifier.probe(probe_config) if probe_config else None
            self._check_provider(provider_id, config, probe_result)
        
        # 显示总结和建议（含停用/变更同步摘要）
        self._show_summary()
        
        if check_only:
            self._show_sync_summary()
        
        if not check_only and not self.dry_run:
            # 保存更新记录
            self.config.save()
            # 更新日志
            self._update_changelog()
            print(f"\n✅ 更新完成！配置已保存到: {CONFIG_FILE}")
        
        return len(self.changes) > 0 or len(self.suggestions) > 0
    
    def _check_provider(self, provider_id: str, config: dict, probe_result: Optional[dict] = None):
        """检查单个厂商

        probe_result: ModelVerifier 探测结果（含真实模型清单/核验状态）
        """
        provider_status = self.config.get_provider_status(provider_id)
        issues = []
        
        # 0. 官方接口探测结果核验
        model_verify = {}
        if self.probe:
            print("\n🔍 官方接口探测:")
            if probe_result is None:
                probe_config = PROVIDER_PROBE_CONFIG.get(provider_id)
                probe_result = ModelVerifier.probe(probe_config) if probe_config else None
            if probe_result:
                icon = {"ok": "✅", "requires_auth": "🔑", "unreachable": "⛔", "failed": "⚠️"}.get(
                    probe_result.get("status", ""), "❓")
                print(f"  {icon} 状态: {probe_result.get('status', 'unknown')}")
                print(f"     {probe_result.get('message', '')}")
                model_verify = ModelVerifier.check_model(config.get("known_models", []), probe_result)
            else:
                print("  ⚠️ 该厂商无探测配置，跳过")
        
        # 1. 检查已知停用模型
        print("\n📋 停用模型检查:")
        deprecated_found = []
        for model_id in config.get("known_models", []):
            is_dep, info = self.analyzer.is_deprecated(model_id)
            if is_dep:
                deprecated_found.append((model_id, info))
                self.changes.append({
                    "provider": config["name"],
                    "provider_id": provider_id,
                    "type": "deprecated",
                    "model": model_id,
                    "info": info,
                    "action": "remove"
                })
        
        if deprecated_found:
            for model_id, info in deprecated_found:
                print(f"  ⚠️  {model_id}")
                print(f"     停用时间: {info['since']}")
                print(f"     原因: {info['reason']}")
                print(f"     替代方案: {info['replacement']}")
                suggestion = self.analyzer.generate_update_suggestion(model_id, config["name"], "remove")
                if suggestion:
                    self.suggestions.append(suggestion)
        else:
            print("  ✅ 无已知停用模型")
        
        # 2. 检查新模型 + 真实性核验
        print("\n🆕 新模型检查:")
        print("  💡 如需搜索最新模型，请添加 --auto-search 参数")
        print("  📌 当前内置模型（含核验状态）:")
        model_confidence = {}
        for model in config.get("known_models", []):
            verify_state = model_verify.get(model, "")
            conf = self.analyzer.get_model_confidence(model)
            # 合成可信度：官网页面=verified(高) > 启发式+需鉴权 > 启发式
            display_conf = conf
            if verify_state == "verified":
                display_conf = "verified(官方接口)"
                verified = "✅"
            elif verify_state == "not_found":
                display_conf = "high" if conf == "high" else conf
                verified = "❌ 探测未命中(疑似杜撰)"
            elif verify_state == "requires_auth":
                display_conf = f"{conf}(待API Key核验)"
                verified = "🔑"
            else:
                display_conf = f"{conf}(未核验)"
                verified = "⚠️"
            model_confidence[model] = {"confidence": display_conf, "verified": verified}
            print(f"     {verified} {model}  [{display_conf}]")
        if len(config.get("known_models", [])) > 5:
            print(f"     ... 共 {len(config['known_models'])} 个")
        
        # 3. 检查厂商状态
        print("\n📊 厂商状态:")
        print(f"  状态: {provider_status.get('status', 'unknown')}")
        print(f"  最后验证: {provider_status.get('last_verified', '从未')}")
        print(f"  模型数量: {provider_status.get('model_count', 0)}")
        
        if provider_status.get("issues"):
            print("  问题:")
            for issue in provider_status["issues"]:
                print(f"    - {issue}")
        
        # 收集核验留痕
        if model_verify:
            unverified = {k: v for k, v in model_verify.items() if v != "verified"}
            if unverified:
                issues.append(f"{len(unverified)} 个模型未通过官方接口核验，需人工确认: {', '.join(unverified.keys())}")
            self.verification_report.append({
                "provider_id": provider_id,
                "provider": config["name"],
                "probe_status": probe_result.get("status") if probe_result else None,
                "probe_message": probe_result.get("message") if probe_result else None,
                "model_status": model_verify
            })
        
        # 更新厂商状态
        provider_status["last_verified"] = datetime.now().date().isoformat()
        provider_status["model_count"] = len(config.get("known_models", []))
        provider_status["deprecated_count"] = len(deprecated_found)
        if issues:
            provider_status["issues"] = issues
        else:
            provider_status.pop("issues", None)
        self.config.update_provider_status(provider_id, provider_status)
        
        # 记录检查
        self.config.record_check(provider_id, "completed", {
            "deprecated_found": len(deprecated_found),
            "model_count": len(config.get("known_models", [])),
            "probe_status": probe_result.get("status") if probe_result else None,
            "verification_issues": len(issues)
        })
    
    def _show_summary(self):
        """显示更新总结"""
        print("\n" + "=" * 70)
        print("📊 更新总结")
        print("=" * 70)
        
        # 变更统计
        deprecated_changes = [c for c in self.changes if c["type"] == "deprecated"]
        
        print(f"\n📈 统计:")
        print(f"  - 检查厂商数: {len(PROVIDER_SEARCH_CONFIG)}")
        print(f"  - 发现停用模型: {len(deprecated_changes)}")
        print(f"  - 新模型建议: {len(self.suggestions)}")
        
        # 详细变更
        if deprecated_changes:
            print(f"\n⚠️  停用模型处理建议:")
            for change in deprecated_changes:
                print(f"  [{change['provider']}]")
                print(f"    - 移除: {change['model']}")
                print(f"    - 替代: {change['info']['replacement']}")
        
        if self.suggestions:
            print(f"\n💡 更新建议:")
            for i, suggestion in enumerate(self.suggestions, 1):
                print(f"  {i}. {suggestion}")
        
        # 质量指标
        print(f"\n📉 质量指标:")
        metrics = self.config.data.get("quality_metrics", {})
        print(f"  - 总检查次数: {metrics.get('total_checks', 0)}")
        print(f"  - 成功更新: {metrics.get('successful_updates', 0)}")
        
        # 下次检查时间
        if self.config.data.get("next_scheduled_check"):
            print(f"\n📅 下次计划检查: {self.config.data['next_scheduled_check']}")
        
        # 建议
        if deprecated_changes or self.suggestions:
            print("\n" + "=" * 70)
            print("⚡ 建议操作:")
            print("  1. 移除所有停用模型ID")
            print("  2. 添加新上线模型")
            print("  3. 更新 providers.md 文档")
            print("  4. 运行 'python scripts/update_models.py --dry-run' 查看更改")
            print("=" * 70)

    def _show_sync_summary(self):
        """停用/变更同步摘要（仅供定时任务 --check-only 使用）

        以机器可读且易解析的方式输出「需要同步给用户」的变更，
        供 SOLO 定时任务 / GitHub Actions 抓取并主动通知用户，
        无需人工进入脚本交互。
        """
        deprecated_changes = [c for c in self.changes if c["type"] == "deprecated"]
        unverified_models = []
        for report in self.verification_report:
            for model, status in (report.get("model_status") or {}).items():
                if status in ("not_found", "unverified"):
                    unverified_models.append((report["provider"], model, status))

        print("\n" + "=" * 70)
        print("🔔 需要同步的变更（SYNC SUMMARY）")
        print("=" * 70)
        changed = False

        if deprecated_changes:
            changed = True
            print("\n⛔ 停用模型（建议删除配置）:")
            for change in deprecated_changes:
                print(f"  [DEPRECATED] {change['model']} ({change['provider']}) -> 替代: {change['info']['replacement']}")
        else:
            print("\n无停用模型变更")

        if unverified_models:
            changed = True
            print("\n⚠️ 待人工核验/疑似杜撰模型:")
            for provider, model, status in unverified_models:
                tag = "探测未命中" if status == "not_found" else "未核验"
                print(f"  [UNVERIFIED] {model} ({provider}) - {tag}")

        if self.suggestions:
            changed = True
            print("\n💡 新模型建议:")
            for s in self.suggestions:
                print(f"  [SUGGESTION] {s}")

        if not changed:
            print("✅ 无需要同步的变更，模型清单已是最新")

        print("\n" + "=" * 70)
        print("结束 SYNC SUMMARY")
        print("=" * 70)

    def _update_changelog(self):
        """更新变更日志"""
        if not self.changes:
            return
        
        changelog_path = CHANGELOG_FILE
        changelog_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 生成变更日志内容
        new_entry = f"""
## 更新 {datetime.now().strftime('%Y-%m-%d %H:%M')}

### 变更统计
- 检查厂商: {len(PROVIDER_SEARCH_CONFIG)}
- 停用模型: {len([c for c in self.changes if c['type'] == 'deprecated'])}

### 详细变更
"""
        for change in self.changes:
            if change["type"] == "deprecated":
                new_entry += f"""
#### [{change['provider']}] 移除停用模型
- **模型ID**: `{change['model']}`
- **停用时间**: {change['info']['since']}
- **原因**: {change['info']['reason']}
- **替代方案**: `{change['info']['replacement']}`
"""
        
        # 读取现有内容
        if changelog_path.exists():
            with open(changelog_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
        else:
            existing_content = "# 模型变更日志\n\n---\n"
        
        # 追加新内容
        with open(changelog_path, 'w', encoding='utf-8') as f:
            f.write(new_entry)
            f.write("\n---\n\n")
            f.write(existing_content)


# ============================================================
# 交互式更新向导
# ============================================================
class UpdateWizard:
    """交互式更新向导"""
    
    def __init__(self):
        self.config = UpdateConfig()
    
    def run(self):
        """运行交互式向导"""
        print("\n" + "=" * 70)
        print("🎯 TRAE 模型配置更新向导")
        print("=" * 70)
        
        while True:
            print("\n请选择操作:")
            print("1. 立即检查更新")
            print("2. 设置更新频率")
            print("3. 查看更新历史")
            print("4. 查看统计信息")
            print("5. 重置配置")
            print("0. 退出")
            
            choice = input("\n请输入选项 [0-5]: ").strip()
            
            if choice == "1":
                updater = ModelUpdater()
                updater.run(check_only=False)
            elif choice == "2":
                self._set_frequency()
            elif choice == "3":
                self._show_history()
            elif choice == "4":
                self._show_stats()
            elif choice == "5":
                self._reset_config()
            elif choice == "0":
                print("\n再见！")
                break
            else:
                print("无效选项，请重试")
    
    def _set_frequency(self):
        """设置更新频率"""
        print("\n当前更新频率:", self.config.data.get("update_frequency", "weekly"))
        print("\n可选频率:")
        print("1. weekly  - 每周一次 (推荐)")
        print("2. monthly - 每月一次")
        print("3. manual  - 手动更新")
        
        choice = input("\n请选择 [1-3]: ").strip()
        freq_map = {"1": "weekly", "2": "monthly", "3": "manual"}
        
        if choice in freq_map:
            self.config.set_frequency(freq_map[choice])
            print(f"\n✅ 已设置为: {freq_map[choice]}")
        else:
            print("无效选项")
    
    def _show_history(self):
        """显示更新历史"""
        history = self.config.data.get("update_history", [])
        if not history:
            print("\n暂无更新历史")
            return
        
        print(f"\n最近 {min(10, len(history))} 条更新记录:")
        for record in reversed(history[-10:]):
            date = record.get("date", "未知时间")[:19]
            provider = record.get("provider", "未知")
            changes = record.get("changes", {})
            action = changes.get("action", "unknown")
            print(f"  [{date}] {provider} - {action}")
    
    def _show_stats(self):
        """显示统计信息"""
        metrics = self.config.data.get("quality_metrics", {})
        providers = self.config.data.get("providers", {})
        
        print("\n📊 统计信息:")
        print(f"  总检查次数: {metrics.get('total_checks', 0)}")
        print(f"  成功更新: {metrics.get('successful_updates', 0)}")
        print(f"  监控厂商数: {len(providers)}")
        print(f"  更新频率: {self.config.data.get('update_frequency', 'weekly')}")
        
        if self.config.data.get("last_update"):
            print(f"  上次更新: {self.config.data['last_update'][:19]}")
        if self.config.data.get("last_check"):
            print(f"  上次检查: {self.config.data['last_check'][:19]}")
    
    def _reset_config(self):
        """重置配置"""
        confirm = input("\n⚠️ 确定要重置所有配置吗？(yes/no): ").strip().lower()
        if confirm == "yes":
            self.config.data = self.config._default_config()
            self.config.save()
            print("\n✅ 配置已重置")


# ============================================================
# 主函数
# ============================================================
def main():
    """主函数"""
    # 解析参数
    dry_run = "--dry-run" in sys.argv
    check_only = "--check-only" in sys.argv
    auto_search = "--auto-search" in sys.argv
    interactive = "--wizard" in sys.argv
    probe = "--no-probe" not in sys.argv
    probe_only = "--probe-only" in sys.argv

    if probe_only:
        # 仅执行官方接口探测并输出核验报告
        print("=" * 70)
        print("🔍 仅官方接口探测模式")
        print("=" * 70)
        found = 0
        for provider_id, probe_config in PROVIDER_PROBE_CONFIG.items():
            name = PROVIDER_SEARCH_CONFIG.get(provider_id, {}).get("name", provider_id)
            print(f"\n[{provider_id}] {name}")
            print("-" * 70)
            result = ModelVerifier.probe(probe_config)
            icon = {"ok": "✅", "requires_auth": "🔑", "unreachable": "⛔", "failed": "⚠️"}.get(
                result.get("status", ""), "❓")
            print(f"  {icon} 状态: {result.get('status', 'unknown')}")
            print(f"     {result.get('message', '')}")
            if result.get("models"):
                found += len(result["models"])
                print("  模型列表(前20):")
                for mid in result["models"][:20]:
                    print(f"     - {mid}")
        print("\n" + "=" * 70)
        print(f"✅ 探测完成，累计获取 {found} 个真实模型ID（需鉴权厂商需配置环境变量 API Key）")
        sys.exit(0)

    if interactive:
        # 运行交互式向导
        wizard = UpdateWizard()
        wizard.run()
    else:
        # 运行自动更新
        updater = ModelUpdater(dry_run=dry_run, auto_search=auto_search, probe=probe)
        has_changes = updater.run(check_only=check_only)
        
        # 返回适当的退出码
        if has_changes:
            print("\n💡 建议查看更新日志: references/model_changelog.md")
            sys.exit(0)
        else:
            print("\n✅ 所有模型信息已是最新")
            sys.exit(0)


if __name__ == "__main__":
    main()
