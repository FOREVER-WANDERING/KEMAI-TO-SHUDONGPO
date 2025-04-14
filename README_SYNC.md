# 蔬东坡订单同步系统

本系统用于自动将收银系统的销售数据同步到蔬东坡订单系统。

## 功能特点

- 自动从收银系统获取销售数据
- 自动将销售数据转换为蔬东坡订单格式
- 自动创建蔬东坡订单
- **防止重复上传**：每天的销售数据只能上传一次，不允许重复上传
- **只上传新数据**：只上传更新的数据，避免重复
- 支持定时执行
- 详细的日志记录
- 邮件通知功能
- 数据备份功能

## 文件说明

- `cashier_to_sdp_order.py`: 核心功能模块，负责从收银系统获取数据并同步到蔬东坡系统
- `sdp_field_mapping.py`: 字段映射配置，定义收银系统字段到蔬东坡系统字段的映射关系
- `sync_sdp_order_new.py`: 主脚本，集成了日志记录、错误通知和数据备份功能
- `notification.py`: 通知模块，用于发送邮件通知
- `backup.py`: 数据备份模块，用于备份订单数据
- `order_record.py`: 订单记录管理模块，用于记录已上传的订单信息，防止重复上传
- `run_daily_sync_new.bat`: 每日同步批处理脚本，支持命令行参数
- `setup_task_new.bat`: Windows计划任务设置脚本
- `test_order_record.py`: 测试订单记录管理功能的脚本

## 使用方法

### 1. 配置

在使用前，请先修改以下配置文件：

1. `notification.py`: 修改邮件配置
   ```python
   EMAIL_CONFIG = {
       "smtp_server": "smtp.example.com",  # 修改为您的SMTP服务器地址
       "smtp_port": 587,                   # 修改为您的SMTP服务器端口
       "smtp_user": "your_email@example.com",  # 修改为您的邮箱
       "smtp_password": "your_password",   # 修改为您的邮箱密码
       "sender": "your_email@example.com", # 修改为发件人
       "receivers": ["admin@example.com"],  # 修改为收件人列表
   }
   ```

2. `backup.py`: 修改备份配置
   ```python
   BACKUP_CONFIG = {
       "backup_dir": "backups",  # 修改为您的备份目录
       "max_backups": 30,        # 修改为您想保留的最大备份数量
   }
   ```

3. `order_record.py`: 修改记录配置
   ```python
   RECORD_CONFIG = {
       "record_dir": "records",                  # 修改为您的记录目录
       "record_file": "uploaded_orders.json",    # 修改为您的记录文件名
       "backup_dir": "records/backup",           # 修改为您的备份目录
       "max_backups": 30,                        # 修改为您想保留的最大备份数量
   }
   ```

4. `sync_sdp_order_new.py`: 修改脚本配置
   ```python
   SCRIPT_CONFIG = {
       "log_dir": "logs",                 # 修改为您的日志目录
       "log_file": "sdp_sync_{date}.log", # 修改为您的日志文件名模板
       "enable_email": True,              # 是否启用邮件通知
       "enable_backup": True,             # 是否启用数据备份
       "force_sync": False,               # 是否强制同步（忽略重复检查）
   }
   ```

### 2. 手动执行

直接运行主脚本即可：

```bash
python sync_sdp_order_new.py
```

支持的命令行参数：

- `--force`: 强制同步，忽略重复检查
- `--no-email`: 不发送邮件通知
- `--no-backup`: 不备份数据
- `--help`: 显示帮助信息

例如，强制同步且不发送邮件通知：

```bash
python sync_sdp_order_new.py --force --no-email
```

或者使用批处理脚本：

```bash
run_daily_sync_new.bat --force
```

### 3. 设置定时任务

#### Windows系统

以管理员身份运行`setup_task_new.bat`脚本，将自动设置每天23:00执行同步任务：

```bash
右键 setup_task_new.bat -> 以管理员身份运行
```

或者手动设置Windows计划任务：

1. 打开"任务计划程序"
2. 点击"创建基本任务"
3. 输入任务名称和描述
4. 选择"每天"
5. 设置开始时间为23:00
6. 选择"启动程序"
7. 程序/脚本输入`run_daily_sync_new.bat`的完整路径
8. 点击"完成"

#### Linux系统

使用crontab设置定时任务：

```bash
crontab -e
```

添加以下内容：

```
0 23 * * * cd /path/to/script && python sync_sdp_order_new.py
```

这将设置每天23:00执行同步任务。

## 防止重复上传功能

系统通过以下机制防止重复上传：

1. 每次上传订单后，系统会记录已上传的订单信息（日期、机构代码、商品编码）
2. 在上传前，系统会检查数据是否已上传
3. 只上传新增/更新的数据，避免重复

如果需要强制上传（忽略重复检查），可以使用`--force`参数：

```bash
python sync_sdp_order_new.py --force
```

## 日志和备份

### 日志记录

系统会详细记录所有操作，包括成功和失败的情况，便于排查问题。

- 日志文件保存在`logs`目录下，按日期命名，例如`sdp_sync_20250411.log`
- 日志级别包括：INFO（信息）、WARNING（警告）、ERROR（错误）
- 日志内容包括：时间、模块名、日志级别、日志消息

### 日志查看工具

系统提供了一个日志查看工具`view_logs.py`，可以方便地查看日志文件。

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

### 数据备份

- 备份文件保存在`backups`目录下，按时间戳命名
- 订单记录保存在`records`目录下，文件名为`uploaded_orders.json`
- 订单记录备份保存在`records/backup`目录下
- 订单记录保存在`records`目录下，文件名为`uploaded_orders.json`

## 故障排除

如果遇到问题，请检查：

1. 日志文件中的错误信息
2. 确保网络连接正常
3. 确保数据库连接配置正确
4. 确保API配置正确
5. 检查订单记录文件是否正常

## 联系支持

如有问题，请联系系统管理员。
