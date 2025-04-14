#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
同步收银系统数据到蔬东坡订单系统的主脚本
支持定时执行和日志记录

命令行参数:
    --force: 强制同步，忽略重复检查
    --help: 显示帮助信息
"""

import os
import sys
import time
import logging
import traceback
import argparse
from datetime import datetime

# 导入自定义模块
from cashier_to_sdp_order import sync_data_to_sdp
from logger_config import setup_logger

# 脚本配置
SCRIPT_CONFIG = {
    "log_dir": "logs",                 # 日志目录
    "log_file": "sdp_sync_{date}.log", # 日志文件名模板
    "force_sync": False,               # 是否强制同步（忽略重复检查）
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

    # 使用新的日志模块设置日志
    setup_logger("sync_sdp_order", log_file)
    setup_logger("cashier_to_sdp", log_file)
    setup_logger("order_record", log_file)

    # 记录脚本启动信息
    logger = logging.getLogger("sync_sdp_order")
    logger.info("=" * 80)
    logger.info("订单同步脚本启动")
    logger.info(f"日志文件: {log_file}")

    return log_file

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='同步收银系统数据到蔬东坡订单系统')
    parser.add_argument('--force', action='store_true', help='强制同步，忽略重复检查')

    args = parser.parse_args()

    # 更新配置
    if args.force:
        SCRIPT_CONFIG["force_sync"] = True

    return args

def main():
    """主函数"""
    # 解析命令行参数
    parse_arguments()

    # 设置日志记录
    log_file = setup_logging()
    logger = logging.getLogger("sync_sdp_order")

    logger.info("=" * 80)
    logger.info("开始同步收银系统数据到蔬东坡订单系统...")

    if SCRIPT_CONFIG["force_sync"]:
        logger.info("强制同步模式：将忽略重复检查")

    try:
        # 记录开始时间
        start_time = time.time()

        # 同步数据
        success = sync_data_to_sdp(force_sync=SCRIPT_CONFIG["force_sync"])

        # 记录结束时间
        end_time = time.time()
        elapsed_time = end_time - start_time

        if success:
            logger.info(f"同步成功完成，耗时 {elapsed_time:.2f} 秒")
            return 0
        else:
            logger.error("同步失败")
            return 1

    except Exception as e:
        # 记录异常信息
        error_msg = f"同步过程中发生异常: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        return 1

    finally:
        logger.info("=" * 80)

if __name__ == "__main__":
    sys.exit(main())
