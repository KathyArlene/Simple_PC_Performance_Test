#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPU性能测试模块
使用矩阵乘法测试GPU性能
"""

import time
import numpy as np

# 尝试导入PyOpenCL用于GPU测试
try:
    import pyopencl as cl
    HAS_OPENCL = True
except ImportError:
    HAS_OPENCL = False
    print("警告: 未安装pyopencl库，GPU加速测试将不可用。请使用 'pip install pyopencl' 安装。")


def gpu_test(gpu_info=None):
    """GPU性能测试 - 使用矩阵乘法基准测试
    
    Args:
        gpu_info: GPU信息字典，用于检测是否有可用GPU
        
    Returns:
        dict: 包含测试结果的字典
    """
    print("正在进行GPU性能测试...")
    
    # 检查是否有GPU
    if gpu_info is None or not gpu_info or gpu_info[0]['name'] == '未知':
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


if __name__ == "__main__":
    # 测试代码
    print("GPU性能测试示例")
    print("=" * 60)
    
    # 模拟GPU信息
    mock_gpu_info = [{'name': 'Test GPU'}]
    
    results = gpu_test(mock_gpu_info)
    
    if results:
        print("\n测试结果摘要:")
        print(f"CPU GFLOPS: {results['cpu_gflops']:.2f}")
        if 'gpu_gflops' in results:
            print(f"GPU GFLOPS: {results['gpu_gflops']:.2f}")
            print(f"加速比: {results['speedup']:.2f}x")
    else:
        print("GPU测试未完成或失败")