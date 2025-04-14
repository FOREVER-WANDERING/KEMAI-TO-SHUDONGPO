#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
蔬东坡订单同步工具 - 图形界面版本
"""

import os
import sys
import time
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime
import subprocess
import io
from contextlib import redirect_stdout, redirect_stderr

# 导入同步脚本
import sync_sdp_order

# 创建一个自定义的输出重定向类
class TextRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.buffer = ""

    def write(self, string):
        self.buffer += string
        # 使用after方法在主线程中更新UI
        self.text_widget.after(10, self.update_text_widget)

    def update_text_widget(self):
        if self.buffer:
            self.text_widget.insert(tk.END, self.buffer)
            self.text_widget.see(tk.END)  # 自动滚动到最后
            self.buffer = ""

    def flush(self):
        pass

class SdpSyncApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SDP Order Sync Tool")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

        # 设置图标（如果有的话）
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 创建标题标签
        title_label = ttk.Label(self.main_frame, text="SDP Order Sync Tool", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # 创建控制框架
        control_frame = ttk.Frame(self.main_frame)
        control_frame.pack(fill=tk.X, pady=10)

        # 创建强制同步复选框
        self.force_var = tk.BooleanVar(value=False)
        force_check = ttk.Checkbutton(control_frame, text="Force Sync (Ignore Duplicate Check)", variable=self.force_var)
        force_check.pack(side=tk.LEFT, padx=5)

        # 创建按钮框架
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side=tk.RIGHT)

        # 创建同步按钮
        self.sync_button = ttk.Button(button_frame, text="Start Sync", command=self.start_sync)
        self.sync_button.pack(side=tk.LEFT, padx=5)

        # 创建查看日志按钮
        self.log_button = ttk.Button(button_frame, text="View Logs", command=self.view_logs)
        self.log_button.pack(side=tk.LEFT, padx=5)

        # 创建退出按钮
        exit_button = ttk.Button(button_frame, text="Exit", command=self.root.quit)
        exit_button.pack(side=tk.LEFT, padx=5)

        # 创建状态标签
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(self.main_frame, textvariable=self.status_var)
        status_label.pack(fill=tk.X, pady=5)

        # 创建进度条
        self.progress = ttk.Progressbar(self.main_frame, mode="indeterminate")
        self.progress.pack(fill=tk.X, pady=5)

        # 创建输出文本框
        output_frame = ttk.LabelFrame(self.main_frame, text="Output")
        output_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=80, height=20)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 创建版权信息
        copyright_label = ttk.Label(self.main_frame, text="© 2025 SDP Order Sync Tool")
        copyright_label.pack(pady=5)

        # 同步线程
        self.sync_thread = None

        # 初始化输出
        self.output_text.insert(tk.END, "Welcome to SDP Order Sync Tool\n")
        self.output_text.insert(tk.END, "Click 'Start Sync' button to start syncing order data\n")
        self.output_text.insert(tk.END, "If you need to force sync (ignore duplicate check), please check the 'Force Sync' option\n")
        self.output_text.insert(tk.END, "=" * 80 + "\n")

    def start_sync(self):
        """开始同步"""
        # 禁用按钮，防止重复点击
        self.sync_button.config(state=tk.DISABLED)

        # 清空输出文本框
        self.output_text.delete(1.0, tk.END)

        # 更新状态
        self.status_var.set("Syncing...")

        # 启动进度条
        self.progress.start()

        # 获取强制同步选项
        force_sync = self.force_var.get()

        # 创建并启动同步线程
        self.sync_thread = threading.Thread(target=self.run_sync, args=(force_sync,))
        self.sync_thread.daemon = True
        self.sync_thread.start()

    def run_sync(self, force_sync):
        """在线程中运行同步"""
        try:
            # 重定向标准输出和标准错误到文本框
            stdout_redirector = TextRedirector(self.output_text)
            stderr_redirector = TextRedirector(self.output_text)

            with redirect_stdout(stdout_redirector), redirect_stderr(stderr_redirector):
                # 设置命令行参数
                sys.argv = ['sync_sdp_order.py']
                if force_sync:
                    sys.argv.append('--force')

                # 运行同步
                result = sync_sdp_order.main()

                # 更新UI
                self.root.after(0, self.sync_completed, result)
        except Exception as e:
            # 更新UI
            self.root.after(0, self.sync_failed, str(e))

    def sync_completed(self, result):
        """同步完成后的处理"""
        # 停止进度条
        self.progress.stop()

        # 更新状态
        if result == 0:
            self.status_var.set("Sync completed successfully")
            messagebox.showinfo("Sync Complete", "Order data synced successfully!")
        else:
            self.status_var.set("Sync failed")
            messagebox.showerror("Sync Failed", "Order data sync failed. Please check the logs for details.")

        # 启用按钮
        self.sync_button.config(state=tk.NORMAL)

    def sync_failed(self, error_msg):
        """同步失败后的处理"""
        # 停止进度条
        self.progress.stop()

        # 更新状态
        self.status_var.set("Sync error")

        # 显示错误信息
        self.output_text.insert(tk.END, f"\nError: {error_msg}\n")
        messagebox.showerror("Sync Error", f"An error occurred during sync:\n{error_msg}")

        # 启用按钮
        self.sync_button.config(state=tk.NORMAL)

    def view_logs(self):
        """查看日志"""
        try:
            # 运行日志查看工具
            subprocess.Popen(["python", "view_logs.py", "--list"])
        except Exception as e:
            messagebox.showerror("Error", f"Cannot start log viewer: {str(e)}")

def main():
    """主函数"""
    root = tk.Tk()
    app = SdpSyncApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
