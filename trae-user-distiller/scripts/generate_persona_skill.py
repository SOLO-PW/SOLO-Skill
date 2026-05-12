#!/usr/bin/env python3
"""
个性化用户技能生成器 v3

根据提取的用户数据生成模仿该用户的标准化 SKILL.md 技能文档。
输出结构符合 skill-creator 最佳实践（progressive disclosure）。
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

MIN_TOTAL_ITEMS = 3
MIN_TOTAL_CHARS = 200


class PersonaSkillGenerator:
    """个性化技能生成器"""

    def __init__(self, user_data_path: str, output_dir: str = None):
        self.user_data_path = Path(user_data_path)
        self.output_dir = Path(output_dir) if output_dir else self.user_data_path.parent
        self.user_data: dict = {}
        self.username: str = ""
        self.skill_name: str = ""

    def load_and_validate(self) -> bool:
        """加载并验证用户数据"""
        if not self.user_data_path.exists():
            print(f"错误: 数据文件不存在: {self.user_data_path}")
            return False

        try:
            with open(self.user_data_path, "r", encoding="utf-8") as f:
                self.user_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"错误: JSON 解析失败: {e}")
            return False

        required_keys = {"username", "profile", "topics", "posts", "stats", "style_analysis"}
        missing = required_keys - set(self.user_data.keys())
        if missing:
            print(f"错误: 数据缺少必要字段: {missing}")
            return False

        self.username = self.user_data["username"]
        normalized = re.sub(r"[^a-zA-Z0-9]+", "-", self.username).strip("-").lower()
        self.skill_name = f"trae-{normalized}" if normalized else "trae-unknown"

        stats = self.user_data.get("stats", {})
        total_items = stats.get("total_topics", 0) + stats.get("total_posts", 0)
        total_chars = self.user_data.get("style_analysis", {}).get("total_chars", 0)

        if total_items < MIN_TOTAL_ITEMS:
            print(f"错误: 数据量不足（{total_items} 条，需 ≥{MIN_TOTAL_ITEMS}）")
            return False
        if total_chars < MIN_TOTAL_CHARS:
            print(f"错误: 文本量不足（{total_chars} 字，需 ≥{MIN_TOTAL_CHARS}）")
            return False

        print(f"  ✓ 验证通过: {total_items} 条, {total_chars} 字")
        return True

    # ─── 特征提取 ───

    def _build_negative_instructions(self) -> list[str]:
        """基于风格数据生成负面指令，防止 LLM 过度模仿"""
        style = self.user_data.get("style_analysis", {})
        scene = style.get("scene_analysis", {})
        instructions: list[str] = []

        # 表情使用
        emoji_rate = style.get("emoji_rate", 0)
        emoji_count = style.get("emoji_count", 0)
        if emoji_count == 0:
            instructions.append("不要使用任何表情符号")
        elif emoji_rate < 0.1:
            instructions.append("不要频繁使用表情符号，该用户几乎不用")

        # 正式度
        formal_score = style.get("formal_score", 0.5)
        if formal_score > 0.7:
            instructions.append("不要使用网络用语（如 yyds、666、绝了）或过度口语化表达")
        elif formal_score < 0.3:
            instructions.append("不要使用过于正式的书面语或学术化措辞")

        # 句长
        avg_sent = style.get("avg_sentence_length", 0)
        if avg_sent > 30:
            instructions.append("不要用过于简短的碎片化回复（如单句\"好的\"\"是的\"）")
        elif avg_sent < 10 and avg_sent > 0:
            instructions.append("不要写过于冗长的段落，保持简短")

        # 语气词
        particle_counts = style.get("particle_counts", {})
        all_particles = {"啊", "呢", "吧", "吗", "嘛", "哦", "哈", "嘿", "嘻", "呀", "啦", "哎", "嗯", "噢"}
        unused_particles = [p for p in all_particles if particle_counts.get(p, 0) == 0]
        if len(unused_particles) > 8:
            # 用户几乎不用语气词
            instructions.append("不要添加语气词（啊、呢、吧、吗等），该用户表达直接")
        elif len(unused_particles) > 3:
            top_unused = [p for p in unused_particles[:5]]
            instructions.append(f"不要使用 {'、'.join(top_unused)} 等该用户不常用的语气词")

        # 标点
        punct = style.get("punct_ratios", {})
        if punct.get("exclamation", 0) < 0.05:
            instructions.append("不要频繁使用感叹号")
        if punct.get("ellipsis", 0) < 0.02:
            instructions.append("不要使用省略号")
        if punct.get("question", 0) < 0.03:
            instructions.append("不要频繁使用反问句式")

        # Markdown
        md = style.get("markdown_habits", {})
        if not md.get("uses_code_blocks"):
            instructions.append("不要在回复中使用代码块")
        if not md.get("uses_lists"):
            instructions.append("不要使用 Markdown 列表格式")

        # 分场景差异
        topic_style = scene.get("topic_style", {})
        reply_style = scene.get("reply_style", {})
        if topic_style and reply_style:
            t_formal = topic_style.get("avg_formal_score", 0.5)
            r_formal = reply_style.get("avg_formal_score", 0.5)
            if abs(t_formal - r_formal) > 0.2:
                if t_formal > r_formal:
                    instructions.append("主动发帖时保持正式严谨，回复他人时可更口语化")
                else:
                    instructions.append("回复他人时保持简洁直接，主动发帖时可更展开")

        return instructions

    def _build_persona_profile(self) -> str:
        """构建人格定义（直接作为指令，不放在代码块中）"""
        style = self.user_data.get("style_analysis", {})
        profile = self.user_data.get("profile", {})
        stats = self.user_data.get("stats", {})
        expression = style.get("expression", {})
        length_dist = style.get("length_distribution", {})
        markdown = style.get("markdown_habits", {})
        punct = style.get("punct_ratios", {})
        top_particles = style.get("top_particles", [])
        scene = style.get("scene_analysis", {})

        formality = style.get("formality", "neutral")
        formal_label = {"formal": "正式严谨", "casual": "轻松随意", "neutral": "自然平衡"}.get(formality, "自然平衡")
        formal_score = max(0.0, min(1.0, style.get("formal_score", 0.5)))

        lines = [
            f"你是 @{self.username} 的数字人格分身，基于其在 Trae 论坛的公开历史发言构建。",
            "",
            "## 核心身份",
            f"- 论坛用户: @{self.username}",
            f"- 信任等级: {profile.get('trust_level', 'unknown')}",
            f"- 注册时间: {profile.get('created_at', 'unknown')[:10]}",
            f"- 累计获赞: {stats.get('likes_received', 0)}",
            f"- 采纳答案: {stats.get('accepted_answers', 0)}",
            "",
            "## 语言风格",
            f"- 整体基调: {formal_label}（正式度 {formal_score:.0%}）",
            f"- 平均句长: {style.get('avg_sentence_length', 0):.0f} 字/句",
            f"- 表情使用: {'频繁' if style.get('emoji_rate', 0) > 0.3 else '偶尔' if style.get('emoji_count', 0) > 0 else '几乎不用'}",
        ]

        # 语气词
        if top_particles:
            top_3 = [p for p, c in top_particles[:3] if c > 0]
            if top_3:
                lines.append(f"- 常用语气词: {'、'.join(top_3)}")

        # 回复长度偏好
        if length_dist:
            short_r = length_dist.get("short_ratio", 0)
            long_r = length_dist.get("long_ratio", 0)
            if long_r > 0.5:
                lines.append("- 倾向写长回复，喜欢详细展开论述")
            elif short_r > 0.5:
                lines.append("- 倾向简短回复，言简意赅")
            else:
                lines.append("- 回复长度灵活，根据话题调整详略")

        # 标点习惯
        if punct:
            if punct.get("exclamation", 0) > 0.15:
                lines.append("- 常用感叹号表达强烈情感")
            if punct.get("ellipsis", 0) > 0.05:
                lines.append("- 常用省略号，语气留有余韵")
            if punct.get("question", 0) > 0.1:
                lines.append("- 喜欢用反问和提问引导思考")

        # Markdown 习惯
        md_traits = []
        if markdown.get("uses_code_blocks"):
            md_traits.append("代码块")
        if markdown.get("uses_lists"):
            md_traits.append("列表")
        if markdown.get("uses_blockquote"):
            md_traits.append("引用")
        if markdown.get("uses_bold"):
            md_traits.append("加粗强调")
        if md_traits:
            lines.append(f"- 格式习惯: 善用{'、'.join(md_traits)}")

        # 表达风格
        if expression.get("examples_rate", 0) > 2:
            lines.append("- 善于通过举例说明观点")
        if expression.get("structure_rate", 0) > 2:
            lines.append("- 思维结构清晰，善用分点论述")
        if expression.get("humility_rate", 0) > 2:
            lines.append("- 表达谦逊，常用保留措辞")
        if expression.get("mentions", 0) > 3:
            lines.append("- 乐于互动，经常 @其他用户")

        # 关注领域
        interests = self._extract_interests()
        if interests:
            lines.extend(["", "## 关注领域"])
            for interest in interests[:8]:
                lines.append(f"- {interest}")

        # 回应原则和边界
        negative = self._build_negative_instructions()
        lines.extend([
            "",
            "## 回应原则",
            f"1. 保持与 @{self.username} 一致的语言风格和表达习惯",
            "2. 在相关领域展现专业性和实际经验",
            "3. 回应真诚有见地，不敷衍不套话",
            "4. 适当使用其常用的语气词和标点习惯",
            "5. 不确定时坦诚表达，不编造该用户的具体经历",
        ])

        # 分场景风格差异
        topic_style = scene.get("topic_style", {})
        reply_style = scene.get("reply_style", {})
        if topic_style and reply_style:
            t_formal = topic_style.get("avg_formal_score", 0.5)
            r_formal = reply_style.get("avg_formal_score", 0.5)
            t_sent = topic_style.get("avg_sentence_length", 0)
            r_sent = reply_style.get("avg_sentence_length", 0)
            lines.extend([
                "",
                "## 场景差异",
                f"- 主动发帖（{topic_style.get('sample_count', 0)} 篇）: "
                f"正式度 {t_formal:.0%}，平均句长 {t_sent:.0f} 字",
                f"- 回复他人（{reply_style.get('sample_count', 0)} 条）: "
                f"正式度 {r_formal:.0%}，平均句长 {r_sent:.0f} 字",
            ])
            if abs(t_formal - r_formal) > 0.15:
                if t_formal > r_formal:
                    lines.append("- 发帖更正式结构化，回复更口语直接")
                else:
                    lines.append("- 发帖更轻松随意，回复更严谨认真")

        # 负面指令
        if negative:
            lines.extend(["", "## 风格禁忌"])
            for i, neg in enumerate(negative, 1):
                lines.append(f"{i}. {neg}")

        lines.extend([
            "",
            "## 边界",
            "- 你是基于历史公开数据模拟的数字分身，不是用户本人",
            "- 超出历史范围的问题，用常识回答但保持其风格",
            "- 避免过度模仿导致不自然，保持对话流畅性",
        ])

        return "\n".join(lines)

    def _extract_interests(self) -> List[str]:
        """提取用户关注领域"""
        interests: List[str] = []

        categories = set()
        for topic in self.user_data.get("topics", []):
            cat = topic.get("category_name", "")
            if cat and not cat.startswith("分类#"):
                categories.add(cat)
        interests.extend(sorted(categories))

        tags: Dict[str, int] = {}
        for topic in self.user_data.get("topics", []):
            for tag in topic.get("tags", []):
                if tag:
                    tags[tag] = tags.get(tag, 0) + 1
        top_tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)[:5]
        interests.extend([f"#{tag}" for tag, _ in top_tags])

        return interests

    def _pick_conversation_examples(self) -> List[Dict[str, str]]:
        """从真实数据中挑选对话示例（确定性输出）"""
        examples: List[Dict[str, str]] = []

        for i, topic in enumerate(self.user_data.get("topics", [])):
            title = topic.get("title", "")
            content = topic.get("content_clean", "")
            if title and content and len(content) > 30:
                # 确定性选择：基于索引交替
                q = f"能详细说说关于「{title}」的看法吗？" if i % 2 == 0 else f"你对「{title}」这个问题是怎么理解的？"
                excerpt = content[:400] + ("..." if len(content) > 400 else "")
                examples.append({"user": q, "assistant": excerpt})
                if len(examples) >= 3:
                    break

        for post in self.user_data.get("posts", []):
            content = post.get("content_clean", "")
            topic_title = post.get("topic_title", "")
            if len(content) > 20:
                q = f"关于「{topic_title}」，你有什么补充吗？" if topic_title else "对这个话题你有什么想法？"
                excerpt = content[:300] + ("..." if len(content) > 300 else "")
                examples.append({"user": q, "assistant": excerpt})
                if len(examples) >= 6:
                    break

        return examples

    # ─── SKILL.md 生成（progressive disclosure）──

    def generate_skill_md(self) -> str:
        """生成标准 SKILL.md（顶层精简，详细数据放 references）"""
        stats = self.user_data.get("stats", {})
        examples = self._pick_conversation_examples()
        persona_prompt = self._build_persona_profile()

        # description: 简洁 1 句
        desc = f"@{self.username} 的数字人格分身，基于 Trae 论坛公开发言数据构建。"

        parts: List[str] = []

        # Frontmatter - YAML格式，description用引号包裹防止特殊字符解析失败
        parts.append(f'---\nname: {self.skill_name}\ndescription: "{desc}"\n---')

        # 标题 + 一句话概述
        parts.append(f"# @{self.username} 的数字人格")
        parts.append("")
        parts.append(f"基于 Trae 论坛 {stats.get('total_topics', 0)} 个话题、"
                      f"{stats.get('total_posts', 0)} 条回复的公开数据构建。"
                      f"累计获赞 {stats.get('likes_received', 0)}，"
                      f"采纳答案 {stats.get('accepted_answers', 0)} 个。")

        # 人格定义（核心指令，直接作为文本）
        parts.append("")
        parts.append(persona_prompt)

        # 对话示例
        if examples:
            parts.append("")
            parts.append("## 对话示例")
            for i, ex in enumerate(examples[:5], 1):
                parts.append("")
                parts.append(f"**Q{i}:** {ex['user']}")
                parts.append("")
                parts.append(f"{ex['assistant']}")

        # 引用详细数据（progressive disclosure）
        parts.append("")
        parts.append("## 参考数据")
        parts.append("")
        parts.append("- 完整历史发言: [conversation_history.md](references/conversation_history.md)")
        parts.append("- 原始提取数据: [user_data.json](user_data.json)")
        parts.append("- 高频词汇和风格统计见 `user_data.json` 中的 `style_analysis` 字段")

        # 页脚
        parts.append("")
        parts.append("---")
        parts.append(f"*trae-user-distiller v3 · {self.user_data.get('extracted_at', '')[:10]}*")

        return "\n".join(parts)

    # ─── references 文档 ───

    def generate_history_md(self) -> str:
        """生成完整历史记录文档"""
        parts: List[str] = []
        parts.append(f"# @{self.username} 的完整历史发言记录")
        parts.append("")
        parts.append(f"> 来源: {self.user_data.get('forum_url', '')} · "
                      f"提取: {self.user_data.get('extracted_at', '')[:10]}")
        parts.append("")

        topics = self.user_data.get("topics", [])
        posts = self.user_data.get("posts", [])

        if topics or posts:
            parts.append("## 目录")
            parts.append("")
            if topics:
                parts.append("- [发布的话题](#发布的话题)")
            if posts:
                parts.append("- [回复记录](#回复记录)")
            parts.append("")

        if topics:
            parts.append("## 发布的话题")
            parts.append("")
            for i, t in enumerate(topics, 1):
                parts.append(f"### {i}. {t.get('title', '无标题')}")
                parts.append("")
                meta = f"- 分类: {t.get('category_name', '未知')} · "
                meta += f"浏览: {t.get('views', 0)} · 回复: {t.get('reply_count', 0)} · 获赞: {t.get('like_count', 0)}"
                parts.append(meta)
                if t.get("tags"):
                    parts.append(f"- 标签: {', '.join(t['tags'])}")
                parts.append(f"- 时间: {t.get('created_at', '')[:10]} · "
                              f"{'原创首帖' if t.get('is_original') else '参与讨论'}")
                parts.append("")
                content = t.get("content_clean", "")
                if content:
                    parts.append(content)
                parts.append("\n---\n")

        if posts:
            parts.append("## 回复记录")
            parts.append("")
            for i, p in enumerate(posts, 1):
                parts.append(f"### 回复 {i}")
                parts.append("")
                if p.get("topic_title"):
                    parts.append(f"- 话题: {p['topic_title']}")
                parts.append(f"- 获赞: {p.get('like_count', 0)} · 阅读: {p.get('reads', 0)} · "
                              f"时间: {p.get('created_at', '')[:10] if p.get('created_at') else '未知'}")
                parts.append("")
                content = p.get("content_clean", "")
                if content:
                    parts.append(content)
                parts.append("\n---\n")

        return "\n".join(parts)

    # ─── 保存 ───

    def save(self) -> Path:
        """保存生成的技能包"""
        skill_dir = self.output_dir / self.skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)

        (skill_dir / "SKILL.md").write_text(self.generate_skill_md(), encoding="utf-8")
        (skill_dir / "user_data.json").write_text(
            json.dumps(self.user_data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        ref_dir = skill_dir / "references"
        ref_dir.mkdir(exist_ok=True)
        (ref_dir / "conversation_history.md").write_text(
            self.generate_history_md(), encoding="utf-8"
        )

        print(f"\n技能已生成: {skill_dir}")
        print(f"  ├── SKILL.md")
        print(f"  ├── user_data.json")
        print(f"  └── references/conversation_history.md")
        return skill_dir

    def generate(self) -> Optional[Path]:
        """执行完整的生成流程"""
        print("生成个性化技能...")
        print(f"  数据: {self.user_data_path}")

        if not self.load_and_validate():
            return None

        print(f"  用户: @{self.username} → {self.skill_name}")
        return self.save()


def main():
    parser = argparse.ArgumentParser(description="根据用户数据生成个性化技能")
    parser.add_argument("user_data", help="用户数据 JSON 文件路径")
    parser.add_argument("--output", "-o", default=".", help="输出目录")
    args = parser.parse_args()

    gen = PersonaSkillGenerator(args.user_data, args.output)
    if not gen.generate():
        sys.exit(1)


if __name__ == "__main__":
    main()
