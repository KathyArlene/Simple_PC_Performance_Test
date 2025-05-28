#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
性能测试报告生成模块
计算性能得分并生成测试报告
"""

import json


def calculate_scores(results):
    """计算各项性能得分
    
    Args:
        results: 包含各项测试结果的字典
        
    Returns:
        dict: 包含各项得分的字典
    """
    scores = {}
    weights = {
        'cpu_single': 0.15,  # 15%
        'cpu_multi': 0.25,   # 25%
        'memory': 0.2,       # 20%
        'disk_write': 0.1,   # 10%
        'disk_read': 0.1,    # 10%
        'gpu': 0.2           # 20%
    }
    
    # CPU单线程得分
    if 'cpu_single_thread' in results:
        scores['cpu_single_thread'] = results['cpu_single_thread']['operations_per_second'] / 5000
    else:
        scores['cpu_single_thread'] = 0
    
    # CPU多线程得分
    if 'cpu_multi_thread' in results:
        scores['cpu_multi_thread'] = results['cpu_multi_thread']['operations_per_second'] / 5000000
    else:
        scores['cpu_multi_thread'] = 0
    
    # 内存得分
    if 'memory' in results and '1024KB' in results['memory']:
        scores['memory'] = results['memory']['1024KB']['throughput_mb_s'] / 100
    else:
        scores['memory'] = 0
    
    # 磁盘I/O得分
    if 'disk_io' in results:
        scores['disk_write'] = results['disk_io']['write_speed_mb_s'] / 100
        scores['disk_read'] = results['disk_io']['read_speed_mb_s'] / 75
    else:
        scores['disk_write'] = 0
        scores['disk_read'] = 0
    
    # GPU得分
    scores['gpu'] = 0
    if 'gpu' in results and results['gpu']:
        if 'gpu_gflops' in results['gpu']:
            # 以10 GFLOPS为基准
            scores['gpu'] = results['gpu']['gpu_gflops'] / 10
        elif 'cpu_gflops' in results['gpu']:
            # 如果没有GPU测试结果，使用CPU结果的一半作为估计
            scores['gpu'] = results['gpu']['cpu_gflops'] / 10
    
    # 计算加权总分
    total_score = (
        scores['cpu_single_thread'] * weights['cpu_single'] +
        scores['cpu_multi_thread'] * weights['cpu_multi'] +
        scores['memory'] * weights['memory'] +
        scores['disk_write'] * weights['disk_write'] +
        scores['disk_read'] * weights['disk_read'] +
        scores['gpu'] * weights['gpu']
    )
    
    scores['total'] = total_score
    scores['weights'] = weights
    
    return scores


def print_report(system_info, results, scores):
    """打印测试报告
    
    Args:
        system_info: 系统信息字典
        results: 测试结果字典
        scores: 性能得分字典
    """
    print("=" * 60)
    print("性能测试报告")
    print("=" * 60)
    
    print(f"CPU单线程性能得分: {scores['cpu_single_thread']:.1f}")
    print(f"CPU多线程性能得分: {scores['cpu_multi_thread']:.1f}")
    print(f"内存性能得分: {scores['memory']:.1f}")
    print(f"磁盘写入性能得分: {scores['disk_write']:.1f}")
    print(f"磁盘读取性能得分: {scores['disk_read']:.1f}")
    print(f"GPU性能得分: {scores['gpu']:.1f}")
    print("-" * 40)
    print(f"综合性能得分: {scores['total']:.1f}")


def save_report(system_info, results, scores, filename='benchmark_report.json'):
    """保存测试报告到文件
    
    Args:
        system_info: 系统信息字典
        results: 测试结果字典
        scores: 性能得分字典
        filename: 报告文件名
        
    Returns:
        str: 保存的文件路径
    """
    report_data = {
        'system_info': system_info,
        'test_results': results,
        'scores': scores
    }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

    print(f"\n详细报告已保存到 {filename}")
    return filename


if __name__ == "__main__":
    # 测试代码
    print("报告生成器测试")
    print("=" * 60)
    
    # 模拟测试结果
    mock_system_info = {
        'platform': 'Windows-10',
        'processor': 'Intel Core i7',
        'cpu_count': 4,
        'logical_cpu_count': 8,
        'total_memory': 16 * 1024 * 1024 * 1024,
        'gpus': [{'name': 'NVIDIA GeForce GTX 1060'}]
    }
    
    mock_results = {
        'cpu_single_thread': {'operations_per_second': 50000},
        'cpu_multi_thread': {'operations_per_second': 5000000},
        'memory': {'1024KB': {'throughput_mb_s': 5000}},
        'disk_io': {'write_speed_mb_s': 500, 'read_speed_mb_s': 600},
        'gpu': {'cpu_gflops': 50, 'gpu_gflops': 500}
    }
    
    # 计算得分
    scores = calculate_scores(mock_results)
    
    # 打印报告
    print_report(mock_system_info, mock_results, scores)
    
    # 保存报告（测试时注释掉以避免创建文件）
    # save_report(mock_system_info, mock_results, scores, 'test_report.json')