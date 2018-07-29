# celery 运行入口，启动celery


from celery import Celery
# 创建celery实例 指定别名，别名没有实际意义
celery_app = Celery('meiduo_04')

# 加载配置 配置了broker_url,让celery_app知道任务队列在哪里
celery_app.config_from_object('celery_tasks.config')

# 自动的将异步任务添加到celery_app，可以添加多个任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])