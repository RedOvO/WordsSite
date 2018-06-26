# WordsSite
# WordsSite
2018 B/S软件体系设计课程作业

1	实验目的

任选一种技术实现一个背单词的网站

2	实验要求

需要实现的基本功能如下：

a	实现用户注册、登录功能，用户注册时需要填写必要的信息并验证，如用户名、密码要求在6字节以上，email的格式验证，并保证用户名和email在系统中唯一。

b	用户登录后可以设置需要背的单词集，如4级、6级等。单词集可以从网上收集，数量多少不影响评分。

c 用户可以维护自己的自定义单词

d 实现基本的背诵计划、复习、考核等功能，记录进度。

e	界面样式需要适配PC和手机的浏览器

增强功能：

f	实现一个Android或iphone客户端软件，功能同网站，支持离线使用，并能实现背诵计划的通知提醒

g	具体一定的学习能力，能根据记忆曲线或用户的使用习惯调整背诵的内容，此项功能在界面上表现不明显时，可以在文档中详细说明

最终完成只实现了基本功能，采用了 react + ajax + django + mysql的架构

运行方法：

pip install django

在setting.py中绑定到自己的mysql

python manage.py makemigrations

python manage.py migrate

python manage.py runserver localhost:port


