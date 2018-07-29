# celery 运行入口，启动celery
import os

from celery import Celery

# 在发送邮件的异步任务中，需要用到django的配置文件，
# 所以我们需要修改celery的启动文件main.py，在其中指明celery可以读取的django配置文件，
# 并且注册添加email的任务
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_web_01.settings.dev'


# 创建celery实例 指定别名，别名没有实际意义
celery_app = Celery('meiduo_04')

# 加载配置 配置了broker_url,让celery_app知道任务队列在哪里
celery_app.config_from_object('celery_tasks.config')

# 自动的将异步任务添加到celery_app，可以添加多个任务
# 1 发短信验证码 2 email验证码
celery_app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.email'])
