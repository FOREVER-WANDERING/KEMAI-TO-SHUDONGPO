#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
语言资源模块，用于支持多语言
"""

# 中文资源
ZH_CN = {
    # 通用
    "app_name": "蔬东坡订单同步工具",
    "ok": "确定",
    "cancel": "取消",
    "save": "保存",
    "close": "关闭",
    "refresh": "刷新",
    "loading": "加载中...",
    "error": "错误",
    "warning": "警告",
    "info": "信息",
    "success": "成功",
    "failed": "失败",
    "yes": "是",
    "no": "否",
    
    # 主界面
    "main_title": "蔬东坡订单同步工具",
    "force_sync": "强制同步（忽略重复检查）",
    "start_sync": "开始同步",
    "view_logs": "查看日志",
    "view_history": "查看历史",
    "settings": "设置",
    "exit": "退出",
    "ready": "就绪",
    "syncing": "正在同步...",
    "sync_success": "同步成功完成",
    "sync_failed": "同步失败",
    "sync_error": "同步出错",
    "output": "输出",
    "welcome": "欢迎使用蔬东坡订单同步工具",
    "click_start": "点击\"开始同步\"按钮开始同步订单数据",
    "force_tip": "如果需要强制同步（忽略重复检查），请勾选\"强制同步\"选项",
    
    # 同步相关
    "sync_complete": "同步完成",
    "sync_success_msg": "订单数据同步成功！",
    "sync_failed_msg": "订单数据同步失败，请查看日志了解详情。",
    "sync_error_msg": "同步过程中发生错误：",
    
    # 日志查看
    "log_viewer": "日志查看器",
    "log_file": "日志文件",
    "log_level": "日志级别",
    "log_time": "时间",
    "log_message": "消息",
    "log_error": "无法启动日志查看工具",
    
    # 历史记录
    "history_viewer": "历史记录查看器",
    "history_type": "类型",
    "history_status": "状态",
    "history_time": "时间",
    "history_message": "消息",
    "history_details": "详细信息",
    "history_empty": "暂无历史记录",
    "history_clear": "清空历史",
    "history_clear_confirm": "确定要清空所有历史记录吗？",
    "history_export": "导出历史",
    "history_type_sync": "同步",
    "history_type_config": "配置",
    "history_type_error": "错误",
    "history_status_success": "成功",
    "history_status_failed": "失败",
    "history_status_warning": "警告",
    
    # 设置
    "settings_title": "设置",
    "settings_general": "常规",
    "settings_database": "数据库",
    "settings_api": "API",
    "settings_ui": "界面",
    "settings_log": "日志",
    "settings_sync": "同步",
    "settings_save_success": "设置保存成功",
    "settings_save_failed": "设置保存失败",
    "settings_reset": "重置设置",
    "settings_reset_confirm": "确定要重置所有设置吗？",
    
    # 数据库设置
    "db_host": "主机",
    "db_port": "端口",
    "db_user": "用户名",
    "db_password": "密码",
    "db_database": "数据库",
    "db_test": "测试连接",
    "db_test_success": "数据库连接成功",
    "db_test_failed": "数据库连接失败",
    
    # API设置
    "api_base_url": "基础URL",
    "api_appid": "应用ID",
    "api_secret": "密钥",
    "api_test": "测试API",
    "api_test_success": "API连接成功",
    "api_test_failed": "API连接失败",
    
    # 界面设置
    "ui_theme": "主题",
    "ui_theme_default": "默认",
    "ui_theme_light": "浅色",
    "ui_theme_dark": "深色",
    "ui_font_size": "字体大小",
    "ui_language": "语言",
    "ui_language_zh_CN": "中文",
    "ui_language_en_US": "英文",
    
    # 日志设置
    "log_level_setting": "日志级别",
    "log_level_debug": "调试",
    "log_level_info": "信息",
    "log_level_warning": "警告",
    "log_level_error": "错误",
    "log_level_critical": "严重",
    "log_max_files": "最大日志文件数",
    "log_max_size": "单个日志文件最大大小(MB)",
    
    # 同步设置
    "sync_auto": "自动同步",
    "sync_time": "同步时间",
    "sync_default_site": "默认站点ID",
    "sync_default_delivery": "默认配送时间段ID",
    "sync_default_pay": "默认支付方式",
    "sync_pay_cod": "货到付款",
    "sync_pay_online": "在线支付",
    
    # 版权信息
    "copyright": "© 2025 蔬东坡订单同步工具"
}

# 英文资源
EN_US = {
    # 通用
    "app_name": "SDP Order Sync Tool",
    "ok": "OK",
    "cancel": "Cancel",
    "save": "Save",
    "close": "Close",
    "refresh": "Refresh",
    "loading": "Loading...",
    "error": "Error",
    "warning": "Warning",
    "info": "Information",
    "success": "Success",
    "failed": "Failed",
    "yes": "Yes",
    "no": "No",
    
    # 主界面
    "main_title": "SDP Order Sync Tool",
    "force_sync": "Force Sync (Ignore Duplicate Check)",
    "start_sync": "Start Sync",
    "view_logs": "View Logs",
    "view_history": "View History",
    "settings": "Settings",
    "exit": "Exit",
    "ready": "Ready",
    "syncing": "Syncing...",
    "sync_success": "Sync completed successfully",
    "sync_failed": "Sync failed",
    "sync_error": "Sync error",
    "output": "Output",
    "welcome": "Welcome to SDP Order Sync Tool",
    "click_start": "Click 'Start Sync' button to start syncing order data",
    "force_tip": "If you need to force sync (ignore duplicate check), please check the 'Force Sync' option",
    
    # 同步相关
    "sync_complete": "Sync Complete",
    "sync_success_msg": "Order data synced successfully!",
    "sync_failed_msg": "Order data sync failed. Please check the logs for details.",
    "sync_error_msg": "An error occurred during sync:",
    
    # 日志查看
    "log_viewer": "Log Viewer",
    "log_file": "Log File",
    "log_level": "Log Level",
    "log_time": "Time",
    "log_message": "Message",
    "log_error": "Cannot start log viewer",
    
    # 历史记录
    "history_viewer": "History Viewer",
    "history_type": "Type",
    "history_status": "Status",
    "history_time": "Time",
    "history_message": "Message",
    "history_details": "Details",
    "history_empty": "No history records",
    "history_clear": "Clear History",
    "history_clear_confirm": "Are you sure you want to clear all history records?",
    "history_export": "Export History",
    "history_type_sync": "Sync",
    "history_type_config": "Config",
    "history_type_error": "Error",
    "history_status_success": "Success",
    "history_status_failed": "Failed",
    "history_status_warning": "Warning",
    
    # 设置
    "settings_title": "Settings",
    "settings_general": "General",
    "settings_database": "Database",
    "settings_api": "API",
    "settings_ui": "UI",
    "settings_log": "Log",
    "settings_sync": "Sync",
    "settings_save_success": "Settings saved successfully",
    "settings_save_failed": "Failed to save settings",
    "settings_reset": "Reset Settings",
    "settings_reset_confirm": "Are you sure you want to reset all settings?",
    
    # 数据库设置
    "db_host": "Host",
    "db_port": "Port",
    "db_user": "Username",
    "db_password": "Password",
    "db_database": "Database",
    "db_test": "Test Connection",
    "db_test_success": "Database connection successful",
    "db_test_failed": "Database connection failed",
    
    # API设置
    "api_base_url": "Base URL",
    "api_appid": "App ID",
    "api_secret": "Secret",
    "api_test": "Test API",
    "api_test_success": "API connection successful",
    "api_test_failed": "API connection failed",
    
    # 界面设置
    "ui_theme": "Theme",
    "ui_theme_default": "Default",
    "ui_theme_light": "Light",
    "ui_theme_dark": "Dark",
    "ui_font_size": "Font Size",
    "ui_language": "Language",
    "ui_language_zh_CN": "Chinese",
    "ui_language_en_US": "English",
    
    # 日志设置
    "log_level_setting": "Log Level",
    "log_level_debug": "Debug",
    "log_level_info": "Info",
    "log_level_warning": "Warning",
    "log_level_error": "Error",
    "log_level_critical": "Critical",
    "log_max_files": "Max Log Files",
    "log_max_size": "Max Log File Size (MB)",
    
    # 同步设置
    "sync_auto": "Auto Sync",
    "sync_time": "Sync Time",
    "sync_default_site": "Default Site ID",
    "sync_default_delivery": "Default Delivery Time ID",
    "sync_default_pay": "Default Payment Method",
    "sync_pay_cod": "Cash on Delivery",
    "sync_pay_online": "Online Payment",
    
    # 版权信息
    "copyright": "© 2025 SDP Order Sync Tool"
}

# 语言资源字典
RESOURCES = {
    "zh_CN": ZH_CN,
    "en_US": EN_US
}

class LanguageManager:
    """语言管理类"""
    
    def __init__(self, language="zh_CN"):
        """初始化语言管理器"""
        self.language = language
        self.resources = RESOURCES.get(language, ZH_CN)
    
    def set_language(self, language):
        """设置语言"""
        if language in RESOURCES:
            self.language = language
            self.resources = RESOURCES.get(language, ZH_CN)
            return True
        return False
    
    def get_text(self, key, default=None):
        """获取文本"""
        return self.resources.get(key, default if default is not None else key)
    
    def get_all_texts(self):
        """获取所有文本"""
        return self.resources

# 创建全局语言管理器实例
language_manager = LanguageManager()

def _(key, default=None):
    """获取文本的快捷方式"""
    return language_manager.get_text(key, default)

if __name__ == "__main__":
    # 测试语言管理器
    print(_("app_name"))
    language_manager.set_language("en_US")
    print(_("app_name"))
