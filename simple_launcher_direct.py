#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
简单启动器，使用相对导入
"""

import os
import sys
import traceback
import tkinter as tk
from tkinter import messagebox

def main():
    """主函数"""
    try:
        # 确保当前目录在sys.path中
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
            
        # 尝试导入所有必要的模块
        import config_manager
        import history_manager
        import language_resources
        import theme_manager
        import settings_dialog
        import history_dialog
        import view_logs
        import sync_sdp_order
        import sdp_sync_gui_new
        
        # 如果成功导入，启动主程序
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
