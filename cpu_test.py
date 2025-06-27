#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CPU性能测试模块
包含单线程和多线程CPU性能测试
"""

import time
import math
import psutil
from concurrent.futures import ThreadPoolExecutor


def cpu_single_thread_test(duration=20):
    """单线程CPU测试
    
    Args:
        duration: 测试持续时间（秒）
        
    Returns:
        dict: 包含测试结果的字典
    """
    print("正在进行单线程CPU测试...")

    def cpu_intensive_task():
        """CPU密集型任务：计算素数"""
        count = 0
        num = 2
        while True:
            is_prime = True
            for i in range(2, int(math.sqrt(num)) + 1):
                if num % i == 0:
                    is_prime = False
                    break
            if is_prime:
                count += 1
            num += 1
            if count >= 15000:  # 计算15000个素数，增加计算量
                break
        return count

    start_time = time.time()
    result = cpu_intensive_task()
    end_time = time.time()

    elapsed_time = end_time - start_time
    operations_per_second = result / elapsed_time

    print(f"单线程CPU测试完成:")
    print(f"  计算素数个数: {result}")
    print(f"  耗时: {elapsed_time:.2f} 秒")
    print(f"  性能: {operations_per_second:.0f} 素数/秒")

    return {
        'primes_calculated': result,
        'time_taken': elapsed_time,
        'operations_per_second': operations_per_second
    }


def cpu_multi_thread_test(duration=5, max_threads=2):
    """多线程CPU测试（优化为低配置硬件）
    
    Args:
        duration: 测试持续时间（秒）
        max_threads: 最大线程数（限制为2以避免跑满CPU）
        
    Returns:
        dict: 包含测试结果的字典
    """
    print("正在进行多线程CPU测试...")

    def worker_task():
        """工作线程任务（降低计算强度）"""
        count = 0
        # 降低计算量以适配低配置硬件
        for i in range(500000):  # 从2000000降低到500000
            count += abs(math.sqrt(i) * math.sin(i))
        return count

    # 确保num_threads不为None
    if max_threads is None or max_threads <= 0:
        num_threads = psutil.cpu_count(logical=True) or 2
    else:
        num_threads = max_threads

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(worker_task) for _ in range(num_threads)]
        results = [future.result() for future in futures]
    end_time = time.time()

    elapsed_time = end_time - start_time
    total_operations = sum(results)
    operations_per_second = total_operations / elapsed_time

    print(f"多线程CPU测试完成 (使用 {num_threads} 个线程):")
    print(f"  总计算量: {total_operations:.0f}")
    print(f"  耗时: {elapsed_time:.2f} 秒")
    print(f"  性能: {operations_per_second:.0f} 操作/秒")

    return {
        'threads_used': num_threads,
        'total_operations': total_operations,
        'time_taken': elapsed_time,
        'operations_per_second': operations_per_second
    }


if __name__ == "__main__":
    # 测试代码
    import psutil
    
    print("CPU性能测试示例")
    print("=" * 60)
    
    # 单线程测试
    single_result = cpu_single_thread_test()
    print()
    
    # 多线程测试
    logical_cpu_count = psutil.cpu_count(logical=True)
    multi_result = cpu_multi_thread_test(logical_cpu_count)