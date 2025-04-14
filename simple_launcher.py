#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
简单启动器，用于测试模块导入
"""

import os
import sys
import traceback
import tkinter as tk
from tkinter import messagebox

def main():
    """主函数"""
    try:
        # 尝试导入所有必要的模块
        import config_manager
        import history_manager
        import language_resources
        import theme_manager
        import settings_dialog
        import history_dialog
        import view_logs
        import sync_sdp_order
        
        # 如果成功导入，显示成功消息
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("成功", "所有模块导入成功！")
        
        # 启动主程序
        import sdp_sync_gui_new
        sdp_sync_gui_new.main()
        
    except ImportError as e:
        # 如果导入失败，显示错误消息
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("错误", f"导入模块失败：\n\n{str(e)}\n\n请确保所有模块文件都在当前目录中")
        print(f"Import error: {str(e)}")
        print(traceback.format_exc())
    except Exception as e:
        # 如果发生其他错误，显示错误消息
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("错误", f"发生错误：\n\n{str(e)}\n\n{traceback.format_exc()}")
        print(f"Error: {str(e)}")
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
