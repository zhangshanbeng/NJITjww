from bs4 import BeautifulSoup
import requests
import re
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def get_url():
    url = 'http://jwc.njit.edu.cn/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all(href=re.compile("content.jsp"),target="_blank",limit=9)
    main_url = 'http://jwc.njit.edu.cn/'
    url_lists = []
    for link in links:
        a = link['href']
        url_lists.append(main_url+a)
    del url_lists[0]
    return url_lists

def get_content():
    title_list = []
    for url in get_url():
        r = requests.get(url=url)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        titles = soup.find('h2', class_="title")
        if titles is None:
            continue
        title = titles.get_text()
        pub_data_text = soup.find('p',text=re.compile("\\d{4}-\\d{2}-\\d{2}")).text
        pub_data=pub_data_text.replace('时间:','')
        current_time = time.strftime('%Y-%m-%d', time.localtime())
        if pub_data == current_time:
            title_list.append(pub_data + " ； 今日通知：" + title + "；" + "详情点击： " + url)
    if len(title_list) == 0:
        sent_email(mail_title='今日没有通知',mail_body='今天没有通知')
    else:
        for title in title_list:
            sent_email(mail_title='今日通知',mail_body=title)
    title_list.clear()

def sent_email(mail_title,mail_body):
    sender = '**********'
    receiver = '*********'
    smtpServer = 'smtp.126.com'
    username = '*********'
    password = '*********'
    mail_title = mail_title
    mail_body = mail_body

    message = MIMEText(mail_body, 'plain', 'utf-8')
    message["Accept-Language"] = "zh-CN"
    message["Accept-Charset"] = "ISO-8859-1,utf-8"
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = Header(mail_title, 'utf-8')

    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpServer)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, message.as_string())
        print('邮件发送成功')
        smtp.quit()
    except smtplib.SMTPException:
        print("邮件发送失败！！！")

def main(self1,self2):
    get_content()
