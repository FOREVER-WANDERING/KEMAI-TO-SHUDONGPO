import pyodbc
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_connection(host, port, user, password, database):
    """测试数据库连接并打印详细信息"""
    try:
        logger.info(f"尝试连接到数据库服务器 {host}:{port}")
        logger.info(f"数据库: {database}")
        logger.info(f"用户名: {user}")
        
        # 构建连接字符串
        conn_str = (
            "DRIVER={SQL Server};"
            f"SERVER={host},{port};"
            f"DATABASE={database};"
            f"UID={user};"
            f"PWD={password}"
        )
        
        conn = pyodbc.connect(conn_str)
        logger.info("数据库连接成功！")
        
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        logger.info(f"SQL Server 版本: {version}")
        
        # 测试数据库权限
        logger.info("测试数据库权限...")
        cursor.execute("""
            SELECT HAS_PERMS_BY_NAME(NULL, NULL, 'VIEW SERVER STATE') as has_view_server_state,
                   HAS_PERMS_BY_NAME(NULL, 'DATABASE', 'VIEW DATABASE STATE') as has_view_database_state,
                   HAS_DBACCESS(DB_NAME()) as has_db_access
        """)
        perms = cursor.fetchone()
        logger.info(f"VIEW SERVER STATE权限: {bool(perms[0])}")
        logger.info(f"VIEW DATABASE STATE权限: {bool(perms[1])}")
        logger.info(f"数据库访问权限: {bool(perms[2])}")
        
        # 测试表访问权限
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
        """)
        tables = cursor.fetchall()
        logger.info(f"可访问的表数量: {len(tables)}")
        if tables:
            logger.info("表名示例:")
            for table in tables[:5]:
                logger.info(f"  - {table[0]}")
        
        conn.close()
        return True
        
    except pyodbc.Error as e:
        logger.error(f"数据库连接错误: {str(e)}")
        if "Login failed for user" in str(e):
            logger.error("可能是用户名或密码错误")
        elif "Cannot open database" in str(e):
            logger.error("可能是数据库名称错误或没有访问权限")
        elif "Server connection failed" in str(e):
            logger.error("可能是服务器地址错误或SQL Server服务未启动")
        return False
    except Exception as e:
        logger.error(f"其他错误: {str(e)}")
        return False

if __name__ == "__main__":
    # 数据库配置
    config = {
        "host": "127.0.0.1，1314",
        "user": "sa",
        "password": "Sotopos123",
        "database": "zhj"
    }
    
    test_connection(**config) 