#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
收银系统数据同步到苏东坡供应链系统 Windows 服务
"""

import os
import sys
import time
import logging
import servicemanager
import win32event
import win32service
import win32serviceutil

# 导入主脚本中的函数
from cashier_to_sdp_order import sync_data_to_sdp

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cashier_to_sdp_service.log'),
    filemode='a'
)
logger = logging.getLogger("cashier_to_sdp_service")

class CashierToSdpService(win32serviceutil.ServiceFramework):
    """Windows服务类"""
    
    _svc_name_ = "CashierToSdpService"
    _svc_display_name_ = "收银系统数据同步到苏东坡供应链系统服务"
    _svc_description_ = "每天23点从收银系统获取当天汇总数据，并传入苏东坡供应链系统生成订单"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = True
    
    def SvcStop(self):
        """服务停止时调用"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.is_running = False
    
    def SvcDoRun(self):
        """服务运行时调用"""
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.main()
    
    def main(self):
        """主函数"""
        logger.info("收银系统数据同步到苏东坡供应链系统服务启动...")
        
        # 计算距离下一个23:00的秒数
        def seconds_until_23():
            now = time.localtime()
            if now.tm_hour < 23:
                # 今天的23:00
                target = time.mktime((now.tm_year, now.tm_mon, now.tm_mday, 23, 0, 0, 0, 0, 0))
            else:
                # 明天的23:00
                tomorrow = time.localtime(time.time() + 86400)
                target = time.mktime((tomorrow.tm_year, tomorrow.tm_mon, tomorrow.tm_mday, 23, 0, 0, 0, 0, 0))
            
            return int(target - time.time())
        
        # 服务运行循环
        while self.is_running:
            # 计算等待时间
            wait_seconds = seconds_until_23()
            logger.info(f"等待 {wait_seconds} 秒后执行同步任务")
            
            # 等待直到23:00或服务停止
            rc = win32event.WaitForSingleObject(self.stop_event, wait_seconds * 1000)
            if rc == win32event.WAIT_OBJECT_0:
                # 服务停止
                break
            
            # 执行同步任务
            try:
                logger.info("开始执行同步任务")
                sync_data_to_sdp()
                logger.info("同步任务执行完成")
            except Exception as e:
                logger.error(f"同步任务执行失败: {e}")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(CashierToSdpService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(CashierToSdpService)
