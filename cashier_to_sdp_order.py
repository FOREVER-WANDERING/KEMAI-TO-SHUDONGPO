#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
收银系统数据同步到苏东坡供应链系统脚本
功能：每天23点从收银系统获取当天汇总数据，并传入苏东坡供应链系统生成订单
"""

import sys
import time
import json
import hashlib
import logging
import datetime
import requests
import pyodbc
from sdp_field_mapping import map_cashier_to_sdp, SDP_API_PATHS

# 获取日志记录器
logger = logging.getLogger("cashier_to_sdp")

# 配置信息
CONFIG = {
    # 收银系统数据库配置
    "db": {
        "host": "127.0.0.1",  # 不要包含端口号
        "port": "1314",       # 端口号应该是字符串
        "user": "sa",
        "password": "Sotopos123",
        "database": "zhj"
    },
    # 苏东坡API配置
    "sdp_api": {
        "base_url": "https://scm.sdongpo.com/cc_thirdparty",  # 恢复为原始URL
        "appid": "3647a33b94f745ed",
        "secret": "7d3c21acab1539c03f9fb62a4754343f"
    },
    # 默认站点ID和发货时间段ID
    "default_site_id": "6",  # 设置默认站点ID为6
    "default_delivery_time": "",  # 将通过API获取
    # 默认支付方式：0货到付款
    "default_pay_way": 0
}

def get_db_connection():
    """获取数据库连接"""
    try:
        # 构建连接字符串
        conn_str = (
            "DRIVER={SQL Server};"  # 使用默认SQL Server驱动
            f"SERVER={CONFIG['db']['host']},{CONFIG['db']['port']};"
            f"DATABASE={CONFIG['db']['database']};"
            f"UID={CONFIG['db']['user']};"
            f"PWD={CONFIG['db']['password']};"
            "TrustServerCertificate=yes"  # 添加信任服务器证书选项
        )

        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        logger.error(f"数据库连接失败: {e}")
        return None

def get_today_date():
    """获取当前日期字符串，格式为 YYYY-MM-DD"""
    return datetime.datetime.now().strftime('%Y-%m-%d')

def get_today_cashier_data():
    """获取当天收银汇总数据"""
    conn = get_db_connection()
    if not conn:
        return {}

    try:
        cursor = conn.cursor()

        # 获取当天日期
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        begin_date = f"{today} 00:00:00"
        end_date = f"{today} 23:59:59"

        # 执行存储过程获取收银汇总数据
        cursor.execute("""
        declare @p32 int
        set @p32=6
        exec Rpt_Pr_Query_Retail @RptId='Rm_Query_ItemSummary_Branch',@TempTable=NULL,@OperId='9001',@OperBranchId='00',@OperSuperGrantFlag='1',@BeginDate=?,@EndDate=?,@SheetId=NULL,@BranchId=NULL,@BranchRegionId=NULL,@BranchClsId=NULL,@ItemClsId=NULL,@ItemBrandId=NULL,@ItemId=NULL,@ItemBarcode=NULL,@ItemName=NULL,@ServesItemFlag=NULL,@CashierId=NULL,@CardId=NULL,@AssistantId=NULL,@VoucherId=NULL,@PickUpState=NULL,@PayFlag=NULL,@Sellway=NULL,@VipId=NULL,@SupplierId=NULL,@LogInfo=NULL,@Memo=NULL,@RetailSalesDeductionFlag=NULL,@CurrentPage=1,@PageSize=50,@TotalSize=@p32 output,@FieldFilters=NULL,@DateModel='0',@SaleWay=NULL,@BeginDutyTime=NULL,@EndDutyTime=NULL,@LPClsName=NULL,@StockFlag=NULL,@PosId=NULL,@O2oOrderno=NULL,@SaleModel=NULL,@GroupByModel=NULL,@CustomOrderByField=NULL,@TotalStrCondi=NULL,@IsTotal=NULL,@Condition=NULL,@SubAmt=NULL,@SheetSourceFlag=NULL,@OperationType=NULL,@SourceType=NULL,@VipTel=NULL,@VipName=NULL,@ItemType=NULL,@ShowGradeItem=NULL
        select @p32 as total_size
        """, (begin_date, end_date))

        # 获取结果集
        results = []
        more_results = True

        while more_results:
            try:
                rows = cursor.fetchall()
                if rows:
                    # 将结果转换为字典
                    columns = [column[0] for column in cursor.description]
                    logger.info(f"结果集字段名: {columns}")

                    for row in rows:
                        result_dict = {}
                        for i, value in enumerate(row):
                            result_dict[columns[i]] = value
                        results.append(result_dict)

                        # 记录第一行数据的所有字段值，用于调试
                        if len(results) == 1:
                            logger.info("首行数据详细信息:")
                            for field, value in result_dict.items():
                                logger.info(f"  {field}: {value}")

                more_results = cursor.nextset()
            except pyodbc.ProgrammingError:
                # 如果结果集不包含数据，继续检查下一个
                more_results = cursor.nextset()
                continue

        # 记录返回的字段名，用于调试
        if results and len(results) > 0:
            logger.info(f"存储过程返回的字段名: {list(results[0].keys())}")
            logger.info(f"返回数据示例: {results[0]}")

        # 按机构代码分组
        org_data = {}
        for row in results:
            # 使用映射函数将收银系统数据转换为苏东坡系统格式
            sdp_row = map_cashier_to_sdp(row)

            # 尝试获取关键字段
            org_code = sdp_row.get('org_code', '')
            commodity_code = sdp_row.get('commodity_code', '')

            # 跳过汇总行和小计行
            if '小计' in str(org_code) or '总计' in str(org_code):
                logger.info(f"跳过汇总/小计行: {sdp_row}")
                continue

            # 处理机构ID中的空格
            if org_code:
                org_code = org_code.strip()

            # 处理商品编码中的空格
            if commodity_code:
                commodity_code = commodity_code.strip()

            if not org_code or not commodity_code:
                logger.warning(f"跳过没有机构代码或商品编码的记录: {row}")
                continue

            # 更新字段值
            sdp_row['org_code'] = org_code
            sdp_row['commodity_code'] = commodity_code

            if org_code not in org_data:
                org_data[org_code] = []

            org_data[org_code].append(sdp_row)

        logger.info(f"获取到 {len(results)} 条收银记录，涉及 {len(org_data)} 个机构")
        return org_data

    except Exception as e:
        logger.error(f"获取收银数据失败: {e}")
        return {}
    finally:
        if conn:
            conn.close()

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
    """调用苏东坡API"""
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
    logger.info(f"请求参数: {json.dumps(params, ensure_ascii=False, default=str)}")

    try:
        # 记录请求开始时间
        start_time = time.time()

        # 禁用SSL证书验证
        requests.packages.urllib3.disable_warnings()
        if method.upper() == 'GET':
            response = requests.get(url, params=params, verify=False)
        else:  # POST
            response = requests.post(url, data=params, verify=False)

        # 记录请求耗时
        elapsed_time = time.time() - start_time
        logger.info(f"请求耗时: {elapsed_time:.3f} 秒")

        # 记录响应状态码
        logger.info(f"响应状态码: {response.status_code}")

        response.raise_for_status()
        result = response.json()
        logger.info(f"API返回结果: {json.dumps(result, ensure_ascii=False)}")

        if result['status'] != 1:
            error_msg = result.get('message', '未知错误')
            logger.error(f"API调用失败: {error_msg}")
            logger.error(f"失败详情: {json.dumps(result, ensure_ascii=False)}")
            return None

        return result['data']

    except requests.exceptions.RequestException as e:
        logger.error(f"API请求异常: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"JSON解析异常: {e}")
        logger.error(f"响应内容: {response.text if 'response' in locals() else '无响应'}")
        return None
    except Exception as e:
        logger.error(f"API调用其他异常: {e}")
        import traceback
        logger.error(f"异常详情: {traceback.format_exc()}")
        return None

def get_site_list():
    """获取站点列表"""
    return call_sdp_api(SDP_API_PATHS["site_list"], {"status": 1})

def get_delivery_time_list():
    """获取配送时间段列表"""
    return call_sdp_api(SDP_API_PATHS["delivery_time_list"], {"status": 1})

def search_customer(org_code):
    """根据机构代码查询客户"""
    # 优先使用官方文档中的客户查询API
    api_path = SDP_API_PATHS["customer_list"][0]  # /openApi/user/query
    logger.info(f"使用客户查询API: {api_path}")

    # 根据官方文档，使用search_value参数进行模糊查询
    params = {
        "search_value": org_code,  # 使用机构代码作为搜索值
        "status": 1,
        "page": 1,
        "page_size": 10
    }

    result = call_sdp_api(api_path, params)
    if result and "list" in result and len(result["list"]) > 0:
        # 返回第一个匹配的客户ID
        logger.info(f"找到匹配客户: {result['list'][0].get('user_name', '')}")
        return result["list"][0]["user_id"]

    # 如果找不到，尝试其他API路径
    logger.info("尝试其他客户API路径...")
    for api_path in SDP_API_PATHS["customer_list"][1:]:
        logger.info(f"尝试客户API路径: {api_path}")
        customers = call_sdp_api(api_path, {"status": 1})
        if customers and len(customers) > 0:
            logger.info(f"使用备用API找到客户")
            return customers[0]["id"]

    # 如果所有API都失败，返回None
    logger.warning(f"未找到机构代码 {org_code} 对应的客户")
    return None

def search_product(product_code):
    """根据商品编码查询商品"""
    # 优先使用官方文档中的商品查询API
    api_path = SDP_API_PATHS["product_list"][0]  # /openApi/commodity/query
    logger.info(f"使用商品查询API: {api_path}")

    # 根据官方文档，使用search_value参数进行模糊查询
    params = {
        "search_value": product_code,  # 使用商品编码作为搜索值
        "status": "Y",  # 正常状态的商品
        "page": 1,
        "page_size": 10
    }

    result = call_sdp_api(api_path, params)
    if result and "list" in result and len(result["list"]) > 0:
        # 返回第一个匹配的商品
        product = result["list"][0]
        logger.info(f"找到匹配商品: {product.get('name', '')}")
        return product

    # 如果找不到，尝试其他API路径
    logger.info("尝试其他商品API路径...")
    for api_path in SDP_API_PATHS["product_list"][1:]:
        logger.info(f"尝试商品API路径: {api_path}")
        # 尝试不同的参数名称
        params_list = [
            {"search_value": product_code, "status": 1},
            {"commodity_code": product_code, "status": 1},
            {"product_code": product_code, "status": 1}
        ]

        for params in params_list:
            products = call_sdp_api(api_path, params)
            if products and len(products) > 0:
                logger.info(f"使用备用API找到商品")
                return products[0]

    # 如果所有API都失败，返回None
    logger.warning(f"未找到商品编码 {product_code} 对应的商品")
    return None

def create_order(user_id, products_data, site_id, delivery_time_id):
    """创建订单

    Args:
        user_id: 客户ID
        products_data: 商品数据列表
        site_id: 站点ID
        delivery_time_id: 配送时间段ID

    Returns:
        订单创建结果
    """
    # 先将商品编码转换为商品ID
    products_with_id = []
    for product in products_data:
        if 'commodity_code' not in product or 'quantity' not in product:
            logger.warning(f"跳过无效商品数据: {product}")
            continue

        # 查询商品ID
        product_info = search_product(product['commodity_code'])
        if not product_info:
            logger.warning(f"未找到商品 {product['commodity_code']}，跳过")
            continue

        # 获取商品ID和单价
        product_id = product_info.get('id')
        if not product_id:
            logger.warning(f"商品 {product['commodity_code']} 缺少ID，跳过")
            continue

        # 获取商品单价
        # 如果传入了unit_price，优先使用传入的单价（收银系统金额除以数量）
        unit_price = 0
        if 'unit_price' in product and float(product['unit_price']) > 0:
            unit_price = float(product['unit_price'])
            logger.info(f"使用收银系统计算的单价: {unit_price}")
        # 如果没有传入单价，尝试使用金额除以数量计算
        elif 'amount' in product and 'quantity' in product and float(product['quantity']) > 0:
            quantity = float(product['quantity'])
            amount = float(product['amount'])
            unit_price = amount / quantity
            logger.info(f"使用金额除以数量计算单价: {amount} / {quantity} = {unit_price}")
        # 如果上述方法都不可行，使用商品信息中的单价
        elif 'unit_list' in product_info and len(product_info['unit_list']) > 0:
            unit = product_info['unit_list'][0]
            unit_price = float(unit.get('price', 0))
            logger.info(f"使用商品信息中的单价: {unit_price}")

        # 确保数量的小数位数不超过2位
        quantity = float(product['quantity'])
        quantity = round(quantity, 2)  # 四舍五入到两位小数

        # 构建商品数据
        product_data = {
            "commodity_id": product_id,  # 商品ID
            "num": quantity,           # 数量
            "price": unit_price,       # 单价
            "remark": "收银系统同步"  # 备注
        }

        # 添加到商品列表
        products_with_id.append(product_data)

    if not products_with_id:
        logger.error("没有有效的商品数据，无法创建订单")
        return None

    # 构建订单参数，根据官方文档调整参数名称
    delivery_date = datetime.datetime.now().strftime('%Y-%m-%d')  # 今天的日期
    params = {
        "user_id": user_id,  # 客户ID
        "site_id": site_id,  # 站点ID
        "delivery_date": delivery_date,  # 发货日期
        "delivery_time": delivery_time_id,  # 发货时间段ID
        "pay_way": CONFIG["default_pay_way"],  # 支付方式：0货到付款
        "remark": "收银系统同步订单",  # 备注
        "commodity_list": json.dumps(products_with_id, ensure_ascii=False)  # 商品列表
    }

    logger.info(f"订单参数: {json.dumps(params, ensure_ascii=False, default=str)}")

    # 记录订单创建请求
    logger.info("=" * 40)
    logger.info("开始创建订单")
    logger.info(f"客户ID: {user_id}")
    logger.info(f"站点ID: {site_id}")
    logger.info(f"配送时间段ID: {delivery_time_id}")
    logger.info(f"商品数量: {len(products_with_id)}")

    # 记录商品详情
    for i, product in enumerate(products_with_id):
        logger.info(f"  商品 {i+1}: ID={product['commodity_id']}, 数量={product['num']}, 单价={product['price']}")

    # 尝试不同的API路径
    for api_path in SDP_API_PATHS["order_save"]:
        logger.info(f"尝试订单创建API路径: {api_path}")
        result = call_sdp_api(api_path, params, method="POST")
        if result:
            logger.info(f"使用API路径 {api_path} 成功创建订单")
            logger.info(f"订单号: {result.get('order_no', 'N/A')}, 订单ID: {result.get('order_id', result.get('id', 'N/A'))}")
            logger.info(f"订单总金额: {result.get('total', 'N/A')}")
            logger.info("=" * 40)
            return result
        else:
            logger.error(f"使用API路径 {api_path} 创建订单失败")

    logger.error("所有订单创建API路径都失败")
    logger.info("=" * 40)
    return None

def sync_data_to_sdp(force_sync=False):
    """同步收银数据到苏东坡系统创建订单"""
    logger.info("开始同步数据到苏东坡系统...")

    # 导入订单记录管理模块
    try:
        from order_record import (
            is_order_uploaded, mark_order_as_uploaded,
            filter_new_products, cleanup_old_records
        )
        has_record_module = True
        if force_sync:
            logger.info("强制同步模式：将忽略重复检查")
        else:
            logger.info("成功加载订单记录管理模块，将进行重复检查")
    except ImportError:
        logger.warning("未找到订单记录管理模块，将不进行重复检查")
        has_record_module = False
        force_sync = True  # 如果没有记录模块，强制同步

    # 获取当前日期
    today = get_today_date()

    # 清理旧记录
    if has_record_module and not force_sync:
        cleanup_old_records(30)  # 保留近30天的记录

    # 1. 获取收银系统数据
    cashier_data = get_today_cashier_data()
    if not cashier_data:
        logger.warning("未获取到收银系统数据")
        return False

    # 2. 获取站点信息
    sites = get_site_list()
    if not sites:
        logger.error("未获取到站点列表")
        return False

    # 获取默认站点
    default_site = next((site for site in sites if site.get('is_default') == '1'), sites[0])
    site_id = default_site['id']
    logger.info(f"使用站点: {default_site.get('company_name', default_site.get('name', ''))} (ID: {site_id})")

    # 3. 获取配送时间段
    delivery_times = get_delivery_time_list()
    if not delivery_times:
        logger.error("未获取到配送时间段列表")
        return False

    # 使用第一个配送时间段
    delivery_time_id = delivery_times[0]['id']
    logger.info(f"使用配送时间段: {delivery_times[0].get('name', '')} (ID: {delivery_time_id})")

    # 4. 按机构创建订单
    success_count = 0
    for org_code, products in cashier_data.items():
        logger.info(f"处理机构 {org_code}，商品数量: {len(products)}")

        # 过滤出新的商品数据（未上传过的）
        if has_record_module and not force_sync:
            # 提取商品编码列表
            product_codes = [p.get('commodity_code', '') for p in products if p.get('commodity_code', '')]

            # 检查是否已上传
            if is_order_uploaded(today, org_code, product_codes):
                logger.info(f"机构 {org_code} 的数据今天已经上传过，跳过")
                continue

            # 过滤出新的商品数据
            new_products = filter_new_products(today, org_code, products)
            if not new_products:
                logger.info(f"机构 {org_code} 没有新的商品数据需要上传，跳过")
                continue

            logger.info(f"机构 {org_code} 有 {len(new_products)} 个新商品需要上传")
            products = new_products
        elif force_sync:
            logger.info(f"强制同步模式：将同步机构 {org_code} 的所有 {len(products)} 个商品")

        # 查找客户
        user_id = search_customer(org_code)
        if not user_id:
            logger.warning(f"未找到机构 {org_code} 对应的客户，跳过")
            # 如果需要自动创建客户，可以在这里添加创建客户的代码
            continue

        # 将收银数据转换为苏东坡商品格式
        products_data = []
        for item in products:
            if 'commodity_code' in item and 'quantity' in item:
                # 使用与 create_order 函数中相同的字段名称
                # 直接使用映射函数中计算的单价
                quantity = float(item['quantity'])
                amount = float(item.get('amount', 0))

                # 如果映射函数已经计算了单价，则使用它
                if 'unit_price' in item:
                    unit_price = float(item['unit_price'])
                else:
                    # 否则重新计算
                    unit_price = amount / quantity if quantity > 0 else 0

                # 确保单价保留两位小数
                unit_price = round(unit_price, 2)

                products_data.append({
                    'commodity_code': item['commodity_code'],  # 商品编码，用于查询商品ID
                    'quantity': quantity,                    # 数量
                    'amount': amount,                        # 金额
                    'unit_price': unit_price                 # 单价
                })

                # 打印商品数据，用于调试
                logger.info(f"商品数据: 编码={item['commodity_code']}, 数量={quantity}, 金额={amount}, 单价={unit_price}")

        if not products_data:
            logger.warning(f"机构 {org_code} 没有有效的商品数据")
            continue

        # 创建订单
        result = create_order(user_id, products_data, site_id, delivery_time_id)
        if result:
            order_id = result.get('order_id', result.get('id', 'N/A'))
            order_no = result.get('order_no', 'N/A')
            logger.info(f"为机构 {org_code} 创建订单成功，订单号: {order_no}, 订单ID: {order_id}")
            success_count += 1

            # 标记订单为已上传
            if has_record_module:
                product_codes = [item.get('commodity_code', '') for item in products_data if item.get('commodity_code', '')]
                mark_order_as_uploaded(today, org_code, product_codes)
                logger.info(f"已标记机构 {org_code} 的 {len(product_codes)} 个商品为已上传")
                if force_sync:
                    logger.info(f"强制同步模式：已标记机构 {org_code} 的商品为已上传，下次将跳过")
        else:
            logger.error(f"为机构 {org_code} 创建订单失败")

    # 记录同步结果
    logger.info("=" * 60)
    if success_count > 0:
        logger.info(f"同步成功，成功创建 {success_count} 个订单")
    else:
        logger.error("同步失败，未创建任何订单")
    logger.info("=" * 60)

    return success_count > 0

def main():
    """主函数"""
    logger.info("收银系统数据同步到苏东坡供应链系统脚本启动...")

    # 立即执行一次同步
    sync_data_to_sdp()

    # 设置每天23点执行同步
    # schedule.every().day.at("23:00").do(sync_data_to_sdp)

    # 持续运行
    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)  # 每分钟检查一次

if __name__ == "__main__":
    main()
