#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内存性能测试模块
测试内存分配和访问速度
"""

import time


def memory_test():
    """内存性能测试
    
    测试不同大小内存块的分配速度
    
    Returns:
        dict: 包含测试结果的字典
    """
    print("正在进行内存性能测试...")

    # 测试内存分配速度
    sizes = [1024, 1024 * 1024, 10 * 1024 * 1024]  # 1KB, 1MB, 10MB
    results = {}

    for size in sizes:
        print(f"  测试 {size // 1024}KB 内存分配...")

        start_time = time.time()
        data_list = []
        for _ in range(100):
            data = bytearray(size)
            data_list.append(data)
        end_time = time.time()

        allocation_time = end_time - start_time
        # 添加检查，防止除零错误
        if allocation_time > 0:
            throughput = (size * 100) / (1024 * 1024) / allocation_time  # MB/s
        else:
            throughput = float('inf')  # 如果时间太短，设置为无穷大

        # 清理内存
        del data_list

        results[f'{size // 1024}KB'] = {
            'allocation_time': allocation_time,
            'throughput_mb_s': throughput
        }

        print(f"    分配时间: {allocation_time:.4f} 秒")
        print(f"    吞吐量: {throughput:.2f} MB/s")

    return results


if __name__ == "__main__":
    # 测试代码
    print("内存性能测试示例")
    print("=" * 60)
    
    results = memory_test()
    
    print("\n测试结果摘要:")
    for size, data in results.items():
        print(f"{size} 内存分配吞吐量: {data['throughput_mb_s']:.2f} MB/s")