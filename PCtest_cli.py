#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电脑性能测试工具 - 命令行版本
基于PCtest.py的功能，提供命令行界面
支持多语言（中文、英文、日文、西班牙语）
"""

import sys
import os
import argparse
import json
import time

# 导入性能测试核心模块
from PCtest_core import PerformanceBenchmark

# 导入多语言支持模块
import language as lang


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description=lang.get('cli_description'))
    
    # 添加测试选项
    parser.add_argument("--cpu", action="store_true", help=lang.get('cli_cpu_help'))
    parser.add_argument("--memory", action="store_true", help=lang.get('cli_memory_help'))
    parser.add_argument("--disk", action="store_true", help=lang.get('cli_disk_help'))
    parser.add_argument("--gpu", action="store_true", help=lang.get('cli_gpu_help'))
    parser.add_argument("--all", action="store_true", help=lang.get('cli_all_help'))
    
    # 添加输出选项
    parser.add_argument("--output", "-o", type=str, help=lang.get('cli_output_help'))
    parser.add_argument("--quiet", "-q", action="store_true", help=lang.get('cli_quiet_help'))
    
    # 添加语言选项
    parser.add_argument("--language", "-l", type=str, choices=lang.SUPPORTED_LANGUAGES,
                        help=lang.get('cli_language_help'))
    
    # 解析参数
    args = parser.parse_args()
    
    # 如果指定了语言，设置语言
    if args.language:
        lang.set_language(args.language)
    
    # 如果没有指定任何测试，默认运行所有测试
    if not (args.cpu or args.memory or args.disk or args.gpu or args.all):
        args.all = True
    
    return args


def main():
    """主函数"""
    # 解析命令行参数
    args = parse_args()
    
    # 创建性能测试实例
    benchmark = PerformanceBenchmark()
    
    # 设置输出文件
    output_file = args.output if args.output else "benchmark_report.json"
    
    try:
        # 打印欢迎信息
        if not args.quiet:
            print(lang.get('cli_welcome'))
            print("=" * 60)
        
        # 获取系统信息
        if not args.quiet:
            benchmark.print_system_info()
        
        # 根据参数运行测试
        if args.all:
            # 运行所有测试
            benchmark.run_all_tests()
        else:
            # 运行选定的测试
            if not args.quiet:
                print(f"\n{lang.get('cli_start_selected')}")
            
            # CPU测试
            if args.cpu:
                if not args.quiet:
                    print("\n" + "=" * 60)
                    print(lang.get('cpu_test'))
                    print("=" * 60)
                benchmark.results['cpu_single_thread'] = benchmark.cpu_single_thread_test()
                benchmark.results['cpu_multi_thread'] = benchmark.cpu_multi_thread_test()
            
            # 内存测试
            if args.memory:
                if not args.quiet:
                    print("\n" + "=" * 60)
                    print(lang.get('memory_test'))
                    print("=" * 60)
                benchmark.results['memory'] = benchmark.memory_test()
            
            # 磁盘I/O测试
            if args.disk:
                if not args.quiet:
                    print("\n" + "=" * 60)
                    print(lang.get('disk_test'))
                    print("=" * 60)
                benchmark.results['disk_io'] = benchmark.disk_io_test()
            
            # GPU测试
            if args.gpu:
                if not args.quiet:
                    print("\n" + "=" * 60)
                    print(lang.get('gpu_test'))
                    print("=" * 60)
                benchmark.results['gpu'] = benchmark.gpu_test()
            
            # 生成报告
            if not args.quiet:
                print("\n" + "=" * 60)
                print(lang.get('performance_report'))
                print("=" * 60)
            
            benchmark.generate_report(output_file)
        
        # 显示报告保存位置
        print(f"\n{lang.get('detailed_report_saved')}: {os.path.abspath(output_file)}")
        
    except KeyboardInterrupt:
        print(f"\n{lang.get('test_interrupted')}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{lang.get('test_error_occurred')}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()