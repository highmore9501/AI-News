## 项目说明

抓取各新闻网站里包含特定关键字的新闻链接，然后保存，以备后用

## 使用须知

需要安装 chromedriver
需要自建一个.env 文件，里面有：

- 腾讯云的 secretId 和 secretKey 的环境变量
- chormedriver 的路径以及调用的 chorme.exe 的路径
- 发送邮件的用户名和密码

具体写法可以参考.env.example 文件
