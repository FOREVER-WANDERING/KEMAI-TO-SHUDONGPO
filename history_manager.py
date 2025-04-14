#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
历史记录管理模块，用于管理同步历史记录
"""

import os
import json
import logging
from datetime import datetime

class HistoryManager:
    """历史记录管理类"""
    
    def __init__(self, history_file="history.json"):
        """初始化历史记录管理器"""
        self.history_file = history_file
        self.history = self.load_history()
        
    def load_history(self):
        """加载历史记录"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # 如果历史记录文件不存在，创建空历史记录
                empty_history = {"records": []}
                self.save_history(empty_history)
                return empty_history
        except Exception as e:
            logging.error(f"加载历史记录失败: {e}")
            return {"records": []}
    
    def save_history(self, history=None):
        """保存历史记录"""
        if history is None:
            history = self.history
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            logging.error(f"保存历史记录失败: {e}")
            return False
    
    def add_record(self, record_type, status, message, details=None):
        """添加历史记录"""
        record = {
            "type": record_type,  # 记录类型：sync, config, error
            "status": status,     # 状态：success, failed, warning
            "message": message,   # 消息
            "details": details,   # 详细信息
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 时间戳
        }
        self.history["records"].insert(0, record)  # 在列表开头插入，保持最新记录在前
        
        # 限制历史记录数量，最多保留100条
        if len(self.history["records"]) > 100:
            self.history["records"] = self.history["records"][:100]
        
        return self.save_history()
    
    def get_records(self, record_type=None, status=None, limit=None):
        """获取历史记录"""
        records = self.history["records"]
        
        # 按类型过滤
        if record_type:
            records = [r for r in records if r["type"] == record_type]
        
        # 按状态过滤
        if status:
            records = [r for r in records if r["status"] == status]
        
        # 限制数量
        if limit and limit > 0:
            records = records[:limit]
        
        return records
    
    def clear_records(self):
        """清空历史记录"""
        self.history["records"] = []
        return self.save_history()

# 创建全局历史记录管理器实例
history_manager = HistoryManager()

if __name__ == "__main__":
    # 测试历史记录管理器
    history_manager.add_record("sync", "success", "同步成功", {"orders": 5, "total": 1000})
    history_manager.add_record("error", "failed", "同步失败", {"error": "网络连接错误"})
    print(json.dumps(history_manager.get_records(), ensure_ascii=False, indent=4))
