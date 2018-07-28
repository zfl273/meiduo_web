import pymysql

pymysql.install_as_MySQLdb()  # 解决python3 python2 都只认识mysqldb 不认识pymysql的问题

# apps 存放Django的应用
# libs 存放第三方的库文件
# settings 存放配置文件的目录，分为开发dev和线上prod
# utils 存放项目自己定义的公共函数或类等
# docs 用于存放一些说明文档资料
# scripts 用于存放管理脚本文件