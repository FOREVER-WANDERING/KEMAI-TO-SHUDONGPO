#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
主题管理模块，用于支持不同的界面主题
"""

import tkinter as tk
from tkinter import ttk
import logging

# 默认主题
DEFAULT_THEME = {
    "bg_color": "#f0f0f0",           # 背景色
    "fg_color": "#333333",           # 前景色（文字颜色）
    "accent_color": "#4a6baf",       # 强调色（按钮、链接等）
    "accent_hover": "#3a5b9f",       # 强调色悬停
    "accent_active": "#2a4b8f",      # 强调色激活
    "success_color": "#28a745",      # 成功色
    "warning_color": "#ffc107",      # 警告色
    "error_color": "#dc3545",        # 错误色
    "info_color": "#17a2b8",         # 信息色
    "border_color": "#cccccc",       # 边框色
    "input_bg": "#ffffff",           # 输入框背景色
    "input_fg": "#333333",           # 输入框前景色
    "disabled_bg": "#e9ecef",        # 禁用背景色
    "disabled_fg": "#6c757d",        # 禁用前景色
    "font_family": "Microsoft YaHei UI", # 字体
    "font_size_small": 9,            # 小字体大小
    "font_size_normal": 10,          # 普通字体大小
    "font_size_large": 12,           # 大字体大小
    "font_size_xlarge": 14,          # 超大字体大小
    "padding_small": 2,              # 小内边距
    "padding_normal": 5,             # 普通内边距
    "padding_large": 10,             # 大内边距
    "margin_small": 2,               # 小外边距
    "margin_normal": 5,              # 普通外边距
    "margin_large": 10,              # 大外边距
    "border_radius": 4,              # 边框圆角
    "border_width": 1,               # 边框宽度
    "shadow": "1px 1px 3px rgba(0,0,0,0.2)" # 阴影
}

# 浅色主题
LIGHT_THEME = {
    "bg_color": "#ffffff",
    "fg_color": "#333333",
    "accent_color": "#007bff",
    "accent_hover": "#0069d9",
    "accent_active": "#0062cc",
    "success_color": "#28a745",
    "warning_color": "#ffc107",
    "error_color": "#dc3545",
    "info_color": "#17a2b8",
    "border_color": "#dee2e6",
    "input_bg": "#ffffff",
    "input_fg": "#495057",
    "disabled_bg": "#e9ecef",
    "disabled_fg": "#6c757d",
    "font_family": "Microsoft YaHei UI",
    "font_size_small": 9,
    "font_size_normal": 10,
    "font_size_large": 12,
    "font_size_xlarge": 14,
    "padding_small": 2,
    "padding_normal": 5,
    "padding_large": 10,
    "margin_small": 2,
    "margin_normal": 5,
    "margin_large": 10,
    "border_radius": 4,
    "border_width": 1,
    "shadow": "1px 1px 3px rgba(0,0,0,0.1)"
}

# 深色主题
DARK_THEME = {
    "bg_color": "#343a40",
    "fg_color": "#f8f9fa",
    "accent_color": "#007bff",
    "accent_hover": "#0069d9",
    "accent_active": "#0062cc",
    "success_color": "#28a745",
    "warning_color": "#ffc107",
    "error_color": "#dc3545",
    "info_color": "#17a2b8",
    "border_color": "#495057",
    "input_bg": "#495057",
    "input_fg": "#f8f9fa",
    "disabled_bg": "#6c757d",
    "disabled_fg": "#adb5bd",
    "font_family": "Microsoft YaHei UI",
    "font_size_small": 9,
    "font_size_normal": 10,
    "font_size_large": 12,
    "font_size_xlarge": 14,
    "padding_small": 2,
    "padding_normal": 5,
    "padding_large": 10,
    "margin_small": 2,
    "margin_normal": 5,
    "margin_large": 10,
    "border_radius": 4,
    "border_width": 1,
    "shadow": "1px 1px 3px rgba(0,0,0,0.3)"
}

# 主题字典
THEMES = {
    "default": DEFAULT_THEME,
    "light": LIGHT_THEME,
    "dark": DARK_THEME
}

class ThemeManager:
    """主题管理类"""
    
    def __init__(self, theme_name="default"):
        """初始化主题管理器"""
        self.theme_name = theme_name
        self.theme = THEMES.get(theme_name, DEFAULT_THEME)
    
    def set_theme(self, theme_name):
        """设置主题"""
        if theme_name in THEMES:
            self.theme_name = theme_name
            self.theme = THEMES.get(theme_name, DEFAULT_THEME)
            return True
        return False
    
    def get_theme(self):
        """获取当前主题"""
        return self.theme
    
    def get_theme_name(self):
        """获取当前主题名称"""
        return self.theme_name
    
    def get_style(self, key, default=None):
        """获取样式"""
        return self.theme.get(key, default)
    
    def apply_theme(self, root):
        """应用主题到tkinter窗口"""
        try:
            # 创建ttk样式
            style = ttk.Style()
            
            # 配置ttk主题
            style.configure("TFrame", background=self.theme["bg_color"])
            style.configure("TLabel", background=self.theme["bg_color"], foreground=self.theme["fg_color"])
            style.configure("TButton", 
                            background=self.theme["accent_color"], 
                            foreground="white", 
                            padding=(self.theme["padding_normal"], self.theme["padding_small"]))
            style.map("TButton",
                     background=[("active", self.theme["accent_active"]), 
                                 ("disabled", self.theme["disabled_bg"])],
                     foreground=[("disabled", self.theme["disabled_fg"])])
            
            style.configure("TCheckbutton", 
                           background=self.theme["bg_color"], 
                           foreground=self.theme["fg_color"])
            
            style.configure("TEntry", 
                           fieldbackground=self.theme["input_bg"], 
                           foreground=self.theme["input_fg"])
            
            style.configure("TNotebook", 
                           background=self.theme["bg_color"], 
                           tabmargins=(2, 5, 2, 0))
            
            style.configure("TNotebook.Tab", 
                           background=self.theme["bg_color"], 
                           foreground=self.theme["fg_color"],
                           padding=(10, 2))
            
            style.map("TNotebook.Tab",
                     background=[("selected", self.theme["accent_color"])],
                     foreground=[("selected", "white")])
            
            # 配置文本框样式
            root.option_add("*Text.Background", self.theme["input_bg"])
            root.option_add("*Text.Foreground", self.theme["input_fg"])
            root.option_add("*Text.selectBackground", self.theme["accent_color"])
            root.option_add("*Text.selectForeground", "white")
            
            # 配置滚动条样式
            style.configure("Vertical.TScrollbar", 
                           background=self.theme["bg_color"], 
                           troughcolor=self.theme["bg_color"],
                           arrowcolor=self.theme["fg_color"])
            
            # 配置进度条样式
            style.configure("TProgressbar", 
                           background=self.theme["accent_color"], 
                           troughcolor=self.theme["bg_color"])
            
            # 配置组合框样式
            style.configure("TCombobox", 
                           fieldbackground=self.theme["input_bg"], 
                           foreground=self.theme["input_fg"])
            
            # 配置分隔线样式
            style.configure("TSeparator", 
                           background=self.theme["border_color"])
            
            # 配置标签框样式
            style.configure("TLabelframe", 
                           background=self.theme["bg_color"], 
                           foreground=self.theme["fg_color"])
            
            style.configure("TLabelframe.Label", 
                           background=self.theme["bg_color"], 
                           foreground=self.theme["fg_color"])
            
            # 设置窗口背景色
            root.configure(background=self.theme["bg_color"])
            
            return True
        except Exception as e:
            logging.error(f"应用主题失败: {e}")
            return False

# 创建全局主题管理器实例
theme_manager = ThemeManager()

if __name__ == "__main__":
    # 测试主题管理器
    root = tk.Tk()
    root.title("主题测试")
    root.geometry("400x300")
    
    theme_manager.apply_theme(root)
    
    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    label = ttk.Label(frame, text="这是一个测试标签")
    label.pack(pady=10)
    
    button = ttk.Button(frame, text="测试按钮")
    button.pack(pady=10)
    
    check = ttk.Checkbutton(frame, text="测试复选框")
    check.pack(pady=10)
    
    entry = ttk.Entry(frame)
    entry.pack(pady=10, fill=tk.X)
    entry.insert(0, "测试输入框")
    
    root.mainloop()
