# 电脑性能测试工具

一个全面的电脑性能测试工具，可以测试CPU、内存、磁盘I/O和GPU性能，并生成详细的性能报告。

## 功能特点

- **CPU性能测试**：单线程和多线程性能测试
- **内存性能测试**：测试内存分配和访问速度
- **磁盘I/O测试**：测试磁盘读写速度
- **GPU性能测试**：使用矩阵乘法测试GPU计算性能
- **系统信息收集**：收集并显示详细的系统硬件信息
- **性能评分系统**：根据测试结果计算各项性能得分和综合得分
- **图形用户界面**：提供友好的图形界面，方便操作
- **命令行界面**：支持命令行参数，可以自动化测试

## 系统要求

- Windows操作系统
- Python 3.6+
- 依赖库：
  - PyQt5（GUI界面）
  - psutil（系统信息收集）
  - numpy（数值计算）
  - wmi（GPU信息收集，可选）
  - pyopencl（GPU加速测试，可选）

## 安装方法

### 方法一：直接运行Python脚本

1. 确保已安装Python 3.6+
2. 安装依赖库：

```bash
pip install PyQt5 psutil numpy
# 可选依赖
pip install wmi pyopencl
```

3. 运行程序：

```bash
# 图形界面版本
python PCtest_gui.py

# 命令行版本
python PCtest_cli.py
```

### 方法二：使用打包好的可执行文件

1. 运行打包脚本生成可执行文件：

```bash
python build_exe.py
```

2. 在`dist`目录中找到生成的`PCtest.exe`文件，双击运行即可

## 使用说明

### 图形界面版本

1. 启动程序后，选择要运行的测试项目（CPU单线程、CPU多线程、内存、磁盘I/O、GPU）
2. 点击"开始测试"按钮开始测试
3. 测试完成后，可以查看测试结果和性能得分
4. 点击"保存报告"按钮可以将详细报告保存为JSON文件

### 命令行版本

```bash
# 运行所有测试
python PCtest_cli.py --all

# 只运行CPU测试
python PCtest_cli.py --cpu

# 只运行内存和磁盘测试
python PCtest_cli.py --memory --disk

# 指定输出文件
python PCtest_cli.py --all --output my_report.json

# 安静模式，只显示最终结果
python PCtest_cli.py --all --quiet
```

## 项目结构

- `PCtest_gui.py` - 图形用户界面主程序
- `PCtest_cli.py` - 命令行界面主程序
- `PCtest_core.py` - 核心测试功能模块
- `system_info.py` - 系统信息收集模块
- `cpu_test.py` - CPU性能测试模块
- `memory_test.py` - 内存性能测试模块
- `disk_test.py` - 磁盘I/O测试模块
- `gpu_test.py` - GPU性能测试模块
- `report_generator.py` - 报告生成模块
- `build_exe.py` - 可执行文件打包脚本

## 性能评分说明

- **CPU单线程性能**：以5000素数/秒为基准
- **CPU多线程性能**：以5000000操作/秒为基准
- **内存性能**：以100MB/s的吞吐量为基准
- **磁盘写入性能**：以100MB/s的写入速度为基准
- **磁盘读取性能**：以75MB/s的读取速度为基准
- **GPU性能**：以10 GFLOPS为基准

各项性能得分的权重：
- CPU单线程：15%
- CPU多线程：25%
- 内存：20%
- 磁盘写入：10%
- 磁盘读取：10%
- GPU：20%

## 许可证

本项目采用MIT许可证。