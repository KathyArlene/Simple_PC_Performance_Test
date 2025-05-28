#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统信息收集模块
用于获取和显示系统硬件信息
支持多语言（中文、英文、日文、西班牙语）
"""

import platform
import psutil

# 导入多语言支持模块
import language as lang

# 尝试导入GPU信息检测库
try:
    import wmi
    HAS_WMI = True
except ImportError:
    HAS_WMI = False
    print(lang.get('warning_wmi_not_installed'))


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
            print(f"{lang.get('error_getting_gpu_info')}: {e}")
            info['gpus'] = [{'name': lang.get('unknown'), 'error': str(e)}]
    else:
        info['gpus'] = [{'name': lang.get('unknown'), 'error': lang.get('wmi_not_installed')}]
        
    return info


def print_system_info(system_info):
    """打印系统信息"""
    print("=" * 60)
    print(lang.get('system_info'))
    print("=" * 60)
    print(f"{lang.get('operating_system')}: {system_info['platform']}")
    print(f"{lang.get('processor')}: {system_info['processor']}")
    print(f"{lang.get('architecture')}: {system_info['architecture']}")
    print(f"{lang.get('physical_cpu_cores')}: {system_info['cpu_count']}")
    print(f"{lang.get('logical_cpu_cores')}: {system_info['logical_cpu_count']}")
    print(f"{lang.get('total_memory')}: {system_info['total_memory'] / (1024 ** 3):.2f} GB")
    print(f"{lang.get('available_memory')}: {system_info['available_memory'] / (1024 ** 3):.2f} GB")
    
    # 打印GPU信息
    if 'gpus' in system_info and system_info['gpus']:
        print(f"\n{lang.get('gpu_info')}:")
        for i, gpu in enumerate(system_info['gpus']):
            print(f"  GPU {i+1}: {gpu['name']}")
            if 'video_memory' in gpu and gpu['video_memory']:
                print(f"    {lang.get('video_memory')}: {gpu['video_memory'] / (1024 ** 3):.2f} GB" if gpu['video_memory'] > 0 else f"    {lang.get('video_memory')}: {lang.get('unknown')}")
            if 'is_integrated' in gpu:
                print(f"    {lang.get('gpu_type')}: {lang.get('integrated_gpu') if gpu['is_integrated'] else lang.get('discrete_gpu')}")
            if 'driver_version' in gpu and gpu['driver_version'] != 'Unknown':
                print(f"    {lang.get('driver_version')}: {gpu['driver_version']}")
    print()


if __name__ == "__main__":
    # 测试代码
    info = get_system_info()
    print_system_info(info)