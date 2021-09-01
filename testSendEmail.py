async def testSendEmail(req=None,dataToSend=None):
    import smtplib
    sender = 'yiiiiihuang@gmail.com'
    receivers = ['ihuang@tsmc.com','chtuz@tsmc.com','henry88819@gmail.com']# ['ihuang@tsmc.com']    
    #创建一个带附件的实例
    message = MIMEMultipart()
    # message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
    message['From'] = Header("菜鸟教程", 'utf-8')   # 发送者
    message['To'] =  Header("测试", 'utf-8')        # 接收者    
    subject = 'Python SMTP 邮件测试'
    message['Subject'] = Header(subject, 'utf-8')
    #邮件正文内容
    message.attach(MIMEText(str(dataToSend) if dataToSend else '这是菜鸟教程Python 邮件发送测试……', 'plain', 'utf-8'))

    # 构造附件1，传送当前目录下的 test.txt 文件
    att1 = MIMEText(open('forTestingUse.txt', 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="forTestingUse.txt"'
    message.attach(att1)    
    # 构造附件2，传送当前目录下的 runoob.txt 文件
    att2 = MIMEText(open('forTestingUse.txt', 'rb').read(), 'base64', 'utf-8')
    att2["Content-Type"] = 'application/octet-stream'
    att2["Content-Disposition"] = 'attachment; filename="runoob.txt"'
    message.attach(att2)

    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com',port=587)#'localhost'
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.ehlo()
        smtpObj.login('yiiiiihuang@gmail.com', 'Taigidian2021')
        smtpObj.sendmail(sender, receivers, message.as_string()) 
        smtpObj.quit()        
        print ("Successfully sent email")
        return Response(status=200,content_type='text/plain') 
    except:
        logging.exception("message")
        print ("Error: unable to send email")
        return Response(status=500,content_type='text/plain') 