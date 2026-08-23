#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_validate_examples.py — validate_examples.py 的单元测试。

覆盖点：
  - 合法 YAML 校验通过
  - 非法 YAML 校验报错（返回 fail，且不再命中 skip/pass）
  - 无语言 / 未知语言代码块被安全跳过（skip，不崩溃）

运行方式（二选一）：
  python3 -m unittest discover -s scripts/tests     # 从仓库根目录运行
  python3 scripts/tests/test_validate_examples.py   # 独立运行

说明：本文件通过 sys.path 将上级 scripts 目录加入导入路径，
以便直接 import validate_examples，两种运行方式均可正常工作。
"""

import os
import sys
import unittest

# 将 scripts 目录（本文件上一级）加入导入路径，使 validate_examples 可被导入
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import validate_examples as ve


class ExtractCodeBlocksTest(unittest.TestCase):
    """代码块提取逻辑测试。"""

    def test_extracts_language_and_line(self):
        text = "前文\n```yaml\nfoo: bar\n```\n后文"
        blocks = ve.extract_code_blocks(text)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0]["lang"], "yaml")
        self.assertEqual(blocks[0]["code"], "foo: bar\n")
        self.assertEqual(blocks[0]["line"], 2)

    def test_extracts_multiple_blocks_in_order(self):
        text = "```bash\necho hi\n```\n```nginx\nserver {}\n```"
        blocks = ve.extract_code_blocks(text)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0]["lang"], "bash")
        self.assertEqual(blocks[1]["lang"], "nginx")
        self.assertEqual(blocks[0]["line"], 1)
        self.assertEqual(blocks[1]["line"], 4)


class YAMLValidationTest(unittest.TestCase):
    """YAML 校验：合法通过、非法报错。"""

    def test_valid_yaml_passes(self):
        status, msg = ve.validate_block("yaml", "version: \"3.9\"\nservices:\n  app:\n    image: redis\n")
        self.assertEqual(status, "pass", msg)

    def test_invalid_yaml_fails(self):
        # 流式序列未闭合，属于非法 YAML，应返回 fail
        status, msg = ve.validate_block("yaml", "services:\n  app: [unclosed: [1,2\n")
        self.assertEqual(status, "fail", msg)

    def test_yml_alias_also_validated(self):
        status, _ = ve.validate_block("yml", "a: 1\nb:\n  - 2\n")
        self.assertEqual(status, "pass")

    def test_empty_yaml_fails(self):
        status, _ = ve.validate_block("yaml", "   \n")
        self.assertEqual(status, "fail")

    def test_multi_document_yaml_passes(self):
        # 多文档 YAML（多个 ---- 分隔，如 kubectl 资源清单）应整体通过
        multi = (
            "apiVersion: v1\nkind: ConfigMap\n---\n"
            "apiVersion: v1\nkind: Secret\n"
        )
        status, _ = ve.validate_block("yaml", multi)
        self.assertEqual(status, "pass")


class NoLanguageSkipTest(unittest.TestCase):
    """无语言 / 未知语言代码块应安全跳过，不崩溃、不误报为通过或失败。"""

    def test_no_language_skipped(self):
        status, _ = ve.validate_block("", "just some text with no syntax")
        self.assertEqual(status, "skip")

    def test_unknown_language_skipped(self):
        status, _ = ve.validate_block("swift", "let x = 1")
        self.assertEqual(status, "skip")

    def test_unknown_language_does_not_crash_in_text(self):
        text = "```txt\n任意内容\n```\n```\n无语言段落\n```"
        results, any_fail = ve.validate_text(text)
        statuses = [s for _, s, _ in results]
        # 两种情况都应是 skip，且整段文本不产生失败
        self.assertEqual(statuses, ["skip", "skip"])
        self.assertFalse(any_fail)

    def test_skip_blocks_do_not_mark_failure(self):
        # 一个合法 + 一个 skip，不应整体判为失败
        text = "```yaml\napiVersion: v1\n```\n```unknown\n{}[]\n```"
        _, any_fail = ve.validate_text(text)
        self.assertFalse(any_fail)


class DockerfileAndNginxValidationTest(unittest.TestCase):
    """Dockerfile / Nginx 基础完整性校验。"""

    def test_dockerfile_with_from_passes(self):
        status, _ = ve.validate_block("dockerfile", "# 注释\nFROM alpine:3.19\nCMD [\"/bin/sh\"]\n")
        self.assertEqual(status, "pass")

    def test_dockerfile_without_from_fails(self):
        status, _ = ve.validate_block("dockerfile", "RUN apt-get update\n")
        self.assertEqual(status, "fail")

    def test_nginx_balanced_braces_passes(self):
        status, _ = ve.validate_block("nginx", "server { listen 80; location / { proxy_pass http://x; } }\n")
        self.assertEqual(status, "pass")

    def test_nginx_unbalanced_braces_fails(self):
        status, _ = ve.validate_block("nginx", "server { listen 80;\n")
        self.assertEqual(status, "fail")

    def test_empty_nginx_fails(self):
        status, _ = ve.validate_block("nginx", "\n\n")
        self.assertEqual(status, "fail")


if __name__ == "__main__":
    unittest.main(verbosity=2)