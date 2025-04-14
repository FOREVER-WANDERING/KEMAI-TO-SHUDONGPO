#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
通知模块，用于发送邮件通知
"""

import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

logger = logging.getLogger("notification")

# 邮件配置
EMAIL_CONFIG = {
    "smtp_server": "smtp.example.com",  # SMTP服务器地址
    "smtp_port": 587,                   # SMTP服务器端口
    "smtp_user": "your_email@example.com",  # 发件人邮箱
    "smtp_password": "your_password",   # 发件人邮箱密码
    "sender": "your_email@example.com", # 发件人
    "receivers": ["admin@example.com"],  # 收件人列表
}

def send_email(subject, content, attachment_path=None):
    """
    发送邮件
    
    Args:
        subject: 邮件主题
        content: 邮件内容
        attachment_path: 附件路径，可选
        
    Returns:
        bool: 是否发送成功
    """
    try:
        # 创建邮件对象
        message = MIMEMultipart()
        message['From'] = EMAIL_CONFIG["sender"]
        message['To'] = ';'.join(EMAIL_CONFIG["receivers"])
        message['Subject'] = Header(subject, 'utf-8')
        
        # 添加邮件正文
        message.attach(MIMEText(content, 'plain', 'utf-8'))
        
        # 添加附件
        if attachment_path and os.path.exists(attachment_path):
            att = MIMEText(open(attachment_path, 'rb').read(), 'base64', 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = f'attachment; filename="{os.path.basename(attachment_path)}"'
            message.attach(att)
        
        # 发送邮件
        server = smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"])
        server.starttls()  # 使用TLS加密
        server.login(EMAIL_CONFIG["smtp_user"], EMAIL_CONFIG["smtp_password"])
        server.sendmail(EMAIL_CONFIG["sender"], EMAIL_CONFIG["receivers"], message.as_string())
        server.quit()
        
        logger.info(f"邮件发送成功: {subject}")
        return True
    except Exception as e:
        logger.error(f"邮件发送失败: {e}")
        return False

def send_success_notification(order_count, log_file=None):
    """
    发送成功通知
    
    Args:
        order_count: 成功创建的订单数量
        log_file: 日志文件路径，可选
    """
    subject = "蔬东坡订单同步成功通知"
    content = f"""
蔬东坡订单同步已成功完成！

成功创建订单数量: {order_count}
执行时间: {get_current_time()}

此邮件由系统自动发送，请勿回复。
"""
    send_email(subject, content, log_file)

def send_error_notification(error_message, log_file=None):
    """
    发送错误通知
    
    Args:
        error_message: 错误信息
        log_file: 日志文件路径，可选
    """
    subject = "蔬东坡订单同步失败通知"
    content = f"""
蔬东坡订单同步失败！

错误信息: {error_message}
执行时间: {get_current_time()}

请检查系统日志获取详细信息。

此邮件由系统自动发送，请勿回复。
"""
    send_email(subject, content, log_file)

def get_current_time():
    """获取当前时间字符串"""
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
