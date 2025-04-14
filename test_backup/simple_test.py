import pyodbc
import traceback

print("开始测试数据库连接...")
print("正在连接到: 127.0.0.1,1314")
print("数据库: zhj")
print("用户名: sa")

try:
    print("尝试建立连接...")
    # 构建连接字符串
    conn_str = (
        "DRIVER={SQL Server};"
        "SERVER=127.0.0.1,1314;"
        "DATABASE=zhj;"
        "UID=sa;"
        "PWD=Sotopos123"
    )
    
    conn = pyodbc.connect(conn_str)
    print("数据库连接成功！")
    
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION")
    version = cursor.fetchone()[0]
    print(f"SQL Server 版本: {version}")
    
    conn.close()
    print("测试完成！")
    
except Exception as e:
    print(f"错误: {str(e)}")
    print("详细错误信息:")
    print(traceback.format_exc())
    print("\n请确认以下信息：")
    print("1. SQL Server 是否允许TCP/IP连接")
    print("2. SQL Server 配置管理器中的TCP/IP端口是否设置为1314")
    print("3. SQL Server Browser服务是否运行")
    print("4. Windows防火墙是否允许1314端口的连接") 