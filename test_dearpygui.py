# -*- coding: utf-8 -*-
"""
简化的DearPyGui测试程序
"""

import dearpygui.dearpygui as dpg

def hello_world():
    print("Hello from DearPyGui!")

def main():
    # 创建上下文
    dpg.create_context()
    
    # 创建窗口
    with dpg.window(label="DearPyGui测试", tag="primary_window"):
        dpg.add_text("🖥️ 电脑性能测试工具 - DearPyGui版本")
        dpg.add_separator()
        dpg.add_text("这是一个现代化的性能测试工具界面")
        dpg.add_button(label="测试按钮", callback=hello_world)
        
        # 测试选项
        dpg.add_text("\n测试选项:")
        dpg.add_checkbox(label="CPU单线程测试", default_value=True)
        dpg.add_checkbox(label="CPU多线程测试", default_value=True)
        dpg.add_checkbox(label="内存测试", default_value=True)
        dpg.add_checkbox(label="磁盘测试", default_value=True)
        dpg.add_checkbox(label="GPU测试", default_value=True)
        
        # 进度条
        dpg.add_text("\n进度:")
        dpg.add_progress_bar(default_value=0.6, width=400)
        
        # 输出区域
        dpg.add_text("\n输出信息:")
        with dpg.child_window(height=200, border=True):
            dpg.add_text("欢迎使用电脑性能测试工具！\n")
            dpg.add_text("这是基于DearPyGui的现代化界面。\n")
            dpg.add_text("界面支持现代化的主题和样式。")
    
    # 设置主窗口
    dpg.set_primary_window("primary_window", True)
    
    # 创建视口
    dpg.create_viewport(title="电脑性能测试工具 - DearPyGui", width=800, height=600)
    dpg.setup_dearpygui()
    
    # 显示并运行
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()