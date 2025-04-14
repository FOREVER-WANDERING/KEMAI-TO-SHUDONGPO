@echo off
chcp 936
echo 卸载收银系统数据同步到苏东坡供应链系统服务...

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

REM 停止服务
echo 正在停止服务...
%PYTHON_CMD% cashier_to_sdp_service.py stop
if %errorlevel% neq 0 (
    echo 警告: 停止服务失败，服务可能已经停止或不存在。
)

REM 卸载服务
echo 正在卸载服务...
%PYTHON_CMD% cashier_to_sdp_service.py remove
if %errorlevel% neq 0 (
    echo 错误: 卸载服务失败。
    pause
    exit /b 1
)

echo 服务已成功卸载！
pause
