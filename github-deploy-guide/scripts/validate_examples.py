#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_examples.py — 校验 references/deploy-examples.md 中的代码块示例。

background:
    该文档内含 Dockerfile / Nginx / K8s / YAML 等配置示例，易在编辑时产生错误产物。
    本脚本提取其中的代码块，并按语言做基础校验：
      - YAML  ：用 pyyaml 解析（可选依赖）；若未安装 pyyaml 则优雅降级，仅做非空与基础括号检查。
      - Dockerfile：非空、含 FROM 关键指令、方括号/引号配对。
      - Nginx / bash/shell：非空、花括号/引号配对等基础完整性。
      - 无语言 / 未知语言：安全跳过，仅给出提示，不崩溃。

用法：
    python3 validate_examples.py [path/to/deploy-examples.md]
    默认读取本脚本同级上一级 references/deploy-examples.md。

退出码：
    0  = 所有代码块均通过（或被安全跳过 / 优雅降级）
    1  = 存在校验失败的代码块（可用于 CI 门禁）

单测：scripts/tests/test_validate_examples.py（可用
      python3 -m unittest discover -s scripts/tests  或
      python3 scripts/tests/test_validate_examples.py 独立运行）。
"""

import os
import re
import sys

# 若 pyyaml 可用则启用 YAML 解析，否则标记不可用（优雅降级）。
try:
    import yaml
    HAS_YAML = True
except ImportError:  # pragma: no cover - 取决于运行环境是否安装 pyyaml
    HAS_YAML = False


# 默认目标文件：scripts/../references/deploy-examples.md
DEFAULT_EXAMPLES = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 os.pardir, "references", "deploy-examples.md")
)


# 允许用于解析的语言别名
YAML_LANGS = {"yaml", "yml"}
DOCKERFILE_LANGS = {"dockerfile", "docker"}
SHELL_LANGS = {"bash", "sh", "shell", "console"}


def extract_code_blocks(markdown_text):
    """提取 markdown 中的 ```lang ... ``` 代码块。

    返回值：list of dict，每项含字段：
        index   代码块序号（从 1 开始）
        lang    语言标记（可能为空字符串，表示无语言标注）
        code    代码块内容（不含首尾 ``` ）
        line    代码块在 markdown 中起始的行号（用于错误定位）
    """
    blocks = []
    # 非贪婪匹配 ```lang\n...\n``` ；语言标记支持 [\w-]+
    pattern = re.compile(r"```([\w\-]*)\n(.*?)```", re.DOTALL)
    for index, match in enumerate(pattern.finditer(markdown_text), start=1):
        lang = match.group(1).strip()
        code = match.group(2)
        # 起始行号 = 该段文本之前已有的换行数 + 1
        line = markdown_text.count("\n", 0, match.start()) + 1
        blocks.append({
            "index": index,
            "lang": lang,
            "code": code,
            "line": line,
        })
    return blocks


def _balance_ok(text, open_ch, close_ch):
    """忽略注释/字符串后进行的基础配对检查（粗略但足够提示编辑错误）。"""
    return text.count(open_ch) == text.count(close_ch)


def _quote_ok(text):
    """检验成对引号：统计未转义的单双引号是否各自成对。"""
    def _count(char):
        # 去掉被反斜杠转义的引号后再统计
        return len(re.findall(r"(?<!\\)" + re.escape(char), text))
    return _count('"') % 2 == 0 and _count("'") % 2 == 0


def _validate_yaml(code):
    """YAML 校验：优先 pyyaml，未安装时降级为浅层检查。"""
    stripped = code.strip()
    if not stripped:
        return ("fail", "YAML 代码块为空")
    if HAS_YAML:
        # 使用 safe_load_all 以支持多文档 YAML（例如一份文件包含多个
        # 用 --- 分隔的资源清单，kubectl apply -f 允许这种写法）。
        try:
            docs = list(yaml.safe_load_all(stripped))
            # 空文档（仅注释/纯 ### 分隔）会被解析为 None，不参与计数
            real_docs = [d for d in docs if d is not None]
            if not real_docs:
                return ("fail", "YAML 解析成功但内容为空")
            return ("pass", f"YAML 解析成功（{len(real_docs)} 个文档）")
        except yaml.YAMLError as exc:
            # pyyaml 会给出具体的行列信息，尽量提取用于定位
            loc = ""
            mark = getattr(exc, "problem_mark", None)
            if mark is not None:
                loc = f"（行 {mark.line + 1}, 列 {mark.column + 1}）"
            problem = getattr(exc, "problem", "") or str(exc)
            return ("fail", f"YAML 解析失败{loc}：{problem}".strip())
    # 未安装 pyyaml：降级，仅做非空与括号（花/方）/引号基础检查
    balanced = (
        _balance_ok(stripped, "{", "}")
        and _balance_ok(stripped, "[", "]")
        and _quote_ok(stripped)
    )
    if balanced:
        return ("pass", "未安装 pyyaml，已降级为浅层检查并通过")
    return ("fail", "未安装 pyyaml，浅层检查发现括号或引号不配对")


def _validate_dockerfile(code):
    """Dockerfile 校验：必须有 FROM，且括号/引号配对。"""
    stripped = code.strip()
    if not stripped:
        return ("fail", "Dockerfile 代码块为空")
    if not re.search(r"^\s*FROM\s+\S+", stripped, re.MULTILINE):
        return ("fail", "缺少必要指令 FROM")
    if not (_balance_ok(stripped, "[", "]") and _quote_ok(stripped)):
        return ("fail", "方括号或引号不配对")
    # 校验带 [] 的指令（如 CMD ["python", "app.py"]）大括号可选，不强求
    return ("pass", "包含 FROM，方括号/引号配对")


def _validate_nginx(code):
    """Nginx 校验：花括号必须配对，且非空。"""
    stripped = code.strip()
    if not stripped:
        return ("fail", "Nginx 代码块为空")
    if not _balance_ok(stripped, "{", "}"):
        return ("fail", "花括号不配对")
    if not _quote_ok(stripped):
        return ("fail", "引号不配对")
    return ("pass", "花括号/引号配对")


def _validate_shell(code):
    """shell 校验：非空，且常见括号/引号配对。"""
    stripped = code.strip()
    if not stripped:
        return ("fail", "shell 代码块为空")
    checks = [
        _balance_ok(stripped, "(", ")"),
        _balance_ok(stripped, "[", "]"),
        _balance_ok(stripped, "{", "}"),
    ]
    if not all(checks):
        return ("fail", "小括号 / 中括号 / 花括号存在不配对")
    if not _quote_ok(stripped):
        return ("fail", "引号不配对")
    return ("pass", "括号/引号配对")


def validate_block(lang, code):
    """按语言校验单个代码块。

    返回 (status, message)：
      "pass"  校验通过
      "skip"  无语言 / 未知语言，安全跳过
      "fail"  校验失败（附定位信息）
    """
    normalized = lang.lower()
    if normalized in YAML_LANGS:
        return _validate_yaml(code)
    if normalized in DOCKERFILE_LANGS:
        return _validate_dockerfile(code)
    if normalized in SHELL_LANGS:
        return _validate_shell(code)
    if normalized in {"nginx", "conf"}:
        return _validate_nginx(code)
    if not normalized:
        return ("skip", "无语言标注，跳过校验（无法确认格式）")
    return ("skip", f"未知语言「{lang}」，跳过校验")


def format_block_summary(block, status, message):
    """把单个代码块的校验结论格式化为一行，便于阅读与定位。"""
    head = f"[代码块 {block['index']:>2} | {block['lang'] or '无语言':<10}| 第 {block['line']} 行]"
    marks = {"pass": "✔ 通过：", "skip": "⚠ 跳过：", "fail": "✘ 失败："}
    return f"{head} {marks[status]}{message}"


def validate_text(markdown_text):
    """校验 markdown 文本中的所有代码块，返回 (结果列表, 是否有失败)。"""
    results = []
    any_fail = False
    for block in extract_code_blocks(markdown_text):
        status, message = validate_block(block["lang"], block["code"])
        results.append((block, status, message))
        if status == "fail":
            any_fail = True
    return results, any_fail


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    target = argv[0] if argv else DEFAULT_EXAMPLES

    if not os.path.isfile(target):
        print(f"文件不存在：{target}")
        return 1

    with open(target, "r", encoding="utf-8") as fh:
        text = fh.read()

    blocks = extract_code_blocks(text)
    print(f"共提取 {len(blocks)} 个代码块，目标文件：{target}")
    if not HAS_YAML:
        print("提示：未安装 pyyaml，YAML 代码块将降级为浅层检查（可用 pip install pyyaml 启用完整解析）。")

    results, any_fail = validate_text(text)
    for block, status, message in results:
        print(format_block_summary(block, status, message))

    passed = sum(1 for _, s, _ in results if s == "pass")
    skipped = sum(1 for _, s, _ in results if s == "skip")
    failed = sum(1 for _, s, _ in results if s == "fail")

    print(f"\n结果：通过 {passed}，跳过 {skipped}，失败 {failed}。")
    if any_fail:
        print("存在校验失败的示例，请检查上述 ✘ 项。")
        return 1
    print("全部可校验示例通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())