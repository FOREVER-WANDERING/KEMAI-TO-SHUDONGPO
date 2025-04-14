@echo off
REM 每日同步蔬东坡订单的批处理脚本

echo 开始执行蔬东坡订单同步...
echo 当前时间: %date% %time%

REM 设置日志文件
set LOG_FILE=daily_sync_%date:~0,4%%date:~5,2%%date:~8,2%.log

REM 处理命令行参数
set PARAMS=

:parse
if "%~1"=="" goto :execute
if /i "%~1"=="--force" set PARAMS=%PARAMS% --force
if /i "%~1"=="--help" (
    echo 用法: %0 [--force] [--help]
    echo   --force     强制同步，忽略重复检查
    echo   --help      显示帮助信息
    exit /b 0
)
shift
goto :parse

:execute
REM 执行Python脚本
echo 执行命令: python sync_sdp_order.py%PARAMS%
python sync_sdp_order.py%PARAMS% > %LOG_FILE% 2>&1

REM 检查执行结果
if %ERRORLEVEL% EQU 0 (
    echo 同步成功完成！
) else (
    echo 同步失败，请查看日志文件 %LOG_FILE%
)

echo 执行完成，时间: %date% %time%
echo.

REM 暂停5秒后关闭窗口
timeout /t 5
