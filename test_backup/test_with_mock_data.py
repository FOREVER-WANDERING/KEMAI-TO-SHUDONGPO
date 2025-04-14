#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
使用模拟数据测试蔬东坡订单同步功能
"""

import sys
import json
import logging
import random
from datetime import datetime
from cashier_to_sdp_order import (
    call_sdp_api, get_site_list, get_delivery_time_list,
    search_customer, create_order
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_mock_data.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("test_mock_data")

# 模拟商品数据
MOCK_PRODUCTS = [
    {"commodity_code": "6935899800032", "name": "滴眼液", "quantity": 2.0, "amount": 96.0},
    {"commodity_code": "250001", "name": "卤煮猪头肉", "quantity": 15.21, "amount": 121.68},
    {"commodity_code": "2059497", "name": "油麦菜 斤", "quantity": 4.47, "amount": 22.34},
    {"commodity_code": "6976108169908", "name": "蒲公英决明子", "quantity": 10.0, "amount": 230.0},
    {"commodity_code": "6920930354438", "name": "爱好矫姿笔筒1", "quantity": 9.0, "amount": 90.0},
    {"commodity_code": "2265001", "name": "新大白菜", "quantity": 1.46, "amount": 2.92},
    {"commodity_code": "6923450657713", "name": "雪花啤酒", "quantity": 6.0, "amount": 36.0},
    {"commodity_code": "6902538005141", "name": "康师傅方便面", "quantity": 5.0, "amount": 25.0},
    {"commodity_code": "6928804011036", "name": "娃哈哈矿泉水", "quantity": 12.0, "amount": 36.0},
    {"commodity_code": "6921168509256", "name": "五粮液", "quantity": 1.0, "amount": 1099.0}
]

# 模拟客户数据
MOCK_CUSTOMERS = [
    {"org_code": "车销5", "user_name": "车销5"},
    {"org_code": "车销6", "user_name": "车销6"},
    {"org_code": "13996512587", "user_name": "车销5"}
]

def generate_mock_order_data(num_products=3, customer_index=0):
    """
    生成模拟订单数据

    Args:
        num_products: 订单中的商品数量
        customer_index: 客户索引

    Returns:
        tuple: (客户信息, 商品列表)
    """
    # 随机选择客户
    customer = MOCK_CUSTOMERS[customer_index % len(MOCK_CUSTOMERS)]

    # 随机选择商品
    selected_products = random.sample(MOCK_PRODUCTS, min(num_products, len(MOCK_PRODUCTS)))

    # 随机调整商品数量
    adjusted_products = []
    for product in selected_products:
        # 复制一份，避免修改原始数据
        new_product = product.copy()
        # 随机调整数量，保留两位小数
        new_product["quantity"] = round(new_product["quantity"] * random.uniform(0.5, 2.0), 2)
        # 根据数量调整金额
        original_quantity = product["quantity"]
        new_product["amount"] = round(product["amount"] * (new_product["quantity"] / original_quantity), 2)
        adjusted_products.append(new_product)

    selected_products = adjusted_products

    return customer, selected_products

def test_with_mock_data(num_orders=1):
    """
    使用模拟数据测试订单创建

    Args:
        num_orders: 要创建的订单数量

    Returns:
        bool: 是否全部成功
    """
    logger.info(f"开始使用模拟数据测试，将创建 {num_orders} 个订单...")

    # 获取站点列表
    sites = get_site_list()
    if not sites:
        logger.error("未获取到站点列表")
        return False

    # 使用第一个站点
    site_id = sites[0]["id"]
    logger.info(f"使用站点: {sites[0].get('company_name', sites[0].get('name', ''))} (ID: {site_id})")

    # 获取配送时间段列表
    delivery_times = get_delivery_time_list()
    if not delivery_times:
        logger.error("未获取到配送时间段列表")
        return False

    # 使用第一个配送时间段
    delivery_time_id = delivery_times[0]["id"]
    logger.info(f"使用配送时间段: {delivery_times[0]['name']} (ID: {delivery_time_id})")

    # 创建订单
    success_count = 0
    for i in range(num_orders):
        logger.info(f"创建第 {i+1} 个订单...")

        # 生成模拟数据
        customer, products = generate_mock_order_data(
            num_products=random.randint(1, 5),
            customer_index=i
        )

        logger.info(f"客户: {customer['user_name']}")
        logger.info(f"商品数量: {len(products)}")
        for j, product in enumerate(products):
            logger.info(f"  商品 {j+1}: {product['name']}, 数量: {product['quantity']}, 金额: {product['amount']}")

        # 查询客户ID
        user_id = search_customer(customer["org_code"])
        if not user_id:
            logger.warning(f"未找到客户 {customer['user_name']}，跳过")
            continue

        # 创建订单
        result = create_order(user_id, products, site_id, delivery_time_id)
        if result:
            order_id = result.get('id', 'N/A')
            order_no = result.get('order_no', 'N/A')
            logger.info(f"订单创建成功，订单号: {order_no}, 订单ID: {order_id}")
            success_count += 1
        else:
            logger.error("订单创建失败")

    logger.info(f"测试完成，成功创建 {success_count}/{num_orders} 个订单")
    return success_count == num_orders

if __name__ == "__main__":
    # 默认创建1个订单，可以通过命令行参数指定数量
    num_orders = 1
    if len(sys.argv) > 1:
        try:
            num_orders = int(sys.argv[1])
        except ValueError:
            logger.error(f"无效的订单数量: {sys.argv[1]}")
            sys.exit(1)

    success = test_with_mock_data(num_orders)
    sys.exit(0 if success else 1)
