#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
配置管理模块，用于管理应用程序的配置
"""

import os
import json
import logging

# 默认配置
DEFAULT_CONFIG = {
    # 数据库配置
    "db": {
        "host": "127.0.0.1",
        "port": "1314",
        "user": "sa",
        "password": "Sotopos123",
        "database": "zhj"
    },
    # 蔬东坡API配置
    "sdp_api": {
        "base_url": "https://scm.sdongpo.com/cc_thirdparty",
        "appid": "3647a33b94f745ed",
        "secret": "7d3c21acab1539c03f9fb62a4754343f"
    },
    # 默认站点ID和发货时间段ID
    "default_site_id": "6",
    "default_delivery_time": "",  # 将通过API获取
    # 默认支付方式：0货到付款
    "default_pay_way": 0,
    # 界面配置
    "ui": {
        "theme": "default",  # 主题：default, light, dark
        "font_size": 10,     # 字体大小
        "language": "zh_CN"  # 语言：zh_CN, en_US
    },
    # 日志配置
    "log": {
        "level": "INFO",     # 日志级别：DEBUG, INFO, WARNING, ERROR, CRITICAL
        "max_files": 10,     # 最大日志文件数
        "max_size": 10       # 单个日志文件最大大小（MB）
    },
    # 同步配置
    "sync": {
        "auto_sync": False,  # 是否自动同步
        "sync_time": "23:00" # 自动同步时间
    }
}

class ConfigManager:
    """配置管理类"""
    
    def __init__(self, config_file="config.json"):
        """初始化配置管理器"""
        self.config_file = config_file
        self.config = self.load_config()
        
    def load_config(self):
        """加载配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # 合并默认配置和加载的配置
                merged_config = DEFAULT_CONFIG.copy()
                self._deep_update(merged_config, config)
                return merged_config
            else:
                # 如果配置文件不存在，创建默认配置
                self.save_config(DEFAULT_CONFIG)
                return DEFAULT_CONFIG
        except Exception as e:
            logging.error(f"加载配置失败: {e}")
            return DEFAULT_CONFIG
    
    def save_config(self, config=None):
        """保存配置"""
        if config is None:
            config = self.config
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            logging.error(f"保存配置失败: {e}")
            return False
    
    def get_config(self, section=None, key=None):
        """获取配置"""
        if section is None:
            return self.config
        if key is None:
            return self.config.get(section, {})
        return self.config.get(section, {}).get(key)
    
    def set_config(self, section, key, value):
        """设置配置"""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
        return self.save_config()
    
    def _deep_update(self, d, u):
        """深度更新字典"""
        for k, v in u.items():
            if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                self._deep_update(d[k], v)
            else:
                d[k] = v

# 创建全局配置管理器实例
config_manager = ConfigManager()

if __name__ == "__main__":
    # 测试配置管理器
    print(json.dumps(config_manager.get_config(), ensure_ascii=False, indent=4))
