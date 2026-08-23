"""
Bilibili UP主分析报告生成器

生成包含数据图表的专业Markdown分析报告。
图表保存为独立PNG文件，通过相对路径引用。
"""

import os
from typing import Dict, List, Any, Optional
from datetime import datetime

# matplotlib 为可选依赖：缺失或 --no-charts 时降级为纯文本渲染，
# 避免在无绘图环境的机器上拉高启动成本。
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    _HAS_MATPLOTLIB = True
except Exception:  # pragma: no cover - 绘图环境缺失
    _HAS_MATPLOTLIB = False


def _text_sparkline(values: List[float], width: int = 14) -> str:
    """纯文本迷你柱状图，用于无图表环境下的趋势展示"""
    if not values:
        return ""
    vmax = max(values)
    if vmax <= 0:
        return "▁" * width
    bars = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
    scaled = [int(round(v / vmax * (len(bars) - 1))) for v in values]
    step = max(1, len(scaled) // width)
    downsample = scaled[::step][:width]
    return "".join(bars[i] for i in downsample)


class ReportGenerator:
    """报告生成器"""

    def __init__(self, output_dir: str = "./reports"):
        self.output_dir = output_dir
        self.chart_dir = os.path.join(output_dir, "charts")
        os.makedirs(self.chart_dir, exist_ok=True)
        self._setup_chinese_font()

    def _setup_chinese_font(self):
        """配置中文字体"""
        if not _HAS_MATPLOTLIB:
            return
        for font_name in ['SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei', 'Noto Sans CJK SC']:
            try:
                plt.rcParams['font.sans-serif'] = [font_name] + plt.rcParams['font.sans-serif']
                plt.rcParams['axes.unicode_minus'] = False
                break
            except Exception:
                continue

    def _save_chart(self, fig, filename: str) -> Optional[str]:
        """保存图表为PNG文件，返回相对路径"""
        try:
            filepath = os.path.join(self.chart_dir, filename)
            plt.tight_layout()
            fig.savefig(filepath, format='png', dpi=120, bbox_inches='tight',
                        facecolor='white', edgecolor='none')
            plt.close(fig)
            return f"charts/{filename}"
        except Exception:
            plt.close(fig)
            return None

    def _create_pie_chart(self, data: List[Dict], title: str,
                          name_key: str = "name", value_key: str = "value",
                          filename: str = "chart.png") -> Optional[str]:
        """创建饼图并保存为文件"""
        if not _HAS_MATPLOTLIB:
            return None
        fig, ax = plt.subplots(figsize=(7, 5))
        labels = [item[name_key] for item in data]
        sizes = [item[value_key] for item in data]

        if len(labels) > 8:
            sorted_data = sorted(zip(labels, sizes), key=lambda x: x[1], reverse=True)
            labels = [x[0] for x in sorted_data[:7]] + ["其他"]
            sizes = [x[1] for x in sorted_data[:7]] + [sum(x[1] for x in sorted_data[7:])]

        colors = plt.cm.Set3(range(len(labels)))
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, autopct='%1.1f%%',
            colors=colors, startangle=90, pctdistance=0.75
        )
        ax.set_title(title, fontsize=13, fontweight='bold', pad=12)
        for t in texts:
            t.set_fontsize(9)
        for t in autotexts:
            t.set_fontsize(8)
            t.set_color('white')
            t.set_fontweight('bold')
        return self._save_chart(fig, filename)

    def _create_radar_chart(self, dimensions: List[str], values: List[float],
                            title: str, filename: str = "radar.png") -> Optional[str]:
        """创建雷达图并保存为文件"""
        if not _HAS_MATPLOTLIB:
            return None
        n = len(dimensions)
        angles = [i / n * 2 * 3.14159265 for i in range(n)]
        values_closed = values + [values[0]]
        angles_closed = angles + angles[:1]

        fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(projection='polar'))
        ax.plot(angles_closed, values_closed, 'o-', linewidth=2, color='#4C72B0')
        ax.fill(angles_closed, values_closed, alpha=0.2, color='#4C72B0')
        ax.set_xticks(angles)
        ax.set_xticklabels(dimensions, fontsize=10)
        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=7)
        ax.grid(True, alpha=0.3)
        ax.set_title(title, fontsize=13, fontweight='bold', pad=20)
        return self._save_chart(fig, filename)

    def _create_line_chart(self, data: Dict[str, int], title: str,
                           xlabel: str = "", ylabel: str = "",
                           filename: str = "trend.png") -> Optional[str]:
        """创建折线图并保存为文件"""
        if not _HAS_MATPLOTLIB:
            return None
        fig, ax = plt.subplots(figsize=(10, 4.5))
        sorted_items = sorted(data.items())
        x_labels = [item[0] for item in sorted_items]
        y_values = [item[1] for item in sorted_items]

        ax.plot(range(len(x_labels)), y_values, marker='o', linewidth=1.8,
                markersize=5, color='#2ca02c')
        ax.fill_between(range(len(x_labels)), y_values, alpha=0.1, color='#2ca02c')
        ax.set_xticks(range(len(x_labels)))
        ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=8)
        ax.set_xlabel(xlabel, fontsize=10)
        ax.set_ylabel(ylabel, fontsize=10)
        ax.set_title(title, fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.2)
        return self._save_chart(fig, filename)

    def _fmt(self, num) -> str:
        """格式化数字"""
        if not isinstance(num, (int, float)):
            return str(num)
        if num >= 100000000:
            return f"{num/100000000:.2f}亿"
        elif num >= 10000:
            return f"{num/10000:.2f}万"
        else:
            return f"{num:,}"

    def _score_bar(self, score: float) -> str:
        """生成分数进度条（纯文本）"""
        filled = int(score / 5)
        empty = 20 - filled
        return "`" + "█" * filled + "░" * empty + f"` {score}"

    def generate_report(
        self,
        up_info: Dict[str, Any],
        videos: List[Dict[str, Any]],
        partition_analysis: Dict[str, Any],
        type_analysis: Dict[str, Any],
        interaction_metrics: Dict[str, Any],
        trend_analysis: Dict[str, Any],
        top_videos: List[Dict[str, Any]],
        content_pattern: Dict[str, Any],
        score_result: Any,
        persona: Any = None,
        enable_charts: bool = True
    ) -> str:
        """生成完整的分析报告"""
        L = []  # report lines

        # ==================== 标题区 ====================
        L.append(f"# Bilibili UP主分析报告")
        L.append("")
        L.append(f"> **分析对象**: {up_info.get('name', '未知')}  ")
        L.append(f"> **分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  ")
        L.append(f"> **分析视频数**: {len(videos)} 个")
        L.append("")
        L.append("---")
        L.append("")

        # ==================== 一、分析摘要 ====================
        L.append("## 一、分析摘要")
        L.append("")

        # 评分卡片
        grade = score_result.grade
        L.append(f"| 综合评分 | 等级 | 评价 |")
        L.append(f"|:--------:|:----:|------|")
        L.append(f"| **{score_result.total_score}** | **{grade}** | {score_result.summary} |")
        L.append("")

        # 核心数据卡片
        L.append("| 粉丝数 | 获赞数 | 视频总数 | 平均播放 | 主要分区 | 更新频率 |")
        L.append("|--------|--------|:--------:|:--------:|:--------:|:--------:|")
        L.append(f"| {self._fmt(up_info.get('follower', 0))} "
                 f"| {self._fmt(up_info.get('like_num', 0))} "
                 f"| {up_info.get('archive_count', 0)} "
                 f"| {self._fmt(interaction_metrics.get('avg_views', 0))} "
                 f"| {partition_analysis.get('primary_partition', '-')} "
                 f"| {content_pattern.get('update_frequency', '-')} |")
        L.append("")

        # ==================== 二、UP主基础信息 ====================
        L.append("## 二、UP主基础信息")
        L.append("")
        L.append(f"| 属性 | 信息 |")
        L.append(f"|------|------|")
        L.append(f"| UID | {up_info.get('uid', '-')} |")
        L.append(f"| 昵称 | {up_info.get('name', '-')} |")
        L.append(f"| 等级 | LV{up_info.get('level', 0)} |")
        sign = up_info.get('sign', '无')
        L.append(f"| 签名 | {sign} |")
        L.append(f"| 粉丝 | {self._fmt(up_info.get('follower', 0))} |")
        L.append(f"| 关注 | {self._fmt(up_info.get('following', 0))} |")
        L.append(f"| 获赞 | {self._fmt(up_info.get('like_num', 0))} |")
        L.append("")

        # ==================== 三、核心数据指标 ====================
        L.append("## 三、核心互动数据")
        L.append("")
        L.append("| 指标 | 平均值 | 互动率 |")
        L.append("|:----:|-------:|:------:|")
        metrics_rows = [
            ("播放量", "avg_views", None),
            ("点赞", "avg_likes", "like_rate"),
            ("投币", "avg_coins", "coin_rate"),
            ("收藏", "avg_favorites", "favorite_rate"),
            ("分享", "avg_shares", "share_rate"),
            ("评论", "avg_replies", "reply_rate"),
            ("弹幕", "avg_danmaku", "danmaku_rate"),
        ]
        for label, key, rate_key in metrics_rows:
            val = self._fmt(interaction_metrics.get(key, 0))
            rate = f"{interaction_metrics.get(rate_key, 0)}%" if rate_key else "-"
            L.append(f"| {label} | {val} | {rate} |")
        L.append("")

        # ==================== 四、发布分区统计 ====================
        L.append("## 四、发布分区统计")
        L.append("")
        L.append(f"- **主要分区**: {partition_analysis.get('primary_partition', '-')}  "
                 f"- **涉及分区**: {partition_analysis.get('partition_count', 0)} 个")
        L.append("")

        # 分区饼图
        if enable_charts and partition_analysis.get('distribution'):
            pie_data = [{"name": d["partition"], "value": d["count"]}
                        for d in partition_analysis['distribution']]
            chart_path = self._create_pie_chart(pie_data, "视频分区分布", filename="partition.png")
            if chart_path:
                L.append(f"![分区分布]({chart_path})")
                L.append("")

        L.append("| 分区 | 视频数 | 占比 | 总播放 | 平均播放 |")
        L.append("|:----:|-------:|:----:|-------:|:--------:|")
        for item in partition_analysis.get('distribution', []):
            L.append(f"| {item['partition']} | {item['count']} "
                     f"| {item['percentage']}% "
                     f"| {self._fmt(item['total_views'])} "
                     f"| {self._fmt(item['avg_views'])} |")
        L.append("")

        # ==================== 五、视频类型分析 ====================
        L.append("## 五、视频类型分析")
        L.append("")
        L.append(f"- **主要类型**: {type_analysis.get('primary_type', '-')}  "
                 f"- **类型数量**: {type_analysis.get('type_count', 0)} 种")
        L.append("")

        if enable_charts and type_analysis.get('distribution'):
            type_data = [{"name": d["type"], "value": d["count"]}
                         for d in type_analysis['distribution']]
            chart_path = self._create_pie_chart(type_data, "视频类型分布", filename="type.png")
            if chart_path:
                L.append(f"![类型分布]({chart_path})")
                L.append("")

        L.append("| 类型 | 视频数 | 占比 |")
        L.append("|:----:|-------:|:----:|")
        for item in type_analysis.get('distribution', []):
            L.append(f"| {item['type']} | {item['count']} | {item['percentage']}% |")
        L.append("")

        # ==================== 六、多维度评分 ====================
        L.append("## 六、多维度评分")
        L.append("")
        L.append(f"**综合得分**: {score_result.total_score} 分  "
                 f"**等级**: {grade}  "
                 f"**评价**: {score_result.summary}")
        L.append("")

        # 雷达图
        if enable_charts and score_result.dimension_scores:
            dims = list(score_result.dimension_scores.keys())
            vals = list(score_result.dimension_scores.values())
            chart_path = self._create_radar_chart(dims, vals, "各维度评分", filename="radar.png")
            if chart_path:
                L.append(f"![评分雷达图]({chart_path})")
                L.append("")

        # 维度得分表（含进度条）
        L.append("| 维度 | 得分 | 可视化 |")
        L.append("|------|:----:|--------|")
        for dim_name, dim_score in score_result.dimension_scores.items():
            bar = self._score_bar(dim_score)
            L.append(f"| {dim_name} | **{dim_score}** | {bar} |")
        L.append("")

        # ==================== 七、趋势分析 ====================
        L.append("## 七、发布趋势")
        L.append("")

        total_days = trend_analysis.get('total_days', 0)
        if total_days and total_days > 0:
            L.append(f"| 指标 | 数值 |")
            L.append(f"|------|------|")
            L.append(f"| 分析时间跨度 | {total_days} 天 |")
            L.append(f"| 月均发布 | {trend_analysis.get('avg_videos_per_month', 0)} 个 |")
            L.append(f"| 周均发布 | {trend_analysis.get('avg_videos_per_week', 0)} 个 |")
            L.append(f"| 最活跃月份 | {trend_analysis.get('most_active_month', '-')} |")
            L.append(f"| 活跃度趋势 | **{trend_analysis.get('activity_trend', '-')}** |")
        else:
            L.append("*视频时间数据不足，无法分析趋势*")
        L.append("")

        monthly_dist = trend_analysis.get('monthly_distribution', {})
        if enable_charts and monthly_dist and len(monthly_dist) >= 2 and _HAS_MATPLOTLIB:
            chart_path = self._create_line_chart(
                monthly_dist, "月度发布趋势", "月份", "视频数", filename="trend.png")
            if chart_path:
                L.append(f"![月度趋势]({chart_path})")
                L.append("")
        elif monthly_dist and len(monthly_dist) >= 2:
            # 无绘图环境/禁用图表时的纯文本降级
            labels = sorted(monthly_dist.keys())
            values = [monthly_dist[k] for k in labels]
            spark = _text_sparkline(values)
            max_val = max(values)
            top_display = ", ".join(f"{k}:{v}" for k, v in
                                    sorted(monthly_dist.items(), key=lambda x: x[1], reverse=True)[:3])
            L.append(f"- 月度发布趋势（纯文本）: `{spark}`")
            L.append(f"- 峰值发布月份: {top_display}")
            L.append(f"- 峰值月发布量: {max_val}")
            L.append("")

        # ==================== 八、热门视频 ====================
        L.append("## 八、热门视频 TOP5")
        L.append("")
        L.append("| # | 标题 | 播放 | 点赞 | 投币 | 收藏 |")
        L.append("|:-:|------|-----:|-----:|-----:|-----:|")
        for i, v in enumerate(top_videos[:5], 1):
            title = v.get('title', '-')
            if len(title) > 35:
                title = title[:35] + "..."
            L.append(f"| {i} | {title} "
                     f"| {self._fmt(v.get('views', 0))} "
                     f"| {self._fmt(v.get('likes', 0))} "
                     f"| {self._fmt(v.get('coins', 0))} "
                     f"| {self._fmt(v.get('favorites', 0))} |")
        L.append("")

        # ==================== 九、内容模式 ====================
        L.append("## 九、内容模式")
        L.append("")
        L.append("| 属性 | 结果 |")
        L.append(f"|------|------|")
        L.append(f"| 系列创作者 | {'是' if content_pattern.get('is_series_creator') else '否'} |")
        if content_pattern.get('series_prefix'):
            L.append(f"| 系列前缀 | {content_pattern['series_prefix']} |")
        L.append(f"| 固定格式 | {'是' if content_pattern.get('has_fixed_format') else '否'} |")
        L.append(f"| 更新频率 | {content_pattern.get('update_frequency', '-')} |")
        L.append("")

        # ==================== 十、UP主画像 ====================
        if persona:
            L.append("## 十、UP主画像")
            L.append("")
            
            # 画像类型标签
            L.append(f"**画像类型**: `{persona.persona_type}`")
            L.append("")
            
            # 画像总结
            L.append(f"> {persona.summary}")
            L.append("")
            
            # 内容创作画像
            L.append("### 内容创作画像")
            L.append("")
            creator = persona.creator
            L.append(f"| 维度 | 特征 | 评分 |")
            L.append(f"|------|------|:----:|")
            L.append(f"| 内容风格 | {creator.content_style} | - |")
            L.append(f"| 创作模式 | {creator.creation_pattern} | - |")
            L.append(f"| 技术水准 | {creator.technical_level} | - |")
            L.append(f"| 创新度 | - | {creator.innovation_score} |")
            L.append(f"| 一致性 | - | {creator.consistency_score} |")
            L.append("")
            L.append(f"**创作标签**: {' '.join([f'`{t}`' for t in creator.tags])}")
            L.append("")
            
            # 受众画像
            L.append("### 受众画像")
            L.append("")
            audience = persona.audience
            L.append(f"| 维度 | 特征 |")
            L.append(f"|------|------|")
            L.append(f"| 互动类型 | {audience.engagement_type} |")
            L.append(f"| 忠诚度 | {audience.loyalty_level} |")
            L.append(f"| 活跃时段 | {audience.active_hours} |")
            L.append(f"| 社区氛围 | {audience.community_vibe} |")
            L.append("")
            L.append(f"**受众偏好**: {' '.join([f'`{t}`' for t in audience.preference_tags])}")
            L.append("")
            
            # 商业价值画像
            L.append("### 商业价值画像")
            L.append("")
            commercial = persona.commercial
            L.append(f"| 维度 | 特征 | 评分 |")
            L.append(f"|------|------|:----:|")
            L.append(f"| 变现潜力 | {commercial.monetization_potential} | - |")
            L.append(f"| 合作价值 | - | {commercial.cooperation_value} |")
            L.append(f"| 内容安全度 | {commercial.content_safety} | - |")
            L.append(f"| 目标人群 | {commercial.target_demographics} | - |")
            L.append("")
            L.append(f"**适配品牌**: {' '.join([f'`{b}`' for b in commercial.brand_fit])}")
            L.append("")
            
            # 成长潜力画像
            L.append("### 成长潜力画像")
            L.append("")
            growth = persona.growth
            L.append(f"| 维度 | 特征 |")
            L.append(f"|------|------|")
            L.append(f"| 成长阶段 | {growth.growth_stage} |")
            L.append(f"| 增长势头 | {growth.growth_momentum} |")
            L.append(f"| 竞争定位 | {growth.competitive_position} |")
            L.append(f"| 潜力天花板 | {growth.potential_ceiling} |")
            L.append("")
            L.append(f"**改进空间**: {' '.join([f'`{a}`' for a in growth.improvement_areas])}")
            L.append("")

        # ==================== 十一、总结与建议 ====================
        L.append("## 十、总结与建议")
        L.append("")

        # 优势
        L.append("### 优势")
        L.append("")
        strengths = []
        if interaction_metrics.get('like_rate', 0) > 3:
            strengths.append("- 点赞率较高（%.1f%%），内容受观众认可" % interaction_metrics['like_rate'])
        if interaction_metrics.get('favorite_rate', 0) > 1:
            strengths.append("- 收藏率良好（%.2f%%），内容具有保存价值" % interaction_metrics['favorite_rate'])
        if trend_analysis.get('activity_trend') == '上升':
            strengths.append("- 发布趋势呈上升态势，创作活跃")
        if content_pattern.get('is_series_creator'):
            strengths.append("- 系列化内容产出，利于粉丝沉淀")
        if score_result.total_score >= 80:
            strengths.append("- 综合评分优秀，整体表现突出")
        L.extend(strengths if strengths else ["- 内容稳定，持续创作中"])
        L.append("")

        # 建议
        L.append("### 改进建议")
        L.append("")
        suggestions = []
        if interaction_metrics.get('share_rate', 0) < 0.1:
            suggestions.append("- 提升内容传播性，适当增加分享引导")
        if interaction_metrics.get('danmaku_rate', 0) < 0.5:
            suggestions.append("- 增加互动点，提升弹幕和评论活跃度")
        if trend_analysis.get('activity_trend') == '下降':
            suggestions.append("- 保持更新频率，避免活跃度持续下降")
        if len(partition_analysis.get('distribution', [])) == 1:
            suggestions.append("- 尝试拓展内容领域，吸引更广泛受众")
        if score_result.total_score < 70:
            suggestions.append("- 参考同类型优秀UP主，提升内容质量")
        L.extend(suggestions if suggestions else ["- 保持当前创作节奏，关注粉丝反馈"])
        L.append("")

        # 页脚
        L.append("---")
        L.append("")
        L.append(f"*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
        L.append("")
        L.append("*注：本报告基于公开数据分析生成，评分结果仅供参考*")

        return "\n".join(L)

    def save_report(self, report_content: str, filename: Optional[str] = None) -> str:
        """保存报告到文件"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"up_analysis_{timestamp}.md"
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        return filepath
