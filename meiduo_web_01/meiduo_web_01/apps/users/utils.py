
def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }

from django.contrib.auth.backends import ModelBackend
import re
from .models import User

def get_user_by_account(account):
    '''
    根据账户获取user对象
    :param account: 账号，可以是用户名，也可以是手机号
    :return: User对象或者None
    '''
    try:
        if re.match(r'^1[3-9]\d{9}', account):
            # 账号为手机号
            user = User.objects.get(mobile=account)
        else:
            # 账号为用户名
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    '''自定义用户认证方式'''
    def authenticate(self, request, username=None, password=None, **kwargs):
        '''
        重写用户认证的方法
        :param request: 本次登录请求对象
        :param username: 本次登录请求用户名
        :param password: 本次登录请求明文密码
        :param kwargs: 其他参数
        :return:如果用户是用户返回user对象
        '''
        # 查询user对象
        user = get_user_by_account(username)
        # 校验user是否存在，密码正确
        if user is not None and user.check_password(password):
            return user