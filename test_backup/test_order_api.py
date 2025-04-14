#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试蔬东坡订单创建API
"""

import sys
import time
import json
import hashlib
import logging
import datetime
import requests

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_order_api.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("test_order_api")

# 配置信息
CONFIG = {
    # 蔬东坡API配置
    "sdp_api": {
        "base_url": "https://scm.sdongpo.com/cc_thirdparty",
        "appid": "3647a33b94f745ed",
        "secret": "7d3c21acab1539c03f9fb62a4754343f"
    }
}

def generate_sign(params, secret):
    """生成签名"""
    # 按照key的字母顺序排序
    sorted_params = sorted(params.items(), key=lambda x: x[0])

    # 拼接字符串
    sign_str = ''
    for key, value in sorted_params:
        sign_str += f"{key}{value}"

    # 加上secret
    sign_str += secret

    # MD5加密并转为大写
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()

    return sign

def call_sdp_api(api_path, params, method='GET'):
    """调用蔬东坡API"""
    base_url = CONFIG["sdp_api"]["base_url"]
    appid = CONFIG["sdp_api"]["appid"]
    secret = CONFIG["sdp_api"]["secret"]

    # 添加公共参数
    params['appid'] = appid
    params['timestamp'] = int(time.time())

    # 生成签名
    sign = generate_sign(params, secret)
    params['sign'] = sign

    url = f"{base_url}{api_path}"
    logger.info(f"请求URL: {url}")
    logger.info(f"请求参数: {json.dumps(params, ensure_ascii=False)}")

    try:
        # 禁用SSL证书验证
        requests.packages.urllib3.disable_warnings()
        if method.upper() == 'GET':
            response = requests.get(url, params=params, verify=False)
        else:  # POST
            response = requests.post(url, data=params, verify=False)

        logger.info(f"HTTP状态码: {response.status_code}")
        
        # 尝试解析JSON响应
        try:
            result = response.json()
            logger.info(f"API返回结果: {json.dumps(result, ensure_ascii=False)}")
            
            if 'status' in result and result['status'] == 1:
                logger.info("API调用成功!")
                return result.get('data')
            else:
                logger.error(f"API调用失败: {result.get('message', '未知错误')}")
                return None
        except ValueError:
            logger.error(f"返回内容不是有效的JSON: {response.text[:200]}")
            return None

    except Exception as e:
        logger.error(f"API调用异常: {e}")
        return None

def get_site_list():
    """获取站点列表"""
    logger.info("获取站点列表...")
    api_path = "/openApi/common/siteList"
    params = {"status": 1}
    return call_sdp_api(api_path, params)

def get_delivery_time_list():
    """获取配送时间段列表"""
    logger.info("获取配送时间段列表...")
    api_path = "/openApi/common/deliveryTimeList"
    params = {"status": 1}
    return call_sdp_api(api_path, params)

def test_order_save():
    """测试创建订单"""
    logger.info("测试创建订单...")
    
    # 获取站点列表
    sites = get_site_list()
    if not sites or len(sites) == 0:
        logger.error("未获取到站点列表")
        return False
    
    site_id = sites[0]["id"]
    logger.info(f"选择站点: {sites[0]['company_name']} (ID: {site_id})")
    
    # 获取配送时间段列表
    delivery_times = get_delivery_time_list()
    if not delivery_times or len(delivery_times) == 0:
        logger.error("未获取到配送时间段列表")
        return False
    
    delivery_time_id = delivery_times[0]["id"]
    logger.info(f"选择配送时间段: {delivery_times[0]['name']} (ID: {delivery_time_id})")
    
    # 构建测试订单数据
    products = [
        {
            "product_id": "测试商品ID",  # 由于没有可用的商品列表API，这里使用测试ID
            "quantity": 2,
            "unit_price": 10.5
        }
    ]
    
    # 尝试不同的订单创建API路径
    api_paths = [
        "/openApi/order/save",
        "/openApi/common/orderSave"
    ]
    
    # 构建订单参数
    order_time = datetime.datetime.now().strftime('%Y-%m-%d')
    params = {
        "user_id": "测试用户ID",  # 由于没有可用的客户列表API，这里使用测试ID
        "site_id": site_id,
        "delivery_time_id": delivery_time_id,
        "pay_way": 0,  # 货到付款
        "remark": "测试订单 - API测试",
        "order_time": order_time,
        "products": json.dumps(products, ensure_ascii=False)
    }
    
    for api_path in api_paths:
        logger.info(f"尝试订单创建API路径: {api_path}")
        result = call_sdp_api(api_path, params, method="POST")
        if result:
            logger.info(f"使用API路径 {api_path} 成功创建订单")
            return True
    
    logger.error("所有订单创建API路径都失败")
    return False

def main():
    """主函数"""
    logger.info("开始测试蔬东坡订单创建API...")
    
    # 测试创建订单
    if test_order_save():
        logger.info("订单创建API测试成功")
    else:
        logger.error("订单创建API测试失败")

if __name__ == "__main__":
    main()
