#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
日志配置模块，用于统一管理日志记录
"""

import os
import sys
import logging
from datetime import datetime

# 日志级别映射
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

# 日志配置
LOG_CONFIG = {
    "log_dir": "logs",                      # 日志目录
    "log_file": "sdp_sync_{date}.log",      # 日志文件名模板
    "console_level": "INFO",                # 控制台日志级别
    "file_level": "DEBUG",                  # 文件日志级别
    "max_bytes": 10 * 1024 * 1024,          # 单个日志文件最大大小（10MB）
    "backup_count": 10,                     # 备份文件数量
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # 日志格式
}

def setup_logger(name, log_file=None):
    """
    设置日志记录器
    
    Args:
        name: 日志记录器名称
        log_file: 日志文件路径，如果为None，则使用默认路径
        
    Returns:
        logging.Logger: 日志记录器
    """
    # 确保日志目录存在
    if not os.path.exists(LOG_CONFIG["log_dir"]):
        os.makedirs(LOG_CONFIG["log_dir"])
    
    # 生成日志文件名
    if log_file is None:
        date_str = datetime.now().strftime('%Y%m%d')
        log_file = os.path.join(LOG_CONFIG["log_dir"], 
                               LOG_CONFIG["log_file"].format(date=date_str))
    
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 设置为最低级别，让handler决定哪些消息被记录
    
    # 清除已有的处理器
    if logger.handlers:
        logger.handlers = []
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(LOG_LEVELS.get(LOG_CONFIG["console_level"], logging.INFO))
    console_formatter = logging.Formatter(LOG_CONFIG["format"])
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # 创建文件处理器
    try:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(LOG_LEVELS.get(LOG_CONFIG["file_level"], logging.DEBUG))
        file_formatter = logging.Formatter(LOG_CONFIG["format"])
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.error(f"无法创建日志文件处理器: {e}")
    
    return logger

def get_logger(name="sdp_sync"):
    """
    获取日志记录器
    
    Args:
        name: 日志记录器名称
        
    Returns:
        logging.Logger: 日志记录器
    """
    return setup_logger(name)

# 创建默认日志记录器
logger = get_logger()
