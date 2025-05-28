#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电脑性能测试工具
测试CPU、内存、磁盘I/O性能
"""

import time
import os
import sys
import platform
import psutil
import threading
import multiprocessing
import tempfile
import random
import math
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import json
import numpy as np

# 尝试导入GPU相关库
try:
    import wmi
    HAS_WMI = True
except ImportError:
    HAS_WMI = False
    print("警告: 未安装wmi库，GPU信息检测将不可用。请使用 'pip install wmi' 安装。")

# 尝试导入PyOpenCL用于GPU测试
try:
    import pyopencl as cl
    HAS_OPENCL = True
except ImportError:
    HAS_OPENCL = False
    print("警告: 未安装pyopencl库，GPU性能测试将不可用。请使用 'pip install pyopencl' 安装。")


class PerformanceBenchmark:
    def __init__(self):
        self.results = {}
        self.system_info = self.get_system_info()

    def get_system_info(self):
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

    def print_system_info(self):
        """打印系统信息"""
        print("=" * 60)
        print("系统信息")
        print("=" * 60)
        print(f"操作系统: {self.system_info['platform']}")
        print(f"处理器: {self.system_info['processor']}")
        print(f"架构: {self.system_info['architecture']}")
        print(f"物理CPU核心: {self.system_info['cpu_count']}")
        print(f"逻辑CPU核心: {self.system_info['logical_cpu_count']}")
        print(f"总内存: {self.system_info['total_memory'] / (1024 ** 3):.2f} GB")
        print(f"可用内存: {self.system_info['available_memory'] / (1024 ** 3):.2f} GB")
        
        # 打印GPU信息
        if 'gpus' in self.system_info and self.system_info['gpus']:
            print("\nGPU信息:")
            for i, gpu in enumerate(self.system_info['gpus']):
                print(f"  GPU {i+1}: {gpu['name']}")
                if 'video_memory' in gpu and gpu['video_memory']:
                    print(f"    显存: {gpu['video_memory'] / (1024 ** 3):.2f} GB" if gpu['video_memory'] > 0 else "    显存: 未知")
                if 'is_integrated' in gpu:
                    print(f"    类型: {'集成显卡' if gpu['is_integrated'] else '独立显卡'}")
                if 'driver_version' in gpu and gpu['driver_version'] != 'Unknown':
                    print(f"    驱动版本: {gpu['driver_version']}")
        print()

    def cpu_single_thread_test(self, duration=5):
        """单线程CPU测试"""
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
                if count >= 10000:  # 计算10000个素数
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

    def cpu_multi_thread_test(self, duration=5):
        """多线程CPU测试"""
        print("正在进行多线程CPU测试...")

        def worker_task():
            """工作线程任务"""
            count = 0
            # 使用绝对值确保结果为正数
            for i in range(1000000):
                count += abs(math.sqrt(i) * math.sin(i))
            return count

        num_threads = self.system_info['logical_cpu_count']

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

    def memory_test(self):
        """内存性能测试"""
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

    def disk_io_test(self, file_size_mb=100):
        """磁盘I/O性能测试"""
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

    def network_test(self):
        """网络性能测试（模拟）"""
        print("正在进行网络性能测试（本地回环）...")

        import socket
        import threading

        def server_thread():
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(('localhost', 0))
            port = server.getsockname()[1]
            server.listen(1)

            conn, addr = server.accept()
            data_received = 0
            start_time = time.time()

            while True:
                data = conn.recv(4096)
                if not data:
                    break
                data_received += len(data)

            end_time = time.time()
            conn.close()
            server.close()

            return data_received, end_time - start_time, port

        # 启动服务器线程
        server_thread_obj = threading.Thread(target=server_thread)
        server_thread_obj.daemon = True
        server_thread_obj.start()

        time.sleep(0.1)  # 等待服务器启动

        # 客户端发送数据
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect(('localhost', 12345))  # 简化版本，使用固定端口

            data = b'x' * 1024  # 1KB数据
            total_sent = 0
            start_time = time.time()

            for _ in range(1000):  # 发送1000次，总共1MB
                client.send(data)
                total_sent += len(data)

            client.close()
            end_time = time.time()

            transfer_time = end_time - start_time
            throughput = (total_sent / (1024 * 1024)) / transfer_time  # MB/s

            print(f"网络测试完成:")
            print(f"  传输数据: {total_sent / (1024 * 1024):.2f} MB")
            print(f"  传输时间: {transfer_time:.2f} 秒")
            print(f"  吞吐量: {throughput:.2f} MB/s")

            return {
                'data_transferred_mb': total_sent / (1024 * 1024),
                'transfer_time': transfer_time,
                'throughput_mb_s': throughput
            }

        except Exception as e:
            print(f"网络测试失败: {e}")
            return None

    def gpu_test(self):
        """GPU性能测试（如果有的话）"""
        print("正在进行GPU性能测试...")
        
        # 检查是否有GPU
        if not 'gpus' in self.system_info or not self.system_info['gpus'] or self.system_info['gpus'][0]['name'] == '未知':
            print("未检测到GPU或无法获取GPU信息，跳过GPU测试")
            return None
            
        # 使用NumPy进行简单的矩阵运算测试
        try:
            # 创建大型矩阵
            matrix_size = 2000
            print(f"  测试 {matrix_size}x{matrix_size} 矩阵乘法...")
            
            # 创建随机矩阵
            matrix_a = np.random.rand(matrix_size, matrix_size).astype(np.float32)
            matrix_b = np.random.rand(matrix_size, matrix_size).astype(np.float32)
            
            # CPU测试作为基准
            start_time = time.time()
            result_cpu = np.dot(matrix_a, matrix_b)
            cpu_time = time.time() - start_time
            
            print(f"    CPU矩阵乘法时间: {cpu_time:.4f} 秒")
            
            # 如果有OpenCL，尝试GPU测试
            gpu_time = None
            if HAS_OPENCL:
                try:
                    # 获取平台和设备
                    platforms = cl.get_platforms()
                    if platforms:
                        # 尝试获取GPU设备，如果没有则使用CPU
                        devices = platforms[0].get_devices(device_type=cl.device_type.GPU)
                        if not devices:
                            devices = platforms[0].get_devices(device_type=cl.device_type.CPU)
                            
                        if devices:
                            # 创建上下文和队列
                            ctx = cl.Context([devices[0]])
                            queue = cl.CommandQueue(ctx)
                            
                            # 创建缓冲区
                            mf = cl.mem_flags
                            a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=matrix_a)
                            b_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=matrix_b)
                            c_buf = cl.Buffer(ctx, mf.WRITE_ONLY, matrix_a.nbytes)
                            
                            # 创建并编译OpenCL程序
                            prg = cl.Program(ctx, """
                            __kernel void matrix_mul(__global float *a, __global float *b, __global float *c, const int size) {
                                int gid = get_global_id(0);
                                int row = gid / size;
                                int col = gid % size;
                                float sum = 0.0f;
                                for (int i = 0; i < size; i++) {
                                    sum += a[row * size + i] * b[i * size + col];
                                }
                                c[row * size + col] = sum;
                            }
                            """).build()
                            
                            # 执行内核
                            start_time = time.time()
                            event = prg.matrix_mul(queue, (matrix_size * matrix_size,), None, a_buf, b_buf, c_buf, np.int32(matrix_size))
                            event.wait()
                            
                            # 获取结果
                            result_gpu = np.empty_like(matrix_a)
                            cl.enqueue_copy(queue, result_gpu, c_buf)
                            gpu_time = time.time() - start_time
                            
                            # 验证结果
                            if np.allclose(result_cpu, result_gpu, rtol=1e-5):
                                print(f"    GPU矩阵乘法时间: {gpu_time:.4f} 秒")
                                if gpu_time > 0 and cpu_time > 0:
                                    speedup = cpu_time / gpu_time
                                    print(f"    GPU加速比: {speedup:.2f}x")
                            else:
                                print("    GPU计算结果与CPU不匹配，可能存在精度问题")
                                gpu_time = None
                except Exception as e:
                    print(f"    OpenCL GPU测试失败: {e}")
            else:
                print("    未安装PyOpenCL，无法进行GPU加速测试")
                
            # 返回测试结果
            result = {
                'matrix_size': matrix_size,
                'cpu_time': cpu_time,
                'operations': matrix_size * matrix_size * (2 * matrix_size - 1),  # 矩阵乘法的操作次数
                'cpu_gflops': (matrix_size * matrix_size * (2 * matrix_size - 1)) / (cpu_time * 1e9) if cpu_time > 0 else 0
            }
            
            if gpu_time:
                result['gpu_time'] = gpu_time
                result['gpu_gflops'] = (matrix_size * matrix_size * (2 * matrix_size - 1)) / (gpu_time * 1e9) if gpu_time > 0 else 0
                result['speedup'] = cpu_time / gpu_time if gpu_time > 0 else 0
                
            return result
            
        except Exception as e:
            print(f"GPU测试失败: {e}")
            import traceback
            traceback.print_exc()
            return None
            
    def gpu_test(self):
        """GPU性能测试 - 使用矩阵乘法基准测试"""
        print("正在进行GPU性能测试...")
        
        # 检查是否有GPU
        if not 'gpus' in self.system_info or not self.system_info['gpus'] or self.system_info['gpus'][0]['name'] == '未知':
            print("未检测到GPU或无法获取GPU信息，跳过GPU测试")
            return None
            
        # 使用NumPy进行简单的矩阵运算测试
        try:
            # 创建大型矩阵
            matrix_size = 2000
            print(f"  测试 {matrix_size}x{matrix_size} 矩阵乘法...")
            
            # 创建随机矩阵
            matrix_a = np.random.rand(matrix_size, matrix_size).astype(np.float32)
            matrix_b = np.random.rand(matrix_size, matrix_size).astype(np.float32)
            
            # CPU测试作为基准
            start_time = time.time()
            result_cpu = np.dot(matrix_a, matrix_b)
            cpu_time = time.time() - start_time
            
            print(f"    CPU矩阵乘法时间: {cpu_time:.4f} 秒")
            
            # 如果有OpenCL，尝试GPU测试
            gpu_time = None
            if HAS_OPENCL:
                try:
                    # 获取平台和设备
                    platforms = cl.get_platforms()
                    if platforms:
                        # 尝试获取GPU设备，如果没有则使用CPU
                        devices = platforms[0].get_devices(device_type=cl.device_type.GPU)
                        if not devices:
                            devices = platforms[0].get_devices(device_type=cl.device_type.CPU)
                            
                        if devices:
                            # 创建上下文和队列
                            ctx = cl.Context([devices[0]])
                            queue = cl.CommandQueue(ctx)
                            
                            # 创建缓冲区
                            mf = cl.mem_flags
                            a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=matrix_a)
                            b_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=matrix_b)
                            c_buf = cl.Buffer(ctx, mf.WRITE_ONLY, matrix_a.nbytes)
                            
                            # 创建并编译OpenCL程序
                            prg = cl.Program(ctx, """
                            __kernel void matrix_mul(__global float *a, __global float *b, __global float *c, const int size) {
                                int gid = get_global_id(0);
                                int row = gid / size;
                                int col = gid % size;
                                float sum = 0.0f;
                                for (int i = 0; i < size; i++) {
                                    sum += a[row * size + i] * b[i * size + col];
                                }
                                c[row * size + col] = sum;
                            }
                            """).build()
                            
                            # 执行内核
                            start_time = time.time()
                            event = prg.matrix_mul(queue, (matrix_size * matrix_size,), None, a_buf, b_buf, c_buf, np.int32(matrix_size))
                            event.wait()
                            
                            # 获取结果
                            result_gpu = np.empty_like(matrix_a)
                            cl.enqueue_copy(queue, result_gpu, c_buf)
                            gpu_time = time.time() - start_time
                            
                            # 验证结果
                            if np.allclose(result_cpu, result_gpu, rtol=1e-5):
                                print(f"    GPU矩阵乘法时间: {gpu_time:.4f} 秒")
                                if gpu_time > 0 and cpu_time > 0:
                                    speedup = cpu_time / gpu_time
                                    print(f"    GPU加速比: {speedup:.2f}x")
                            else:
                                print("    GPU计算结果与CPU不匹配，可能存在精度问题")
                                gpu_time = None
                except Exception as e:
                    print(f"    OpenCL GPU测试失败: {e}")
            else:
                print("    未安装PyOpenCL，无法进行GPU加速测试")
                
            # 返回测试结果
            result = {
                'matrix_size': matrix_size,
                'cpu_time': cpu_time,
                'operations': matrix_size * matrix_size * (2 * matrix_size - 1),  # 矩阵乘法的操作次数
                'cpu_gflops': (matrix_size * matrix_size * (2 * matrix_size - 1)) / (cpu_time * 1e9) if cpu_time > 0 else 0
            }
            
            if gpu_time:
                result['gpu_time'] = gpu_time
                result['gpu_gflops'] = (matrix_size * matrix_size * (2 * matrix_size - 1)) / (gpu_time * 1e9) if gpu_time > 0 else 0
                result['speedup'] = cpu_time / gpu_time if gpu_time > 0 else 0
                
            return result
            
        except Exception as e:
            print(f"GPU测试失败: {e}")
            import traceback
            traceback.print_exc()
            return None
            
    def run_all_tests(self):
        """运行所有测试"""
        try:
            print("开始性能测试...\n")
            
            self.print_system_info()

            # CPU测试
            print("=" * 60)
            print("CPU性能测试")
            print("=" * 60)
            self.results['cpu_single_thread'] = self.cpu_single_thread_test()
            print()
            self.results['cpu_multi_thread'] = self.cpu_multi_thread_test()
            print()

            # 内存测试
            print("=" * 60)
            print("内存性能测试")
            print("=" * 60)
            self.results['memory'] = self.memory_test()
            print()

            # 磁盘I/O测试
            print("=" * 60)
            print("磁盘I/O性能测试")
            print("=" * 60)
            self.results['disk_io'] = self.disk_io_test()
            print()
            
            # GPU测试
            print("=" * 60)
            print("GPU性能测试")
            print("=" * 60)
            self.results['gpu'] = self.gpu_test()
            print()

            # 生成报告
            self.generate_report()
            
        except KeyboardInterrupt:
            print("\n测试被用户中断")
            sys.exit(1)
        except Exception as e:
            print(f"\n测试过程中出现错误: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

    def generate_report(self):
        """生成测试报告"""
        print("=" * 60)
        print("性能测试报告")
        print("=" * 60)

        # 计算原始分数，不设置上限
        cpu_single_score = self.results['cpu_single_thread']['operations_per_second'] / 5000
        cpu_multi_score = self.results['cpu_multi_thread']['operations_per_second'] / 5000000
        memory_1mb_score = self.results['memory']['1024KB']['throughput_mb_s'] / 100
        
        # 磁盘性能评分 - 更宽松的标准
        disk_write_score = self.results['disk_io']['write_speed_mb_s'] / 100  # 从200改回100
        disk_read_score = self.results['disk_io']['read_speed_mb_s'] / 75  # 从150改为75，更宽松

        # 计算GPU得分（如果有）
        gpu_score = 0
        if 'gpu' in self.results and self.results['gpu']:
            # 如果有GPU测试结果，计算得分
            if 'gpu_gflops' in self.results['gpu']:
                # 以10 GFLOPS为基准
                gpu_score = self.results['gpu']['gpu_gflops'] / 10
            elif 'cpu_gflops' in self.results['gpu']:
                # 如果没有GPU测试结果，使用CPU结果的一半作为估计
                gpu_score = self.results['gpu']['cpu_gflops'] / 10
        
        # 计算加权总分，给予不同测试项目不同的权重
        weights = {
            'cpu_single': 0.15,  # 15%
            'cpu_multi': 0.25,   # 25%
            'memory': 0.2,      # 20%
            'disk_write': 0.1, # 10%
            'disk_read': 0.1,   # 10%
            'gpu': 0.2         # 20%
        }
        
        total_score = (cpu_single_score * weights['cpu_single'] +
                      cpu_multi_score * weights['cpu_multi'] +
                      memory_1mb_score * weights['memory'] +
                      disk_write_score * weights['disk_write'] +
                      disk_read_score * weights['disk_read'] +
                      gpu_score * weights['gpu'])

        print(f"CPU单线程性能得分: {cpu_single_score:.1f}")
        print(f"CPU多线程性能得分: {cpu_multi_score:.1f}")
        print(f"内存性能得分: {memory_1mb_score:.1f}")
        print(f"磁盘写入性能得分: {disk_write_score:.1f}")
        print(f"磁盘读取性能得分: {disk_read_score:.1f}")
        print(f"GPU性能得分: {gpu_score:.1f}")
        print("-" * 40)
        print(f"综合性能得分: {total_score:.1f}")

        # 保存详细结果到文件
        report_data = {
            'system_info': self.system_info,
            'test_results': self.results,
            'scores': {
                'cpu_single_thread': cpu_single_score,
                'cpu_multi_thread': cpu_multi_score,
                'memory': memory_1mb_score,
                'disk_write': disk_write_score,
                'disk_read': disk_read_score,
                'gpu': gpu_score,
                'total': total_score,
                'weights': weights  # 添加权重信息到报告中
            }
        }

        with open('benchmark_report.json', 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        print("\n详细报告已保存到 benchmark_report.json")


def main():
    """主函数"""
    try:
        benchmark = PerformanceBenchmark()
        benchmark.run_all_tests()
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()