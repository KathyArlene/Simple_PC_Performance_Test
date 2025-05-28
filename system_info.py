#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统信息收集模块
用于获取和显示系统硬件信息
"""

import platform
import psutil

# 尝试导入GPU信息检测库
try:
    import wmi
    HAS_WMI = True
except ImportError:
    HAS_WMI = False
    print("警告: 未安装wmi库，GPU信息检测将不可用。请使用 'pip install wmi' 安装。")


def get_system_info():
    """获取系统信息"""
    info = {
        'platform': platform.platform(),
        'processor': platform.processor(),
        'architecture': platform.architecture()[0],
        'cpu_count': psutil.cpu_count(logical=False),
        'logical_cpu_count': psutil.cpu_count(logical=True),
        'total_memory': psutil.virtual_memory().total,
        'available_memory': psutil.virtual_memory().available,
    }
    
    # 获取GPU信息
    if HAS_WMI:
        try:
            computer = wmi.WMI()
            gpu_infos = computer.Win32_VideoController()
            gpus = []
            
            for i, gpu in enumerate(gpu_infos):
                gpu_data = {
                    'name': gpu.Name,
                    'driver_version': gpu.DriverVersion if hasattr(gpu, 'DriverVersion') else 'Unknown',
                    'video_memory': gpu.AdapterRAM if hasattr(gpu, 'AdapterRAM') else 0,
                    'video_processor': gpu.VideoProcessor if hasattr(gpu, 'VideoProcessor') else 'Unknown',
                    'is_integrated': 'Intel' in gpu.Name or 'UHD' in gpu.Name or 'HD Graphics' in gpu.Name
                }
                gpus.append(gpu_data)
            
            info['gpus'] = gpus
        except Exception as e:
            print(f"获取GPU信息时出错: {e}")
            info['gpus'] = [{'name': '未知', 'error': str(e)}]
    else:
        info['gpus'] = [{'name': '未知', 'error': 'WMI库未安装'}]
        
    return info


def print_system_info(system_info):
    """打印系统信息"""
    print("=" * 60)
    print("系统信息")
    print("=" * 60)
    print(f"操作系统: {system_info['platform']}")
    print(f"处理器: {system_info['processor']}")
    print(f"架构: {system_info['architecture']}")
    print(f"物理CPU核心: {system_info['cpu_count']}")
    print(f"逻辑CPU核心: {system_info['logical_cpu_count']}")
    print(f"总内存: {system_info['total_memory'] / (1024 ** 3):.2f} GB")
    print(f"可用内存: {system_info['available_memory'] / (1024 ** 3):.2f} GB")
    
    # 打印GPU信息
    if 'gpus' in system_info and system_info['gpus']:
        print("\nGPU信息:")
        for i, gpu in enumerate(system_info['gpus']):
            print(f"  GPU {i+1}: {gpu['name']}")
            if 'video_memory' in gpu and gpu['video_memory']:
                print(f"    显存: {gpu['video_memory'] / (1024 ** 3):.2f} GB" if gpu['video_memory'] > 0 else "    显存: 未知")
            if 'is_integrated' in gpu:
                print(f"    类型: {'集成显卡' if gpu['is_integrated'] else '独立显卡'}")
            if 'driver_version' in gpu and gpu['driver_version'] != 'Unknown':
                print(f"    驱动版本: {gpu['driver_version']}")
    print()


if __name__ == "__main__":
    # 测试代码
    info = get_system_info()
    print_system_info(info)