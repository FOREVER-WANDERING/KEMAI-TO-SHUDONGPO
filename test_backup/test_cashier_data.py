#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试从收银系统获取数据并同步到蔬东坡系统
"""

import sys
import json
import logging
from cashier_to_sdp_order import get_today_cashier_data, sync_data_to_sdp

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_cashier_data.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("test_cashier_data")

def test_get_cashier_data():
    """测试从收银系统获取数据"""
    logger.info("开始测试从收银系统获取数据...")
    
    # 调用函数获取数据
    cashier_data = get_today_cashier_data()
    
    if not cashier_data:
        logger.error("未获取到收银系统数据")
        return False
    
    # 输出获取到的数据概况
    logger.info(f"获取到 {len(cashier_data)} 个机构的数据")
    
    # 输出每个机构的商品数量
    for org_code, products in cashier_data.items():
        logger.info(f"机构 {org_code} 有 {len(products)} 个商品")
        
        # 输出前3个商品的详细信息作为示例
        for i, product in enumerate(products[:3]):
            logger.info(f"  商品 {i+1}: {json.dumps(product, ensure_ascii=False)}")
    
    return True

def test_sync_to_sdp():
    """测试同步数据到蔬东坡系统"""
    logger.info("开始测试同步数据到蔬东坡系统...")
    
    # 调用同步函数
    result = sync_data_to_sdp()
    
    if result:
        logger.info("数据同步成功")
    else:
        logger.error("数据同步失败")
    
    return result

def main():
    """主函数"""
    logger.info("开始测试从收银系统获取数据并同步到蔬东坡系统...")
    
    # 测试获取收银数据
    if not test_get_cashier_data():
        logger.error("获取收银数据测试失败，终止后续测试")
        return
    
    # 测试同步到蔬东坡系统
    test_sync_to_sdp()

if __name__ == "__main__":
    main()
