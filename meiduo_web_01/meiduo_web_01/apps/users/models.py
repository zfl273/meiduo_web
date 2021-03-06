from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData
from django.conf import settings

from meiduo_web_01.utils.models import BaseModel
from . import constants


# Django认证系统中提供了用户模型类User保存用户的数据，默认的User包含以下常见的基本字段：
# 必选:username  password
# 可选:first_name ,last_name ,email
# groups           与Group 之间的多对多关系
# user_permissions 与Permission 之间的多对多关系
# is_staff 布尔值。 指示用户是否可以访问Admin 站点。
# is_active 布尔值。 指示用户的账号是否激活。 我们建议您将此标志设置为False而不是删除帐户；这样，如果您的应用程序对用户有任何外键，则外键不会中断。它不是用来控制用户是否能够登录。
# is_superuser 布尔值。 指定这个用户拥有所有的权限而不需要给他们分配明确的权xian
# Django提供了django.contrib.auth.models.AbstractUser用户抽象模型类允许我们继承，扩展字段来使用Django认证系统的用户模型类
# last_login 用户最后一次登录的时间。
# date_joined 账户创建的时间。 当账号创建时，默认设置为当前的date/time。

# set_password(raw_password) 设置用户的密码为给定的原始字符串，并负责密码的。 不会保存User 对象。当None 为raw_password 时，密码将设置为一个不可用的密码
# check_password(raw_password) 如果给定的raw_password是用户的真实密码，则返回True，可以在校验用户密码时使用。
class User(AbstractUser):  # 我们自定义的用户模型类还不能直接被Django的认证系统所识别，需要在配置文件中告知Django认证系统使用我们自定义的模型类。
    '''用户模型类User
    '''
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    # 在用户列表里添加一个字段用来记录邮箱是否已经验证
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')
    # 为User模型类添加默认地址
    default_address = models.ForeignKey('Address', related_name='users', null=True, blank=True,
                                        on_delete=models.SET_NULL, verbose_name='默认地址')
    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name  # 复数形式为 用户

    def generate_verify_email_url(self):
        '''生成激活码'''
        # 激活连接的有效期
        serializer = Serializer(settings.SECRET_KEY, expires_in=constants.VERIFY_EMAIL_TOKEN_EXPIRES)
        data = {'user_id': self.id, 'email': self.email}
        token = serializer.dumps(data).decode()
        verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token=' + token
        return verify_url
        # 在User模型类中定义验证token的方法

    @staticmethod
    def check_verify_email_token(token):
        '''
        解码token,读取出user_id, 查询出当前要认证的用户
        :return: user
        '''
        serializer = Serializer(settings.SECRET_KEY, expires_in=constants.VERIFY_EMAIL_TOKEN_EXPIRES)
        try:
            # data == {'user_id':self.id, 'email':self.email}
            data = serializer.loads(token)
        except BadData:
            return None
        else:
            user_id = data.get('user_id')
            email = data.get('email')
            try:
                user = User.objects.get(id=user_id, email=email)
            except User.DoesNotExist:
                return None
            else:
                return user


class Address(BaseModel):
    """
    用户地址
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    title = models.CharField(max_length=20, verbose_name='地址名称')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    province = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='province_addresses',
                                 verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city_addresses', verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='district_addresses',
                                 verbose_name='区')
    place = models.CharField(max_length=50, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    tel = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='固定电话')
    email = models.CharField(max_length=30, null=True, blank=True, default='', verbose_name='电子邮箱')
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']
