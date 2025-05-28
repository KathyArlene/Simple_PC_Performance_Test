#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
磁盘I/O性能测试模块
测试磁盘读写速度
"""

import os
import time
import random
import tempfile


def disk_io_test(file_size_mb=100):
    """磁盘I/O性能测试
    
    Args:
        file_size_mb: 测试文件大小（MB）
        
    Returns:
        dict: 包含测试结果的字典
    """
    print(f"正在进行磁盘I/O测试 (文件大小: {file_size_mb}MB)...")

    test_file = os.path.join(tempfile.gettempdir(), 'benchmark_test.dat')
    file_size = file_size_mb * 1024 * 1024  # 转换为字节

    try:
        # 写入测试
        print("  测试写入性能...")
        data = bytearray(random.getrandbits(8) for _ in range(1024 * 1024))  # 1MB随机数据

        start_time = time.time()
        with open(test_file, 'wb') as f:
            for _ in range(file_size_mb):
                f.write(data)
        end_time = time.time()

        write_time = end_time - start_time
        write_speed = file_size_mb / write_time

        print(f"    写入时间: {write_time:.2f} 秒")
        print(f"    写入速度: {write_speed:.2f} MB/s")

        # 读取测试
        print("  测试读取性能...")
        start_time = time.time()
        with open(test_file, 'rb') as f:
            while f.read(1024 * 1024):  # 每次读取1MB
                pass
        end_time = time.time()

        read_time = end_time - start_time
        read_speed = file_size_mb / read_time

        print(f"    读取时间: {read_time:.2f} 秒")
        print(f"    读取速度: {read_speed:.2f} MB/s")

        return {
            'file_size_mb': file_size_mb,
            'write_time': write_time,
            'write_speed_mb_s': write_speed,
            'read_time': read_time,
            'read_speed_mb_s': read_speed
        }

    finally:
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)


if __name__ == "__main__":
    # 测试代码
    print("磁盘I/O性能测试示例")
    print("=" * 60)
    
    # 使用较小的文件大小进行测试
    results = disk_io_test(file_size_mb=50)
    
    print("\n测试结果摘要:")
    print(f"写入速度: {results['write_speed_mb_s']:.2f} MB/s")
    print(f"读取速度: {results['read_speed_mb_s']:.2f} MB/s")