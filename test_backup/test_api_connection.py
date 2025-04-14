#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试蔬东坡API连接
"""

import sys
import time
import json
import hashlib
import logging
import requests

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_api_connection.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("test_api_connection")

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

def test_site_list():
    """测试获取站点列表"""
    logger.info("测试获取站点列表...")
    api_path = "/openApi/common/siteList"
    params = {"status": 1}
    return call_sdp_api(api_path, params)

def test_delivery_time_list():
    """测试获取配送时间段列表"""
    logger.info("测试获取配送时间段列表...")
    api_path = "/openApi/common/deliveryTimeList"
    params = {"status": 1}
    return call_sdp_api(api_path, params)

def test_customer_list():
    """测试获取客户列表"""
    logger.info("测试获取客户列表...")

    # 尝试多个API路径
    api_paths = [
        "/openApi/user/list",
        "/openApi/common/userList",
        "/openApi/customer/list"
    ]

    params = {"status": 1}

    for api_path in api_paths:
        logger.info(f"尝试客户API路径: {api_path}")
        result = call_sdp_api(api_path, params)
        if result:
            return result

    return None

def test_product_list():
    """测试获取商品列表"""
    logger.info("测试获取商品列表...")

    # 尝试多个API路径
    api_paths = [
        "/openApi/commodity/list",
        "/openApi/common/commodityList",
        "/openApi/product/list"
    ]

    params = {"status": 1}

    for api_path in api_paths:
        logger.info(f"尝试商品API路径: {api_path}")
        result = call_sdp_api(api_path, params)
        if result:
            return result

    return None

def main():
    """主函数"""
    logger.info("开始测试蔬东坡API连接...")

    # 测试站点列表
    sites = test_site_list()
    if sites:
        logger.info(f"成功获取到 {len(sites)} 个站点")
    else:
        logger.error("获取站点列表失败")

    # 测试配送时间段列表
    delivery_times = test_delivery_time_list()
    if delivery_times:
        logger.info(f"成功获取到 {len(delivery_times)} 个配送时间段")
    else:
        logger.error("获取配送时间段列表失败")

    # 测试客户列表
    customers = test_customer_list()
    if customers:
        logger.info(f"成功获取到 {len(customers)} 个客户")
    else:
        logger.error("获取客户列表失败")

    # 测试商品列表
    products = test_product_list()
    if products:
        logger.info(f"成功获取到 {len(products)} 个商品")
    else:
        logger.error("获取商品列表失败")

if __name__ == "__main__":
    main()
