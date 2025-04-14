@echo off
REM 设置Windows计划任务，定时执行蔬东坡订单同步脚本

echo 正在设置蔬东坡订单同步计划任务...

REM 获取当前脚本所在目录的绝对路径
set SCRIPT_DIR=%~dp0
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

REM 设置Python脚本路径
set PYTHON_SCRIPT=%SCRIPT_DIR%\sync_sdp_order.py

REM 设置Python解释器路径（根据实际情况修改）
set PYTHON_EXE=python

REM 设置任务名称
set TASK_NAME=SDP_Order_Sync

REM 创建计划任务
schtasks /create /tn %TASK_NAME% /tr "%PYTHON_EXE% %PYTHON_SCRIPT%" /sc DAILY /st 23:00 /ru SYSTEM /f

if %ERRORLEVEL% EQU 0 (
    echo 计划任务设置成功！
    echo 任务名称: %TASK_NAME%
    echo 执行时间: 每天 23:00
    echo 执行命令: %PYTHON_EXE% %PYTHON_SCRIPT%
) else (
    echo 计划任务设置失败，请以管理员身份运行此脚本。
)

pause
