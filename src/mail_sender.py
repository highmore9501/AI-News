import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import dotenv


def send_email(sender_email, sender_password, recipient_email, subject, body, attachment_path=None, smtp_server='smtp.163.com'):
    # 创建一个 MIMEMultipart 对象
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # 添加邮件正文
    msg.attach(MIMEText(body, 'plain'))

    # 如果有附件，添加附件
    if attachment_path:
        # 打开附件文件
        with open(attachment_path, 'rb') as attachment:
            # 创建一个 MIMEBase 对象
            attachment_mime = MIMEBase('application', 'octet-stream')
            attachment_mime.set_payload(attachment.read())

            # 使用 Base64 编码
            encoders.encode_base64(attachment_mime)

            # 设置附件的 Content-Disposition
            attachment_mime.add_header(
                'Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')

            # 将附件添加到 MIMEMultipart 对象中
            msg.attach(attachment_mime)

    # 连接到 163 邮箱的 SMTP 服务器
    smtp_server = smtplib.SMTP(smtp_server, 25)
    smtp_server.starttls()
    smtp_server.login(sender_email, sender_password)

    # 发送邮件
    smtp_server.sendmail(sender_email, recipient_email, msg.as_string())

    # 断开连接
    smtp_server.quit()


if __name__ == '__main__':
    # 读取环境变量
    dotenv.load_dotenv()
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')

    # 接收者的邮箱地址
    recipient_email = '523985539@qq.com'
    # 邮件主题
    subject = '测试邮件'
    # 邮件正文
    body = '这是一封测试邮件'
    # 附件路径
    attachment_path = '../data/result/News_2024-01-14.md'

    send_email(sender_email, sender_password, recipient_email,
               subject, body, attachment_path)
