@echo off
chcp 65001 > nul
echo 正在修复language_resources.py文件...

echo #!/usr/bin/env python > language_resources.py
echo # -*- coding: utf-8 -*- >> language_resources.py
echo. >> language_resources.py
echo """>> language_resources.py
echo 语言资源模块，用于支持多语言>> language_resources.py
echo """>> language_resources.py
echo. >> language_resources.py
echo # 中文资源>> language_resources.py
echo ZH_CN = {>> language_resources.py
echo     # 通用>> language_resources.py
echo     "app_name": "蔬东坡订单同步工具",>> language_resources.py
echo     "ok": "确定",>> language_resources.py
echo     "cancel": "取消",>> language_resources.py
echo     "save": "保存",>> language_resources.py
echo     "close": "关闭",>> language_resources.py
echo     "refresh": "刷新",>> language_resources.py
echo     "loading": "加载中...",>> language_resources.py
echo     "error": "错误",>> language_resources.py
echo     "warning": "警告",>> language_resources.py
echo     "info": "信息",>> language_resources.py
echo     "success": "成功",>> language_resources.py
echo     "failed": "失败",>> language_resources.py
echo     "yes": "是",>> language_resources.py
echo     "no": "否",>> language_resources.py
echo     >> language_resources.py
echo     # 主界面>> language_resources.py
echo     "main_title": "蔬东坡订单同步工具",>> language_resources.py
echo     "force_sync": "强制同步（忽略重复检查）",>> language_resources.py
echo     "start_sync": "开始同步",>> language_resources.py
echo     "view_logs": "查看日志",>> language_resources.py
echo     "view_history": "查看历史",>> language_resources.py
echo     "settings": "设置",>> language_resources.py
echo     "exit": "退出",>> language_resources.py
echo     "ready": "就绪",>> language_resources.py
echo     "syncing": "正在同步...",>> language_resources.py
echo     "sync_success": "同步成功完成",>> language_resources.py
echo     "sync_failed": "同步失败",>> language_resources.py
echo     "sync_error": "同步出错",>> language_resources.py
echo     "output": "输出",>> language_resources.py
echo     "welcome": "欢迎使用蔬东坡订单同步工具",>> language_resources.py
echo     "click_start": "点击\"开始同步\"按钮开始同步订单数据",>> language_resources.py
echo     "force_tip": "如果需要强制同步（忽略重复检查），请勾选\"强制同步\"选项",>> language_resources.py
echo     >> language_resources.py
echo     # 同步相关>> language_resources.py
echo     "sync_complete": "同步完成",>> language_resources.py
echo     "sync_success_msg": "订单数据同步成功！",>> language_resources.py
echo     "sync_failed_msg": "订单数据同步失败，请查看日志了解详情。",>> language_resources.py
echo     "sync_error_msg": "同步过程中发生错误：",>> language_resources.py
echo     >> language_resources.py
echo     # 日志查看>> language_resources.py
echo     "log_viewer": "日志查看器",>> language_resources.py
echo     "log_file": "日志文件",>> language_resources.py
echo     "log_level": "日志级别",>> language_resources.py
echo     "log_time": "时间",>> language_resources.py
echo     "log_message": "消息",>> language_resources.py
echo     "log_error": "无法启动日志查看工具",>> language_resources.py
echo     >> language_resources.py
echo     # 历史记录>> language_resources.py
echo     "history_viewer": "历史记录查看器",>> language_resources.py
echo     "history_type": "类型",>> language_resources.py
echo     "history_status": "状态",>> language_resources.py
echo     "history_time": "时间",>> language_resources.py
echo     "history_message": "消息",>> language_resources.py
echo     "history_details": "详细信息",>> language_resources.py
echo     "history_empty": "暂无历史记录",>> language_resources.py
echo     "history_clear": "清空历史",>> language_resources.py
echo     "history_clear_confirm": "确定要清空所有历史记录吗？",>> language_resources.py
echo     "history_export": "导出历史",>> language_resources.py
echo     "history_type_sync": "同步",>> language_resources.py
echo     "history_type_config": "配置",>> language_resources.py
echo     "history_type_error": "错误",>> language_resources.py
echo     "history_status_success": "成功",>> language_resources.py
echo     "history_status_failed": "失败",>> language_resources.py
echo     "history_status_warning": "警告",>> language_resources.py
echo     >> language_resources.py
echo     # 设置>> language_resources.py
echo     "settings_title": "设置",>> language_resources.py
echo     "settings_general": "常规",>> language_resources.py
echo     "settings_database": "数据库",>> language_resources.py
echo     "settings_api": "API",>> language_resources.py
echo     "settings_ui": "界面",>> language_resources.py
echo     "settings_log": "日志",>> language_resources.py
echo     "settings_sync": "同步",>> language_resources.py
echo     "settings_save_success": "设置保存成功",>> language_resources.py
echo     "settings_save_failed": "设置保存失败",>> language_resources.py
echo     "settings_reset": "重置设置",>> language_resources.py
echo     "settings_reset_confirm": "确定要重置所有设置吗？",>> language_resources.py
echo     >> language_resources.py
echo     # 数据库设置>> language_resources.py
echo     "db_host": "主机",>> language_resources.py
echo     "db_port": "端口",>> language_resources.py
echo     "db_user": "用户名",>> language_resources.py
echo     "db_password": "密码",>> language_resources.py
echo     "db_database": "数据库",>> language_resources.py
echo     "db_test": "测试连接",>> language_resources.py
echo     "db_test_success": "数据库连接成功",>> language_resources.py
echo     "db_test_failed": "数据库连接失败",>> language_resources.py
echo     >> language_resources.py
echo     # API设置>> language_resources.py
echo     "api_base_url": "基础URL",>> language_resources.py
echo     "api_appid": "应用ID",>> language_resources.py
echo     "api_secret": "密钥",>> language_resources.py
echo     "api_test": "测试API",>> language_resources.py
echo     "api_test_success": "API连接成功",>> language_resources.py
echo     "api_test_failed": "API连接失败",>> language_resources.py
echo     >> language_resources.py
echo     # 界面设置>> language_resources.py
echo     "ui_theme": "主题",>> language_resources.py
echo     "ui_theme_default": "默认",>> language_resources.py
echo     "ui_theme_light": "浅色",>> language_resources.py
echo     "ui_theme_dark": "深色",>> language_resources.py
echo     "ui_font_size": "字体大小",>> language_resources.py
echo     "ui_language": "语言",>> language_resources.py
echo     "ui_language_zh_CN": "中文",>> language_resources.py
echo     "ui_language_en_US": "英文",>> language_resources.py
echo     >> language_resources.py
echo     # 日志设置>> language_resources.py
echo     "log_level_setting": "日志级别",>> language_resources.py
echo     "log_level_debug": "调试",>> language_resources.py
echo     "log_level_info": "信息",>> language_resources.py
echo     "log_level_warning": "警告",>> language_resources.py
echo     "log_level_error": "错误",>> language_resources.py
echo     "log_level_critical": "严重",>> language_resources.py
echo     "log_max_files": "最大日志文件数",>> language_resources.py
echo     "log_max_size": "单个日志文件最大大小(MB)",>> language_resources.py
echo     >> language_resources.py
echo     # 同步设置>> language_resources.py
echo     "sync_auto": "自动同步",>> language_resources.py
echo     "sync_time": "同步时间",>> language_resources.py
echo     "sync_default_site": "默认站点ID",>> language_resources.py
echo     "sync_default_delivery": "默认配送时间段ID",>> language_resources.py
echo     "sync_default_pay": "默认支付方式",>> language_resources.py
echo     "sync_pay_cod": "货到付款",>> language_resources.py
echo     "sync_pay_online": "在线支付",>> language_resources.py
echo     >> language_resources.py
echo     # 版权信息>> language_resources.py
echo     "copyright": "© 2025 蔬东坡订单同步工具">> language_resources.py
echo }>> language_resources.py
echo. >> language_resources.py
echo # 英文资源>> language_resources.py
echo EN_US = {>> language_resources.py
echo     # 通用>> language_resources.py
echo     "app_name": "SDP Order Sync Tool",>> language_resources.py
echo     "ok": "OK",>> language_resources.py
echo     "cancel": "Cancel",>> language_resources.py
echo     "save": "Save",>> language_resources.py
echo     "close": "Close",>> language_resources.py
echo     "refresh": "Refresh",>> language_resources.py
echo     "loading": "Loading...",>> language_resources.py
echo     "error": "Error",>> language_resources.py
echo     "warning": "Warning",>> language_resources.py
echo     "info": "Information",>> language_resources.py
echo     "success": "Success",>> language_resources.py
echo     "failed": "Failed",>> language_resources.py
echo     "yes": "Yes",>> language_resources.py
echo     "no": "No",>> language_resources.py
echo     >> language_resources.py
echo     # 主界面>> language_resources.py
echo     "main_title": "SDP Order Sync Tool",>> language_resources.py
echo     "force_sync": "Force Sync (Ignore Duplicate Check)",>> language_resources.py
echo     "start_sync": "Start Sync",>> language_resources.py
echo     "view_logs": "View Logs",>> language_resources.py
echo     "view_history": "View History",>> language_resources.py
echo     "settings": "Settings",>> language_resources.py
echo     "exit": "Exit",>> language_resources.py
echo     "ready": "Ready",>> language_resources.py
echo     "syncing": "Syncing...",>> language_resources.py
echo     "sync_success": "Sync completed successfully",>> language_resources.py
echo     "sync_failed": "Sync failed",>> language_resources.py
echo     "sync_error": "Sync error",>> language_resources.py
echo     "output": "Output",>> language_resources.py
echo     "welcome": "Welcome to SDP Order Sync Tool",>> language_resources.py
echo     "click_start": "Click 'Start Sync' button to start syncing order data",>> language_resources.py
echo     "force_tip": "If you need to force sync (ignore duplicate check), please check the 'Force Sync' option",>> language_resources.py
echo     >> language_resources.py
echo     # 同步相关>> language_resources.py
echo     "sync_complete": "Sync Complete",>> language_resources.py
echo     "sync_success_msg": "Order data synced successfully!",>> language_resources.py
echo     "sync_failed_msg": "Order data sync failed. Please check the logs for details.",>> language_resources.py
echo     "sync_error_msg": "An error occurred during sync:",>> language_resources.py
echo     >> language_resources.py
echo     # 日志查看>> language_resources.py
echo     "log_viewer": "Log Viewer",>> language_resources.py
echo     "log_file": "Log File",>> language_resources.py
echo     "log_level": "Log Level",>> language_resources.py
echo     "log_time": "Time",>> language_resources.py
echo     "log_message": "Message",>> language_resources.py
echo     "log_error": "Cannot start log viewer",>> language_resources.py
echo     >> language_resources.py
echo     # 历史记录>> language_resources.py
echo     "history_viewer": "History Viewer",>> language_resources.py
echo     "history_type": "Type",>> language_resources.py
echo     "history_status": "Status",>> language_resources.py
echo     "history_time": "Time",>> language_resources.py
echo     "history_message": "Message",>> language_resources.py
echo     "history_details": "Details",>> language_resources.py
echo     "history_empty": "No history records",>> language_resources.py
echo     "history_clear": "Clear History",>> language_resources.py
echo     "history_clear_confirm": "Are you sure you want to clear all history records?",>> language_resources.py
echo     "history_export": "Export History",>> language_resources.py
echo     "history_type_sync": "Sync",>> language_resources.py
echo     "history_type_config": "Config",>> language_resources.py
echo     "history_type_error": "Error",>> language_resources.py
echo     "history_status_success": "Success",>> language_resources.py
echo     "history_status_failed": "Failed",>> language_resources.py
echo     "history_status_warning": "Warning",>> language_resources.py
echo     >> language_resources.py
echo     # 设置>> language_resources.py
echo     "settings_title": "Settings",>> language_resources.py
echo     "settings_general": "General",>> language_resources.py
echo     "settings_database": "Database",>> language_resources.py
echo     "settings_api": "API",>> language_resources.py
echo     "settings_ui": "UI",>> language_resources.py
echo     "settings_log": "Log",>> language_resources.py
echo     "settings_sync": "Sync",>> language_resources.py
echo     "settings_save_success": "Settings saved successfully",>> language_resources.py
echo     "settings_save_failed": "Failed to save settings",>> language_resources.py
echo     "settings_reset": "Reset Settings",>> language_resources.py
echo     "settings_reset_confirm": "Are you sure you want to reset all settings?",>> language_resources.py
echo     >> language_resources.py
echo     # 数据库设置>> language_resources.py
echo     "db_host": "Host",>> language_resources.py
echo     "db_port": "Port",>> language_resources.py
echo     "db_user": "Username",>> language_resources.py
echo     "db_password": "Password",>> language_resources.py
echo     "db_database": "Database",>> language_resources.py
echo     "db_test": "Test Connection",>> language_resources.py
echo     "db_test_success": "Database connection successful",>> language_resources.py
echo     "db_test_failed": "Database connection failed",>> language_resources.py
echo     >> language_resources.py
echo     # API设置>> language_resources.py
echo     "api_base_url": "Base URL",>> language_resources.py
echo     "api_appid": "App ID",>> language_resources.py
echo     "api_secret": "Secret",>> language_resources.py
echo     "api_test": "Test API",>> language_resources.py
echo     "api_test_success": "API connection successful",>> language_resources.py
echo     "api_test_failed": "API connection failed",>> language_resources.py
echo     >> language_resources.py
echo     # 界面设置>> language_resources.py
echo     "ui_theme": "Theme",>> language_resources.py
echo     "ui_theme_default": "Default",>> language_resources.py
echo     "ui_theme_light": "Light",>> language_resources.py
echo     "ui_theme_dark": "Dark",>> language_resources.py
echo     "ui_font_size": "Font Size",>> language_resources.py
echo     "ui_language": "Language",>> language_resources.py
echo     "ui_language_zh_CN": "Chinese",>> language_resources.py
echo     "ui_language_en_US": "English",>> language_resources.py
echo     >> language_resources.py
echo     # 日志设置>> language_resources.py
echo     "log_level_setting": "Log Level",>> language_resources.py
echo     "log_level_debug": "Debug",>> language_resources.py
echo     "log_level_info": "Info",>> language_resources.py
echo     "log_level_warning": "Warning",>> language_resources.py
echo     "log_level_error": "Error",>> language_resources.py
echo     "log_level_critical": "Critical",>> language_resources.py
echo     "log_max_files": "Max Log Files",>> language_resources.py
echo     "log_max_size": "Max Log File Size (MB)",>> language_resources.py
echo     >> language_resources.py
echo     # 同步设置>> language_resources.py
echo     "sync_auto": "Auto Sync",>> language_resources.py
echo     "sync_time": "Sync Time",>> language_resources.py
echo     "sync_default_site": "Default Site ID",>> language_resources.py
echo     "sync_default_delivery": "Default Delivery Time ID",>> language_resources.py
echo     "sync_default_pay": "Default Payment Method",>> language_resources.py
echo     "sync_pay_cod": "Cash on Delivery",>> language_resources.py
echo     "sync_pay_online": "Online Payment",>> language_resources.py
echo     >> language_resources.py
echo     # 版权信息>> language_resources.py
echo     "copyright": "© 2025 SDP Order Sync Tool">> language_resources.py
echo }>> language_resources.py
echo. >> language_resources.py
echo # 语言资源字典>> language_resources.py
echo RESOURCES = {>> language_resources.py
echo     "zh_CN": ZH_CN,>> language_resources.py
echo     "en_US": EN_US>> language_resources.py
echo }>> language_resources.py
echo. >> language_resources.py
echo class LanguageManager:>> language_resources.py
echo     """语言管理类""">> language_resources.py
echo     >> language_resources.py
echo     def __init__(self, language="zh_CN"):>> language_resources.py
echo         """初始化语言管理器""">> language_resources.py
echo         self.language = language>> language_resources.py
echo         self.resources = RESOURCES.get(language, ZH_CN)>> language_resources.py
echo     >> language_resources.py
echo     def set_language(self, language):>> language_resources.py
echo         """设置语言""">> language_resources.py
echo         if language in RESOURCES:>> language_resources.py
echo             self.language = language>> language_resources.py
echo             self.resources = RESOURCES.get(language, ZH_CN)>> language_resources.py
echo             return True>> language_resources.py
echo         return False>> language_resources.py
echo     >> language_resources.py
echo     def get_text(self, key, default=None):>> language_resources.py
echo         """获取文本""">> language_resources.py
echo         return self.resources.get(key, default if default is not None else key)>> language_resources.py
echo     >> language_resources.py
echo     def get_all_texts(self):>> language_resources.py
echo         """获取所有文本""">> language_resources.py
echo         return self.resources>> language_resources.py
echo. >> language_resources.py
echo # 创建全局语言管理器实例>> language_resources.py
echo language_manager = LanguageManager()>> language_resources.py
echo. >> language_resources.py
echo def _(key, default=None):>> language_resources.py
echo     """获取文本的快捷方式""">> language_resources.py
echo     return language_manager.get_text(key, default)>> language_resources.py
echo. >> language_resources.py
echo if __name__ == "__main__":>> language_resources.py
echo     # 测试语言管理器>> language_resources.py
echo     print(_("app_name"))>> language_resources.py
echo     language_manager.set_language("en_US")>> language_resources.py
echo     print(_("app_name"))>> language_resources.py

echo 同样修复dist目录中的文件...
copy language_resources.py dist\SDP_Order_Sync_Tool\ /Y

echo 修复完成！
pause
