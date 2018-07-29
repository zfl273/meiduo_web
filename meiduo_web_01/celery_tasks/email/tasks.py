#  定义异步任务的文件，必须为tasks
from django.core.mail import send_mail
from django.conf import settings

from celery_tasks.main import celery_app


@celery_app.task(name='send_verify_email')
def send_verify_email(to_email, verify_url):
    """
        发送验证邮箱邮件
        :param to_email: 收件人邮箱
        :param verify_url: 验证链接
        :return: None
    """
    # 在django.core.mail模块提供了send_mail来发送邮件。
    # send_mail(subject, message, from_email, recipient_list, html_message=None)
    #
    # subject  邮件标题
    # message  普通邮件正文， 普通字符串
    # from_email  发件人
    # recipient_list  收件人列表
    # html_message  多媒体邮件正文，可以是html字符串

    # 发送邮件
    subject = '飞龙商城邮箱验证'
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用飞龙商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)
    send_mail(subject=subject,
              message='',
              from_email=settings.EMAIL_FROM,
              recipient_list=[to_email],
              html_message=html_message)
