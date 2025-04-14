# 收银系统数据同步到苏东坡订单系统

本系统用于将收银系统的销售数据同步到苏东坡供应链系统，自动创建订单。

## 主要功能

- 从收银系统获取当天销售数据
- 将销售数据转换为苏东坡订单格式
- 自动计算单价（金额除以数量）
- 防止重复上传，只上传新的或更新的数据
- 详细记录所有操作，包括成功和失败的情况

## 文件说明

- `sync_sdp_order.py`: 主同步脚本
- `cashier_to_sdp_order.py`: 收银系统数据同步到苏东坡订单系统的核心功能
- `sdp_field_mapping.py`: 字段映射配置
- `order_record.py`: 订单记录管理
- `logger_config.py`: 日志配置
- `view_logs.py`: 日志查看工具
- `run_daily_sync.bat`: 每日同步批处理脚本
- `setup_task.bat`: 设置Windows计划任务

## 使用方法

### 手动运行

```bash
# 正常运行
python sync_sdp_order.py

# 强制同步（忽略重复检查）
python sync_sdp_order.py --force
```

### 设置计划任务

运行`setup_task.bat`脚本，将在Windows计划任务中创建一个每天23:00自动运行的任务。

```bash
setup_task.bat
```

### 查看日志

使用`view_logs.py`工具查看日志文件：

```bash
# 列出所有日志文件
python view_logs.py --list

# 查看最新的日志文件（默认显示最后50行）
python view_logs.py

# 查看指定的日志文件（序号从1开始）
python view_logs.py --file 2

# 显示更多行数
python view_logs.py --lines 100

# 显示全部日志
python view_logs.py --lines 0

# 过滤日志（只显示包含指定字符串的行）
python view_logs.py --filter "错误"
```

## 配置说明

在`cashier_to_sdp_order.py`文件中，您可以修改以下配置：

```python
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
        "base_url": "https://scm.sdongpo.com/cc_thirdparty",
        "appid": "3647a33b94f745ed",
        "secret": "7d3c21acab1539c03f9fb62a4754343f"
    },
    # 默认站点ID和发货时间段ID
    "default_site_id": "6",
    "default_delivery_time": "",  # 将通过API获取
    # 默认支付方式：0货到付款
    "default_pay_way": 0
}
```

## 故障排除

1. 如果批处理文件报错"不是内部或外部命令，也不是可运行的程序"：
   - 这通常是因为Python没有正确安装或没有添加到系统PATH中
   - 我们已经更新了批处理文件，它会自动尝试查找Python安装路径
   - 如果仍然失败，请安装Python并确保将其添加到系统PATH中

2. 如果服务无法启动，请检查日志文件中的错误信息

3. 如果安装依赖包失败：
   - 确保服务器能够访问互联网
   - 如果服务器在内网环境，可能需要手动安装依赖包
   - 手动安装命令：`pip install pymssql requests schedule pywin32`

4. 如果数据库连接失败：
   - 确保数据库连接信息正确
   - 确保服务器能够访问数据库服务器(127.0.0.1,1314)
   - 检查防火墙设置，确保允许数据库连接

5. 如果存储过程调用失败：
   - 检查收银系统中是否存在`Rpt_Pr_Query_Retail`存储过程
   - 查看日志文件中的错误信息

6. 如果API调用失败：
   - 确保苏东坡API的appid和secret正确
   - 确保服务器能够访问苏东坡API服务器
   - 检查网络连接是否正常

## 日志记录

系统会详细记录所有操作，包括成功和失败的情况，便于排查问题。

- 日志文件保存在`logs`目录下，按日期命名，例如`sdp_sync_20250411.log`
- 日志级别包括：INFO（信息）、WARNING（警告）、ERROR（错误）
- 日志内容包括：时间、模块名、日志级别、日志消息

### 订单记录

- 订单记录保存在`records`目录下，文件名为`uploaded_orders.json`

## 注意事项

- 每天的销售数据只能上传一次，不允许上传重复，只能上传更新的数据
- 苏东坡系统中的单价是通过收银系统的金额除以数量计算得出
- 收银系统传输字段包括'BranchName'、'barcode'、'SalesQty'、'SalesAmt'
- 脚本使用存储过程 `Rpt_Pr_Query_Retail` 获取收银汇总数据
- 苏东坡系统中的客户编号必须与收银系统的机构代码匹配
