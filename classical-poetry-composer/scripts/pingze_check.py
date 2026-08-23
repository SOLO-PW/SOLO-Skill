#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
平仄自动校检脚本 pingze_check.py
================================

以 `references/pingze-verification-manual.md` 为单一数据源，自动读取
「入声字表」（2.2）与「平水韵韵部表」（3.1/3.2），对诗词逐字标注平仄，
并进行结构（字数）、孤平、三平调、押韵等核查，减少手工逐字核对成本。

支持：
  - 逐字平仄标注：在入声表 → 仄；否则用 pypinyin 取现代读音（一二声→平、
    三四声→仄）；轻声/未知 → 标记为 ?
  - 结构检查：可指定统一字数（5/7 言）或每句字数序列（用于词牌）
  - 孤平检测、三平调检测
  - 押韵核查：按韵脚索引反查平水韵韵部，判定是否一致

pypinyin 为【可选】依赖。未安装时脚本仍可运行，仅基于入声表 + 结构/韵部
检查，无法判定的字标为 ?

用法示例：
  python scripts/pingze_check.py --lines "窗外雨声如诉" "独倚空庭谁顾" --chars 6 --韵脚 1 2 4
"""

import argparse
import os
import re

# 参考手册路径：脚本位于 scripts/ 下，手册位于上级 references/ 下
MANUAL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "references", "pingze-verification-manual.md",
)

# 中文字符（不包含标点）
_HAN = re.compile(r"[\u4e00-\u9fff]")
# 2.2 入声字表小节标题，如：#### 一屋韵（49字） / #### 常用补充（35字）
_RUSHENG_HEAD = re.compile(r"^####\s+")
# 入声字表行，如：> 屋木竹目服……
_CHAR_LINE = re.compile(r"^>\s*(.+)$")
# 平水韵韵部行，如：**一东**：东同铜…… / **去声七遇**：遇路露……
_YUNBU_HEAD = re.compile(r"^\*\*([^*]+?)\*\*[：:]\s*(.*)$")
# 韵部标注注解，如（窄韵）（极宽韵）
_PAREN = re.compile(r"[（(][^）)]*[）)]")

# pypinyin 为可选依赖，尽力导入；失败则 _PY 置为 False
try:
    from pypinyin import Style, pinyin
    _PY = True
except ImportError:
    _PY = False


def _han_chars(text):
    """从文本中抽取所有汉字（用于字数统计与韵脚字提取）。"""
    return _HAN.findall(text)


def load_rusheng():
    """
    从手册 2.2 节解析入声字表，返回入声字集合。
    保持位字符（2.2 按韵部排列 + 常用补充）全部汇总为一个集合。
    """
    rusheng = set()
    if not os.path.exists(MANUAL_PATH):
        return rusheng
    with open(MANUAL_PATH, encoding="utf-8") as f:
        lines = f.read().splitlines()
    in_section = False
    for line in lines:
        if re.match(r"^##\s*二、", line):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            # 进入下一顶层小节，结束 2.2 解析
            in_section = False
        # 仅收集入声字表小节的 > 行
        if in_section and _RUSHENG_HEAD.match(line):
            continue  # 小节标题本身不含字
        m = _CHAR_LINE.match(line)
        if in_section and m:
            rusheng.update(_han_chars(_PAREN.sub("", m.group(1))))
    return rusheng


def load_yunbu():
    """
    从手册 3.1 / 3.2 解析平水韵韵部表，返回 {字: {韵部名,...}}。
    一个汉字可能出现在多个韵部中。
    """
    yunbu = {}
    if not os.path.exists(MANUAL_PATH):
        return yunbu
    with open(MANUAL_PATH, encoding="utf-8") as f:
        lines = f.read().splitlines()
    in_section = False
    for line in lines:
        if re.match(r"^##\s*三、", line):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            in_section = False
        if not in_section:
            continue
        m = _YUNBU_HEAD.match(line)
        if not m:
            continue
        name = m.group(1).strip()
        clean_chars = _han_chars(_PAREN.sub("", m.group(2)))
        for ch in clean_chars:
            yunbu.setdefault(ch, set()).add(name)
    return yunbu


def modern_tone(char):
    """取某个字现代读音的声调（1/2/3/4/5），无法确定则返回 None。"""
    if not _PY:
        return None
    try:
        # heteronym=False 取最常用读音；TONE3 使声调以数字结尾
        seg = pinyin(char, style=Style.TONE3, heteronym=False)[0][0]
    except Exception:
        return None
    m = re.search(r"([1-5])$", seg)
    return int(m.group(1)) if m else None


def tone_of(char, rusheng, use_pinyin=True):
    """
    判断单字平仄：
      在入声表 → 仄（无论现代读几声，最高优先级）
      否则按现代读音 → 一二声=平、三四声=仄
      轻声/未知 → ?
    """
    if char in rusheng:
        return "仄"
    if not use_pinyin:
        return "?"
    t = modern_tone(char)
    if t is None or t == 5:  # 5=轻声 → 平仄不明
        return "?"
    return "平" if t in (1, 2) else "仄"


def annotate_lines(lines, rusheng, use_pinyin=True):
    """逐句逐字标注平仄，返回每句的平仄列表。"""
    return [[tone_of(ch, rusheng, use_pinyin) for ch in _han_chars(line)]
            for line in lines]


def count_han(line):
    """统计一句中的汉字字数（去除标点）。"""
    return len(_han_chars(line))


def check_chars(lines, chars_spec, indent="  "):
    """
    结构/字数检查。chars_spec 为 int（统一字数）或 list（每句字数序列）。
    返回 (结果列表, 是否全部通过)。
    """
    reports, ok = [], True
    single_int = isinstance(chars_spec, int)
    for i, line in enumerate(lines):
        n = count_han(line)
        exp = chars_spec if single_int else chars_spec[i]
        match = n == exp
        ok = ok and match
        status = "错误" if not match else "通过"
        reports.append(
            f"{indent}第{i + 1}句：{n} 字（要求 {exp}）→ {'✅' if match else '❌ ' + status}")
    return reports, ok


def check_gubu(lines, tones):
    """
    孤平检测。按「平平仄仄平」句式（七言简化为后五字）判断：
      仄平仄仄平 → 孤平未救
      仄平平仄平 → 已拗救，合格
    存在 ? 的句子无法断定，跳过并提示。
    """
    reports = []
    for i, t in enumerate(tones):
        if len(t) < 5:
            continue
        tail = t[-5:]  # 五言即整句，七言取后五字
        if "?" in tail:
            reports.append(f"  第{i + 1}句：存在不明平仄（?），需人工复核孤平")
            continue
        if tail == ["仄", "平", "仄", "仄", "平"]:
            reports.append(f"  第{i + 1}句：❌ 孤平（{''.join(t)}，句中仅一个平声未救）")
        elif tail == ["仄", "平", "平", "仄", "平"]:
            reports.append(f"  第{i + 1}句：✅ 首字仄但已拗救，非孤平")
        else:
            reports.append(f"  第{i + 1}句：✅ 无孤平")
    return reports


def check_sanping(lines, tones):
    """三平调检测：句末三个字若全为平则不合格（入声按仄计）。"""
    reports = []
    for i, t in enumerate(tones):
        if len(t) < 3:
            reports.append(f"  第{i + 1}句：不足三字，跳过三平调检查")
            continue
        tail = t[-3:]
        if "?" in tail:
            reports.append(f"  第{i + 1}句：存在不明平仄（?），需人工复核三平调")
        elif tail == ["平", "平", "平"]:
            reports.append(f"  第{i + 1}句：❌ 三平调（句末三连平：{''.join(tail)}）")
        else:
            reports.append(f"  第{i + 1}句：✅ 无三平调")
    return reports


def last_han(line):
    """取一句的最后一个汉字（一般为韵脚字）。"""
    chars = _han_chars(line)
    return chars[-1] if chars else ""


def check_rhyme(lines, indices, yunbu, indent="  "):
    """
    押韵核查：对每个韵脚索引（1 起）取句末字，反查平水韵韵部，取交集判定一致与否。
    """
    reports = []
    chars_info = []  # [(行号, 末字, 韵部集合|None, 备注)]
    for idx in indices:
        if idx < 1 or idx > len(lines):
            reports.append(f"{indent}韵脚索引 {idx} 越界（共 {len(lines)} 句），忽略")
            chars_info.append((idx, "", None, "索引越界"))
            continue
        ch = last_han(lines[idx - 1])
        names = set(yunbu.get(ch, set()))
        if not names:
            reports.append(
                f"{indent}第{idx}句韵脚「{ch}」：⚠ 未在平水韵表中找到，待人工确认")
            chars_info.append((idx, ch, None, "未找到"))
        else:
            reports.append(
                f"{indent}第{idx}句韵脚「{ch}」→ {'/'.join(sorted(names))}")
            chars_info.append((idx, ch, names, ""))
    # 用非空韵部集合取交集
    valid = [info for info in chars_info if info[2]]
    if not valid:
        reports.append(f"{indent}判定：无法判定押韵（存在未收录韵脚），需人工复核")
    else:
        common = set(valid[0][2])
        for _, _, names, _ in valid[1:]:
            common &= names
        if common:
            reports.append(f"{indent}判定：✅ 押韵一致（共同韵部：{'/'.join(sorted(common))}）")
        else:
            reports.append(f"{indent}判定：❌ 押韵不一致（韵脚分属不同韵部）")
    return reports


def parse_chars_spec(chars_raw):
    """
    解析 --chars：单数字 → 统一字数（int）；逗号分隔 → 每句字数序列（list）。
    """
    if chars_raw is None:
        return None
    parts = [p.strip() for p in chars_raw.split(",") if p.strip()]
    if len(parts) == 1:
        return int(parts[0])
    return [int(p) for p in parts]


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="平仄自动校检：逐字标注 + 结构/孤平/三平调/押韵核查")
    parser.add_argument("--lines", nargs="+", required=True,
                        help="待核查的诗句（多句以空格分隔）")
    parser.add_argument("--chars", default=None,
                        help="每句字数：单数字（如 5/7）或逗号分隔序列（如 6,6,5,6,2,2,6）")
    parser.add_argument("--韵脚", dest="yun_jiao", type=int, nargs="*",
                        help="韵脚所在句子的行号（1 起），用于押韵核查，如 1 2 4")
    args = parser.parse_args(argv)

    lines = args.lines
    chars_spec = parse_chars_spec(args.chars)
    rusheng = load_rusheng()
    yunbu = load_yunbu()

    print("== 平仄自动校检 ==")
    print(f"数据源：{os.path.abspath(MANUAL_PATH)}")
    if not _PY:
        print("提示：未安装 pypinyin，现代读音无法判定，将仅基于入声表 + 结构/韵部检查运行")
    print(f"入声字个数：{len(rusheng)}；韵脚候选韵部：{len(yunbu)} 个不同字")

    # 逐字标注
    tones = annotate_lines(lines, rusheng, use_pinyin=_PY)
    print("\n【逐字平仄标注】")
    for i, line in enumerate(lines):
        chars = _han_chars(line)
        shown = "".join(ch for ch in chars)  # 汉字序列
        tone_str = "/".join(tones[i])
        print(f"  第{i + 1}句 {shown}  →  {tone_str}")

    # 字数检查
    print("\n【结构检查（字数）】")
    if chars_spec is None:
        print("  未指定 --chars，跳过字数检查")
    else:
        char_reports, ok = check_chars(lines, chars_spec)
        for r in char_reports:
            print(r)
        print(f"  结果：{'✅ 全部通过' if ok else '❌ 存在出律'}")

    # 孤平
    print("\n【孤平检测】")
    for r in check_gubu(lines, tones):
        print(r)

    # 三平调
    print("\n【三平调检测】")
    for r in check_sanping(lines, tones):
        print(r)

    # 押韵
    print("\n【押韵核查】")
    if not args.yun_jiao:
        print("  未指定 --韵脚，跳过押韵核查")
    else:
        for r in check_rhyme(lines, args.yun_jiao, yunbu):
            print(r)

    print("\n== 校检结束 ==")
    return 0


if __name__ == "__main__":
    main()