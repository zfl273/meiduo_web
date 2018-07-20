# celery 运行入口启动


from celery import Celery
# 创建实例 指定别名
celery_app = Celery('meiduo_04')

# 加载配置
celery_app.config_from_object('celery_tasks.config')

#将异步任务添加到celery_app
celery_app.autodiscover_tasks(['celery_tasks.sms'])