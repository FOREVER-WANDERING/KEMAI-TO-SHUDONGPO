@echo off
chcp 936
echo 安装收银系统数据同步到苏东坡供应链系统服务...

REM 尝试查找Python安装路径
SET PYTHON_CMD=python

REM 检查Python是否已安装
%PYTHON_CMD% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 尝试查找Python安装路径...

    REM 尝试常见的Python安装路径
    IF EXIST "C:\Python39\python.exe" SET PYTHON_CMD=C:\Python39\python.exe
    IF EXIST "C:\Python38\python.exe" SET PYTHON_CMD=C:\Python38\python.exe
    IF EXIST "C:\Python37\python.exe" SET PYTHON_CMD=C:\Python37\python.exe
    IF EXIST "C:\Python36\python.exe" SET PYTHON_CMD=C:\Python36\python.exe
    IF EXIST "C:\Program Files\Python39\python.exe" SET PYTHON_CMD=C:\Program Files\Python39\python.exe
    IF EXIST "C:\Program Files\Python38\python.exe" SET PYTHON_CMD=C:\Program Files\Python38\python.exe
    IF EXIST "C:\Program Files\Python37\python.exe" SET PYTHON_CMD=C:\Program Files\Python37\python.exe
    IF EXIST "C:\Program Files\Python36\python.exe" SET PYTHON_CMD=C:\Program Files\Python36\python.exe
    IF EXIST "C:\Program Files (x86)\Python39\python.exe" SET PYTHON_CMD=C:\Program Files (x86)\Python39\python.exe
    IF EXIST "C:\Program Files (x86)\Python38\python.exe" SET PYTHON_CMD=C:\Program Files (x86)\Python38\python.exe
    IF EXIST "C:\Program Files (x86)\Python37\python.exe" SET PYTHON_CMD=C:\Program Files (x86)\Python37\python.exe
    IF EXIST "C:\Program Files (x86)\Python36\python.exe" SET PYTHON_CMD=C:\Program Files (x86)\Python36\python.exe

    REM 再次检查Python
    %PYTHON_CMD% --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo 错误: 未找到Python，请先安装Python 3.6或更高版本。
        echo 请确保Python已添加到系统PATH中，或者手动编辑此脚本指定Python路径。
        pause
        exit /b 1
    )
)

echo 找到Python: %PYTHON_CMD%

REM 设置pip命令
SET PIP_CMD=%PYTHON_CMD% -m pip

REM 安装必要的依赖包
echo 正在安装必要的依赖包...
%PIP_CMD% install pymssql requests schedule pywin32
if %errorlevel% neq 0 (
    echo 错误: 安装依赖包失败，请检查网络连接或手动安装以下包:
    echo pymssql requests schedule pywin32
    pause
    exit /b 1
)

REM 安装服务
echo 正在安装服务...
%PYTHON_CMD% cashier_to_sdp_service.py install
if %errorlevel% neq 0 (
    echo 错误: 安装服务失败。
    pause
    exit /b 1
)

REM 启动服务
echo 正在启动服务...
%PYTHON_CMD% cashier_to_sdp_service.py start
if %errorlevel% neq 0 (
    echo 错误: 启动服务失败。
    pause
    exit /b 1
)

echo 服务安装并启动成功！
echo 服务名称: CashierToSdpService
echo 服务显示名称: 收银系统数据同步到苏东坡供应链系统服务
echo.
echo 您可以在Windows服务管理器中查看和管理此服务。
pause
