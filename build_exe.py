#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包脚本
将PCtest_gui.py打包成可执行文件
"""

import os
import sys
import subprocess
import shutil


def check_requirements():
    """检查必要的依赖是否已安装"""
    required_packages = ['PyQt5', 'pyinstaller', 'psutil', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"缺少必要的依赖包: {', '.join(missing_packages)}")
        install = input("是否自动安装这些依赖? (y/n): ")
        if install.lower() == 'y':
            for package in missing_packages:
                print(f"正在安装 {package}...")
                subprocess.call([sys.executable, "-m", "pip", "install", package])
        else:
            print("请手动安装缺少的依赖后再运行此脚本。")
            sys.exit(1)


def build_executable():
    """使用PyInstaller打包程序"""
    print("开始打包程序...")
    
    # 清理旧的构建文件
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
        # 构建命令
    cmd = [
        'pyinstaller',
        '--name=PCtest',
        '--windowed',  # 无控制台窗口
        '--onefile',   # 打包成单个文件
        '--clean',     # 清理临时文件
        '--noconfirm',  # 不询问确认
        # '--add-data=LICENSE;.',  # 注释掉这一行
        'PCtest_gui.py'  # 主程序文件
    ]
    
    # 执行打包命令
    try:
        subprocess.call(cmd)
        print("\n打包完成!")
        print(f"可执行文件位置: {os.path.abspath('dist/PCtest.exe')}")
    except Exception as e:
        print(f"打包过程中出错: {e}")
        sys.exit(1)


def main():
    """主函数"""
    print("电脑性能测试工具 - 打包脚本")
    print("=" * 60)
    
    # 检查当前目录是否包含所需文件
    required_files = ['PCtest_gui.py', 'PCtest_core.py', 'system_info.py', 
                     'cpu_test.py', 'memory_test.py', 'disk_test.py', 
                     'gpu_test.py', 'report_generator.py']
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print(f"错误: 缺少必要的源文件: {', '.join(missing_files)}")
        print("请确保所有源文件都在当前目录中。")
        sys.exit(1)
    
    # 检查依赖
    check_requirements()
    
    # 打包程序
    build_executable()
    
    print("\n提示: 如果您想要添加图标，请修改打包命令添加 --icon=your_icon.ico 参数。")


if __name__ == "__main__":
    main()