# -*- coding: utf-8 -*-
"""
硬件检测模块
用于检测CPU和GPU型号，并根据性能基准数据调整测试负载
"""

import platform
import subprocess
import re
import psutil
import os

class HardwareDetector:
    """硬件检测器"""
    
    def __init__(self):
        # CPU性能数据库 (Cinebench R23 单核分数)
        self.cpu_benchmarks = {
            # Intel 最高端
            'Intel Core i9-14900KS': 2375,
            'Intel Core i9-14900KF': 2290,
            'Intel Core i9-14900K': 2293,
            'Intel Core i9-13900KS': 2339,
            'Intel Core i9-13900KF': 2262,
            'Intel Core i9-13900K': 2076,
            'Intel Core i9-13900': 2191,
            'Intel Core i7-14700KF': 2160,
            'Intel Core i7-14700K': 2072,
            'Intel Core i7-13700KF': 2126,
            'Intel Core i7-13700K': 2126,
            'Intel Core i7-13700': 2107,
            'Intel Core i5-14600KF': 2097,
            'Intel Core i5-14600K': 2097,
            'Intel Core i5-13600K': 1950,
            'Intel Core i5-12600K': 1850,
            'Intel Core i5-12400': 1700,
            'Intel Core i3-12100': 1500,
            'Intel Core i3-10100': 1100,
            
            # AMD 高端
            'AMD Ryzen 9 9950X3D': 2242,
            'AMD Ryzen 9 9950X': 2243,
            'AMD Ryzen 9 9900X3D': 2190,
            'AMD Ryzen 9 9900X': 2231,
            'AMD Ryzen 9 7950X3D': 2053,
            'AMD Ryzen 9 7950X': 2009,
            'AMD Ryzen 7 9700X': 2206,
            'AMD Ryzen 7 7700X': 1950,
            'AMD Ryzen 5 9600X': 2163,
            'AMD Ryzen 5 7600X': 1900,
            'AMD Ryzen 5 5600X': 1600,
            'AMD Ryzen 5 3600': 1200,
            'AMD Ryzen 3 3300X': 1200,
        }
        
        # GPU性能数据库 (3DMark TimeSpy Graphics Score)
        self.gpu_benchmarks = {
            # NVIDIA RTX 50系列 (未来)
            'RTX 5090': 55000,
            
            # NVIDIA RTX 40系列
            'RTX 4090': 35000,
            'RTX 4080 Super': 28500,
            'RTX 4080': 28000,
            'RTX 4070 Ti Super': 23500,
            'RTX 4070 Ti': 22000,
            'RTX 4070 Super': 19500,
            'RTX 4070': 18000,
            'RTX 4060 Ti 16GB': 14500,
            'RTX 4060 Ti': 14000,
            'RTX 4060': 11000,
            
            # NVIDIA RTX 30系列
            'RTX 3090 Ti': 19500,
            'RTX 3090': 19000,
            'RTX 3080 Ti': 18000,
            'RTX 3080': 17000,
            'RTX 3070 Ti': 14000,
            'RTX 3070': 13000,
            'RTX 3060 Ti': 11000,
            'RTX 3060': 8500,
            'RTX 3050': 6000,
            
            # NVIDIA GTX系列
            'GTX 1660 Ti': 6000,
            'GTX 1660 Super': 5800,
            'GTX 1660': 5500,
            'GTX 1650 Super': 4200,
            'GTX 1650': 3500,
            'GTX 1050 Ti': 3000,
            'GTX 1050': 2500,
            
            # AMD RX 7000系列
            'RX 7900 XTX': 24000,
            'RX 7900 XT': 20000,
            'RX 7800 XT': 16000,
            'RX 7700 XT': 13000,
            'RX 7600': 10000,
            
            # AMD RX 6000系列
            'RX 6950 XT': 16500,
            'RX 6900 XT': 16000,
            'RX 6800 XT': 15000,
            'RX 6800': 13500,
            'RX 6750 XT': 12500,
            'RX 6700 XT': 12000,
            'RX 6650 XT': 10500,
            'RX 6600 XT': 10000,
            'RX 6600': 8000,
            'RX 6500 XT': 5500,
            
            # AMD RX 5000系列及更早
            'RX 5700 XT': 9000,
            'RX 5700': 8000,
            'RX 580': 4000,
            'RX 570': 3500,
            'RX 560': 2500,
        }
    
    def extract_cpu_model(self, cpu_name):
        """从完整的CPU名称中提取具体型号（如i3、i5、i7等）"""
        if not cpu_name or cpu_name == 'Unknown CPU':
            return cpu_name
        
        cpu_upper = cpu_name.upper()
        
        # Intel处理器型号提取
        intel_patterns = [
            r'CORE\s+I9[\-\s]*(\d+\w*)',  # i9系列
            r'CORE\s+I7[\-\s]*(\d+\w*)',  # i7系列
            r'CORE\s+I5[\-\s]*(\d+\w*)',  # i5系列
            r'CORE\s+I3[\-\s]*(\d+\w*)',  # i3系列
            r'(I9[\-\s]*\d+\w*)',         # 简化i9
            r'(I7[\-\s]*\d+\w*)',         # 简化i7
            r'(I5[\-\s]*\d+\w*)',         # 简化i5
            r'(I3[\-\s]*\d+\w*)',         # 简化i3
            r'(PENTIUM\s+\w+)',           # 奔腾系列
            r'(CELERON\s+\w+)',           # 赛扬系列
            r'(ATOM\s+\w+)'               # 凌动系列
        ]
        
        # AMD处理器型号提取
        amd_patterns = [
            r'RYZEN\s+9\s+(\d+\w*)',     # Ryzen 9系列
            r'RYZEN\s+7\s+(\d+\w*)',     # Ryzen 7系列
            r'RYZEN\s+5\s+(\d+\w*)',     # Ryzen 5系列
            r'RYZEN\s+3\s+(\d+\w*)',     # Ryzen 3系列
            r'(RYZEN\s+\d+\s+\d+\w*)',   # 通用Ryzen
            r'(ATHLON\s+\w+)',           # 速龙系列
            r'(FX[\-\s]*\d+\w*)'         # FX系列
        ]
        
        # 尝试Intel模式匹配
        for pattern in intel_patterns:
            match = re.search(pattern, cpu_upper)
            if match:
                if 'CORE' in pattern:
                    # 提取完整的Intel Core型号
                    if 'I9' in cpu_upper:
                        return f"Intel Core i9-{match.group(1)}"
                    elif 'I7' in cpu_upper:
                        return f"Intel Core i7-{match.group(1)}"
                    elif 'I5' in cpu_upper:
                        return f"Intel Core i5-{match.group(1)}"
                    elif 'I3' in cpu_upper:
                        return f"Intel Core i3-{match.group(1)}"
                else:
                    return f"Intel Core {match.group(1).replace('-', '-').replace(' ', '-')}"
        
        # 尝试AMD模式匹配
        for pattern in amd_patterns:
            match = re.search(pattern, cpu_upper)
            if match:
                if 'RYZEN' in pattern and 'RYZEN\s+\d+\s+\d+' not in pattern:
                    # 提取Ryzen系列型号
                    if 'RYZEN 9' in cpu_upper:
                        return f"AMD Ryzen 9 {match.group(1)}"
                    elif 'RYZEN 7' in cpu_upper:
                        return f"AMD Ryzen 7 {match.group(1)}"
                    elif 'RYZEN 5' in cpu_upper:
                        return f"AMD Ryzen 5 {match.group(1)}"
                    elif 'RYZEN 3' in cpu_upper:
                        return f"AMD Ryzen 3 {match.group(1)}"
                else:
                    return f"AMD {match.group(1)}"
        
        # 如果没有匹配到具体型号，尝试提取品牌和基本信息
        if 'INTEL' in cpu_upper:
            if 'I9' in cpu_upper:
                return "Intel Core i9 (未知型号)"
            elif 'I7' in cpu_upper:
                return "Intel Core i7 (未知型号)"
            elif 'I5' in cpu_upper:
                return "Intel Core i5 (未知型号)"
            elif 'I3' in cpu_upper:
                return "Intel Core i3 (未知型号)"
            elif 'PENTIUM' in cpu_upper:
                return "Intel Pentium"
            elif 'CELERON' in cpu_upper:
                return "Intel Celeron"
            else:
                return "Intel 处理器"
        elif 'AMD' in cpu_upper:
            if 'RYZEN' in cpu_upper:
                if 'RYZEN 9' in cpu_upper:
                    return "AMD Ryzen 9 (未知型号)"
                elif 'RYZEN 7' in cpu_upper:
                    return "AMD Ryzen 7 (未知型号)"
                elif 'RYZEN 5' in cpu_upper:
                    return "AMD Ryzen 5 (未知型号)"
                elif 'RYZEN 3' in cpu_upper:
                    return "AMD Ryzen 3 (未知型号)"
                else:
                    return "AMD Ryzen (未知型号)"
            elif 'ATHLON' in cpu_upper:
                return "AMD Athlon"
            elif 'FX' in cpu_upper:
                return "AMD FX"
            else:
                return "AMD 处理器"
        
        # 返回原始名称（如果无法识别）
        return cpu_name
    
    def get_cpu_info(self):
        """获取CPU信息 - 使用多种方法提高检测成功率"""
        cpu_name = 'Unknown CPU'
        
        # 方法1: 使用platform.processor()
        try:
            cpu_name = platform.processor()
            if cpu_name and cpu_name.strip() and cpu_name != 'Unknown':
                print(f"通过platform.processor()检测到CPU: {cpu_name}")
            else:
                cpu_name = None
        except Exception as e:
            print(f"platform.processor()检测失败: {e}")
            cpu_name = None
        
        # 方法2: 使用wmic (Windows)
        if not cpu_name and platform.system() == "Windows":
            try:
                result = subprocess.run(['wmic', 'cpu', 'get', 'name'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
                    if len(lines) > 1 and lines[1] != 'Name':
                        cpu_name = lines[1]
                        print(f"通过wmic检测到CPU: {cpu_name}")
            except Exception as e:
                print(f"wmic检测CPU失败: {e}")
        
        # 方法3: 使用注册表 (Windows)
        if not cpu_name and platform.system() == "Windows":
            try:
                result = subprocess.run(['reg', 'query', 
                                       'HKEY_LOCAL_MACHINE\\HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0', 
                                       '/v', 'ProcessorNameString'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if 'ProcessorNameString' in line:
                            cpu_name = line.split('REG_SZ')[1].strip()
                            print(f"通过注册表检测到CPU: {cpu_name}")
                            break
            except Exception as e:
                print(f"注册表检测CPU失败: {e}")
        
        # 方法4: 使用/proc/cpuinfo (Linux)
        if not cpu_name and platform.system() == "Linux":
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    for line in f:
                        if 'model name' in line:
                            cpu_name = line.split(':')[1].strip()
                            print(f"通过/proc/cpuinfo检测到CPU: {cpu_name}")
                            break
            except Exception as e:
                print(f"/proc/cpuinfo检测CPU失败: {e}")
        
        # 如果所有方法都失败，使用默认值
        if not cpu_name or cpu_name.strip() == '':
            cpu_name = 'Unknown CPU'
            print("所有CPU检测方法都失败，使用默认值")
        
        # 提取CPU型号
        cpu_model = self.extract_cpu_model(cpu_name)
        print(f"提取的CPU型号: {cpu_model}")
        
        # 获取CPU核心数
        try:
            cpu_cores = psutil.cpu_count(logical=False) or 4
            cpu_threads = psutil.cpu_count(logical=True) or 8
        except Exception as e:
            print(f"获取CPU核心数失败: {e}")
            cpu_cores = 4
            cpu_threads = 8
        
        return {
            'name': cpu_model,  # 使用提取的型号而不是原始名称
            'full_name': cpu_name,  # 保留完整名称用于调试
            'cores': cpu_cores,
            'threads': cpu_threads
        }
    
    def get_gpu_info(self):
        """获取GPU信息 - 使用多种方法提高检测成功率"""
        gpu_name = 'Unknown GPU'
        
        if platform.system() == "Windows":
            # 方法1: 使用wmic获取GPU信息
            try:
                result = subprocess.run(['wmic', 'path', 'win32_VideoController', 
                                       'get', 'name'], capture_output=True, text=True, timeout=15)
                if result.returncode == 0:
                    gpu_lines = [line.strip() for line in result.stdout.split('\n') 
                               if line.strip() and 'Name' not in line and line.strip() != '']
                    if gpu_lines:
                        # 优先选择独立显卡
                        for line in gpu_lines:
                            if any(keyword in line.upper() for keyword in ['NVIDIA', 'AMD', 'RADEON', 'GTX', 'RTX', 'RX']):
                                gpu_name = line
                                print(f"通过wmic检测到独立GPU: {gpu_name}")
                                break
                        else:
                            gpu_name = gpu_lines[0]
                            print(f"通过wmic检测到GPU: {gpu_name}")
            except Exception as e:
                print(f"wmic检测GPU失败: {e}")
            
            # 方法2: 使用PowerShell获取GPU信息
            if gpu_name == 'Unknown GPU':
                try:
                    ps_cmd = "Get-WmiObject -Class Win32_VideoController | Select-Object Name"
                    result = subprocess.run(['powershell', '-Command', ps_cmd], 
                                          capture_output=True, text=True, timeout=15)
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')
                        for line in lines[2:]:  # 跳过标题行
                            line = line.strip()
                            if line and line != '----':
                                if any(keyword in line.upper() for keyword in ['NVIDIA', 'AMD', 'RADEON', 'GTX', 'RTX', 'RX']):
                                    gpu_name = line
                                    print(f"通过PowerShell检测到独立GPU: {gpu_name}")
                                    break
                                elif gpu_name == 'Unknown GPU':
                                    gpu_name = line
                                    print(f"通过PowerShell检测到GPU: {gpu_name}")
                except Exception as e:
                    print(f"PowerShell检测GPU失败: {e}")
            
            # 方法3: 使用dxdiag (Windows)
            if gpu_name == 'Unknown GPU':
                try:
                    result = subprocess.run(['dxdiag', '/t', 'temp_dxdiag.txt'], 
                                          capture_output=True, text=True, timeout=20)
                    if os.path.exists('temp_dxdiag.txt'):
                        with open('temp_dxdiag.txt', 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            # 查找显卡信息
                            lines = content.split('\n')
                            for i, line in enumerate(lines):
                                if 'Card name:' in line or 'Chip type:' in line:
                                    gpu_info = line.split(':')[1].strip()
                                    if gpu_info and gpu_info != 'Unknown':
                                        gpu_name = gpu_info
                                        print(f"通过dxdiag检测到GPU: {gpu_name}")
                                        break
                        os.remove('temp_dxdiag.txt')
                except Exception as e:
                    print(f"dxdiag检测GPU失败: {e}")
                    if os.path.exists('temp_dxdiag.txt'):
                        try:
                            os.remove('temp_dxdiag.txt')
                        except:
                            pass
        
        else:
            # Linux系统使用lspci
            try:
                result = subprocess.run(['lspci'], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if 'VGA' in line or 'Display' in line or '3D' in line:
                            gpu_info = line.split(':')[-1].strip()
                            if gpu_info:
                                gpu_name = gpu_info
                                print(f"通过lspci检测到GPU: {gpu_name}")
                                break
            except Exception as e:
                print(f"lspci检测GPU失败: {e}")
        
        # 如果所有方法都失败，使用默认值
        if not gpu_name or gpu_name.strip() == '' or gpu_name == 'Unknown GPU':
            gpu_name = 'Unknown GPU'
            print("所有GPU检测方法都失败，使用默认值")
        
        return {'name': gpu_name}
    
    def estimate_cpu_performance(self, cpu_name):
        """估算CPU性能等级"""
        cpu_name_upper = cpu_name.upper()
        
        # 查找匹配的CPU型号
        for model, score in self.cpu_benchmarks.items():
            if model.upper() in cpu_name_upper:
                return score
        
        # 基于关键词估算
        if any(keyword in cpu_name_upper for keyword in ['I9', 'RYZEN 9']):
            return 35000  # 高端
        elif any(keyword in cpu_name_upper for keyword in ['I7', 'RYZEN 7']):
            return 25000  # 中高端
        elif any(keyword in cpu_name_upper for keyword in ['I5', 'RYZEN 5']):
            return 18000  # 中端
        elif any(keyword in cpu_name_upper for keyword in ['I3', 'RYZEN 3']):
            return 10000  # 低端
        elif any(keyword in cpu_name_upper for keyword in ['PENTIUM', 'CELERON', 'ATOM']):
            return 5000   # 入门级
        else:
            return 12000  # 默认中等性能
    
    def estimate_gpu_performance(self, gpu_name):
        """估算GPU性能等级"""
        gpu_name_upper = gpu_name.upper()
        
        # 查找匹配的GPU型号
        for model, score in self.gpu_benchmarks.items():
            if model.upper() in gpu_name_upper:
                return score
        
        # 基于关键词估算
        if any(keyword in gpu_name_upper for keyword in ['RTX 4090', 'RTX 4080']):
            return 30000  # 顶级
        elif any(keyword in gpu_name_upper for keyword in ['RTX 4070', 'RTX 3080', 'RX 7900']):
            return 20000  # 高端
        elif any(keyword in gpu_name_upper for keyword in ['RTX 4060', 'RTX 3070', 'RX 7700', 'RX 6700']):
            return 12000  # 中端
        elif any(keyword in gpu_name_upper for keyword in ['RTX 3060', 'GTX 1660', 'RX 6600']):
            return 8000   # 中低端
        elif any(keyword in gpu_name_upper for keyword in ['GTX 1650', 'GTX 1050', 'RX 580']):
            return 4000   # 低端
        elif any(keyword in gpu_name_upper for keyword in ['UHD', 'IRIS', 'VEGA']):
            return 2000   # 集显
        else:
            return 6000   # 默认中等性能
    
    def get_performance_tier(self, cpu_score, gpu_score):
        """根据CPU和GPU性能确定硬件等级"""
        # CPU等级判断 - 基于Cinebench R23单核分数
        if cpu_score >= 2000:  # 高端：2000+分
            cpu_tier = 'high'
        elif cpu_score >= 1500:  # 中端：1500-2000分
            cpu_tier = 'medium'
        else:  # 低端：<1500分
            cpu_tier = 'low'
        
        # GPU等级判断 - 基于3DMark TimeSpy Graphics Score
        if gpu_score >= 20000:  # 高端：20000+分
            gpu_tier = 'high'
        elif gpu_score >= 8000:  # 中端：8000-20000分
            gpu_tier = 'medium'
        else:  # 低端：<8000分
            gpu_tier = 'low'
        
        return cpu_tier, gpu_tier
    
    def get_test_parameters(self, cpu_tier, gpu_tier):
        """根据硬件等级返回测试参数"""
        # CPU测试参数
        cpu_params = {
            'high': {
                'single_duration': 10,
                'multi_duration': 10,
                'max_threads': 0,  # 0表示使用所有线程
                'calculation_count': 2000000
            },
            'medium': {
                'single_duration': 8,
                'multi_duration': 8,
                'max_threads': 8,
                'calculation_count': 1000000
            },
            'low': {
                'single_duration': 5,
                'multi_duration': 5,
                'max_threads': 4,
                'calculation_count': 500000
            }
        }
        
        # GPU测试参数
        gpu_params = {
            'high': {'max_load': 1.0},      # 100%负载
            'medium': {'max_load': 0.7},    # 70%负载
            'low': {'max_load': 0.5}        # 50%负载
        }
        
        # 内存测试参数
        memory_params = {
            'high': {'size_mb': 500, 'max_block_mb': 50},
            'medium': {'size_mb': 300, 'max_block_mb': 30},
            'low': {'size_mb': 200, 'max_block_mb': 20}
        }
        
        # 磁盘测试参数
        disk_params = {
            'high': {'file_size_mb': 200},
            'medium': {'file_size_mb': 100},
            'low': {'file_size_mb': 50}
        }
        
        # 选择较低的等级以确保稳定性
        overall_tier = 'low' if cpu_tier == 'low' or gpu_tier == 'low' else (
            'medium' if cpu_tier == 'medium' or gpu_tier == 'medium' else 'high'
        )
        
        return {
            'cpu': cpu_params[cpu_tier],
            'gpu': gpu_params[gpu_tier],
            'memory': memory_params[overall_tier],
            'disk': disk_params[overall_tier]
        }
    
    def detect_and_configure(self):
        """检测硬件并返回配置参数"""
        # 获取硬件信息
        cpu_info = self.get_cpu_info()
        gpu_info = self.get_gpu_info()
        
        # 估算性能
        cpu_score = self.estimate_cpu_performance(cpu_info['name'])
        gpu_score = self.estimate_gpu_performance(gpu_info['name'])
        
        # 确定性能等级
        cpu_tier, gpu_tier = self.get_performance_tier(cpu_score, gpu_score)
        
        # 获取测试参数
        test_params = self.get_test_parameters(cpu_tier, gpu_tier)
        
        return {
            'hardware_info': {
                'cpu': cpu_info,
                'gpu': gpu_info,
                'cpu_score': cpu_score,
                'gpu_score': gpu_score,
                'cpu_tier': cpu_tier,
                'gpu_tier': gpu_tier
            },
            'test_parameters': test_params
        }

if __name__ == '__main__':
    # 测试硬件检测功能
    detector = HardwareDetector()
    result = detector.detect_and_configure()
    
    print("硬件信息:")
    print(f"CPU: {result['hardware_info']['cpu']['name']}")
    print(f"GPU: {result['hardware_info']['gpu']['name']}")
    print(f"CPU性能分数: {result['hardware_info']['cpu_score']}")
    print(f"GPU性能分数: {result['hardware_info']['gpu_score']}")
    print(f"CPU等级: {result['hardware_info']['cpu_tier']}")
    print(f"GPU等级: {result['hardware_info']['gpu_tier']}")
    print("\n推荐测试参数:")
    print(f"CPU参数: {result['test_parameters']['cpu']}")
    print(f"GPU参数: {result['test_parameters']['gpu']}")
    print(f"内存参数: {result['test_parameters']['memory']}")
    print(f"磁盘参数: {result['test_parameters']['disk']}")