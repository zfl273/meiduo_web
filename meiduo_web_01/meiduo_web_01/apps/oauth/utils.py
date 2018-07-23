
from urllib.parse import urlencode
from django.conf import settings

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


