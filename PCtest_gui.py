#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电脑性能测试工具 - GUI版本
基于PCtest.py的功能，提供图形用户界面
"""

import sys
import os
import json
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QProgressBar, 
                             QTabWidget, QTextEdit, QGroupBox, QCheckBox, 
                             QMessageBox, QFileDialog, QSplitter)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QIcon

# 导入性能测试核心模块
from PCtest_core import PerformanceBenchmark


class BenchmarkThread(QThread):
    """性能测试线程，避免界面卡死"""
    update_signal = pyqtSignal(str)  # 更新信息信号
    progress_signal = pyqtSignal(int)  # 进度信号
    finished_signal = pyqtSignal(dict)  # 测试完成信号
    error_signal = pyqtSignal(str)  # 错误信号
    
    def __init__(self, test_options):
        super().__init__()
        self.test_options = test_options
        self.benchmark = PerformanceBenchmark()
        
    def run(self):
        try:
            # 发送系统信息
            self.update_signal.emit("获取系统信息...")
            system_info_text = self._format_system_info()
            self.update_signal.emit(system_info_text)
            self.progress_signal.emit(5)
            
            # 根据选项运行测试
            results = {}
            
            # CPU单线程测试
            if self.test_options.get('cpu_single', True):
                self.update_signal.emit("\n正在进行CPU单线程测试...")
                results['cpu_single_thread'] = self.benchmark.cpu_single_thread_test()
                self.progress_signal.emit(20)
            
            # CPU多线程测试
            if self.test_options.get('cpu_multi', True):
                self.update_signal.emit("\n正在进行CPU多线程测试...")
                results['cpu_multi_thread'] = self.benchmark.cpu_multi_thread_test()
                self.progress_signal.emit(40)
            
            # 内存测试
            if self.test_options.get('memory', True):
                self.update_signal.emit("\n正在进行内存性能测试...")
                results['memory'] = self.benchmark.memory_test()
                self.progress_signal.emit(60)
            
            # 磁盘测试
            if self.test_options.get('disk', True):
                self.update_signal.emit("\n正在进行磁盘I/O性能测试...")
                results['disk_io'] = self.benchmark.disk_io_test()
                self.progress_signal.emit(80)
            
            # GPU测试
            if self.test_options.get('gpu', True):
                self.update_signal.emit("\n正在进行GPU性能测试...")
                results['gpu'] = self.benchmark.gpu_test()
                self.progress_signal.emit(95)
            
            # 保存结果
            self.benchmark.results = results
            
            # 生成报告
            self.update_signal.emit("\n生成性能测试报告...")
            report_text = self._generate_report()
            self.update_signal.emit(report_text)
            
            # 发送完成信号
            self.progress_signal.emit(100)
            self.finished_signal.emit(self.benchmark.results)
            
        except Exception as e:
            import traceback
            error_msg = f"测试过程中出现错误: {str(e)}\n{traceback.format_exc()}"
            self.error_signal.emit(error_msg)
    
    def _format_system_info(self):
        """格式化系统信息"""
        info = self.benchmark.system_info
        text = "系统信息:\n"
        text += f"操作系统: {info['platform']}\n"
        text += f"处理器: {info['processor']}\n"
        text += f"架构: {info['architecture']}\n"
        text += f"物理CPU核心: {info['cpu_count']}\n"
        text += f"逻辑CPU核心: {info['logical_cpu_count']}\n"
        text += f"总内存: {info['total_memory'] / (1024 ** 3):.2f} GB\n"
        text += f"可用内存: {info['available_memory'] / (1024 ** 3):.2f} GB\n"
        
        # GPU信息
        if 'gpus' in info and info['gpus']:
            text += "\nGPU信息:\n"
            for i, gpu in enumerate(info['gpus']):
                text += f"  GPU {i+1}: {gpu['name']}\n"
                if 'video_memory' in gpu and gpu['video_memory']:
                    text += f"    显存: {gpu['video_memory'] / (1024 ** 3):.2f} GB\n" if gpu['video_memory'] > 0 else "    显存: 未知\n"
                if 'is_integrated' in gpu:
                    text += f"    类型: {'集成显卡' if gpu['is_integrated'] else '独立显卡'}\n"
                if 'driver_version' in gpu and gpu['driver_version'] != 'Unknown':
                    text += f"    驱动版本: {gpu['driver_version']}\n"
        
        return text
    
    def _generate_report(self):
        """生成报告文本"""
        # 计算得分
        scores = self.benchmark.generate_scores()
        
        # 格式化报告文本
        text = "\n性能测试报告:\n"
        text += f"CPU单线程性能得分: {scores['cpu_single_thread']:.1f}\n"
        text += f"CPU多线程性能得分: {scores['cpu_multi_thread']:.1f}\n"
        text += f"内存性能得分: {scores['memory']:.1f}\n"
        text += f"磁盘写入性能得分: {scores['disk_write']:.1f}\n"
        text += f"磁盘读取性能得分: {scores['disk_read']:.1f}\n"
        text += f"GPU性能得分: {scores['gpu']:.1f}\n"
        text += "-" * 40 + "\n"
        text += f"综合性能得分: {scores['total']:.1f}\n"
        
        return text


class MainWindow(QMainWindow):
    """主窗口"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("电脑性能测试工具")
        self.setMinimumSize(800, 600)
        
        # 创建中心部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(self.central_widget)
        
        # 创建选项区域
        options_group = QGroupBox("测试选项")
        options_layout = QHBoxLayout()
        
        # 测试选项复选框
        self.cpu_single_check = QCheckBox("CPU单线程")
        self.cpu_single_check.setChecked(True)
        self.cpu_multi_check = QCheckBox("CPU多线程")
        self.cpu_multi_check.setChecked(True)
        self.memory_check = QCheckBox("内存")
        self.memory_check.setChecked(True)
        self.disk_check = QCheckBox("磁盘I/O")
        self.disk_check.setChecked(True)
        self.gpu_check = QCheckBox("GPU")
        self.gpu_check.setChecked(True)
        
        options_layout.addWidget(self.cpu_single_check)
        options_layout.addWidget(self.cpu_multi_check)
        options_layout.addWidget(self.memory_check)
        options_layout.addWidget(self.disk_check)
        options_layout.addWidget(self.gpu_check)
        options_group.setLayout(options_layout)
        
        main_layout.addWidget(options_group)
        
        # 创建按钮区域
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("开始测试")
        self.start_button.setMinimumHeight(40)
        self.start_button.clicked.connect(self.start_benchmark)
        
        self.save_button = QPushButton("保存报告")
        self.save_button.setMinimumHeight(40)
        self.save_button.clicked.connect(self.save_report)
        self.save_button.setEnabled(False)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.save_button)
        
        main_layout.addLayout(button_layout)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)
        
        # 输出区域
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Consolas", 10))
        main_layout.addWidget(self.output_text)
        
        # 初始化变量
        self.benchmark_thread = None
        self.results = None
        
        # 显示欢迎信息
        self.output_text.setText("欢迎使用电脑性能测试工具！\n\n"
                               "请选择要运行的测试项目，然后点击'开始测试'按钮。\n"
                               "测试完成后，可以点击'保存报告'按钮将结果保存到文件。")
    
    def start_benchmark(self):
        """开始性能测试"""
        # 获取测试选项
        test_options = {
            'cpu_single': self.cpu_single_check.isChecked(),
            'cpu_multi': self.cpu_multi_check.isChecked(),
            'memory': self.memory_check.isChecked(),
            'disk': self.disk_check.isChecked(),
            'gpu': self.gpu_check.isChecked()
        }
        
        # 检查是否至少选择了一项测试
        if not any(test_options.values()):
            QMessageBox.warning(self, "警告", "请至少选择一项测试！")
            return
        
        # 清空输出区域
        self.output_text.clear()
        
        # 禁用按钮
        self.start_button.setEnabled(False)
        self.save_button.setEnabled(False)
        
        # 重置进度条
        self.progress_bar.setValue(0)
        
        # 创建并启动测试线程
        self.benchmark_thread = BenchmarkThread(test_options)
        self.benchmark_thread.update_signal.connect(self.update_output)
        self.benchmark_thread.progress_signal.connect(self.update_progress)
        self.benchmark_thread.finished_signal.connect(self.test_finished)
        self.benchmark_thread.error_signal.connect(self.test_error)
        self.benchmark_thread.start()
    
    def update_output(self, text):
        """更新输出文本"""
        self.output_text.append(text)
        # 滚动到底部
        self.output_text.verticalScrollBar().setValue(
            self.output_text.verticalScrollBar().maximum())
    
    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar.setValue(value)
    
    def test_finished(self, results):
        """测试完成"""
        self.results = results
        self.start_button.setEnabled(True)
        self.save_button.setEnabled(True)
        QMessageBox.information(self, "完成", "性能测试已完成！")
    
    def test_error(self, error_msg):
        """测试出错"""
        self.output_text.append(f"\n错误: {error_msg}")
        self.start_button.setEnabled(True)
        QMessageBox.critical(self, "错误", f"测试过程中出现错误:\n{error_msg}")
    
    def save_report(self):
        """保存测试报告"""
        if not self.results:
            QMessageBox.warning(self, "警告", "没有可保存的测试结果！")
            return
        
        # 获取保存路径
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存测试报告", 
            os.path.join(os.path.expanduser("~"), "Desktop", "benchmark_report.json"),
            "JSON文件 (*.json);;所有文件 (*.*)"
        )
        
        if not file_path:
            return
        
        try:
            # 获取完整的报告数据
            benchmark = self.benchmark_thread.benchmark
            report_data = {
                'system_info': benchmark.system_info,
                'test_results': benchmark.results,
                'scores': benchmark.generate_scores()
            }
            
            # 保存到文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            QMessageBox.information(self, "成功", f"测试报告已保存到:\n{file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存报告时出错:\n{str(e)}")


def main():
    """主函数"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()