#!/usr/bin/env python3
"""
Bilibili UP主分析主脚本

入口脚本，整合数据采集、分析、评分和报告生成功能。
支持通过UID、用户名、主页链接作为输入。
"""

import argparse
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_fetcher import BilibiliDataFetcher
from data_analyzer import VideoAnalyzer
from scoring_system import UpScoringSystem
from report_generator import ReportGenerator
from persona_analyzer import PersonaAnalyzer


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="Bilibili UP主视频内容分析工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python analyze_up.py 159285873
  python analyze_up.py Jason_Shane
  python analyze_up.py "https://space.bilibili.com/159285873"
  python analyze_up.py Jason_Shane --recent 20 --cache
  python analyze_up.py Jason_Shane --all --output ./reports/
        """
    )

    # 输入参数（位置参数，支持UID/用户名/URL）
    parser.add_argument(
        "target",
        type=str,
        help="UP主UID、用户名或主页链接",
    )

    # 分析范围
    parser.add_argument(
        "--recent", "-r",
        type=int,
        default=10,
        help="分析最近N个视频，默认10",
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="分析全部视频（覆盖--recent）",
    )

    # 缓存设置
    parser.add_argument(
        "--cache", "-c",
        action="store_true",
        help="启用数据缓存",
    )
    parser.add_argument(
        "--cache-dir",
        type=str,
        default="./cache",
        help="缓存目录，默认./cache",
    )
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="清除缓存后运行",
    )

    # 输出设置
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="./reports",
        help="报告输出目录，默认./reports",
    )
    parser.add_argument(
        "--format", "-f",
        type=str,
        default="markdown",
        choices=["markdown", "json"],
        help="报告格式，默认markdown",
    )
    parser.add_argument(
        "--no-charts",
        action="store_true",
        help="禁用图表生成",
    )
    parser.add_argument(
        "--filename",
        type=str,
        help="指定输出文件名",
    )

    # 其他选项
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="显示详细日志",
    )

    return parser.parse_args()


def main():
    """主函数"""
    args = parse_arguments()

    # 初始化采集器
    fetcher = BilibiliDataFetcher(
        cache_dir=args.cache_dir,
        enable_cache=args.cache,
    )

    # 预热（获取基础Cookie）
    if args.verbose:
        print("预热：获取基础Cookie...")
    fetcher._warm_up()
    time.sleep(4)

    # 解析UID（支持UID/用户名/URL）
    if args.verbose:
        print(f"解析输入: {args.target}")
    uid = fetcher.resolve_uid(args.target)
    if not uid:
        print(f"错误: 无法解析UP主标识: {args.target}")
        print("请提供有效的UID（数字）、用户名或主页链接")
        sys.exit(1)
    if args.verbose:
        print(f"解析到UID: {uid}")

    # 搜索后需要等待，避免连续请求触发风控
    time.sleep(3)

    # 清除缓存（如果需要）
    if args.clear_cache:
        if args.verbose:
            print("清除缓存...")
        fetcher.clear_cache(uid)

    # 1. 获取UP主信息
    if args.verbose:
        print("获取UP主信息...")
    up_info = fetcher.get_up_info(uid)
    if not up_info:
        print(f"错误: 无法获取UP主信息 (UID: {uid})")
        sys.exit(1)
    if args.verbose:
        print(f"UP主: {up_info.get('name')}, 粉丝: {up_info.get('follower')}, "
              f"获赞: {up_info.get('like_num')}, 视频: {up_info.get('archive_count')}")

    # 2. 获取视频列表
    if args.verbose:
        print("获取视频列表...")
    up_name = up_info.get("name", "")
    if args.all:
        videos = fetcher.get_all_videos(uid, up_name=up_name)
    else:
        videos = fetcher.get_all_videos(uid, up_name=up_name, max_videos=args.recent)
    if not videos:
        print(f"错误: 未获取到视频数据 (UID: {uid})")
        sys.exit(1)
    if args.verbose:
        print(f"获取到 {len(videos)} 个视频")

    # 3. 补充视频详情数据
    if args.verbose:
        print("补充视频详情数据...")
    for i, video in enumerate(videos):
        fetcher.enrich_video_stat(video)
        if args.verbose and (i + 1) % 20 == 0:
            print(f"  已处理 {i + 1}/{len(videos)} 个视频")
        if i < len(videos) - 1:
            time.sleep(0.5)

    # 补充：从视频数据中累加总获赞数（未登录时API不返回like_num）
    if not up_info.get("like_num"):
        total_likes = sum(v.get("stat", {}).get("like", 0) or 0 for v in videos)
        up_info["like_num"] = total_likes
        if args.verbose:
            print(f"补充获赞数: {total_likes}")

    # 4. 数据分析
    if args.verbose:
        print("进行数据分析...")
    analyzer = VideoAnalyzer()
    partition_analysis = analyzer.analyze_partition_distribution(videos)
    type_analysis = analyzer.analyze_video_types(videos)
    interaction_metrics = analyzer.calculate_interaction_metrics(videos)
    trend_analysis = analyzer.analyze_trends(videos)
    top_videos = analyzer.identify_top_videos(videos, top_n=5)
    content_pattern = analyzer.detect_content_pattern(videos)

    # 5. 评分计算
    if args.verbose:
        print("计算综合评分...")
    scoring_system = UpScoringSystem()
    video_types = [item["type"] for item in type_analysis.get("distribution", [])]
    score_result = scoring_system.calculate_score(
        up_info=up_info,
        videos=videos,
        metrics=interaction_metrics,
        primary_partition=partition_analysis.get("primary_partition", "未知"),
        video_types=video_types,
    )

    # 6. UP主画像分析
    if args.verbose:
        print("生成UP主画像...")
    persona_analyzer = PersonaAnalyzer()
    persona = persona_analyzer.analyze(
        up_info=up_info,
        videos=videos,
        type_analysis=type_analysis,
        content_pattern=content_pattern,
        interaction_metrics=interaction_metrics,
        partition_analysis=partition_analysis,
        trend_analysis=trend_analysis,
        score_result=score_result,
    )

    # 7. 生成报告
    if args.verbose:
        print("生成分析报告...")
    report_generator = ReportGenerator(output_dir=args.output)

    if args.format == "markdown":
        report_content = report_generator.generate_report(
            up_info=up_info,
            videos=videos,
            partition_analysis=partition_analysis,
            type_analysis=type_analysis,
            interaction_metrics=interaction_metrics,
            trend_analysis=trend_analysis,
            top_videos=top_videos,
            content_pattern=content_pattern,
            score_result=score_result,
            persona=persona,
            enable_charts=not args.no_charts,
        )
        if args.filename:
            filename = args.filename if args.filename.endswith('.md') else f"{args.filename}.md"
        else:
            filename = None
        report_path = report_generator.save_report(report_content, filename)
        print(f"\n分析完成!")
        print(f"UP主: {up_info.get('name')}")
        print(f"综合评分: {score_result.total_score} 分 (等级: {score_result.grade})")
        print(f"报告已保存: {report_path}")

    elif args.format == "json":
        import json
        from datetime import datetime
        result = {
            "up_info": up_info,
            "video_count": len(videos),
            "partition_analysis": partition_analysis,
            "type_analysis": type_analysis,
            "interaction_metrics": interaction_metrics,
            "trend_analysis": trend_analysis,
            "top_videos": top_videos,
            "content_pattern": content_pattern,
            "score": {
                "total": score_result.total_score,
                "grade": score_result.grade,
                "dimensions": score_result.dimension_scores,
                "summary": score_result.summary,
            },
        }
        if args.filename:
            json_filename = args.filename if args.filename.endswith('.json') else f"{args.filename}.json"
        else:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            json_filename = f"up_analysis_{uid}_{timestamp}.json"
        json_path = os.path.join(args.output, json_filename)
        os.makedirs(args.output, exist_ok=True)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n分析完成!")
        print(f"UP主: {up_info.get('name')}")
        print(f"综合评分: {score_result.total_score} 分 (等级: {score_result.grade})")
        print(f"JSON报告已保存: {json_path}")


if __name__ == "__main__":
    main()
