#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
日志查看工具，用于查看最新的日志文件
"""

import os
import sys
import argparse
import re
from datetime import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# 导入自定义模块
try:
    from language_resources import _, language_manager
    from theme_manager import theme_manager
    from config_manager import config_manager
    HAS_GUI = True
except ImportError:
    # 如果找不到自定义模块，使用命令行模式
    HAS_GUI = False

    def _(text):
        return text

def get_log_files(log_dir="logs"):
    """
    获取日志目录下的所有日志文件

    Args:
        log_dir: 日志目录

    Returns:
        list: 日志文件列表，按修改时间排序
    """
    if not os.path.exists(log_dir):
        print(f"日志目录 {log_dir} 不存在")
        return []

    # 获取所有日志文件
    log_files = []
    for file in os.listdir(log_dir):
        if file.endswith(".log"):
            file_path = os.path.join(log_dir, file)
            log_files.append({
                "path": file_path,
                "name": file,
                "size": os.path.getsize(file_path),
                "mtime": os.path.getmtime(file_path)
            })

    # 按修改时间排序
    log_files.sort(key=lambda x: x["mtime"], reverse=True)

    return log_files

def format_size(size):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"

def format_time(timestamp):
    """格式化时间戳"""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def list_log_files(log_dir="logs"):
    """列出日志文件"""
    log_files = get_log_files(log_dir)

    if not log_files:
        print("没有找到日志文件")
        return

    print(f"找到 {len(log_files)} 个日志文件:")
    print("-" * 80)
    print(f"{'序号':<5} {'文件名':<30} {'大小':<10} {'修改时间':<20}")
    print("-" * 80)

    for i, log_file in enumerate(log_files):
        print(f"{i+1:<5} {log_file['name']:<30} {format_size(log_file['size']):<10} {format_time(log_file['mtime']):<20}")

def view_log_file(log_file, lines=50, filter_str=None):
    """
    查看日志文件内容

    Args:
        log_file: 日志文件路径
        lines: 显示的行数
        filter_str: 过滤字符串
    """
    if not os.path.exists(log_file):
        print(f"日志文件 {log_file} 不存在")
        return

    try:
        # 读取日志文件
        with open(log_file, 'r', encoding='utf-8') as f:
            log_lines = f.readlines()

        # 过滤日志
        if filter_str:
            log_lines = [line for line in log_lines if filter_str in line]
            print(f"过滤条件: '{filter_str}', 匹配 {len(log_lines)} 行")

        # 显示日志
        if lines > 0:
            log_lines = log_lines[-lines:]
            print(f"显示最后 {len(log_lines)} 行:")

        print("-" * 80)
        for line in log_lines:
            print(line.rstrip())
        print("-" * 80)

    except Exception as e:
        print(f"读取日志文件失败: {e}")

class LogViewer(tk.Tk):
    """日志查看器类"""

    def __init__(self, log_file=None, log_dir="logs"):
        """初始化日志查看器"""
        super().__init__()
        self.title(_("日志查看器"))
        self.geometry("900x700")
        self.minsize(800, 600)

        # 设置图标（如果有的话）
        try:
            self.iconbitmap("icon.ico")
        except:
            pass

        # 应用主题
        self.apply_theme()

        # 日志文件目录
        self.log_dir = log_dir

        # 日志文件
        self.log_file = log_file
        self.log_files = get_log_files(self.log_dir)

        # 创建界面
        self.create_widgets()

        # 加载日志
        if log_file:
            self.load_log(log_file)
        elif self.log_files:
            self.log_file = self.log_files[0]["path"]
            self.log_file_var.set(self.log_files[0]["name"])
            self.load_log(self.log_file)

    def apply_theme(self):
        """应用主题"""
        if not HAS_GUI:
            return

        # 获取主题设置
        theme_name = config_manager.get_config("ui", "theme")
        theme_manager.set_theme(theme_name)

        # 应用主题
        theme_manager.apply_theme(self)

        # 设置字体大小
        font_size = config_manager.get_config("ui", "font_size")
        self.option_add("*Font", f"Microsoft YaHei UI {font_size}")

    def create_widgets(self):
        """创建界面元素"""
        # 创建主框架
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 创建工具栏框架
        self.toolbar_frame = ttk.Frame(self.main_frame)
        self.toolbar_frame.pack(fill=tk.X, pady=(0, 10))

        # 创建日志文件选择框架
        self.file_frame = ttk.LabelFrame(self.toolbar_frame, text=_("日志文件"))
        self.file_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 创建日志文件下拉框
        self.log_file_var = tk.StringVar()
        self.log_file_combo = ttk.Combobox(self.file_frame, textvariable=self.log_file_var, state="readonly", width=50)
        self.log_file_combo["values"] = [log_file["name"] for log_file in self.log_files]
        self.log_file_combo.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        self.log_file_combo.bind("<<ComboboxSelected>>", self.on_log_file_change)

        # 创建刷新按钮
        self.refresh_button = ttk.Button(self.file_frame, text=_("刷新"), command=self.refresh_logs)
        self.refresh_button.pack(side=tk.LEFT, padx=5, pady=5)

        # 创建过滤框架
        self.filter_frame = ttk.LabelFrame(self.toolbar_frame, text=_("过滤"))
        self.filter_frame.pack(side=tk.RIGHT, padx=(10, 0))

        # 创建日志级别过滤
        ttk.Label(self.filter_frame, text=_("日志级别")).pack(side=tk.LEFT, padx=5, pady=5)
        self.log_level_var = tk.StringVar(value="ALL")
        log_level_combo = ttk.Combobox(self.filter_frame, textvariable=self.log_level_var, state="readonly", width=10)
        log_level_combo["values"] = ["ALL", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        log_level_combo.pack(side=tk.LEFT, padx=5, pady=5)
        log_level_combo.bind("<<ComboboxSelected>>", self.filter_log)

        # 创建过滤字符串输入框
        ttk.Label(self.filter_frame, text=_("关键字")).pack(side=tk.LEFT, padx=5, pady=5)
        self.filter_var = tk.StringVar()
        filter_entry = ttk.Entry(self.filter_frame, textvariable=self.filter_var, width=15)
        filter_entry.pack(side=tk.LEFT, padx=5, pady=5)
        filter_entry.bind("<Return>", self.filter_log)

        # 创建过滤按钮
        self.filter_button = ttk.Button(self.filter_frame, text=_("过滤"), command=self.filter_log)
        self.filter_button.pack(side=tk.LEFT, padx=5, pady=5)

        # 创建日志内容框架
        self.log_frame = ttk.LabelFrame(self.main_frame, text=_("日志内容"))
        self.log_frame.pack(fill=tk.BOTH, expand=True)

        # 创建日志文本框
        self.log_text = scrolledtext.ScrolledText(self.log_frame, wrap=tk.WORD, width=80, height=30)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_text.config(state=tk.DISABLED)

        # 创建按钮框架
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=(10, 0))

        # 创建关闭按钮
        self.close_button = ttk.Button(self.button_frame, text=_("关闭"), command=self.destroy)
        self.close_button.pack(side=tk.RIGHT)

    def load_log(self, log_file):
        """加载日志文件"""
        if not os.path.exists(log_file):
            messagebox.showerror(_("错误"), f"{_('日志文件不存在')}: {log_file}")
            return

        try:
            # 读取日志文件
            with open(log_file, "r", encoding="utf-8") as f:
                log_content = f.read()

            # 显示日志内容
            self.log_text.config(state=tk.NORMAL)
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, log_content)
            self.log_text.config(state=tk.DISABLED)

            # 设置标题
            self.title(f"{_('日志查看器')} - {os.path.basename(log_file)}")

            # 应用日志级别过滤
            self.filter_log()
        except Exception as e:
            messagebox.showerror(_("错误"), f"{_('加载日志失败')}: {str(e)}")

    def on_log_file_change(self, event=None):
        """日志文件变更事件处理"""
        log_file_name = self.log_file_var.get()
        if not log_file_name:
            return

        # 查找选中的日志文件
        for log_file in self.log_files:
            if log_file["name"] == log_file_name:
                self.log_file = log_file["path"]
                self.load_log(self.log_file)
                break

    def refresh_logs(self):
        """刷新日志文件列表"""
        # 获取日志文件列表
        self.log_files = get_log_files(self.log_dir)

        # 更新下拉框
        self.log_file_combo["values"] = [log_file["name"] for log_file in self.log_files]

        # 如果当前日志文件不在列表中，选择第一个
        current_file_exists = False
        for log_file in self.log_files:
            if log_file["path"] == self.log_file:
                current_file_exists = True
                break

        if not current_file_exists and self.log_files:
            self.log_file = self.log_files[0]["path"]
            self.log_file_var.set(self.log_files[0]["name"])

        # 重新加载当前日志文件
        if self.log_file:
            self.load_log(self.log_file)

    def filter_log(self, event=None):
        """过滤日志内容"""
        if not self.log_file:
            return

        # 获取日志级别和过滤字符串
        log_level = self.log_level_var.get()
        filter_str = self.filter_var.get()

        try:
            # 读取日志文件
            with open(self.log_file, "r", encoding="utf-8") as f:
                log_content = f.readlines()

            # 过滤日志
            filtered_lines = []
            for line in log_content:
                # 日志级别过滤
                if log_level != "ALL" and not re.search(f"\\[{log_level}\\]", line):
                    continue

                # 关键字过滤
                if filter_str and filter_str not in line:
                    continue

                filtered_lines.append(line)

            # 显示过滤后的日志内容
            self.log_text.config(state=tk.NORMAL)
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, "".join(filtered_lines))
            self.log_text.config(state=tk.DISABLED)

            # 更新标题
            filter_info = ""
            if log_level != "ALL":
                filter_info += f" [{log_level}]"
            if filter_str:
                filter_info += f" [\"{filter_str}\"]"

            if filter_info:
                self.title(f"{_('日志查看器')} - {os.path.basename(self.log_file)} - {_('过滤')}{filter_info}")
            else:
                self.title(f"{_('日志查看器')} - {os.path.basename(self.log_file)}")

            # 显示过滤结果
            messagebox.showinfo(_("过滤结果"), f"{_('共找到')} {len(filtered_lines)} {_('行匹配的日志')}")
        except Exception as e:
            messagebox.showerror(_("错误"), f"{_('过滤日志失败')}: {str(e)}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description=_('日志查看工具'))
    parser.add_argument('--dir', default='logs', help=_('日志目录'))
    parser.add_argument('--list', action='store_true', help=_('列出日志文件'))
    parser.add_argument('--file', type=int, default=1, help=_('查看的日志文件序号（默认为1，即最新的日志文件）'))
    parser.add_argument('--lines', type=int, default=50, help=_('显示的行数（默认为50，0表示显示全部）'))
    parser.add_argument('--filter', help=_('过滤字符串'))
    parser.add_argument('--gui', action='store_true', help=_('使用图形界面'))

    args = parser.parse_args()

    # 如果指定了使用图形界面并且支持GUI
    if args.gui and HAS_GUI:
        # 加载配置
        config = config_manager.get_config()

        # 设置语言
        language = config["ui"]["language"]
        language_manager.set_language(language)

        # 创建日志查看器
        log_viewer = LogViewer(log_dir=args.dir)
        log_viewer.mainloop()
        return

    # 列出日志文件
    if args.list:
        list_log_files(args.dir)
        return

    # 获取日志文件
    log_files = get_log_files(args.dir)

    if not log_files:
        print(_("没有找到日志文件"))
        return

    # 查看日志文件
    file_index = args.file - 1
    if file_index < 0 or file_index >= len(log_files):
        print(f"{_('无效的文件序号')}: {args.file}，{_('有效范围')}: 1-{len(log_files)}")
        return

    log_file = log_files[file_index]
    print(f"{_('查看日志文件')}: {log_file['name']}")
    view_log_file(log_file['path'], args.lines, args.filter)

if __name__ == "__main__":
    main()
