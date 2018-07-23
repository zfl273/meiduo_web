
from urllib.parse import urlencode, parse_qs
from django.conf import settings
from urllib.request import urlopen
import logging
logger = logging.getLogger('django')
import json

from .exceptions import QQAPIException

class OAuthQQ(object):
    '''工具类'''
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, state=None):
        '''构造'''
        # QQ_CLIENT_ID = '101474184'
        # QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'
        # QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'
        # QQ_STATE = '/'
        self.client_id = client_id or settings.QQ_CLIENT_ID
        self.client_secret = client_secret or settings.QQ_CLIENT_SECRET
        self.redirect_uri = redirect_uri or settings.QQ_REDIRECT_URI
        self.state = state or settings.QQ_STATE


    def get_login_url(self):
        # url = 'https://graph.qq.com/oauth2.0/authorize?'
        login_url = 'https://graph.qq.com/oauth2.0/authorize?'

        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'state': self.state,
            'scope': 'get_user_info'
        }

        query_params = urlencode(params)

        login_url += query_params

        return login_url

    def get_access_token(self, code):
        '''使用code获取access——token'''
        # url = https://graph.qq.com/oauth2.0/token?
        url = 'https://graph.qq.com/oauth2.0/token?'
        params = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'code': code,
        }

        url += urlencode(params)
        try:
            # 发送请求
            response_str = urlopen(url).read().decode()
            response_dict = parse_qs(response_str)# 将查询字符串转成字典

            access_token = response_dict.get('access_token')[0]
        except Exception as e:
            logger.error(e)
            raise QQAPIException('获取access_token异常')

        return access_token

    def get_open_id(self, access_token):
        '''使用access——token获取open_id'''
        url = 'https://graph.qq.com/oauth2.0/me?access_token=%s' % access_token
        # 请求
        response_str = ''
        try:
            response_data = urlopen(url).read()
            response_str = response_data.decode()

            response_dict = json.loads(response_str[10:-4])
            open_id = response_dict.get('oepnid')
        except Exception as e:
            err_data = parse_qs(response_str)
            logger.error(e)
            raise QQAPIException('code=%s msg=%s'%(err_data.get('code'), err_data.get('msg')))

        return open_id