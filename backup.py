#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据备份模块，用于备份订单数据
"""

import os
import json
import shutil
import logging
from datetime import datetime

logger = logging.getLogger("backup")

# 备份配置
BACKUP_CONFIG = {
    "backup_dir": "backups",  # 备份目录
    "max_backups": 30,        # 最大保留备份数量
}

def ensure_backup_dir():
    """确保备份目录存在"""
    if not os.path.exists(BACKUP_CONFIG["backup_dir"]):
        os.makedirs(BACKUP_CONFIG["backup_dir"])
        logger.info(f"创建备份目录: {BACKUP_CONFIG['backup_dir']}")

def backup_data(data, prefix="order_data"):
    """
    备份数据
    
    Args:
        data: 要备份的数据
        prefix: 备份文件名前缀
        
    Returns:
        str: 备份文件路径
    """
    ensure_backup_dir()
    
    # 生成备份文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(BACKUP_CONFIG["backup_dir"], f"{prefix}_{timestamp}.json")
    
    try:
        # 将数据写入备份文件
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"数据备份成功: {backup_file}")
        
        # 清理旧备份
        cleanup_old_backups(prefix)
        
        return backup_file
    except Exception as e:
        logger.error(f"数据备份失败: {e}")
        return None

def backup_log_file(log_file):
    """
    备份日志文件
    
    Args:
        log_file: 日志文件路径
        
    Returns:
        str: 备份文件路径
    """
    if not os.path.exists(log_file):
        logger.warning(f"日志文件不存在: {log_file}")
        return None
    
    ensure_backup_dir()
    
    # 生成备份文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(BACKUP_CONFIG["backup_dir"], f"log_{timestamp}.log")
    
    try:
        # 复制日志文件
        shutil.copy2(log_file, backup_file)
        logger.info(f"日志备份成功: {backup_file}")
        return backup_file
    except Exception as e:
        logger.error(f"日志备份失败: {e}")
        return None

def cleanup_old_backups(prefix):
    """
    清理旧备份文件，只保留最近的N个备份
    
    Args:
        prefix: 备份文件名前缀
    """
    backup_dir = BACKUP_CONFIG["backup_dir"]
    max_backups = BACKUP_CONFIG["max_backups"]
    
    # 获取所有匹配前缀的备份文件
    backup_files = [f for f in os.listdir(backup_dir) if f.startswith(prefix) and f.endswith('.json')]
    
    # 按文件修改时间排序
    backup_files.sort(key=lambda x: os.path.getmtime(os.path.join(backup_dir, x)), reverse=True)
    
    # 删除超出保留数量的旧备份
    if len(backup_files) > max_backups:
        for old_file in backup_files[max_backups:]:
            old_file_path = os.path.join(backup_dir, old_file)
            try:
                os.remove(old_file_path)
                logger.info(f"删除旧备份: {old_file}")
            except Exception as e:
                logger.error(f"删除旧备份失败: {old_file}, 错误: {e}")
