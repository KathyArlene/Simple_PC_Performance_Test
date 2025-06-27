# -*- coding: utf-8 -*-
"""
电脑性能测试工具 - DearPyGui版本
基于PCtest.py的功能，提供现代化的图形用户界面
支持多语言（中文、英文、日文、西班牙语）
"""

import dearpygui.dearpygui as dpg
import threading
import time
import json
import os
from datetime import datetime

# 导入性能测试核心模块
from PCtest_core import PerformanceBenchmark

# 导入多语言支持模块
import language as lang

# 导入硬件检测模块
from hardware_detector import HardwareDetector


class PCTestDearPyGUI:
    """基于DearPyGui的性能测试工具"""
    
    def __init__(self):
        self.benchmark = PerformanceBenchmark()
        self.hardware_detector = HardwareDetector()
        self.test_params = None
        self.results = None
        self.is_testing = False
        
        # 测试选项
        self.test_options = {
            'cpu_single': True,
            'cpu_multi': True,
            'memory': True,
            'disk': True,
            'gpu': True
        }
        
        # 创建DearPyGui上下文
        dpg.create_context()
        
        # 设置字体（支持中文）
        self.setup_font()
        
        # 设置主题
        self.setup_theme()
        
        # 创建界面
        self.create_ui()
        
        # 设置视口
        dpg.create_viewport(title=lang.get('window_title'), width=1000, height=700)
        dpg.setup_dearpygui()
        
    def setup_font(self):
        """设置字体以支持中文显示"""
        try:
            # 尝试加载系统中文字体
            import os
            import platform
            
            font_path = None
            system = platform.system()
            
            if system == "Windows":
                # Windows系统字体路径
                possible_fonts = [
                    "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
                    "C:/Windows/Fonts/simsun.ttc",  # 宋体
                    "C:/Windows/Fonts/simhei.ttf",  # 黑体
                ]
            elif system == "Darwin":  # macOS
                possible_fonts = [
                    "/System/Library/Fonts/PingFang.ttc",
                    "/System/Library/Fonts/STHeiti Light.ttc",
                ]
            else:  # Linux
                possible_fonts = [
                    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                ]
            
            # 查找可用字体
            for font in possible_fonts:
                if os.path.exists(font):
                    font_path = font
                    break
            
            if font_path:
                # 加载字体
                with dpg.font_registry():
                    # 创建字体（大小16，支持中文字符范围）
                    with dpg.font(font_path, 16) as default_font:
                        # 添加中文字符范围
                        dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)
                        dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common)
                
                # 绑定字体
                dpg.bind_font(default_font)
                print(f"已加载字体: {font_path}")
            else:
                print("警告: 未找到合适的中文字体，可能会出现乱码")
                
        except Exception as e:
            print(f"字体加载失败: {e}")
            print("将使用默认字体，可能会出现中文乱码")
        
    def setup_theme(self):
        """设置现代化主题"""
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (15, 15, 15), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (25, 25, 25), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (35, 35, 35), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Border, (70, 70, 70), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (40, 40, 40), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (60, 60, 60), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (80, 80, 80), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (25, 25, 25), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (35, 35, 35), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Button, (70, 130, 180), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (90, 150, 200), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (50, 110, 160), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (70, 130, 180), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (70, 130, 180), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (90, 150, 200), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Header, (70, 130, 180), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (90, 150, 200), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (50, 110, 160), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255), category=dpg.mvThemeCat_Core)
                
                # 设置样式
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 8, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 6, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 4, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 12, 12, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 8, 4, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 6, category=dpg.mvThemeCat_Core)
                
        dpg.bind_theme(global_theme)
        
    def create_ui(self):
        """创建用户界面"""
        with dpg.window(label=lang.get('window_title'), tag="primary_window"):
            
            # 标题区域
            with dpg.group(horizontal=True):
                dpg.add_text("🖥️ " + lang.get('window_title'), tag="title_text")
                dpg.add_spacer(width=20)
                dpg.add_text("现代化性能测试工具", color=(150, 150, 150))
            
            dpg.add_separator()
            dpg.add_spacer(height=10)
            
            # 语言选择区域
            with dpg.collapsing_header(label="🌐 语言选择", default_open=False):
                with dpg.group(horizontal=True):
                    dpg.add_button(label="中文", callback=self.change_language, user_data="zh")
                    dpg.add_button(label="English", callback=self.change_language, user_data="en")
                    dpg.add_button(label="日本語", callback=self.change_language, user_data="ja")
                    dpg.add_button(label="Español", callback=self.change_language, user_data="es")
            
            dpg.add_spacer(height=10)
            
            # 测试选项区域
            with dpg.collapsing_header(label="⚙️ 测试选项", default_open=True):
                with dpg.group(horizontal=True):
                    dpg.add_checkbox(label="CPU单线程", tag="cpu_single_check", default_value=True)
                    dpg.add_checkbox(label="CPU多线程", tag="cpu_multi_check", default_value=True)
                    dpg.add_checkbox(label="内存测试", tag="memory_check", default_value=True)
                with dpg.group(horizontal=True):
                    dpg.add_checkbox(label="磁盘测试", tag="disk_check", default_value=True)
                    dpg.add_checkbox(label="GPU测试", tag="gpu_check", default_value=True)
            
            dpg.add_spacer(height=15)
            
            # 控制按钮区域
            with dpg.group(horizontal=True):
                dpg.add_button(label="🚀 开始测试", tag="start_button", 
                             callback=self.start_benchmark, width=150, height=40)
                dpg.add_spacer(width=20)
                dpg.add_button(label="💾 保存报告", tag="save_button", 
                             callback=self.save_report, width=150, height=40, enabled=False)
                dpg.add_spacer(width=20)
                dpg.add_button(label="📊 显示图表", tag="show_chart_button", 
                             callback=self.show_performance_chart, width=150, height=40, enabled=False)
            
            dpg.add_spacer(height=15)
            
            # 进度条
            dpg.add_progress_bar(label="测试进度", tag="progress_bar", width=-1)
            
            dpg.add_spacer(height=10)
            
            # 输出区域
            with dpg.child_window(label="输出信息", height=300, border=True):
                dpg.add_text("欢迎使用电脑性能测试工具！\n请选择测试项目并点击开始测试。", tag="output_text", wrap=0)
        
        # 设置主窗口
        dpg.set_primary_window("primary_window", True)
        
    def change_language(self, sender, app_data, user_data):
        """切换语言"""
        lang_code = user_data
        lang.set_language(lang_code)
        self.update_ui_texts()
        
    def update_ui_texts(self):
        """更新界面文本"""
        try:
            # 更新窗口标题
            dpg.configure_item("primary_window", label=lang.get('window_title'))
            dpg.set_value("title_text", "🖥️ " + lang.get('window_title'))
            
            # 更新按钮标签
            dpg.configure_item("start_button", label="🚀 " + lang.get('start_test'))
            dpg.configure_item("save_button", label="💾 " + lang.get('save_report'))
            dpg.configure_item("show_chart_button", label="📊 " + lang.get('show_chart'))
            
            # 更新复选框标签
            dpg.configure_item("cpu_single_check", label=lang.get('cpu_single'))
            dpg.configure_item("cpu_multi_check", label=lang.get('cpu_multi'))
            dpg.configure_item("memory_check", label=lang.get('memory'))
            dpg.configure_item("disk_check", label=lang.get('disk'))
            dpg.configure_item("gpu_check", label=lang.get('gpu'))
            
            # 更新欢迎信息
            welcome_msg = lang.get('welcome_message')
            dpg.set_value("output_text", welcome_msg)
            
        except Exception as e:
            print(f"更新界面文本时出错: {e}")
        
    def update_output(self, text):
        """更新输出文本"""
        current_text = dpg.get_value("output_text")
        new_text = current_text + "\n" + text
        dpg.set_value("output_text", new_text)
        
    def update_progress(self, value):
        """更新进度条"""
        dpg.set_value("progress_bar", value / 100.0)
        
    def start_benchmark(self):
        """开始性能测试"""
        if self.is_testing:
            return
            
        # 获取测试选项
        self.test_options = {
            'cpu_single': dpg.get_value("cpu_single_check"),
            'cpu_multi': dpg.get_value("cpu_multi_check"),
            'memory': dpg.get_value("memory_check"),
            'disk': dpg.get_value("disk_check"),
            'gpu': dpg.get_value("gpu_check")
        }
        
        # 检查是否至少选择了一个测试
        if not any(self.test_options.values()):
            self.update_output("❌ 请至少选择一个测试项目！")
            return
            
        # 重置界面
        dpg.set_value("output_text", "")
        self.update_progress(0)
        dpg.configure_item("start_button", enabled=False)
        dpg.configure_item("save_button", enabled=False)
        dpg.configure_item("show_chart_button", enabled=False)
        
        self.is_testing = True
        
        # 在新线程中运行测试
        test_thread = threading.Thread(target=self.run_benchmark)
        test_thread.daemon = True
        test_thread.start()
        
    def run_benchmark(self):
        """运行性能测试（在后台线程中）"""
        try:
            # 硬件检测和参数配置
            self.update_output("🔍 " + lang.get('detecting_hardware'))
            hardware_config = self.hardware_detector.detect_and_configure()
            self.test_params = hardware_config['test_parameters']
            
            # 显示硬件信息
            hardware_info = hardware_config['hardware_info']
            self.display_hardware_info(hardware_info)
            
            # 显示系统信息
            self.update_output("\n📋 " + lang.get('getting_system_info'))
            system_info_text = self.format_system_info(hardware_info)
            self.update_output(system_info_text)
            self.update_progress(5)
            
            # 根据选项运行测试
            results = {}
            
            # CPU单线程测试
            if self.test_options.get('cpu_single', True):
                self.update_output(f"\n🔥 {lang.get('running_cpu_single_test')}")
                cpu_params = self.test_params['cpu']
                results['cpu_single_thread'] = self.benchmark.cpu_single_thread_test(
                    duration=cpu_params['single_duration'],
                    calculation_count=cpu_params['calculation_count']
                )
                self.update_progress(20)
            
            # CPU多线程测试
            if self.test_options.get('cpu_multi', True):
                self.update_output(f"\n⚡ {lang.get('running_cpu_multi_test')}")
                cpu_params = self.test_params['cpu']
                results['cpu_multi_thread'] = self.benchmark.cpu_multi_thread_test(
                    duration=cpu_params['multi_duration'],
                    max_threads=cpu_params['max_threads'] if cpu_params['max_threads'] > 0 else None,
                    calculation_count=cpu_params['calculation_count']
                )
                self.update_progress(40)
            
            # 内存测试
            if self.test_options.get('memory', True):
                self.update_output(f"\n💾 {lang.get('running_memory_test')}")
                memory_params = self.test_params['memory']
                results['memory'] = self.benchmark.memory_test(
                    size_mb=memory_params['size_mb']
                )
                self.update_progress(60)
            
            # 磁盘测试
            if self.test_options.get('disk', True):
                self.update_output(f"\n💿 {lang.get('running_disk_test')}")
                disk_params = self.test_params['disk']
                results['disk_io'] = self.benchmark.disk_io_test(
                    file_size_mb=disk_params['file_size_mb']
                )
                self.update_progress(80)
            
            # GPU测试
            if self.test_options.get('gpu', True):
                self.update_output(f"\n🎮 {lang.get('running_gpu_test')}")
                gpu_params = self.test_params['gpu']
                results['gpu'] = self.benchmark.gpu_test(
                    max_load=gpu_params['max_load']
                )
                self.update_progress(95)
            
            # 保存结果
            self.benchmark.results = results
            self.results = results
            
            # 生成报告
            self.update_output(f"\n📊 {lang.get('generating_report')}")
            report_text = self.generate_report()
            self.update_output(report_text)
            
            # 完成
            self.update_progress(100)
            self.update_output("\n✅ 测试完成！")
            
            # 启用按钮
            dpg.configure_item("start_button", enabled=True)
            dpg.configure_item("save_button", enabled=True)
            dpg.configure_item("show_chart_button", enabled=True)
            
        except Exception as e:
            import traceback
            error_msg = f"❌ {lang.get('test_error')}: {str(e)}\n{traceback.format_exc()}"
            self.update_output(error_msg)
            dpg.configure_item("start_button", enabled=True)
        finally:
            self.is_testing = False
            
    def display_hardware_info(self, hardware_info):
        """显示硬件检测信息"""
        info_text = f"\n🔧 {lang.get('hardware_detection')}:\n"
        info_text += f"  {lang.get('detected_cpu')}: {hardware_info['cpu']['name']}\n"
        info_text += f"  {lang.get('detected_gpu')}: {hardware_info['gpu']['name']}\n"
        info_text += f"  {lang.get('cpu_performance_score')}: {hardware_info['cpu_score']}\n"
        info_text += f"  {lang.get('gpu_performance_score')}: {hardware_info['gpu_score']}\n"
        info_text += f"  {lang.get('cpu_tier')}: {hardware_info['cpu_tier'].upper()}\n"
        info_text += f"  {lang.get('gpu_tier')}: {hardware_info['gpu_tier'].upper()}\n"
        info_text += "-" * 50
        self.update_output(info_text)
        
    def format_system_info(self, hardware_info=None):
        """格式化系统信息"""
        info = self.benchmark.system_info
        text = f"{lang.get('system_info')}:\n"
        text += f"  {lang.get('os')}: {info['platform']}\n"
        text += f"  {lang.get('processor')}: {info['processor']}\n"
        text += f"  {lang.get('architecture')}: {info['architecture']}\n"
        text += f"  {lang.get('physical_cores')}: {info['cpu_count']}\n"
        text += f"  {lang.get('logical_cores')}: {info['logical_cpu_count']}\n"
        text += f"  {lang.get('total_memory')}: {info['total_memory'] / (1024 ** 3):.2f} GB\n"
        text += f"  {lang.get('available_memory')}: {info['available_memory'] / (1024 ** 3):.2f} GB\n"
        
        # GPU信息
        if 'gpus' in info and info['gpus']:
            text += f"\n  {lang.get('gpu_info')}:\n"
            for i, gpu in enumerate(info['gpus']):
                text += f"    GPU {i+1}: {gpu['name']}\n"
                if 'video_memory' in gpu and gpu['video_memory']:
                    text += f"      {lang.get('video_memory')}: {gpu['video_memory'] / (1024 ** 3):.2f} GB\n" if gpu['video_memory'] > 0 else f"      {lang.get('video_memory')}: {lang.get('unknown')}\n"
                if 'is_integrated' in gpu:
                    text += f"      {lang.get('gpu_type')}: {lang.get('integrated_gpu') if gpu['is_integrated'] else lang.get('discrete_gpu')}\n"
                if 'driver_version' in gpu and gpu['driver_version'] != 'Unknown':
                    text += f"      {lang.get('driver_version')}: {gpu['driver_version']}\n"
        
        return text
        
    def generate_report(self):
        """生成报告文本"""
        # 计算得分
        scores = self.benchmark.generate_scores()
        
        # 格式化报告文本
        text = f"\n📈 {lang.get('performance_report')}:\n"
        text += f"  {lang.get('cpu_single_thread_score')}: {scores['cpu_single_thread']:.1f}\n"
        text += f"  {lang.get('cpu_multi_thread_score')}: {scores['cpu_multi_thread']:.1f}\n"
        text += f"  {lang.get('memory_score')}: {scores['memory']:.1f}\n"
        text += f"  {lang.get('disk_write_score')}: {scores['disk_write']:.1f}\n"
        text += f"  {lang.get('disk_read_score')}: {scores['disk_read']:.1f}\n"
        text += f"  {lang.get('gpu_score')}: {scores['gpu']:.1f}\n"
        text += "-" * 40 + "\n"
        text += f"  🏆 {lang.get('total_score')}: {scores['total']:.1f}\n"
        
        return text
        
    def save_report(self):
        """保存测试报告"""
        if not self.results:
            self.update_output("❌ 没有可保存的测试结果！")
            return
            
        try:
            # 生成报告文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"benchmark_report_{timestamp}.json"
            
            # 保存报告
            report_path = self.benchmark.generate_report(filename)
            self.update_output(f"✅ 报告已保存到: {report_path}")
            
        except Exception as e:
            self.update_output(f"❌ 保存报告失败: {str(e)}")
            
    def show_performance_chart(self):
        """显示性能图表"""
        if not self.results:
            self.update_output("❌ 没有可显示的测试结果！")
            return
            
        # 创建图表窗口
        with dpg.window(label="📊 性能测试结果图表", width=600, height=400, modal=True, tag="chart_window"):
            
            # 计算得分
            scores = self.benchmark.generate_scores()
            
            # 准备数据
            test_names = []
            test_scores = []
            
            if 'cpu_single_thread' in scores:
                test_names.append("CPU单线程")
                test_scores.append(scores['cpu_single_thread'])
            if 'cpu_multi_thread' in scores:
                test_names.append("CPU多线程")
                test_scores.append(scores['cpu_multi_thread'])
            if 'memory' in scores:
                test_names.append("内存")
                test_scores.append(scores['memory'])
            if 'disk_write' in scores:
                test_names.append("磁盘写入")
                test_scores.append(scores['disk_write'])
            if 'disk_read' in scores:
                test_names.append("磁盘读取")
                test_scores.append(scores['disk_read'])
            if 'gpu' in scores:
                test_names.append("GPU")
                test_scores.append(scores['gpu'])
                
            # 创建柱状图
            with dpg.plot(label="性能得分", height=300, width=-1):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, label="测试项目")
                dpg.add_plot_axis(dpg.mvYAxis, label="得分", tag="y_axis")
                
                # 添加柱状图数据
                x_data = list(range(len(test_names)))
                dpg.add_bar_series(x_data, test_scores, label="性能得分", parent="y_axis")
                
            # 关闭按钮
            dpg.add_button(label="关闭", callback=lambda: dpg.delete_item("chart_window"))
            
    def run(self):
        """运行应用程序"""
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()


def main():
    """主函数"""
    try:
        app = PCTestDearPyGUI()
        app.run()
    except Exception as e:
        print(f"启动失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()