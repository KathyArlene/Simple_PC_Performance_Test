#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电脑性能测试工具 - GUI版本
基于PCtest.py的功能，提供图形用户界面
支持多语言（中文、英文、日文、西班牙语）
"""

import sys
import os
import json
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QProgressBar, 
                             QTabWidget, QTextEdit, QGroupBox, QCheckBox, 
                             QMessageBox, QFileDialog, QSplitter, QComboBox,
                             QAction, QMenu, QMenuBar)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QIcon

# 导入性能测试核心模块
from PCtest_core import PerformanceBenchmark

# 导入多语言支持模块
import language as lang


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
            self.update_signal.emit(lang.get('getting_system_info'))
            system_info_text = self._format_system_info()
            self.update_signal.emit(system_info_text)
            self.progress_signal.emit(5)
            
            # 根据选项运行测试
            results = {}
            
            # CPU单线程测试
            if self.test_options.get('cpu_single', True):
                self.update_signal.emit(f"\n{lang.get('running_cpu_single_test')}")
                results['cpu_single_thread'] = self.benchmark.cpu_single_thread_test()
                self.progress_signal.emit(20)
            
            # CPU多线程测试
            if self.test_options.get('cpu_multi', True):
                self.update_signal.emit(f"\n{lang.get('running_cpu_multi_test')}")
                results['cpu_multi_thread'] = self.benchmark.cpu_multi_thread_test()
                self.progress_signal.emit(40)
            
            # 内存测试
            if self.test_options.get('memory', True):
                self.update_signal.emit(f"\n{lang.get('running_memory_test')}")
                results['memory'] = self.benchmark.memory_test()
                self.progress_signal.emit(60)
            
            # 磁盘测试
            if self.test_options.get('disk', True):
                self.update_signal.emit(f"\n{lang.get('running_disk_test')}")
                results['disk_io'] = self.benchmark.disk_io_test()
                self.progress_signal.emit(80)
            
            # GPU测试
            if self.test_options.get('gpu', True):
                self.update_signal.emit(f"\n{lang.get('running_gpu_test')}")
                results['gpu'] = self.benchmark.gpu_test()
                self.progress_signal.emit(95)
            
            # 保存结果
            self.benchmark.results = results
            
            # 生成报告
            self.update_signal.emit(f"\n{lang.get('generating_report')}")
            report_text = self._generate_report()
            self.update_signal.emit(report_text)
            
            # 发送完成信号
            self.progress_signal.emit(100)
            self.finished_signal.emit(self.benchmark.results)
            
        except Exception as e:
            import traceback
            error_msg = f"{lang.get('test_error')}: {str(e)}\n{traceback.format_exc()}"
            self.error_signal.emit(error_msg)
    
    def _format_system_info(self):
        """格式化系统信息"""
        info = self.benchmark.system_info
        text = f"{lang.get('system_info')}:\n"
        text += f"{lang.get('os')}: {info['platform']}\n"
        text += f"{lang.get('processor')}: {info['processor']}\n"
        text += f"{lang.get('architecture')}: {info['architecture']}\n"
        text += f"{lang.get('physical_cores')}: {info['cpu_count']}\n"
        text += f"{lang.get('logical_cores')}: {info['logical_cpu_count']}\n"
        text += f"{lang.get('total_memory')}: {info['total_memory'] / (1024 ** 3):.2f} GB\n"
        text += f"{lang.get('available_memory')}: {info['available_memory'] / (1024 ** 3):.2f} GB\n"
        
        # GPU信息
        if 'gpus' in info and info['gpus']:
            text += f"\n{lang.get('gpu_info')}:\n"
            for i, gpu in enumerate(info['gpus']):
                text += f"  GPU {i+1}: {gpu['name']}\n"
                if 'video_memory' in gpu and gpu['video_memory']:
                    text += f"    {lang.get('video_memory')}: {gpu['video_memory'] / (1024 ** 3):.2f} GB\n" if gpu['video_memory'] > 0 else f"    {lang.get('video_memory')}: {lang.get('unknown')}\n"
                if 'is_integrated' in gpu:
                    text += f"    {lang.get('gpu_type')}: {lang.get('integrated_gpu') if gpu['is_integrated'] else lang.get('discrete_gpu')}\n"
                if 'driver_version' in gpu and gpu['driver_version'] != 'Unknown':
                    text += f"    {lang.get('driver_version')}: {gpu['driver_version']}\n"
        
        return text
    
    def _generate_report(self):
        """生成报告文本"""
        # 计算得分
        scores = self.benchmark.generate_scores()
        
        # 格式化报告文本
        text = f"\n{lang.get('performance_report')}:\n"
        text += f"{lang.get('cpu_single_thread_score')}: {scores['cpu_single_thread']:.1f}\n"
        text += f"{lang.get('cpu_multi_thread_score')}: {scores['cpu_multi_thread']:.1f}\n"
        text += f"{lang.get('memory_score')}: {scores['memory']:.1f}\n"
        text += f"{lang.get('disk_write_score')}: {scores['disk_write']:.1f}\n"
        text += f"{lang.get('disk_read_score')}: {scores['disk_read']:.1f}\n"
        text += f"{lang.get('gpu_score')}: {scores['gpu']:.1f}\n"
        text += "-" * 40 + "\n"
        text += f"{lang.get('total_score')}: {scores['total']:.1f}\n"
        
        return text


class MainWindow(QMainWindow):
    """主窗口类"""
    def __init__(self):
        super().__init__()
        
        # 设置窗口属性
        self.setWindowTitle(lang.get('window_title'))
        self.setMinimumSize(800, 600)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建中央部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(self.central_widget)
        
        # 创建选项区域
        self.options_group = QGroupBox(lang.get('test_options'))
        options_layout = QHBoxLayout()
        
        # 测试选项复选框
        self.cpu_single_check = QCheckBox(lang.get('cpu_single'))
        self.cpu_single_check.setChecked(True)
        self.cpu_multi_check = QCheckBox(lang.get('cpu_multi'))
        self.cpu_multi_check.setChecked(True)
        self.memory_check = QCheckBox(lang.get('memory'))
        self.memory_check.setChecked(True)
        self.disk_check = QCheckBox(lang.get('disk'))
        self.disk_check.setChecked(True)
        self.gpu_check = QCheckBox(lang.get('gpu'))
        self.gpu_check.setChecked(True)
        
        options_layout.addWidget(self.cpu_single_check)
        options_layout.addWidget(self.cpu_multi_check)
        options_layout.addWidget(self.memory_check)
        options_layout.addWidget(self.disk_check)
        options_layout.addWidget(self.gpu_check)
        self.options_group.setLayout(options_layout)
        
        main_layout.addWidget(self.options_group)
        
        # 创建按钮区域
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton(lang.get('start_test'))
        self.start_button.setMinimumHeight(40)
        self.start_button.clicked.connect(self.start_benchmark)
        
        self.save_button = QPushButton(lang.get('save_report'))
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
        self.output_text.setText(lang.get('welcome_message'))
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menu_bar = self.menuBar()
        
        # 语言菜单
        language_menu = menu_bar.addMenu(lang.get('language'))
        
        # 添加语言选项
        for lang_code, lang_name in lang.LANGUAGE_NAMES.items():
            language_action = QAction(lang_name, self)
            language_action.setData(lang_code)
            language_action.triggered.connect(self.change_language)
            language_menu.addAction(language_action)
    
    def change_language(self):
        """切换语言"""
        action = self.sender()
        if action:
            lang_code = action.data()
            lang.set_language(lang_code)
            self.update_ui_texts()
    
    def update_ui_texts(self):
        """更新UI文本"""
        # 更新窗口标题
        self.setWindowTitle(lang.get('window_title'))
        
        # 更新菜单
        self.menuBar().clear()
        self.create_menu_bar()
        
        # 更新选项组标题
        self.options_group.setTitle(lang.get('test_options'))
        
        # 更新复选框文本
        self.cpu_single_check.setText(lang.get('cpu_single'))
        self.cpu_multi_check.setText(lang.get('cpu_multi'))
        self.memory_check.setText(lang.get('memory'))
        self.disk_check.setText(lang.get('disk'))
        self.gpu_check.setText(lang.get('gpu'))
        
        # 更新按钮文本
        self.start_button.setText(lang.get('start_test'))
        self.save_button.setText(lang.get('save_report'))
        
        # 更新欢迎信息
        if not self.benchmark_thread or not self.benchmark_thread.isRunning():
            self.output_text.setText(lang.get('welcome_message'))
    
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
            QMessageBox.warning(self, lang.get('warning'), lang.get('select_one_test'))
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
        QMessageBox.information(self, lang.get('completed'), lang.get('test_completed'))
    
    def test_error(self, error_msg):
        """测试出错"""
        self.output_text.append(f"\n{lang.get('error')}: {error_msg}")
        self.start_button.setEnabled(True)
        QMessageBox.critical(self, lang.get('error'), f"{lang.get('test_error')}\n{error_msg}")
    
    def save_report(self):
        """保存测试报告"""
        if not self.results:
            QMessageBox.warning(self, lang.get('warning'), lang.get('no_results'))
            return
        
        # 获取保存路径
        file_path, _ = QFileDialog.getSaveFileName(
            self, lang.get('save_test_report'), 
            os.path.join(os.path.expanduser("~"), "Desktop", "benchmark_report.json"),
            lang.get('json_files')
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
            
            QMessageBox.information(self, lang.get('success'), f"{lang.get('report_saved')}\n{file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, lang.get('error'), f"{lang.get('save_error')}\n{str(e)}")


def main():
    """主函数"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()