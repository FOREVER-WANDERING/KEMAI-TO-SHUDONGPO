#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
同步收银系统数据到蔬东坡订单系统的主脚本
支持定时执行、日志记录、错误通知和数据备份
"""

import os
import sys
import time
import logging
import traceback
from datetime import datetime

# 导入自定义模块
from cashier_to_sdp_order import sync_data_to_sdp
from notification import send_success_notification, send_error_notification
from backup import backup_data, backup_log_file

# 脚本配置
SCRIPT_CONFIG = {
    "log_dir": "logs",                 # 日志目录
    "log_file": "sdp_sync_{date}.log", # 日志文件名模板
    "enable_email": True,              # 是否启用邮件通知
    "enable_backup": True,             # 是否启用数据备份
}

def setup_logging():
    """
    设置日志记录
    
    Returns:
        str: 日志文件路径
    """
    # 确保日志目录存在
    if not os.path.exists(SCRIPT_CONFIG["log_dir"]):
        os.makedirs(SCRIPT_CONFIG["log_dir"])
    
    # 生成日志文件名
    date_str = datetime.now().strftime('%Y%m%d')
    log_file = os.path.join(SCRIPT_CONFIG["log_dir"], 
                           SCRIPT_CONFIG["log_file"].format(date=date_str))
    
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return log_file

def main():
    """主函数"""
    # 设置日志记录
    log_file = setup_logging()
    logger = logging.getLogger("sync_sdp_order")
    
    logger.info("=" * 80)
    logger.info("开始同步收银系统数据到蔬东坡订单系统...")
    
    try:
        # 记录开始时间
        start_time = time.time()
        
        # 同步数据
        success = sync_data_to_sdp()
        
        # 记录结束时间
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        if success:
            logger.info(f"同步成功完成，耗时 {elapsed_time:.2f} 秒")
            
            # 发送成功通知
            if SCRIPT_CONFIG["enable_email"]:
                send_success_notification(1, log_file)
            
            # 备份日志
            if SCRIPT_CONFIG["enable_backup"]:
                backup_log_file(log_file)
            
            return 0
        else:
            logger.error("同步失败")
            
            # 发送错误通知
            if SCRIPT_CONFIG["enable_email"]:
                send_error_notification("同步失败，未创建任何订单", log_file)
            
            # 备份日志
            if SCRIPT_CONFIG["enable_backup"]:
                backup_log_file(log_file)
            
            return 1
    
    except Exception as e:
        # 记录异常信息
        error_msg = f"同步过程中发生异常: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        
        # 发送错误通知
        if SCRIPT_CONFIG["enable_email"]:
            send_error_notification(error_msg, log_file)
        
        # 备份日志
        if SCRIPT_CONFIG["enable_backup"]:
            backup_log_file(log_file)
        
        return 1
    
    finally:
        logger.info("=" * 80)

if __name__ == "__main__":
    sys.exit(main())
