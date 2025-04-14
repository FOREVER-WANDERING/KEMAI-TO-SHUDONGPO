#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试存储过程调用
"""

import sys
import logging
import datetime
import pyodbc

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_stored_procedure.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("test_stored_procedure")

# 数据库配置
DB_CONFIG = {
    "host": "127.0.0.1",
    "port": "1314",
    "user": "sa",
    "password": "Sotopos123",
    "database": "zhj"
}

def test_stored_procedure():
    """测试存储过程调用"""
    try:
        # 构建连接字符串
        conn_str = (
            "DRIVER={SQL Server};"
            f"SERVER={DB_CONFIG['host']},{DB_CONFIG['port']};"
            f"DATABASE={DB_CONFIG['database']};"
            f"UID={DB_CONFIG['user']};"
            f"PWD={DB_CONFIG['password']}"
        )
        
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # 获取当天日期
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        begin_date = f"{today} 00:00:00"
        end_date = f"{today} 23:59:59"

        # 直接执行存储过程
        sql = """
        declare @p32 int
        set @p32=6
        exec Rpt_Pr_Query_Retail @RptId='Rm_Query_ItemSummary_Branch',@TempTable=NULL,@OperId='9001',@OperBranchId='00',@OperSuperGrantFlag='1',@BeginDate=?,@EndDate=?,@SheetId=NULL,@BranchId=NULL,@BranchRegionId=NULL,@BranchClsId=NULL,@ItemClsId=NULL,@ItemBrandId=NULL,@ItemId=NULL,@ItemBarcode=NULL,@ItemName=NULL,@ServesItemFlag=NULL,@CashierId=NULL,@CardId=NULL,@AssistantId=NULL,@VoucherId=NULL,@PickUpState=NULL,@PayFlag=NULL,@Sellway=NULL,@VipId=NULL,@SupplierId=NULL,@LogInfo=NULL,@Memo=NULL,@RetailSalesDeductionFlag=NULL,@CurrentPage=1,@PageSize=50,@TotalSize=@p32 output,@FieldFilters=NULL,@DateModel='0',@SaleWay=NULL,@BeginDutyTime=NULL,@EndDutyTime=NULL,@LPClsName=NULL,@StockFlag=NULL,@PosId=NULL,@O2oOrderno=NULL,@SaleModel=NULL,@GroupByModel=NULL,@CustomOrderByField=NULL,@TotalStrCondi=NULL,@IsTotal=NULL,@Condition=NULL,@SubAmt=NULL,@SheetSourceFlag=NULL,@OperationType=NULL,@SourceType=NULL,@VipTel=NULL,@VipName=NULL,@ItemType=NULL,@ShowGradeItem=NULL
        select @p32
        """
        
        cursor.execute(sql, (begin_date, end_date))
        
        # 处理所有结果集
        more_results = True
        result_count = 0
        
        while more_results:
            try:
                results = cursor.fetchall()
                if results:
                    result_count += len(results)
                    # 将结果转换为字典
                    columns = [column[0] for column in cursor.description]
                    logger.info(f"结果集字段名: {columns}")
                    
                    for row in results:
                        result_dict = dict(zip(columns, row))
                        # 记录完整的字段信息
                        logger.info("结果包含以下字段:")
                        for field, value in result_dict.items():
                            logger.info(f"  {field}: {value}")
                        logger.info(f"完整记录示例: {result_dict}")
                        break  # 只显示第一条记录
                more_results = cursor.nextset()
            except pyodbc.ProgrammingError:
                # 如果结果集不包含数据，继续检查下一个
                more_results = cursor.nextset()
                continue

        if result_count > 0:
            logger.info(f"存储过程调用成功，共处理 {result_count} 条记录")
        else:
            logger.warning("存储过程调用成功，但未返回数据")

        return True

    except Exception as e:
        logger.error(f"存储过程调用失败: {e}")
        return False

    finally:
        if 'conn' in locals() and conn:
            conn.close()

def main():
    """主函数"""
    logger.info("开始测试存储过程调用...")
    
    if test_stored_procedure():
        logger.info("存储过程测试通过！")
    else:
        logger.error("存储过程测试失败，请检查配置。")

if __name__ == "__main__":
    main()
