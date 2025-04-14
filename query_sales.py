import pyodbc
import datetime
import traceback

def get_db_connection():
    conn_str = (
        "DRIVER={SQL Server};"
        "SERVER=127.0.0.1,1314;"
        "DATABASE=zhj;"
        "UID=sa;"
        "PWD=Sotopos123;"
        "TrustServerCertificate=yes"
    )
    try:
        print(f"尝试连接到数据库: {conn_str}")
        conn = pyodbc.connect(conn_str)
        print("数据库连接成功!")
        return conn
    except Exception as e:
        print(f"数据库连接失败: {str(e)}")
        traceback.print_exc()
        return None

def query_sales():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            print('数据库连接失败，请检查配置')
            return
            
        cursor = conn.cursor()
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        print(f'查询日期: {today}')

        # 执行存储过程
        cursor.execute('''
            declare @p32 int
            set @p32=6
            exec Rpt_Pr_Query_Retail 
            @RptId='Rm_Query_ItemSummary_Branch',
            @TempTable=NULL,
            @OperId='9001',
            @OperBranchId='00',
            @OperSuperGrantFlag='1',
            @BeginDate=?, 
            @EndDate=?,
            @SheetId=NULL,
            @BranchId=NULL,
            @BranchRegionId=NULL,
            @BranchClsId=NULL,
            @ItemClsId=NULL,
            @ItemBrandId=NULL,
            @ItemId=NULL,
            @ItemBarcode=NULL,
            @ItemName=NULL,
            @ServesItemFlag=NULL,
            @CashierId=NULL,
            @CardId=NULL,
            @AssistantId=NULL,
            @VoucherId=NULL,
            @PickUpState=NULL,
            @PayFlag=NULL,
            @Sellway=NULL,
            @VipId=NULL,
            @SupplierId=NULL,
            @LogInfo=NULL,
            @Memo=NULL,
            @RetailSalesDeductionFlag=NULL,
            @CurrentPage=1,
            @PageSize=50,
            @TotalSize=@p32 output,
            @FieldFilters=NULL,
            @DateModel='0',
            @SaleWay=NULL,
            @BeginDutyTime=NULL,
            @EndDutyTime=NULL,
            @LPClsName=NULL,
            @StockFlag=NULL,
            @PosId=NULL,
            @O2oOrderno=NULL,
            @SaleModel=NULL,
            @GroupByModel=NULL,
            @CustomOrderByField=NULL,
            @TotalStrCondi=NULL,
            @IsTotal=NULL,
            @Condition=NULL,
            @SubAmt=NULL,
            @SheetSourceFlag=NULL,
            @OperationType=NULL,
            @SourceType=NULL,
            @VipTel=NULL,
            @VipName=NULL,
            @ItemType=NULL,
            @ShowGradeItem=NULL
            select @p32
        ''', (
            f'{today} 00:00:00',
            f'{today} 23:59:59'
        ))

        # 获取各结果集
        more_results = True
        
        while more_results:
            try:
                # 检查 cursor.description 是否为 None
                if cursor.description is None:
                    print("当前结果集没有可用的列信息")
                    more_results = cursor.nextset()
                    continue
                    
                # 获取列名
                columns = [column[0] for column in cursor.description]
                print('\n列名:', columns)
                
                # 详细输出每个字段定义
                print('\n字段详细信息:')
                for i, col in enumerate(cursor.description):
                    print(f'字段 {i+1}: {col[0]}, 类型: {col[1].__name__}, 显示大小: {col[2]}, 内部大小: {col[3]}')
    
                # 获取并打印所有记录
                print('\n数据记录:')
                rows = cursor.fetchall()
                for i, row in enumerate(rows):
                    print(f'\n---记录 {i+1}---')
                    for j, value in enumerate(row):
                        print(f'{columns[j]}: {value}')
                    print('---记录结束---')
    
                print(f'\n总记录数: {len(rows)}')
                more_results = cursor.nextset()
            except pyodbc.ProgrammingError:
                # 如果结果集不包含数据，继续检查下一个
                print("处理结果集时发生编程错误，尝试下一个结果集")
                more_results = cursor.nextset()
                continue

    except Exception as e:
        print(f'查询出错: {str(e)}')
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    query_sales() 