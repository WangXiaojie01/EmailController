# EmailController
###功能
支持通过读取email.json配置文件来发送对应邮件内容

###配置文件内容
- 配置文件为json文件，共有email_hosts、email_senders、name_email_map、email_receivers四个字段
- email_hosts配置了发送邮件服务器
- email_senders配置了发送邮件的邮箱
- email_receivers配置了邮件接收者
- name_email_map为可选字段，email_receivers会根据name_email_map来获取对应人员的邮箱

###使用样例
```
emailController = EmailController() #实例化一个EmailController
confFile = os.path.abspath(os.path.join(__file__, "../etc/email.json"))
result = emailController.initWithConfigFile(confFile) #使用配置文件初始化
ret = emailController.sendEmailWithTag("test", "测试邮件", "这是一份测试邮件")
```