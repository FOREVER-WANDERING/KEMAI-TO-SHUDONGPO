@echo off
chcp 936
echo 测试存储过程调用...

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
%PIP_CMD% install pymssql
if %errorlevel% neq 0 (
    echo 错误: 安装依赖包失败，请检查网络连接或手动安装以下包:
    echo pymssql
    pause
    exit /b 1
)

REM 运行测试脚本
echo 正在运行存储过程测试...
%PYTHON_CMD% test_stored_procedure.py
if %errorlevel% neq 0 (
    echo 错误: 测试失败。
    pause
    exit /b 1
)

echo 测试完成，请查看上面的结果和test_stored_procedure.log文件了解详情。
pause
