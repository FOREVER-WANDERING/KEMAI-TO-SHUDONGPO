@echo off
REM 每日同步蔬东坡订单的批处理脚本

echo 开始执行蔬东坡订单同步...
echo 当前时间: %date% %time%

REM 设置日志文件
set LOG_FILE=daily_sync_%date:~0,4%%date:~5,2%%date:~8,2%.log

REM 执行Python脚本
python sync_sdp_order.py > %LOG_FILE% 2>&1

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
