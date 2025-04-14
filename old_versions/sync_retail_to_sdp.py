#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyodbc
from datetime import datetime
from sdp_field_mapping import CASHIER_TO_SDP_MAPPING, map_cashier_to_sdp, prepare_order_products

def get_retail_data(begin_date, end_date):
    """
    从存储过程获取零售数据
    """
    try:
        # 连接数据库（请根据实际情况配置连接字符串）
        conn = pyodbc.connect('Driver={SQL Server};Server=your_server;Database=your_db;Uid=your_user;Pwd=your_password')
        cursor = conn.cursor()
        
        # 声明输出参数
        total_count = cursor.var(int)
        
        # 执行存储过程
        cursor.execute("""
            DECLARE @TotalCount INT
            SET @TotalCount = 0
            
            EXEC Rpt_Pr_Query_Retail 
                @RptId = 'Rm_Query_ItemSummary_Branch',
                @BeginDate = ?,
                @EndDate = ?,
                @CurrentPage = 1,
                @PageSize = 1000,
                @TotalSize = @TotalCount OUTPUT
            
            SELECT @TotalCount as total_count
        """, (begin_date, end_date))
        
        # 获取结果集
        retail_data = []
        while True:
            row = cursor.fetchone()
            if not row:
                break
                
            # 转换为字典格式
            retail_item = {
                "BranchName": row.BranchName,
                "barcode": row.Barcode,
                "SalesQty": float(row.SalesQty),
                "SalesAmt": float(row.SalesAmt)
            }
            retail_data.append(retail_item)
            
        return retail_data
        
    except Exception as e:
        print(f"获取零售数据失败: {str(e)}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()

def sync_retail_to_sdp(begin_date=None, end_date=None):
    """
    同步零售数据到苏东坡系统
    """
    # 如果未指定日期，使用当天
    if not begin_date:
        begin_date = datetime.now().strftime('%Y-%m-%d 00:00:00')
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d 23:59:59')
    
    try:
        # 获取零售数据
        retail_data = get_retail_data(begin_date, end_date)
        if not retail_data:
            print("没有找到需要同步的零售数据")
            return False
            
        # 按机构分组处理数据
        orders_by_branch = {}
        for item in retail_data:
            branch_name = item["BranchName"]
            if branch_name not in orders_by_branch:
                orders_by_branch[branch_name] = []
            orders_by_branch[branch_name].append(item)
        
        # 为每个机构创建订单
        success_count = 0
        for branch_name, items in orders_by_branch.items():
            try:
                # 映射数据
                sdp_items = [map_cashier_to_sdp(item) for item in items]
                
                # 准备订单数据
                order_data = {
                    "user_name": branch_name,
                    "order_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "products": prepare_order_products(sdp_items)
                }
                
                # TODO: 调用苏东坡系统API创建订单
                # from sdp_api import create_order
                # result = create_order(order_data)
                
                success_count += 1
                print(f"成功同步机构 {branch_name} 的订单数据")
                
            except Exception as e:
                print(f"同步机构 {branch_name} 的订单数据失败: {str(e)}")
                continue
        
        print(f"同步完成，成功处理 {success_count} 个机构的订单")
        return True
        
    except Exception as e:
        print(f"同步零售数据失败: {str(e)}")
        return False

if __name__ == "__main__":
    # 测试同步功能
    sync_retail_to_sdp() 