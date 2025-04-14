#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
设置对话框模块
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
import requests
import json
import logging
import time

from config_manager import config_manager
from language_resources import _
from theme_manager import theme_manager

class SettingsDialog(tk.Toplevel):
    """设置对话框类"""

    def __init__(self, parent):
        """初始化设置对话框"""
        super().__init__(parent)
        self.parent = parent
        self.title(_("settings_title"))
        self.geometry("600x500")
        self.minsize(500, 400)
        self.resizable(True, True)
        self.transient(parent)  # 设置为父窗口的临时窗口
        self.grab_set()  # 模态对话框

        # 应用主题
        theme_manager.apply_theme(self)

        # 设置字体
        self.button_font = ("SimHei", 10)

        # 创建界面
        self.create_widgets()

        # 加载配置
        self.load_config()

        # 居中显示
        self.center_window()

    def create_widgets(self):
        """创建界面元素"""
        # 创建主框架
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 创建选项卡
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # 创建数据库设置选项卡
        self.db_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.db_frame, text=_("settings_database"))
        self.create_db_settings()

        # 创建API设置选项卡
        self.api_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.api_frame, text=_("settings_api"))
        self.create_api_settings()

        # 创建界面设置选项卡
        self.ui_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.ui_frame, text=_("settings_ui"))
        self.create_ui_settings()

        # 创建日志设置选项卡
        self.log_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.log_frame, text=_("settings_log"))
        self.create_log_settings()

        # 创建同步设置选项卡
        self.sync_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.sync_frame, text=_("settings_sync"))
        self.create_sync_settings()

        # 创建按钮框架
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=10)

        # 创建重置按钮
        self.reset_button = tk.Button(self.button_frame, text=_("settings_reset"), command=self.reset_settings, font=self.button_font, bg="#f0f0f0")
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # 创建保存按钮
        self.save_button = tk.Button(self.button_frame, text=_("save"), command=self.save_settings, font=self.button_font, bg="#f0f0f0")
        self.save_button.pack(side=tk.RIGHT, padx=5)

        # 创建取消按钮
        self.cancel_button = tk.Button(self.button_frame, text=_("cancel"), command=self.destroy, font=self.button_font, bg="#f0f0f0")
        self.cancel_button.pack(side=tk.RIGHT, padx=5)

    def create_db_settings(self):
        """创建数据库设置界面"""
        # 创建表单框架
        form_frame = ttk.Frame(self.db_frame)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # 主机
        ttk.Label(form_frame, text=_("db_host")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.db_host_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.db_host_var).grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        # 端口
        ttk.Label(form_frame, text=_("db_port")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.db_port_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.db_port_var).grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

        # 用户名
        ttk.Label(form_frame, text=_("db_user")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.db_user_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.db_user_var).grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)

        # 密码
        ttk.Label(form_frame, text=_("db_password")).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.db_password_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.db_password_var, show="*").grid(row=3, column=1, sticky=tk.EW, padx=5, pady=5)

        # 数据库
        ttk.Label(form_frame, text=_("db_database")).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.db_database_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.db_database_var).grid(row=4, column=1, sticky=tk.EW, padx=5, pady=5)

        # 测试连接按钮
        tk.Button(form_frame, text=_("db_test"), command=self.test_db_connection, font=self.button_font, bg="#f0f0f0").grid(row=5, column=1, sticky=tk.E, padx=5, pady=10)

        # 设置列权重
        form_frame.columnconfigure(1, weight=1)

    def create_api_settings(self):
        """创建API设置界面"""
        # 创建表单框架
        form_frame = ttk.Frame(self.api_frame)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # 基础URL
        ttk.Label(form_frame, text=_("api_base_url")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.api_base_url_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.api_base_url_var).grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        # 应用ID
        ttk.Label(form_frame, text=_("api_appid")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.api_appid_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.api_appid_var).grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

        # 密钥
        ttk.Label(form_frame, text=_("api_secret")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.api_secret_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.api_secret_var, show="*").grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)

        # 测试API按钮
        tk.Button(form_frame, text=_("api_test"), command=self.test_api_connection, font=self.button_font, bg="#f0f0f0").grid(row=3, column=1, sticky=tk.E, padx=5, pady=10)

        # 设置列权重
        form_frame.columnconfigure(1, weight=1)

    def create_ui_settings(self):
        """创建界面设置界面"""
        # 创建表单框架
        form_frame = ttk.Frame(self.ui_frame)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # 主题
        ttk.Label(form_frame, text=_("ui_theme")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ui_theme_var = tk.StringVar()
        theme_combo = ttk.Combobox(form_frame, textvariable=self.ui_theme_var, state="readonly")
        theme_combo["values"] = [_("ui_theme_default"), _("ui_theme_light"), _("ui_theme_dark")]
        theme_combo.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        # 字体大小
        ttk.Label(form_frame, text=_("ui_font_size")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.ui_font_size_var = tk.IntVar()
        font_size_combo = ttk.Combobox(form_frame, textvariable=self.ui_font_size_var, state="readonly")
        font_size_combo["values"] = [8, 9, 10, 11, 12, 14, 16]
        font_size_combo.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

        # 语言
        ttk.Label(form_frame, text=_("ui_language")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.ui_language_var = tk.StringVar()
        language_combo = ttk.Combobox(form_frame, textvariable=self.ui_language_var, state="readonly")
        language_combo["values"] = [_("ui_language_zh_CN"), _("ui_language_en_US")]
        language_combo.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)

        # 设置列权重
        form_frame.columnconfigure(1, weight=1)

    def create_log_settings(self):
        """创建日志设置界面"""
        # 创建表单框架
        form_frame = ttk.Frame(self.log_frame)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # 日志级别
        ttk.Label(form_frame, text=_("log_level_setting")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.log_level_var = tk.StringVar()
        log_level_combo = ttk.Combobox(form_frame, textvariable=self.log_level_var, state="readonly")
        log_level_combo["values"] = [_("log_level_debug"), _("log_level_info"), _("log_level_warning"), _("log_level_error"), _("log_level_critical")]
        log_level_combo.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        # 最大日志文件数
        ttk.Label(form_frame, text=_("log_max_files")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.log_max_files_var = tk.IntVar()
        ttk.Entry(form_frame, textvariable=self.log_max_files_var).grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

        # 单个日志文件最大大小
        ttk.Label(form_frame, text=_("log_max_size")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.log_max_size_var = tk.IntVar()
        ttk.Entry(form_frame, textvariable=self.log_max_size_var).grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)

        # 设置列权重
        form_frame.columnconfigure(1, weight=1)

    def create_sync_settings(self):
        """创建同步设置界面"""
        # 创建表单框架
        form_frame = ttk.Frame(self.sync_frame)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # 自动同步
        self.sync_auto_var = tk.BooleanVar()
        ttk.Checkbutton(form_frame, text=_("sync_auto"), variable=self.sync_auto_var).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)

        # 同步时间
        ttk.Label(form_frame, text=_("sync_time")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.sync_time_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.sync_time_var).grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

        # 默认站点ID
        ttk.Label(form_frame, text=_("sync_default_site")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.sync_default_site_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.sync_default_site_var).grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)

        # 默认配送时间段ID
        ttk.Label(form_frame, text=_("sync_default_delivery")).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.sync_default_delivery_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.sync_default_delivery_var).grid(row=3, column=1, sticky=tk.EW, padx=5, pady=5)

        # 默认支付方式
        ttk.Label(form_frame, text=_("sync_default_pay")).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.sync_default_pay_var = tk.IntVar()
        pay_frame = ttk.Frame(form_frame)
        pay_frame.grid(row=4, column=1, sticky=tk.EW, padx=5, pady=5)
        ttk.Radiobutton(pay_frame, text=_("sync_pay_cod"), variable=self.sync_default_pay_var, value=0).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(pay_frame, text=_("sync_pay_online"), variable=self.sync_default_pay_var, value=1).pack(side=tk.LEFT, padx=5)

        # 设置列权重
        form_frame.columnconfigure(1, weight=1)

    def load_config(self):
        """加载配置"""
        # 数据库配置
        self.db_host_var.set(config_manager.get_config("db", "host"))
        self.db_port_var.set(config_manager.get_config("db", "port"))
        self.db_user_var.set(config_manager.get_config("db", "user"))
        self.db_password_var.set(config_manager.get_config("db", "password"))
        self.db_database_var.set(config_manager.get_config("db", "database"))

        # API配置
        self.api_base_url_var.set(config_manager.get_config("sdp_api", "base_url"))
        self.api_appid_var.set(config_manager.get_config("sdp_api", "appid"))
        self.api_secret_var.set(config_manager.get_config("sdp_api", "secret"))

        # 界面配置
        theme = config_manager.get_config("ui", "theme")
        if theme == "default":
            self.ui_theme_var.set(_("ui_theme_default"))
        elif theme == "light":
            self.ui_theme_var.set(_("ui_theme_light"))
        elif theme == "dark":
            self.ui_theme_var.set(_("ui_theme_dark"))

        self.ui_font_size_var.set(config_manager.get_config("ui", "font_size"))

        language = config_manager.get_config("ui", "language")
        if language == "zh_CN":
            self.ui_language_var.set(_("ui_language_zh_CN"))
        elif language == "en_US":
            self.ui_language_var.set(_("ui_language_en_US"))

        # 日志配置
        log_level = config_manager.get_config("log", "level")
        if log_level == "DEBUG":
            self.log_level_var.set(_("log_level_debug"))
        elif log_level == "INFO":
            self.log_level_var.set(_("log_level_info"))
        elif log_level == "WARNING":
            self.log_level_var.set(_("log_level_warning"))
        elif log_level == "ERROR":
            self.log_level_var.set(_("log_level_error"))
        elif log_level == "CRITICAL":
            self.log_level_var.set(_("log_level_critical"))

        self.log_max_files_var.set(config_manager.get_config("log", "max_files"))
        self.log_max_size_var.set(config_manager.get_config("log", "max_size"))

        # 同步配置
        self.sync_auto_var.set(config_manager.get_config("sync", "auto_sync"))
        self.sync_time_var.set(config_manager.get_config("sync", "sync_time"))
        self.sync_default_site_var.set(config_manager.get_config("default_site_id"))
        self.sync_default_delivery_var.set(config_manager.get_config("default_delivery_time"))
        self.sync_default_pay_var.set(config_manager.get_config("default_pay_way"))

    def save_settings(self):
        """保存设置"""
        try:
            # 数据库配置
            config_manager.set_config("db", "host", self.db_host_var.get())
            config_manager.set_config("db", "port", self.db_port_var.get())
            config_manager.set_config("db", "user", self.db_user_var.get())
            config_manager.set_config("db", "password", self.db_password_var.get())
            config_manager.set_config("db", "database", self.db_database_var.get())

            # API配置
            config_manager.set_config("sdp_api", "base_url", self.api_base_url_var.get())
            config_manager.set_config("sdp_api", "appid", self.api_appid_var.get())
            config_manager.set_config("sdp_api", "secret", self.api_secret_var.get())

            # 界面配置
            theme = "default"
            if self.ui_theme_var.get() == _("ui_theme_default"):
                theme = "default"
            elif self.ui_theme_var.get() == _("ui_theme_light"):
                theme = "light"
            elif self.ui_theme_var.get() == _("ui_theme_dark"):
                theme = "dark"
            config_manager.set_config("ui", "theme", theme)

            config_manager.set_config("ui", "font_size", self.ui_font_size_var.get())

            language = "zh_CN"
            if self.ui_language_var.get() == _("ui_language_zh_CN"):
                language = "zh_CN"
            elif self.ui_language_var.get() == _("ui_language_en_US"):
                language = "en_US"
            config_manager.set_config("ui", "language", language)

            # 日志配置
            log_level = "INFO"
            if self.log_level_var.get() == _("log_level_debug"):
                log_level = "DEBUG"
            elif self.log_level_var.get() == _("log_level_info"):
                log_level = "INFO"
            elif self.log_level_var.get() == _("log_level_warning"):
                log_level = "WARNING"
            elif self.log_level_var.get() == _("log_level_error"):
                log_level = "ERROR"
            elif self.log_level_var.get() == _("log_level_critical"):
                log_level = "CRITICAL"
            config_manager.set_config("log", "level", log_level)

            config_manager.set_config("log", "max_files", self.log_max_files_var.get())
            config_manager.set_config("log", "max_size", self.log_max_size_var.get())

            # 同步配置
            config_manager.set_config("sync", "auto_sync", self.sync_auto_var.get())
            config_manager.set_config("sync", "sync_time", self.sync_time_var.get())
            config_manager.set_config("default_site_id", self.sync_default_site_var.get())
            config_manager.set_config("default_delivery_time", self.sync_default_delivery_var.get())
            config_manager.set_config("default_pay_way", self.sync_default_pay_var.get())

            # 保存配置
            if config_manager.save_config():
                messagebox.showinfo(_("success"), _("settings_save_success"))
                # 通知父窗口更新设置
                self.parent.update_settings()
                self.destroy()
            else:
                messagebox.showerror(_("error"), _("settings_save_failed"))
        except Exception as e:
            logging.error(f"保存设置失败: {e}")
            messagebox.showerror(_("error"), f"{_('settings_save_failed')}: {str(e)}")

    def reset_settings(self):
        """重置设置"""
        if messagebox.askyesno(_("warning"), _("settings_reset_confirm")):
            # 重置配置
            config_manager.save_config(config_manager.DEFAULT_CONFIG)
            # 重新加载配置
            self.load_config()

    def test_db_connection(self):
        """测试数据库连接"""
        try:
            # 构建连接字符串
            conn_str = f"DRIVER={{SQL Server}};SERVER={self.db_host_var.get()},{self.db_port_var.get()};DATABASE={self.db_database_var.get()};UID={self.db_user_var.get()};PWD={self.db_password_var.get()}"

            # 尝试连接
            conn = pyodbc.connect(conn_str)
            conn.close()

            messagebox.showinfo(_("success"), _("db_test_success"))
        except Exception as e:
            logging.error(f"数据库连接测试失败: {e}")
            messagebox.showerror(_("error"), f"{_('db_test_failed')}: {str(e)}")

    def test_api_connection(self):
        """测试API连接"""
        try:
            # 构建请求参数
            base_url = self.api_base_url_var.get()
            appid = self.api_appid_var.get()
            secret = self.api_secret_var.get()

            # 构建请求URL
            url = f"{base_url}/openApi/common/siteList"

            # 构建请求参数
            params = {
                "status": 1,
                "appid": appid,
                "timestamp": int(time.time()),
                "sign": self.generate_sign(appid, secret)
            }

            # 发送请求
            response = requests.get(url, params=params, verify=False)
            response.raise_for_status()

            # 解析响应
            result = response.json()

            if result["status"] == 1:
                messagebox.showinfo(_("success"), _("api_test_success"))
            else:
                messagebox.showerror(_("error"), f"{_('api_test_failed')}: {result.get('message', '未知错误')}")
        except Exception as e:
            logging.error(f"API连接测试失败: {e}")
            messagebox.showerror(_("error"), f"{_('api_test_failed')}: {str(e)}")

    def generate_sign(self, appid, secret):
        """生成签名"""
        import hashlib
        import time

        # 获取当前时间戳
        timestamp = int(time.time())

        # 构建签名字符串
        sign_str = f"{appid}{timestamp}{secret}"

        # 计算MD5
        md5 = hashlib.md5()
        md5.update(sign_str.encode("utf-8"))
        sign = md5.hexdigest().upper()

        return sign

    def center_window(self):
        """居中显示窗口"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    # 测试设置对话框
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    # 创建设置对话框
    dialog = SettingsDialog(root)

    # 等待对话框关闭
    root.wait_window(dialog)

    # 退出
    root.destroy()
