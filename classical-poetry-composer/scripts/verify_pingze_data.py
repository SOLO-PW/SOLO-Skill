#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
入声字表数据一致性校验脚本 verify_pingze_data.py
================================================

校验 `references/pingze-verification-manual.md` 中：
  第六节「入声字速查索引（按拼音排序）」中的每个字，
  是否都能在 2.2「按韵部排列的完整入声字表」中找到。

作用：便于维护 500+ 入声字表，找出速查索引与韵部表之间
的遗漏/不一致（例如索引新增了字但忘了同步到韵部表）。

用法：
  python scripts/verify_pingze_data.py
"""

import os
import re
import sys

# 复用 pingze_check 中基于同一参考手册的解析逻辑，保证一致
from pingze_check import MANUAL_PATH, _han_chars, load_rusheng

# 速查索引行，如：> 八 拔 白 百 柏……
_CHAR_LINE = re.compile(r"^>\s*(.+)$")


def load_index():
    """
    解析 2.2——第六节「入声字速查索引」中的全部字。
    对形如「恶（善恶）」「度（踱）」的条目取括号前的汉字。
    """
    chars = set()
    if not os.path.exists(MANUAL_PATH):
        return chars
    with open(MANUAL_PATH, encoding="utf-8") as f:
        lines = f.read().splitlines()
    started = False
    for line in lines:
        if re.match(r"^##\s*六、", line):
            started = True
            continue
        if started and line.startswith("## "):
            started = False  # 已离开第六节
        if not started:
            continue
        m = _CHAR_LINE.match(line)
        if not m:
            continue
        for tok in m.group(1).split():
            # 去掉括号注解后提取汉字
            chars.update(_han_chars(tok.split("（")[0]))
    return chars


def main():
    print("== 入声字表数据一致性校验 ==")
    print(f"数据源：{os.path.abspath(MANUAL_PATH)}")
    rusheng = load_rusheng()
    index = load_index()
    print(f"2.2 韵部表入声字：{len(rusheng)} 个")
    print(f"六、拼音速查索引：{len(index)} 个")

    # 索引中出现但韵部表 2.2 中不存在 → 应补充到 2.2
    missing_in_table = index - rusheng
    # 韵部表中有但速查索引未收录 → 建议同步到索引（非阻塞信息）
    missing_in_index = rusheng - index

    if missing_in_table:
        print("\n⚠ 以下字在【拼音速查索引（六）】中出现，但【2.2 韵部表】中未找到，"
              "请补充到对应韵部：")
        for ch in sorted(missing_in_table):
            print(f"  - {ch}")
    else:
        print("\n✅ 速查索引（六）中的字均能在 2.2 韵部表中找到。")

    print("\n⚠ 以下字在【2.2 韵部表】中，但【拼音速查索引（六）】未收录（可选同步）：")
    if missing_in_index:
        for ch in sorted(missing_in_index):
            print(f"  - {ch}")
    else:
        print("  （无）")

    ok = not missing_in_table
    print(f"\n== 校验结果：{'通过 ✅' if ok else '存在遗漏 ⚠'} ==")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())