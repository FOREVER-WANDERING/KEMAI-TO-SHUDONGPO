#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试数据库连接和API调用
"""

import sys
import time
import json
import hashlib
import logging
import datetime
import requests
import pyodbc

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_connection.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("test_connection")

# 配置信息
CONFIG = {
    # 收银系统数据库配置
    "db": {
        "host": "127.0.0.1",
        "port": "1314",
        "user": "sa",
        "password": "Sotopos123",
        "database": "zhj"
    },
    # 苏东坡API配置
    "sdp_api": {
        "base_url": "https://scm.sdongpo.com/cc_thirdparty",
        "appid": "3647a33b94f745ed",
        "secret": "7d3c21acab1539c03f9fb62a4754343f"
    }
}

def test_db_connection():
    """测试数据库连接"""
    logger.info("测试数据库连接...")

    try:
        # 构建连接字符串
        conn_str = (
            "DRIVER={SQL Server};"
            f"SERVER={CONFIG['db']['host']},{CONFIG['db']['port']};"
            f"DATABASE={CONFIG['db']['database']};"
            f"UID={CONFIG['db']['user']};"
            f"PWD={CONFIG['db']['password']}"
        )
        
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        row = cursor.fetchone()

        if row:
            logger.info(f"数据库连接成功！SQL Server版本: {row[0]}")

            # 尝试获取表信息
            cursor.execute("""
            SELECT TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE'
            """)

            tables = cursor.fetchall()
            logger.info(f"数据库中的表数量: {len(tables)}")
            logger.info(f"表名示例: {[table[0] for table in tables[:5]]}")

            # 测试存储过程
            logger.info("测试存储过程 Rpt_Pr_Query_Retail...")
            try:
                # 获取当天日期
                today = datetime.datetime.now().strftime('%Y-%m-%d')
                begin_date = f"{today} 00:00:00"
                end_date = f"{today} 23:59:59"

                cursor = conn.cursor()
                cursor.execute("""
                declare @p32 int
                set @p32=6
                exec Rpt_Pr_Query_Retail @RptId='Rm_Query_ItemSummary_Branch',@TempTable=NULL,@OperId='9001',@OperBranchId='00',@OperSuperGrantFlag='1',@BeginDate=?,@EndDate=?,@SheetId=NULL,@BranchId=NULL,@BranchRegionId=NULL,@BranchClsId=NULL,@ItemClsId=NULL,@ItemBrandId=NULL,@ItemId=NULL,@ItemBarcode=NULL,@ItemName=NULL,@ServesItemFlag=NULL,@CashierId=NULL,@CardId=NULL,@AssistantId=NULL,@VoucherId=NULL,@PickUpState=NULL,@PayFlag=NULL,@Sellway=NULL,@VipId=NULL,@SupplierId=NULL,@LogInfo=NULL,@Memo=NULL,@RetailSalesDeductionFlag=NULL,@CurrentPage=1,@PageSize=50,@TotalSize=@p32 output,@FieldFilters=NULL,@DateModel='0',@SaleWay=NULL,@BeginDutyTime=NULL,@EndDutyTime=NULL,@LPClsName=NULL,@StockFlag=NULL,@PosId=NULL,@O2oOrderno=NULL,@SaleModel=NULL,@GroupByModel=NULL,@CustomOrderByField=NULL,@TotalStrCondi=NULL,@IsTotal=NULL,@Condition=NULL,@SubAmt=NULL,@SheetSourceFlag=NULL,@OperationType=NULL,@SourceType=NULL,@VipTel=NULL,@VipName=NULL,@ItemType=NULL,@ShowGradeItem=NULL
                select @p32 as total_size
                """, (begin_date, end_date))

                # 获取结果集
                results = cursor.fetchall()

                # 由于存储过程可能返回多个结果集，我们需要获取最后一个结果集
                while cursor.nextset():
                    temp_results = cursor.fetchall()
                    if temp_results:
                        results = temp_results
                        # 记录字段名
                        columns = [column[0] for column in cursor.description]
                        logger.info(f"结果集字段名: {columns}")

                if results and len(results) > 0:
                    logger.info(f"存储过程调用成功，返回 {len(results)} 条记录")
                    if len(results) > 0:
                        # 将结果转换为字典
                        columns = [column[0] for column in cursor.description]
                        # 打印所有列名
                        logger.info(f"返回的字段名: {columns}")
                        
                        # 记录第一条记录的详细信息
                        result_dict = dict(zip(columns, results[0]))
                        logger.info("首行数据详细信息:")
                        for field, value in result_dict.items():
                            logger.info(f"  {field}: {value}")
                        logger.info(f"完整记录示例: {result_dict}")
                else:
                    logger.warning("存储过程调用成功，但未返回数据")
            except Exception as e:
                logger.error(f"存储过程调用失败: {e}")

            return True
        else:
            logger.error("数据库连接失败：无法获取版本信息")
            return False

    except Exception as e:
        logger.error(f"数据库连接失败: {e}")
        return False
    finally:
        if 'conn' in locals() and conn:
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

def test_sdp_api():
    """测试苏东坡API调用"""
    logger.info("测试苏东坡API调用...")

    base_url = CONFIG["sdp_api"]["base_url"]
    appid = CONFIG["sdp_api"]["appid"]
    secret = CONFIG["sdp_api"]["secret"]

    # 测试获取站点列表API
    api_path = "/openApi/common/siteList"

    # 添加公共参数
    params = {
        "appid": appid,
        "timestamp": int(time.time()),
        "status": 1
    }

    # 生成签名
    sign = generate_sign(params, secret)
    params['sign'] = sign

    url = f"{base_url}{api_path}"

    try:
        # 禁用SSL证书验证
        response = requests.get(url, params=params, verify=False)
        response.raise_for_status()
        result = response.json()

        if result['status'] == 1:
            logger.info(f"API调用成功！获取到 {len(result['data'])} 个站点")
            logger.info(f"站点示例: {json.dumps(result['data'][0], ensure_ascii=False)}")
            return True
        else:
            logger.error(f"API调用失败: {result.get('message', '未知错误')}")
            return False

    except Exception as e:
        logger.error(f"API调用异常: {e}")
        return False

def main():
    """主函数"""
    logger.info("开始测试连接...")

    db_success = test_db_connection()
    api_success = test_sdp_api()

    if db_success and api_success:
        logger.info("所有连接测试通过！系统可以正常运行。")
    else:
        if not db_success:
            logger.error("数据库连接测试失败，请检查配置。")
        if not api_success:
            logger.error("API调用测试失败，请检查配置。")

if __name__ == "__main__":
    main()
