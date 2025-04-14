#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
订单记录管理模块，用于记录已上传的订单信息，防止重复上传
"""

import os
import json
import logging
import datetime
from collections import defaultdict

logger = logging.getLogger("order_record")

# 配置信息
RECORD_CONFIG = {
    "record_dir": "records",                  # 记录文件目录
    "record_file": "uploaded_orders.json",    # 记录文件名
    "backup_dir": "records/backup",           # 备份目录
    "max_backups": 30,                        # 最大备份数量
}

def ensure_record_dir():
    """确保记录目录存在"""
    if not os.path.exists(RECORD_CONFIG["record_dir"]):
        os.makedirs(RECORD_CONFIG["record_dir"])
        logger.info(f"创建记录目录: {RECORD_CONFIG['record_dir']}")
    
    if not os.path.exists(RECORD_CONFIG["backup_dir"]):
        os.makedirs(RECORD_CONFIG["backup_dir"])
        logger.info(f"创建备份目录: {RECORD_CONFIG['backup_dir']}")

def get_record_file_path():
    """获取记录文件路径"""
    return os.path.join(RECORD_CONFIG["record_dir"], RECORD_CONFIG["record_file"])

def load_uploaded_records():
    """
    加载已上传的订单记录
    
    Returns:
        dict: 已上传的订单记录，格式为 {日期: {机构代码: [商品编码列表]}}
    """
    ensure_record_dir()
    record_file = get_record_file_path()
    
    if not os.path.exists(record_file):
        logger.info(f"记录文件不存在，创建新记录: {record_file}")
        return {}
    
    try:
        with open(record_file, 'r', encoding='utf-8') as f:
            records = json.load(f)
        logger.info(f"成功加载记录文件: {record_file}")
        return records
    except Exception as e:
        logger.error(f"加载记录文件失败: {e}")
        return {}

def save_uploaded_records(records):
    """
    保存已上传的订单记录
    
    Args:
        records: 订单记录，格式为 {日期: {机构代码: [商品编码列表]}}
    """
    ensure_record_dir()
    record_file = get_record_file_path()
    
    # 备份当前记录文件
    backup_record_file()
    
    try:
        with open(record_file, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        logger.info(f"成功保存记录文件: {record_file}")
        return True
    except Exception as e:
        logger.error(f"保存记录文件失败: {e}")
        return False

def backup_record_file():
    """备份记录文件"""
    record_file = get_record_file_path()
    if not os.path.exists(record_file):
        return
    
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(RECORD_CONFIG["backup_dir"], f"uploaded_orders_{timestamp}.json")
    
    try:
        import shutil
        shutil.copy2(record_file, backup_file)
        logger.info(f"成功备份记录文件: {backup_file}")
        
        # 清理旧备份
        cleanup_old_backups()
    except Exception as e:
        logger.error(f"备份记录文件失败: {e}")

def cleanup_old_backups():
    """清理旧备份文件"""
    backup_dir = RECORD_CONFIG["backup_dir"]
    max_backups = RECORD_CONFIG["max_backups"]
    
    # 获取所有备份文件
    backup_files = [f for f in os.listdir(backup_dir) if f.startswith('uploaded_orders_') and f.endswith('.json')]
    
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

def is_order_uploaded(date, org_code, product_codes):
    """
    检查订单是否已上传
    
    Args:
        date: 日期，格式为 YYYY-MM-DD
        org_code: 机构代码
        product_codes: 商品编码列表
        
    Returns:
        bool: 是否已上传
    """
    records = load_uploaded_records()
    
    # 检查日期记录是否存在
    if date not in records:
        return False
    
    # 检查机构记录是否存在
    if org_code not in records[date]:
        return False
    
    # 检查商品编码是否全部已上传
    uploaded_products = set(records[date][org_code])
    check_products = set(product_codes)
    
    # 如果所有商品编码都已上传，则认为订单已上传
    return check_products.issubset(uploaded_products)

def mark_order_as_uploaded(date, org_code, product_codes):
    """
    标记订单为已上传
    
    Args:
        date: 日期，格式为 YYYY-MM-DD
        org_code: 机构代码
        product_codes: 商品编码列表
    """
    records = load_uploaded_records()
    
    # 确保日期记录存在
    if date not in records:
        records[date] = {}
    
    # 确保机构记录存在
    if org_code not in records[date]:
        records[date][org_code] = []
    
    # 添加商品编码
    for code in product_codes:
        if code not in records[date][org_code]:
            records[date][org_code].append(code)
    
    # 保存记录
    save_uploaded_records(records)
    
    logger.info(f"已标记订单为已上传: 日期={date}, 机构={org_code}, 商品数量={len(product_codes)}")

def filter_new_products(date, org_code, products):
    """
    过滤出新的商品数据（未上传过的）
    
    Args:
        date: 日期，格式为 YYYY-MM-DD
        org_code: 机构代码
        products: 商品数据列表
        
    Returns:
        list: 新的商品数据列表
    """
    records = load_uploaded_records()
    
    # 如果没有该日期的记录，所有商品都是新的
    if date not in records:
        return products
    
    # 如果没有该机构的记录，所有商品都是新的
    if org_code not in records[date]:
        return products
    
    # 获取已上传的商品编码
    uploaded_products = set(records[date][org_code])
    
    # 过滤出新的商品数据
    new_products = []
    for product in products:
        if 'commodity_code' in product and product['commodity_code'] not in uploaded_products:
            new_products.append(product)
    
    logger.info(f"过滤结果: 总商品数={len(products)}, 新商品数={len(new_products)}")
    return new_products

def cleanup_old_records(days_to_keep=30):
    """
    清理旧记录
    
    Args:
        days_to_keep: 保留的天数
    """
    records = load_uploaded_records()
    
    # 计算截止日期
    cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=days_to_keep)).strftime('%Y-%m-%d')
    
    # 找出需要删除的日期
    dates_to_remove = []
    for date in records:
        if date < cutoff_date:
            dates_to_remove.append(date)
    
    # 删除旧记录
    for date in dates_to_remove:
        del records[date]
        logger.info(f"删除旧记录: {date}")
    
    # 保存记录
    if dates_to_remove:
        save_uploaded_records(records)
        logger.info(f"已清理 {len(dates_to_remove)} 天的旧记录")
