"""邮件工具：发送邮件。"""

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import Any

from nanobot.agent.tools.base import Tool


class EmailTool(Tool):
    """发送邮件工具。"""
    
    name = "send_email"
    description = "发送邮件，支持发送文本内容和HTML内容。"
    
    # 默认邮件配置
    DEFAULT_SENDER = "yuxinzhang233@163.com"
    DEFAULT_PASSWORD = "GXQBQ35rdr6hJgAg"
    DEFAULT_RECEIVER = "2658687132@qq.com"
    DEFAULT_SMTP_SERVER = "smtp.163.com"
    DEFAULT_SMTP_PORT = 465
    
    parameters = {
        "type": "object",
        "properties": {
            "sender": {"type": "string", "default": "yuxinzhang233@163.com", "description": "发件人邮箱"},
            "password": {"type": "string", "default": "GXQBQ35rdr6hJgAg", "description": "邮箱授权码"},
            "receiver": {"type": "string", "default": "2658687132@qq.com", "description": "收件人邮箱"},
            "smtp_server": {"type": "string", "default": "smtp.163.com", "description": "SMTP服务器地址"},
            "smtp_port": {"type": "integer", "default": 465, "description": "SMTP端口"},
            "subject": {"type": "string", "description": "邮件主题"},
            "content": {"type": "string", "description": "邮件内容"},
            "content_type": {"type": "string", "enum": ["plain", "html"], "default": "plain", "description": "内容类型"}
        },
        "required": ["subject", "content"]
    }
    
    async def execute(self, sender: str = "yuxinzhang233@163.com", password: str = "GXQBQ35rdr6hJgAg", receiver: str = "2658687132@qq.com", smtp_server: str = "smtp.163.com", smtp_port: int = 465, subject: str = "", content: str = "", content_type: str = "plain", **kwargs: Any) -> str:
        """发送邮件。"""
        try:
            # 创建邮件对象
            msg = MIMEMultipart()
            
            # 设置邮件头部
            msg['From'] = Header(sender, 'utf-8')
            msg['To'] = Header(receiver, 'utf-8')
            msg['Subject'] = Header(subject, 'utf-8')
            
            # 添加邮件内容
            msg.attach(MIMEText(content, content_type, 'utf-8'))
            
            # 连接SMTP服务器并发送邮件
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            server.login(sender, password)
            # 将收件人转换为列表格式
            receivers = [receiver] if isinstance(receiver, str) else receiver
            server.sendmail(sender, receivers, msg.as_string())
            server.quit()
            
            return json.dumps({"status": "success", "message": "邮件发送成功"})
            
        except Exception as e:
            return json.dumps({"status": "error", "message": f"邮件发送失败: {str(e)}"})
