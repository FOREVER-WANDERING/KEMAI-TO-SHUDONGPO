#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
历史记录查看对话框模块
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

from history_manager import history_manager
from language_resources import _
from theme_manager import theme_manager

class HistoryDialog(tk.Toplevel):
    """历史记录查看对话框类"""

    def __init__(self, parent):
        """初始化历史记录查看对话框"""
        super().__init__(parent)
        self.parent = parent
        self.title(_("history_viewer"))
        self.geometry("800x600")
        self.minsize(600, 400)
        self.resizable(True, True)
        self.transient(parent)  # 设置为父窗口的临时窗口
        self.grab_set()  # 模态对话框

        # 应用主题
        theme_manager.apply_theme(self)

        # 创建界面
        self.create_widgets()

        # 加载历史记录
        self.load_history()

        # 居中显示
        self.center_window()

    def create_widgets(self):
        """创建界面元素"""
        # 创建主框架
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 创建工具栏框架
        self.toolbar_frame = ttk.Frame(self.main_frame)
        self.toolbar_frame.pack(fill=tk.X, pady=(0, 10))

        # 创建过滤框架
        self.filter_frame = ttk.LabelFrame(self.toolbar_frame, text=_("filter"))
        self.filter_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 创建类型过滤
        ttk.Label(self.filter_frame, text=_("history_type")).pack(side=tk.LEFT, padx=5)
        self.type_var = tk.StringVar(value="all")
        type_combo = ttk.Combobox(self.filter_frame, textvariable=self.type_var, state="readonly", width=10)
        type_combo["values"] = ["all", _("history_type_sync"), _("history_type_config"), _("history_type_error")]
        type_combo.pack(side=tk.LEFT, padx=5)
        type_combo.bind("<<ComboboxSelected>>", self.filter_history)

        # 创建状态过滤
        ttk.Label(self.filter_frame, text=_("history_status")).pack(side=tk.LEFT, padx=5)
        self.status_var = tk.StringVar(value="all")
        status_combo = ttk.Combobox(self.filter_frame, textvariable=self.status_var, state="readonly", width=10)
        status_combo["values"] = ["all", _("history_status_success"), _("history_status_failed"), _("history_status_warning")]
        status_combo.pack(side=tk.LEFT, padx=5)
        status_combo.bind("<<ComboboxSelected>>", self.filter_history)

        # 创建按钮框架
        self.button_frame = ttk.Frame(self.toolbar_frame)
        self.button_frame.pack(side=tk.RIGHT)

        # 创建刷新按钮
        button_font = ("SimHei", 10)
        self.refresh_button = tk.Button(self.button_frame, text=_("refresh"), command=self.load_history, font=button_font, bg="#f0f0f0")
        self.refresh_button.pack(side=tk.LEFT, padx=5)

        # 创建导出按钮
        self.export_button = tk.Button(self.button_frame, text=_("history_export"), command=self.export_history, font=button_font, bg="#f0f0f0")
        self.export_button.pack(side=tk.LEFT, padx=5)

        # 创建清空按钮
        self.clear_button = tk.Button(self.button_frame, text=_("history_clear"), command=self.clear_history, font=button_font, bg="#f0f0f0")
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # 创建历史记录表格
        self.create_history_table()

        # 创建详细信息框架
        self.details_frame = ttk.LabelFrame(self.main_frame, text=_("history_details"))
        self.details_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # 创建详细信息文本框
        self.details_text = tk.Text(self.details_frame, wrap=tk.WORD, width=80, height=10)
        self.details_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.details_text.config(state=tk.DISABLED)

        # 创建关闭按钮
        self.close_button = tk.Button(self.main_frame, text=_("close"), command=self.destroy, font=button_font, bg="#f0f0f0")
        self.close_button.pack(side=tk.RIGHT, pady=(10, 0))

    def create_history_table(self):
        """创建历史记录表格"""
        # 创建表格框架
        self.table_frame = ttk.Frame(self.main_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        # 创建滚动条
        scrollbar_y = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar_x = ttk.Scrollbar(self.table_frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # 创建表格
        self.table = ttk.Treeview(self.table_frame,
                                 columns=("type", "status", "time", "message"),
                                 show="headings",
                                 yscrollcommand=scrollbar_y.set,
                                 xscrollcommand=scrollbar_x.set)

        # 设置列宽和对齐方式
        self.table.column("type", width=100, anchor=tk.CENTER)
        self.table.column("status", width=100, anchor=tk.CENTER)
        self.table.column("time", width=150, anchor=tk.CENTER)
        self.table.column("message", width=400, anchor=tk.W)

        # 设置表头
        self.table.heading("type", text=_("history_type"))
        self.table.heading("status", text=_("history_status"))
        self.table.heading("time", text=_("history_time"))
        self.table.heading("message", text=_("history_message"))

        # 绑定滚动条
        scrollbar_y.config(command=self.table.yview)
        scrollbar_x.config(command=self.table.xview)

        # 绑定选择事件
        self.table.bind("<<TreeviewSelect>>", self.on_select)

        # 显示表格
        self.table.pack(fill=tk.BOTH, expand=True)

    def load_history(self):
        """加载历史记录"""
        # 清空表格
        for item in self.table.get_children():
            self.table.delete(item)

        # 获取历史记录
        records = history_manager.get_records()

        if not records:
            # 如果没有历史记录，显示提示信息
            self.table.insert("", tk.END, values=("", "", "", _("history_empty")))
            return

        # 添加历史记录到表格
        for record in records:
            # 获取记录类型
            record_type = record["type"]
            if record_type == "sync":
                record_type = _("history_type_sync")
            elif record_type == "config":
                record_type = _("history_type_config")
            elif record_type == "error":
                record_type = _("history_type_error")

            # 获取记录状态
            status = record["status"]
            if status == "success":
                status = _("history_status_success")
            elif status == "failed":
                status = _("history_status_failed")
            elif status == "warning":
                status = _("history_status_warning")

            # 添加记录到表格
            self.table.insert("", tk.END, values=(record_type, status, record["timestamp"], record["message"]), tags=(record["status"],))

        # 设置行颜色
        self.table.tag_configure("success", background="#d4edda")
        self.table.tag_configure("failed", background="#f8d7da")
        self.table.tag_configure("warning", background="#fff3cd")

    def filter_history(self, event=None):
        """过滤历史记录"""
        # 获取过滤条件
        type_filter = self.type_var.get()
        status_filter = self.status_var.get()

        # 转换为英文
        if type_filter == _("history_type_sync"):
            type_filter = "sync"
        elif type_filter == _("history_type_config"):
            type_filter = "config"
        elif type_filter == _("history_type_error"):
            type_filter = "error"

        if status_filter == _("history_status_success"):
            status_filter = "success"
        elif status_filter == _("history_status_failed"):
            status_filter = "failed"
        elif status_filter == _("history_status_warning"):
            status_filter = "warning"

        # 清空表格
        for item in self.table.get_children():
            self.table.delete(item)

        # 获取历史记录
        records = history_manager.get_records()

        if not records:
            # 如果没有历史记录，显示提示信息
            self.table.insert("", tk.END, values=("", "", "", _("history_empty")))
            return

        # 过滤历史记录
        filtered_records = []
        for record in records:
            # 类型过滤
            if type_filter != "all" and record["type"] != type_filter:
                continue

            # 状态过滤
            if status_filter != "all" and record["status"] != status_filter:
                continue

            filtered_records.append(record)

        if not filtered_records:
            # 如果没有符合条件的历史记录，显示提示信息
            self.table.insert("", tk.END, values=("", "", "", _("history_empty")))
            return

        # 添加历史记录到表格
        for record in filtered_records:
            # 获取记录类型
            record_type = record["type"]
            if record_type == "sync":
                record_type = _("history_type_sync")
            elif record_type == "config":
                record_type = _("history_type_config")
            elif record_type == "error":
                record_type = _("history_type_error")

            # 获取记录状态
            status = record["status"]
            if status == "success":
                status = _("history_status_success")
            elif status == "failed":
                status = _("history_status_failed")
            elif status == "warning":
                status = _("history_status_warning")

            # 添加记录到表格
            self.table.insert("", tk.END, values=(record_type, status, record["timestamp"], record["message"]), tags=(record["status"],))

    def on_select(self, event=None):
        """选择事件处理"""
        # 获取选中的项
        selected_items = self.table.selection()
        if not selected_items:
            return

        # 获取选中项的索引
        item_id = selected_items[0]
        item_index = self.table.index(item_id)

        # 获取历史记录
        records = history_manager.get_records()

        if not records or item_index >= len(records):
            return

        # 获取选中的记录
        record = records[item_index]

        # 显示详细信息
        self.show_details(record)

    def show_details(self, record):
        """显示详细信息"""
        # 清空详细信息文本框
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)

        # 添加详细信息
        if record["details"]:
            details = json.dumps(record["details"], ensure_ascii=False, indent=4)
            self.details_text.insert(tk.END, details)
        else:
            self.details_text.insert(tk.END, _("no_details"))

        # 禁用详细信息文本框
        self.details_text.config(state=tk.DISABLED)

    def clear_history(self):
        """清空历史记录"""
        if messagebox.askyesno(_("warning"), _("history_clear_confirm")):
            # 清空历史记录
            history_manager.clear_records()
            # 重新加载历史记录
            self.load_history()

    def export_history(self):
        """导出历史记录"""
        try:
            # 获取历史记录
            records = history_manager.get_records()

            if not records:
                messagebox.showinfo(_("info"), _("history_empty"))
                return

            # 生成文件名
            filename = f"history_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"

            # 导出历史记录
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(records, f, ensure_ascii=False, indent=4)

            messagebox.showinfo(_("success"), f"{_('export_success')}: {filename}")
        except Exception as e:
            messagebox.showerror(_("error"), f"{_('export_failed')}: {str(e)}")

    def center_window(self):
        """居中显示窗口"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    # 测试历史记录查看对话框
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    # 添加一些测试数据
    history_manager.add_record("sync", "success", "同步成功", {"orders": 5, "total": 1000})
    history_manager.add_record("error", "failed", "同步失败", {"error": "网络连接错误"})
    history_manager.add_record("config", "warning", "配置已更改", {"old": {"host": "localhost"}, "new": {"host": "127.0.0.1"}})

    # 创建历史记录查看对话框
    dialog = HistoryDialog(root)

    # 等待对话框关闭
    root.wait_window(dialog)

    # 退出
    root.destroy()
