#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
蔬东坡订单同步工具 - 图形界面版本
"""

import os
import sys
import time
import threading
import traceback
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime
import subprocess
import io
from contextlib import redirect_stdout, redirect_stderr

# 导入自定义模块
try:
    import sync_sdp_order
    from config_manager import config_manager
    from history_manager import history_manager
    from language_resources import _, language_manager
    from theme_manager import theme_manager
    from settings_dialog import SettingsDialog
    from history_dialog import HistoryDialog

    # 检查模块是否存在
    HAS_MODULES = True
except ImportError as e:
    print(f"Error importing modules: {e}")
    HAS_MODULES = False

    # 定义一个简单的翻译函数
    def _(text):
        return text

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
        self.root.title(_("app_name"))
        self.root.geometry("900x700")
        self.root.minsize(800, 600)

        # 设置图标（如果有的话）
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

        # 应用主题
        self.apply_theme()

        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 创建标题框架
        self.title_frame = ttk.Frame(self.main_frame)
        self.title_frame.pack(fill=tk.X, pady=(0, 10))

        # 创建标题标签
        title_font = ("SimHei", 12, "bold")
        title_label = ttk.Label(self.title_frame, text=_("main_title"), font=title_font)
        title_label.pack(side=tk.LEFT, pady=10)

        # 创建设置按钮
        button_font = ("SimHei", int(config_manager.get_config("ui", "font_size")))
        self.settings_button = tk.Button(self.title_frame, text=_("settings"), command=self.open_settings, font=button_font, bg="#f0f0f0")
        self.settings_button.pack(side=tk.RIGHT, padx=5)

        # 创建控制框架
        # 创建自定义样式
        style = ttk.Style()
        style.configure("Custom.TLabelframe.Label", font=button_font)
        control_frame = ttk.LabelFrame(self.main_frame, text=_("control"), style="Custom.TLabelframe")
        control_frame.pack(fill=tk.X, pady=10)

        # 创建控制内容框架
        control_content_frame = ttk.Frame(control_frame, padding="10")
        control_content_frame.pack(fill=tk.X)

        # 创建强制同步复选框
        self.force_var = tk.BooleanVar(value=False)
        force_check = tk.Checkbutton(control_content_frame, text=_("force_sync"), variable=self.force_var, font=button_font, bg="#f0f0f0")
        force_check.pack(side=tk.LEFT, padx=5)

        # 创建按钮框架
        button_frame = ttk.Frame(control_content_frame)
        button_frame.pack(side=tk.RIGHT)

        # 创建同步按钮
        self.sync_button = tk.Button(button_frame, text=_("start_sync"), command=self.start_sync, font=button_font, bg="#f0f0f0")
        self.sync_button.pack(side=tk.LEFT, padx=5)

        # 创建查看日志按钮
        self.log_button = tk.Button(button_frame, text=_("view_logs"), command=self.view_logs, font=button_font, bg="#f0f0f0")
        self.log_button.pack(side=tk.LEFT, padx=5)

        # 创建查看历史按钮
        self.history_button = tk.Button(button_frame, text=_("view_history"), command=self.view_history, font=button_font, bg="#f0f0f0")
        self.history_button.pack(side=tk.LEFT, padx=5)

        # 创建退出按钮
        exit_button = tk.Button(button_frame, text=_("exit"), command=self.root.quit, font=button_font, bg="#f0f0f0")
        exit_button.pack(side=tk.LEFT, padx=5)

        # 创建状态框架
        status_frame = ttk.Frame(self.main_frame)
        status_frame.pack(fill=tk.X, pady=5)

        # 创建状态标签
        self.status_var = tk.StringVar(value=_("ready"))
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(side=tk.LEFT, fill=tk.X)

        # 创建进度条
        self.progress = ttk.Progressbar(status_frame, mode="indeterminate")
        self.progress.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))

        # 创建输出框架
        output_frame = ttk.LabelFrame(self.main_frame, text=_("output"), style="Custom.TLabelframe")
        output_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # 创建输出文本框
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=80, height=20)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 创建版权信息
        copyright_label = ttk.Label(self.main_frame, text=_("copyright"))
        copyright_label.pack(pady=5)

        # 同步线程
        self.sync_thread = None

        # 初始化输出
        self.output_text.insert(tk.END, f"{_('welcome')}\n")
        self.output_text.insert(tk.END, f"{_('click_start')}\n")
        self.output_text.insert(tk.END, f"{_('force_tip')}\n")
        self.output_text.insert(tk.END, "=" * 80 + "\n")

    def apply_theme(self):
        """应用主题"""
        # 获取主题设置
        theme_name = config_manager.get_config("ui", "theme")
        theme_manager.set_theme(theme_name)

        # 应用主题
        theme_manager.apply_theme(self.root)

        # 设置字体大小
        font_size = config_manager.get_config("ui", "font_size")
        # 使用黑体，这个字体在大多数系统上都可用
        try:
            # 设置全局字体
            self.root.option_add("*Font", f"SimHei {font_size}")
            # 特别设置按钮字体
            self.root.option_add("*TButton*Font", f"SimHei {font_size}")
            self.root.option_add("*TLabel*Font", f"SimHei {font_size}")
            self.root.option_add("*TCheckbutton*Font", f"SimHei {font_size}")
            self.root.option_add("*TLabelframe*Font", f"SimHei {font_size}")
        except Exception as e:
            print(f"Warning: Could not set font: {e}")

    def update_settings(self):
        """更新设置"""
        # 应用主题
        self.apply_theme()

        # 更新语言
        language = config_manager.get_config("ui", "language")
        language_manager.set_language(language)

        # 更新界面文本
        self.root.title(_("app_name"))
        self.settings_button.config(text=_("settings"))
        self.sync_button.config(text=_("start_sync"))
        self.log_button.config(text=_("view_logs"))
        self.history_button.config(text=_("view_history"))
        self.status_var.set(_("ready"))

        # 重新加载界面
        self.root.update()

    def start_sync(self):
        """开始同步"""
        # 禁用按钮，防止重复点击
        self.sync_button.config(state=tk.DISABLED)

        # 清空输出文本框
        self.output_text.delete(1.0, tk.END)

        # 更新状态
        self.status_var.set(_("syncing"))

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
                start_time = time.time()
                result = sync_sdp_order.main()
                end_time = time.time()

                # 记录历史
                if result == 0:
                    history_manager.add_record("sync", "success", _("sync_success"), {
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "duration": f"{end_time - start_time:.2f}s",
                        "force": force_sync
                    })
                else:
                    history_manager.add_record("sync", "failed", _("sync_failed"), {
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "duration": f"{end_time - start_time:.2f}s",
                        "force": force_sync
                    })

                # 更新UI
                self.root.after(0, self.sync_completed, result)
        except Exception as e:
            # 记录历史
            history_manager.add_record("error", "failed", str(e), {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "traceback": traceback.format_exc()
            })

            # 更新UI
            self.root.after(0, self.sync_failed, str(e))

    def sync_completed(self, result):
        """同步完成后的处理"""
        # 停止进度条
        self.progress.stop()

        # 更新状态
        if result == 0:
            self.status_var.set(_("sync_success"))
            messagebox.showinfo(_("sync_complete"), _("sync_success_msg"))
        else:
            self.status_var.set(_("sync_failed"))
            messagebox.showerror(_("sync_failed"), _("sync_failed_msg"))

        # 启用按钮
        self.sync_button.config(state=tk.NORMAL)

    def sync_failed(self, error_msg):
        """同步失败后的处理"""
        # 停止进度条
        self.progress.stop()

        # 更新状态
        self.status_var.set(_("sync_error"))

        # 显示错误信息
        self.output_text.insert(tk.END, f"\n{_('error')}: {error_msg}\n")
        messagebox.showerror(_("sync_error"), f"{_('sync_error_msg')}\n{error_msg}")

        # 启用按钮
        self.sync_button.config(state=tk.NORMAL)

    def view_logs(self):
        """查看日志"""
        try:
            # 运行日志查看工具
            subprocess.Popen(["python", "view_logs.py", "--list"])
        except Exception as e:
            messagebox.showerror(_("error"), f"{_('log_error')}: {str(e)}")

    def view_history(self):
        """查看历史记录"""
        try:
            # 创建历史记录查看对话框
            history_dialog = HistoryDialog(self.root)
        except Exception as e:
            messagebox.showerror(_("error"), f"{_('history_error')}: {str(e)}")

    def open_settings(self):
        """打开设置对话框"""
        try:
            # 创建设置对话框
            settings_dialog = SettingsDialog(self.root)
        except Exception as e:
            messagebox.showerror(_("error"), f"{_('settings_error')}: {str(e)}")

def main():
    """主函数"""
    try:
        # 检查模块是否存在
        if not HAS_MODULES:
            # 显示错误对话框
            root = tk.Tk()
            root.withdraw()  # 隐藏主窗口
            messagebox.showerror("错误", "无法加载必要的模块\n\n请确保所有模块文件都在当前目录中")
            return

        # 加载配置
        config = config_manager.get_config()

        # 设置语言
        language = config["ui"]["language"]
        language_manager.set_language(language)

        # 创建主窗口
        root = tk.Tk()
        app = SdpSyncApp(root)
        root.mainloop()
    except Exception as e:
        # 显示错误对话框
        try:
            root = tk.Tk()
            root.withdraw()  # 隐藏主窗口
            messagebox.showerror("错误", f"启动应用程序时出错\n\n{str(e)}\n\n{traceback.format_exc()}")
        except:
            print(f"Critical error: {str(e)}")
            print(traceback.format_exc())

if __name__ == "__main__":
    main()
