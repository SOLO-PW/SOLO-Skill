#!/usr/bin/env python3
"""
从 references/templates.json 重新生成 references/templates.md

用法：python3 scripts/sync_templates.py

templates.json 是机器可读的单一数据源，templates.md 由本脚本派生生成为
人类可读的模板库，保证两者内容一致、避免双份维护失同步。
"""
import json
from collections import OrderedDict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
JSON_PATH = ROOT_DIR / "references" / "templates.json"
MD_PATH = ROOT_DIR / "references" / "templates.md"

# 废话文学类型中文映射（与 generator.py 保持一致）
TYPE_CN = {
    "synonym_repeat": "同义反复型",
    "time_loop": "时间循环型",
    "conditional": "条件假设型",
    "unit_conversion": "单位转换型",
    "obvious": "众所周知型",
    "leader_speech": "领导讲话型",
    "reversal": "逆转型",
    "assumption": "假设型",
    "follow_up": "顺接型",
    "rhyme": "押韵型",
    "long_sentence": "长句式型",
    "contradiction": "前后矛盾型",
    "literature": "文学改编型",
    "hope": "美好希望型",
    "redundancy": "冗余信息型",
}


def main() -> None:
    """读取 JSON 并按类型分组生成 templates.md"""
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    # 按类型分组，保持 JSON 中出现的顺序
    grouped = OrderedDict()
    for item in data["templates"]:
        grouped.setdefault(item["type"], []).append(item)

    lines = ["# 废话文学模板库", ""]
    lines.append("> 本文件由 `scripts/sync_templates.py` 从 `references/templates.json` 自动生成，请勿手动编辑。")
    lines.append("")

    for ttype, tpls in grouped.items():
        lines.append(f"## {TYPE_CN.get(ttype, ttype)}")
        lines.append("")
        for tpl in tpls:
            lines.append(f"- {tpl['template']}")
            for example in tpl.get("examples", []):
                lines.append(f"  - 示例：{example}")
        lines.append("")

    lines.append("## 场景关键词映射")
    lines.append("")
    for scene, types in data.get("scene_keywords", {}).items():
        cn = "、".join(TYPE_CN.get(t, t) for t in types)
        lines.append(f"- {scene}：{cn}")
    lines.append("")

    MD_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"已生成：{MD_PATH}")


if __name__ == "__main__":
    main()