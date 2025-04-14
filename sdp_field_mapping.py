#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
苏东坡系统字段映射配置
定义收银系统字段到苏东坡系统字段的映射关系
"""

# 收银系统字段到苏东坡系统字段的映射
CASHIER_TO_SDP_MAPPING = {
    # 基本字段映射
    "BranchName": "user_name",           # 收银系统机构名称映射到苏东坡系统的客户名称
    "Barcode": "commodity_code",         # 收银系统商品条码映射到苏东坡系统的商品编码
    "SalesQty": "quantity",              # 销售数量
    "SalesAmt": "amount"                 # 销售金额
}

# 苏东坡系统订单字段
SDP_ORDER_FIELDS = {
    "user_id": "客户ID",
    "site_id": "站点ID",
    "delivery_time_id": "配送时间段ID",
    "pay_way": "支付方式",
    "remark": "备注",
    "order_time": "订单时间",
    "products": "商品列表"
}

# 苏东坡系统商品字段
SDP_PRODUCT_FIELDS = {
    "product_id": "商品ID",
    "quantity": "数量",
    "amount": "金额"
}

# 苏东坡API路径配置
SDP_API_PATHS = {
    "site_list": "/openApi/common/siteList",                    # 站点列表
    "delivery_time_list": "/openApi/common/deliveryTimeList",  # 配送时间段列表
    "customer_list": [
        # 根据官方文档，正确的客户查询API
        "/openApi/user/query",
        # 备用客户列表API
        "/openApi/common/userList",
        "/openApi/user/list",
        "/openApi/customer/list",
        "/openApi/customer/search"
    ],
    "customer_save": [
        # 根据官方文档，正确的客户创建API
        "/openApi/user/create",
        # 备用客户创建API
        "/openApi/common/userSave",
        "/openApi/customer/save"
    ],
    "product_list": [
        # 根据官方文档，正确的商品查询API
        "/openApi/commodity/query",
        # 已确认可用的商品列表API
        "/openApi/commodity/list",
        # 备用商品列表API
        "/openApi/common/commodityList",
        "/openApi/product/list",
        "/openApi/product/search"
    ],
    "product_save": [
        # 根据官方文档，正确的商品创建API
        "/openApi/commodity/create",
        # 备用商品创建API
        "/openApi/commodity/save",
        "/openApi/common/commoditySave",
        "/openApi/product/save"
    ],
    "order_save": [
        # 根据官方文档，正确的订单创建API
        "/openApi/order/create",
        # 备用订单创建API
        "/openApi/order/save",
        "/openApi/common/orderSave"
    ]
}

def map_cashier_to_sdp(cashier_data):
    """将收银系统数据映射为苏东坡系统数据格式

    收银系统字段：
    - BranchName: 机构名称
    - Barcode: 商品条码
    - SalesQty: 销售数量
    - SalesAmt: 销售金额

    苏东坡系统字段：
    - user_name: 客户名称
    - org_code: 机构代码
    - commodity_code: 商品编码
    - quantity: 数量
    - amount: 金额
    - unit_price: 单价（金额除以数量）
    """
    sdp_data = {}

    # 处理机构名称作为客户名称
    if 'BranchName' in cashier_data:
        branch_name = str(cashier_data['BranchName']).strip()
        if branch_name and not any(x in branch_name for x in ['小计', '总计']):
            sdp_data['user_name'] = branch_name
            # 使用机构名称作为机构代码
            sdp_data['org_code'] = branch_name

    # 处理商品条码作为商品编码
    if 'Barcode' in cashier_data:
        barcode = str(cashier_data['Barcode']).strip()
        if barcode:
            sdp_data['commodity_code'] = barcode

    # 处理数量和金额
    if 'SalesQty' in cashier_data and 'SalesAmt' in cashier_data:
        quantity = float(cashier_data['SalesQty'])
        amount = float(cashier_data['SalesAmt'])

        sdp_data['quantity'] = quantity
        sdp_data['amount'] = amount

        # 计算单价（金额除以数量）
        if quantity > 0:
            sdp_data['unit_price'] = amount / quantity
        else:
            sdp_data['unit_price'] = 0

    # 打印映射后的数据，用于调试
    import logging
    logger = logging.getLogger("cashier_to_sdp")
    logger.info(f"映射后的数据: {sdp_data}")

    return sdp_data

def prepare_order_products(products_data):
    """准备订单商品数据"""
    product_list = []
    for product in products_data:
        if 'commodity_code' in product and 'quantity' in product:
            product_item = {
                "commodity_code": product["commodity_code"],
                "quantity": float(product["quantity"]),
                "amount": float(product.get("amount", 0))
            }
            product_list.append(product_item)
    return product_list