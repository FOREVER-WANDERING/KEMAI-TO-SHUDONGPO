@echo off
echo 正在构建蔬东坡订单同步工具安装程序...

REM 检查Inno Setup是否已安装
set INNO_COMPILER="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist %INNO_COMPILER% (
    echo 错误: 未找到Inno Setup编译器。
    echo 请先安装Inno Setup 6，然后再运行此脚本。
    echo 您可以从 https://jrsoftware.org/isdl.php 下载Inno Setup。
    pause
    exit /b 1
)

REM 确保已经构建了可执行文件
if not exist "dist\蔬东坡订单同步工具\蔬东坡订单同步工具.exe" (
    echo 错误: 未找到可执行文件。
    echo 请先运行 build_exe.bat 构建可执行文件。
    pause
    exit /b 1
)

REM 创建installer目录
if not exist "installer" mkdir installer

REM 使用Inno Setup构建安装程序
%INNO_COMPILER% setup.iss

echo.
if %ERRORLEVEL% == 0 (
    echo 安装程序构建成功！
    echo 安装程序位于 installer 目录中
) else (
    echo 安装程序构建失败，请检查错误信息
)

pause
