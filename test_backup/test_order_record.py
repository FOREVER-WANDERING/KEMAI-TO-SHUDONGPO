#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试订单记录管理功能
"""

import sys
import logging
from datetime import datetime
from order_record import (
    is_order_uploaded, mark_order_as_uploaded,
    filter_new_products, cleanup_old_records,
    load_uploaded_records, save_uploaded_records
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_order_record.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("test_order_record")

def test_order_record():
    """测试订单记录管理功能"""
    logger.info("开始测试订单记录管理功能...")
    
    # 获取当前日期
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 模拟数据
    org_code = "车销5"
    product_codes = ["6935899800032", "250001", "2059497"]
    
    # 检查是否已上传
    if is_order_uploaded(today, org_code, product_codes):
        logger.info(f"机构 {org_code} 的数据今天已经上传过")
    else:
        logger.info(f"机构 {org_code} 的数据今天尚未上传")
    
    # 标记为已上传
    mark_order_as_uploaded(today, org_code, product_codes)
    logger.info(f"已标记机构 {org_code} 的数据为已上传")
    
    # 再次检查是否已上传
    if is_order_uploaded(today, org_code, product_codes):
        logger.info(f"机构 {org_code} 的数据现在已经标记为已上传")
    else:
        logger.error(f"标记失败，机构 {org_code} 的数据仍未标记为已上传")
    
    # 模拟新的商品数据
    products = [
        {"commodity_code": "6935899800032", "name": "滴眼液", "quantity": 2.0, "amount": 96.0},
        {"commodity_code": "250001", "name": "卤煮猪头肉", "quantity": 15.21, "amount": 121.68},
        {"commodity_code": "2059497", "name": "油麦菜 斤", "quantity": 4.47, "amount": 22.34},
        {"commodity_code": "6976108169908", "name": "蒲公英决明子", "quantity": 10.0, "amount": 230.0},  # 新商品
        {"commodity_code": "6920930354438", "name": "爱好矫姿笔筒1", "quantity": 9.0, "amount": 90.0}   # 新商品
    ]
    
    # 过滤出新的商品数据
    new_products = filter_new_products(today, org_code, products)
    logger.info(f"过滤出 {len(new_products)} 个新商品")
    for product in new_products:
        logger.info(f"  新商品: {product.get('name', '')}, 编码: {product.get('commodity_code', '')}")
    
    # 标记新商品为已上传
    if new_products:
        new_product_codes = [p.get('commodity_code', '') for p in new_products if p.get('commodity_code', '')]
        mark_order_as_uploaded(today, org_code, new_product_codes)
        logger.info(f"已标记 {len(new_product_codes)} 个新商品为已上传")
    
    # 清理旧记录
    cleanup_old_records(30)
    logger.info("已清理30天前的旧记录")
    
    # 显示当前记录
    records = load_uploaded_records()
    logger.info(f"当前记录: {records}")
    
    logger.info("测试完成")
    return True

if __name__ == "__main__":
    test_order_record()
