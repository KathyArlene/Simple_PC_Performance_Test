#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统信息收集模块
用于获取和显示系统硬件信息
支持多语言（中文、英文、日文、西班牙语）
支持CPU和GPU频率、温度监测
"""

import platform
import psutil
import time
import subprocess
import re
import os

# 导入多语言支持模块
import language as lang

# 尝试导入GPU信息检测库
try:
    import wmi
    HAS_WMI = True
except ImportError:
    HAS_WMI = False
    print(lang.get('warning_wmi_not_installed'))

# 尝试导入OpenHardwareMonitor库
try:
    import clr
    # 添加OpenHardwareMonitor DLL引用
    ohm_dll_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'OpenHardwareMonitorLib.dll')
    if os.path.exists(ohm_dll_path):
        clr.AddReference(ohm_dll_path)
        from OpenHardwareMonitor.Hardware import Computer
        HAS_OHM = True
    else:
        HAS_OHM = False
        print(f"警告: 未找到OpenHardwareMonitor库 ({ohm_dll_path})")
except ImportError:
    HAS_OHM = False
    print("警告: 未安装pythonnet库，无法使用OpenHardwareMonitor。请使用 'pip install pythonnet' 安装。")


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
    
    # 获取GPU信息 - 使用多种方法提高检测成功率
    gpus = []
    gpu_detected = False
    
    # 方法1: 使用WMI (如果可用)
    if HAS_WMI:
        try:
            computer = wmi.WMI()
            gpu_infos = computer.Win32_VideoController()
            
            for i, gpu in enumerate(gpu_infos):
                if gpu.Name and gpu.Name.strip():
                    gpu_data = {
                        'name': gpu.Name,
                        'driver_version': gpu.DriverVersion if hasattr(gpu, 'DriverVersion') else 'Unknown',
                        'video_memory': gpu.AdapterRAM if hasattr(gpu, 'AdapterRAM') else 0,
                        'video_processor': gpu.VideoProcessor if hasattr(gpu, 'VideoProcessor') else 'Unknown',
                        'is_integrated': 'Intel' in gpu.Name or 'UHD' in gpu.Name or 'HD Graphics' in gpu.Name
                    }
                    gpus.append(gpu_data)
                    gpu_detected = True
                    print(f"通过WMI检测到GPU: {gpu.Name}")
        except Exception as e:
            print(f"WMI检测GPU失败: {e}")
    
    # 方法2: 使用wmic命令 (如果WMI失败或未安装)
    if not gpu_detected and platform.system() == "Windows":
        try:
            result = subprocess.run(['wmic', 'path', 'win32_VideoController', 
                                   'get', 'name'], capture_output=True, text=True, timeout=15)
            if result.returncode == 0:
                gpu_lines = [line.strip() for line in result.stdout.split('\n') 
                           if line.strip() and 'Name' not in line and line.strip() != '']
                for gpu_name in gpu_lines:
                    if gpu_name and gpu_name != 'Unknown':
                        gpu_data = {
                            'name': gpu_name,
                            'driver_version': 'Unknown',
                            'video_memory': 0,
                            'video_processor': 'Unknown',
                            'is_integrated': 'Intel' in gpu_name or 'UHD' in gpu_name or 'HD Graphics' in gpu_name
                        }
                        gpus.append(gpu_data)
                        gpu_detected = True
                        print(f"通过wmic检测到GPU: {gpu_name}")
        except Exception as e:
            print(f"wmic检测GPU失败: {e}")
    
    # 方法3: 使用PowerShell (Windows)
    if not gpu_detected and platform.system() == "Windows":
        try:
            ps_cmd = "Get-WmiObject -Class Win32_VideoController | Select-Object Name"
            result = subprocess.run(['powershell', '-Command', ps_cmd], 
                                  capture_output=True, text=True, timeout=15)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines[2:]:  # 跳过标题行
                    line = line.strip()
                    if line and line != '----' and line != 'Name':
                        gpu_data = {
                            'name': line,
                            'driver_version': 'Unknown',
                            'video_memory': 0,
                            'video_processor': 'Unknown',
                            'is_integrated': 'Intel' in line or 'UHD' in line or 'HD Graphics' in line
                        }
                        gpus.append(gpu_data)
                        gpu_detected = True
                        print(f"通过PowerShell检测到GPU: {line}")
        except Exception as e:
            print(f"PowerShell检测GPU失败: {e}")
    
    # 方法4: Linux系统使用lspci
    if not gpu_detected and platform.system() == "Linux":
        try:
            result = subprocess.run(['lspci'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'VGA' in line or 'Display' in line or '3D' in line:
                        gpu_info = line.split(':')[-1].strip()
                        if gpu_info:
                            gpu_data = {
                                'name': gpu_info,
                                'driver_version': 'Unknown',
                                'video_memory': 0,
                                'video_processor': 'Unknown',
                                'is_integrated': 'Intel' in gpu_info
                            }
                            gpus.append(gpu_data)
                            gpu_detected = True
                            print(f"通过lspci检测到GPU: {gpu_info}")
        except Exception as e:
            print(f"lspci检测GPU失败: {e}")
    
    # 如果所有方法都失败，添加默认GPU信息
    if not gpu_detected:
        print("所有GPU检测方法都失败，使用默认值")
        gpus = [{
            'name': lang.get('unknown') if 'lang' in globals() else 'Unknown GPU',
            'driver_version': 'Unknown',
            'video_memory': 0,
            'video_processor': 'Unknown',
            'is_integrated': False,
            'error': 'Detection failed'
        }]
    
    info['gpus'] = gpus
        
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


def get_cpu_stats():
    """获取CPU频率和温度信息
    
    Returns:
        dict: 包含CPU频率和温度的字典
    """
    stats = {
        'frequency': {},
        'temperature': {}
    }
    
    # 获取CPU频率
    try:
        cpu_freq = psutil.cpu_freq()
        if cpu_freq:
            stats['frequency']['current'] = cpu_freq.current
            if hasattr(cpu_freq, 'min'):
                stats['frequency']['min'] = cpu_freq.min
            if hasattr(cpu_freq, 'max'):
                stats['frequency']['max'] = cpu_freq.max
    except Exception as e:
        print(f"获取CPU频率失败: {e}")
    
    # 尝试使用OpenHardwareMonitor获取CPU温度
    if HAS_OHM:
        try:
            computer = Computer()
            computer.CPUEnabled = True
            computer.Open()
            
            for hardware in computer.Hardware:
                if hardware.HardwareType == 0:  # CPU
                    hardware.Update()
                    for sensor in hardware.Sensors:
                        if sensor.SensorType == 2:  # Temperature
                            stats['temperature'][sensor.Name] = sensor.Value
            
            computer.Close()
        except Exception as e:
            print(f"使用OpenHardwareMonitor获取CPU温度失败: {e}")
    
    # 已删除使用WMI获取CPU温度的代码
    
    return stats


def get_gpu_stats():
    """获取GPU频率和温度信息
    
    Returns:
        list: 包含每个GPU频率和温度的字典列表
    """
    gpu_stats = []
    
    # 尝试使用OpenHardwareMonitor获取GPU信息
    if HAS_OHM:
        try:
            computer = Computer()
            computer.GPUEnabled = True
            computer.Open()
            
            gpu_index = 0
            for hardware in computer.Hardware:
                if hardware.HardwareType == 1:  # GPU
                    hardware.Update()
                    gpu_data = {
                        'name': hardware.Name,
                        'frequency': {},
                        'temperature': {},
                        'fan': {}
                    }
                    
                    for sensor in hardware.Sensors:
                        if sensor.SensorType == 2:  # Temperature
                            gpu_data['temperature'][sensor.Name] = sensor.Value
                        elif sensor.SensorType == 3:  # Clock
                            gpu_data['frequency'][sensor.Name] = sensor.Value
                        elif sensor.SensorType == 4:  # Fan
                            gpu_data['fan'][sensor.Name] = sensor.Value
                    
                    gpu_stats.append(gpu_data)
                    gpu_index += 1
            
            computer.Close()
        except Exception as e:
            print(f"使用OpenHardwareMonitor获取GPU信息失败: {e}")
    
    # 如果OpenHardwareMonitor不可用或未获取到数据，尝试使用NVIDIA-SMI（仅适用于NVIDIA显卡）
    if not gpu_stats:
        try:
            # 检查是否有NVIDIA显卡
            nvidia_smi_output = subprocess.check_output(['nvidia-smi', '--query-gpu=name,temperature.gpu,clocks.current.graphics,clocks.current.memory', '--format=csv,noheader,nounits'], universal_newlines=True)
            
            for i, line in enumerate(nvidia_smi_output.strip().split('\n')):
                values = [x.strip() for x in line.split(',')]
                if len(values) >= 4:
                    gpu_data = {
                        'name': values[0],
                        'temperature': {'GPU': float(values[1])},
                        'frequency': {
                            'Graphics': float(values[2]),
                            'Memory': float(values[3])
                        }
                    }
                    gpu_stats.append(gpu_data)
        except (subprocess.SubprocessError, FileNotFoundError, ValueError) as e:
            # NVIDIA-SMI不可用或出错，忽略
            pass
    
    # 如果仍然没有数据，尝试使用WMI获取基本信息
    if not gpu_stats and HAS_WMI:
        try:
            w = wmi.WMI()
            gpu_infos = w.Win32_VideoController()
            
            for i, gpu in enumerate(gpu_infos):
                gpu_data = {
                    'name': gpu.Name,
                    'frequency': {},
                    'temperature': {}
                }
                
                # WMI通常无法获取GPU频率和温度，但我们至少可以获取名称
                gpu_stats.append(gpu_data)
        except Exception as e:
            print(f"使用WMI获取GPU信息失败: {e}")
    
    return gpu_stats


def get_hardware_stats():
    """获取硬件实时状态（CPU和GPU的频率、温度等）
    
    Returns:
        dict: 包含CPU和GPU状态的字典
    """
    stats = {
        'timestamp': time.time(),
        'cpu': {
            'usage_percent': psutil.cpu_percent(interval=0.1, percpu=True),
            'stats': get_cpu_stats()
        },
        'gpu': get_gpu_stats()
    }
    
    return stats


if __name__ == "__main__":
    # 测试代码
    info = get_system_info()
    print_system_info(info)
    
    print("\n获取硬件实时状态...")
    stats = get_hardware_stats()
    
    print("\nCPU状态:")
    print(f"使用率: {stats['cpu']['usage_percent']}")
    if 'frequency' in stats['cpu']['stats']:
        print(f"频率: {stats['cpu']['stats']['frequency']}")
    if 'temperature' in stats['cpu']['stats']:
        print(f"温度: {stats['cpu']['stats']['temperature']}")
    
    print("\nGPU状态:")
    for i, gpu in enumerate(stats['gpu']):
        print(f"GPU {i+1}: {gpu['name']}")
        if 'temperature' in gpu and gpu['temperature']:
            print(f"  温度: {gpu['temperature']}")
        if 'frequency' in gpu and gpu['frequency']:
            print(f"  频率: {gpu['frequency']}")
        if 'fan' in gpu and gpu['fan']:
            print(f"  风扇: {gpu['fan']}")