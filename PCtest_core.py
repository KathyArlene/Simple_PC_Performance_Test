#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电脑性能测试工具 - 核心模块
整合所有测试功能
支持多语言（中文、英文、日文、西班牙语）
"""

import sys
import time

# 导入各个测试模块
from system_info import get_system_info, print_system_info
from cpu_test import cpu_single_thread_test, cpu_multi_thread_test
from memory_test import memory_test
from disk_test import disk_io_test
from gpu_test import gpu_test
from report_generator import calculate_scores, print_report, save_report

# 导入多语言支持模块
import language as lang


class PerformanceBenchmark:
    """性能测试基准类
    
    整合所有测试功能，提供统一的接口
    """
    def __init__(self):
        """初始化性能测试基准类"""
        self.results = {}
        self.system_info = get_system_info()
    
    def print_system_info(self):
        """打印系统信息"""
        print_system_info(self.system_info)
    
    def cpu_single_thread_test(self, duration=5):
        """运行CPU单线程测试"""
        return cpu_single_thread_test(duration)
    
    def cpu_multi_thread_test(self, duration=5):
        """运行CPU多线程测试"""
        return cpu_multi_thread_test(self.system_info['logical_cpu_count'], duration)
    
    def memory_test(self):
        """运行内存性能测试"""
        return memory_test()
    
    def disk_io_test(self, file_size_mb=100):
        """运行磁盘I/O性能测试"""
        return disk_io_test(file_size_mb)
    
    def gpu_test(self):
        """运行GPU性能测试"""
        return gpu_test(self.system_info.get('gpus'))
    
    def run_all_tests(self):
        """运行所有测试"""
        try:
            print(f"{lang.get('start_performance_test')}\n")
            
            self.print_system_info()

            # CPU测试
            print("=" * 60)
            print(lang.get('cpu_test'))
            print("=" * 60)
            self.results['cpu_single_thread'] = self.cpu_single_thread_test()
            print()
            self.results['cpu_multi_thread'] = self.cpu_multi_thread_test()
            print()

            # 内存测试
            print("=" * 60)
            print(lang.get('memory_test'))
            print("=" * 60)
            self.results['memory'] = self.memory_test()
            print()

            # 磁盘I/O测试
            print("=" * 60)
            print(lang.get('disk_test'))
            print("=" * 60)
            self.results['disk_io'] = self.disk_io_test()
            print()
            
            # GPU测试
            print("=" * 60)
            print(lang.get('gpu_test'))
            print("=" * 60)
            self.results['gpu'] = self.gpu_test()
            print()

            # 生成报告
            self.generate_report()
            
        except KeyboardInterrupt:
            print(f"\n{lang.get('test_interrupted')}")
            sys.exit(1)
        except Exception as e:
            print(f"\n{lang.get('test_error_occurred')}: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    def generate_scores(self):
        """计算性能得分"""
        return calculate_scores(self.results)
    
    def generate_report(self, filename='benchmark_report.json'):
        """生成测试报告"""
        scores = self.generate_scores()
        print_report(self.system_info, self.results, scores)
        return save_report(self.system_info, self.results, scores, filename)


def main():
    """主函数"""
    try:
        benchmark = PerformanceBenchmark()
        benchmark.run_all_tests()
    except KeyboardInterrupt:
        print(f"\n{lang.get('test_interrupted')}")
    except Exception as e:
        print(f"{lang.get('test_error_occurred')}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()