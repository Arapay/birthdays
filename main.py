import os
import csv
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 1. 获取今天的月份和日期 (例如今天的 05 和 28)
today = datetime.now()
today_month = today.strftime('%m')
today_day = today.strftime('%d')

# 2. 从环境变量中读取邮箱配置 (保护隐私)
SMTP_SERVER = "smtp.163.com"  # 如果用163邮箱改回 smtp.163.com
SMTP_PORT = 465
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')      # 发件人邮箱
AUTH_CODE = os.environ.get('AUTH_CODE')            # 刚刚拿到的16位授权码
RECEIVER_EMAIL = os.environ.get('RECEIVER_EMAIL')  # 接收提醒的邮箱

def send_email(birthday_people):
    names = "、".join(birthday_people)
    subject = f"🎂 今天是 {names} 的生日！"
    body = f"Hi，别忘了送上祝福！今天是 【{names}】 的生日哦！🎉"
    
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['From'] = Header("生日提醒小助手", 'utf-8')
    msg['To'] = Header("主人", 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    
    try:
        # 使用 SSL 加密连接服务器
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER_EMAIL, AUTH_CODE)
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
        server.quit()
        print("邮件发送成功！")
    except Exception as e:
        print(f"邮件发送失败: {e}")

# 3. 读取 CSV 文件并比对
birthday_people = []
if os.path.exists('birthdays.csv'):
    with open('birthdays.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 去除前后空格并比对
            if row['month'].strip() == today_month and row['day'].strip() == today_day:
                birthday_people.append(row['name'])

# 4. 如果有人今天生日，则发送邮件
if birthday_people:
    send_email(birthday_people)
else:
    print(f"今天 ({today_month}-{today_day}) 没有人过生日。")