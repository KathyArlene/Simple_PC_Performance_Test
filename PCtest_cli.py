#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电脑性能测试工具 - 命令行界面
提供命令行参数解析和测试执行
"""

import sys
import argparse
import os
from PCtest_core import PerformanceBenchmark


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="电脑性能测试工具")
    
    # 添加测试选项
    parser.add_argument("--cpu", action="store_true", help="仅运行CPU测试")
    parser.add_argument("--memory", action="store_true", help="仅运行内存测试")
    parser.add_argument("--disk", action="store_true", help="仅运行磁盘I/O测试")
    parser.add_argument("--gpu", action="store_true", help="仅运行GPU测试")
    parser.add_argument("--all", action="store_true", help="运行所有测试（默认）")
    
    # 添加输出选项
    parser.add_argument("--output", "-o", type=str, help="指定报告输出文件路径")
    parser.add_argument("--quiet", "-q", action="store_true", help="安静模式，仅显示最终结果")
    
    # 解析参数
    args = parser.parse_args()
    
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
            print("电脑性能测试工具 - 命令行版本")
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
                print("\n开始选定的性能测试...")
            
            # CPU测试
            if args.cpu:
                if not args.quiet:
                    print("\n" + "=" * 60)
                    print("CPU性能测试")
                    print("=" * 60)
                benchmark.results['cpu_single_thread'] = benchmark.cpu_single_thread_test()
                benchmark.results['cpu_multi_thread'] = benchmark.cpu_multi_thread_test()
            
            # 内存测试
            if args.memory:
                if not args.quiet:
                    print("\n" + "=" * 60)
                    print("内存性能测试")
                    print("=" * 60)
                benchmark.results['memory'] = benchmark.memory_test()
            
            # 磁盘I/O测试
            if args.disk:
                if not args.quiet:
                    print("\n" + "=" * 60)
                    print("磁盘I/O性能测试")
                    print("=" * 60)
                benchmark.results['disk_io'] = benchmark.disk_io_test()
            
            # GPU测试
            if args.gpu:
                if not args.quiet:
                    print("\n" + "=" * 60)
                    print("GPU性能测试")
                    print("=" * 60)
                benchmark.results['gpu'] = benchmark.gpu_test()
            
            # 生成报告
            if not args.quiet:
                print("\n" + "=" * 60)
                print("性能测试报告")
                print("=" * 60)
            
            benchmark.generate_report(output_file)
        
        # 显示报告保存位置
        print(f"\n详细报告已保存到: {os.path.abspath(output_file)}")
        
    except KeyboardInterrupt:
        print("\n测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()