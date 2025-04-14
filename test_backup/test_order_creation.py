#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试订单创建功能
"""

import sys
import json
import logging
from cashier_to_sdp_order import (
    call_sdp_api, get_site_list, get_delivery_time_list,
    search_customer, search_product, create_order
)
from sdp_field_mapping import SDP_API_PATHS

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_order_creation.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("test_order_creation")

def test_site_list():
    """测试获取站点列表"""
    logger.info("测试获取站点列表...")
    sites = get_site_list()
    if sites:
        logger.info(f"成功获取到 {len(sites)} 个站点")
        for site in sites:
            logger.info(f"站点: {site.get('company_name', site.get('name', ''))} (ID: {site.get('id')})")
        return sites[0]['id']
    else:
        logger.error("获取站点列表失败")
        return None

def test_delivery_time_list():
    """测试获取配送时间段列表"""
    logger.info("测试获取配送时间段列表...")
    delivery_times = get_delivery_time_list()
    if delivery_times:
        logger.info(f"成功获取到 {len(delivery_times)} 个配送时间段")
        for dt in delivery_times:
            logger.info(f"配送时间段: {dt.get('name', '')} (ID: {dt.get('id')})")
        return delivery_times[0]['id']
    else:
        logger.error("获取配送时间段列表失败")
        return None

def test_customer_query(search_value="测试客户"):
    """测试客户查询"""
    logger.info(f"测试客户查询，搜索值: {search_value}...")
    user_id = search_customer(search_value)
    if user_id:
        logger.info(f"成功找到客户，ID: {user_id}")
        return user_id
    else:
        logger.error(f"未找到客户: {search_value}")
        return None

def test_product_query(search_value="测试商品"):
    """测试商品查询"""
    logger.info(f"测试商品查询，搜索值: {search_value}...")
    product = search_product(search_value)
    if product:
        logger.info(f"成功找到商品: {product.get('name', '')} (ID: {product.get('id')})")
        return product
    else:
        logger.error(f"未找到商品: {search_value}")
        return None

def test_order_creation():
    """测试订单创建"""
    logger.info("开始测试订单创建...")
    
    # 1. 获取站点ID
    site_id = test_site_list()
    if not site_id:
        return False
    
    # 2. 获取配送时间段ID
    delivery_time_id = test_delivery_time_list()
    if not delivery_time_id:
        return False
    
    # 3. 获取客户ID
    user_id = test_customer_query()
    if not user_id:
        logger.warning("未找到客户，尝试使用第一个客户...")
        # 尝试获取第一个客户
        api_path = SDP_API_PATHS["customer_list"][0]
        params = {"page": 1, "page_size": 1}
        result = call_sdp_api(api_path, params)
        if result and "list" in result and len(result["list"]) > 0:
            user_id = result["list"][0]["user_id"]
            logger.info(f"使用第一个客户，ID: {user_id}")
        else:
            logger.error("无法获取客户，无法创建订单")
            return False
    
    # 4. 准备测试商品数据
    products_data = []
    
    # 尝试查询商品
    product = test_product_query()
    if product:
        # 使用查询到的商品
        products_data.append({
            'commodity_code': product.get('commodity_code', ''),
            'quantity': 1,
            'amount': 10
        })
    else:
        logger.warning("未找到商品，使用测试商品数据...")
        # 使用测试商品数据
        products_data = [
            {
                'commodity_code': '测试商品001',
                'quantity': 2,
                'amount': 20
            },
            {
                'commodity_code': '测试商品002',
                'quantity': 3,
                'amount': 30
            }
        ]
    
    # 5. 创建订单
    logger.info("开始创建测试订单...")
    result = create_order(user_id, products_data, site_id, delivery_time_id)
    if result:
        order_id = result.get('id', 'N/A')
        logger.info(f"订单创建成功，订单ID: {order_id}")
        return True
    else:
        logger.error("订单创建失败")
        return False

def main():
    """主函数"""
    logger.info("开始测试订单创建功能...")
    
    if test_order_creation():
        logger.info("订单创建测试成功")
    else:
        logger.error("订单创建测试失败")

if __name__ == "__main__":
    main()
