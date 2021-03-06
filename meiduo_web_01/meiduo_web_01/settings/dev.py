"""
Django settings for meiduo_web_01 project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# 根路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # cd ../../dev
print('settings中dev根路由是:BASE_DIR----->%s' % BASE_DIR)  # BASE_DIR 为里面的 meiduo_web_01

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# django默认生成的秘钥，项目中有些功能需要签名计算，可以直接使用，不用自己创建
SECRET_KEY = '-!jlj-jy96xzzvcoe6q2v5gio)xgd!=#grssdzu=o2o!b$@hur'

# 默认开启调试，打印两次的原因 上线改为false
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = [] 增加可以访问后端的域名
ALLOWED_HOSTS = ['api.meiduo.site',
                 'www.meiduo.site',
                 '127.0.0.1',
                 'localhost', ]


# 补充白名单 跨越白名单 域名 凡是出现在白名单中的域名，都可以访问后端接口
CORS_ORIGIN_WHITELIST = ['api.meiduo.site:8000',
                         'www.meiduo.site:8080',
                         '127.0.0.1:8080',
                         'localhost:8080', ]
# 跨越请求允许携带cookie， CORS_ALLOW_CREDENTIALS 指明在跨域访问中，后端是否支持对cookie的操作
CORS_ALLOW_CREDENTIALS = True

# 添加导包路径
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
for i in sys.path:
    print('导包路径有：------>%s' % i)
# print(sys.path)


# 注册安装的应用，自己创建的子应用，第三方扩展的应用
# Application definition
INSTALLED_APPS = [
    # 1 系统自带
    'django.contrib.admin',
    'django.contrib.auth',  # 用户认证系统
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 2 扩展应用
    'rest_framework',  # DRF
    'corsheaders',  # 解决js跨域请求的插件
    'ckeditor',  # 富文本编辑器
    'ckeditor_uploader',  # 富文本编辑器上传图片模块

    # 3 自己创建的应用
    # 为了还能像如下方式简便的注册引用，我们需要向Python解释器的导包路径中添加apps应用目录的路径
    'users.apps.UsersConfig',
    # 如果创建一个应用，比如users，那么在配置文件的INSTALLED_APPS中注册应用应该如下：
    # 'meiduo_web_01.apps.users.apps.UsersConfig',

    'oauth.apps.OauthConfig',  # 第三方登录
    'areas.apps.AreasConfig',  # 省市区三级联动
    'goods.apps.GoodsConfig',  # 商品
    'contents.apps.ContentsConfig',  # 主页广告
]

# 中间件，请求自上而下，返回自下而上。
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # 最外层的请求解决跨域问题
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 路由配置，路由的入口
ROOT_URLCONF = 'meiduo_web_01.urls'

# 模版文件配置项
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 将来部署上线后，程序的wsgi协议的入口
WSGI_APPLICATION = 'meiduo_web_01.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
# 连接数据库的选项
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',  # 数据库主机
        'PORT': 3306,  # 数据库端口
        'USER': 'meiduo',  # 数据库用户名
        'PASSWORD': 'meiduo',  # 数据库用户密码
        'NAME': 'meiduo_web'  # 数据库名字
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

# 验证密码的规则
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
# LANGUAGE_CODE = 'en-us' #默认语言
LANGUAGE_CODE = 'zh-hans'
# TIME_ZONE = 'UTC' # 时间 时区
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# 配置静态文件的路由前缀 相当于flask的static_url_path = None
STATIC_URL = '/static/'# 访问静态文件的URL前缀
# 当DEBUG=False工作在生产模式时，Django不再对外提供静态文件，
# 需要是用collectstatic命令来收集静态文件并交由其他静态文件服务器来提供。
# 将静态文件存放在一个静态的服务器nginx
# STATICFILES_DIRS = [ # 存放查找静态文件的目录，可以多个地方存放
#     os.path.join(BASE_DIR, 'static_files')
# ]

# 安装django-redis，配置， caches：<电脑>快速缓冲贮存区
CACHES = {
    "default": {  # 缓存地址三级联动
        "BACKEND": "django_redis.cache.RedisCache",  # backend 后端; 后台; 后段; 编译器后端;
        "LOCATION": "redis://127.0.0.1:6379/0",  # 位置：redis://ip:port/0号数据库
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",  # 客户端_类
        }
    },
    "session": {  # 修改了Django的Session机制使用redis保存，且使用名为'session'的redis配置。此处修改Django的Session机制存储主要是为了给Admin站点使用
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "verify_codes": {  # 存储 图片验证码， 短信验证码
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/2',
        'OPTION': {
            "CLIENT_CLASS": 'django_redis.client.DefaultClient',
        }
    },
    # redis://127.0.0.1/14 redis14号库用来存放celery异步任务，发送短信任务
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"  # session 引擎
SESSION_CACHE_ALIAS = "session"  # alias:别名，化名;

# DRF扩展
REST_FRAMEWORK_EXTENSIONS = {
    # 缓存时间
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 60,
    # 缓存存储
    'DEFAULT_USE_CACHE': 'default',
}

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {  # 详细格式
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {  # 简单样式
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/meiduo.log"),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 一个日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}
# DRF所有配置
REST_FRAMEWORK = {
    # 异常处理 如果未声明，会采用默认的方式  'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler'
    'EXCEPTION_HANDLER': 'meiduo_web_01.utils.exceptions.exception_handler',
    # drf认证 jwt
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',# 默认认证
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}
JWT_AUTH = {  # 配置json web token的有效期，状态保持，不宜太久
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),  # 格林威治时间
    # 为JWT登录视图补充返回值 utils中
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils.jwt_response_payload_handler',
}
# 指定django是被指定用户身份验证的类 utils中
AUTHENTICATION_BACKENDS = [
    'users.utils.UsernameMobileAuthBackend',
]

# 配置文件中进行设置User模型类 指定User模型类为Django项目中的用户认证的系统中的模型类
# AUTH_USER_MODEL = 'users.User' AUTH_USER_MODEL 参数的设置以点.来分隔，表示应用名.模型类名。
# 注意：Django建议我们对于AUTH_USER_MODEL参数的设置一定要在第一次数据库迁移之前就设置好，否则后续使用可能出现未知错误。
AUTH_USER_MODEL = 'users.User'

# QQ登录参数 在配置文件中添加关于QQ登录的应用开发信息
QQ_CLIENT_ID = '101474184'
QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'
QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'
QQ_STATE = '/'

# 配置邮箱服务器 Django send_mall()
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 导入邮件模块
EMAIL_HOST = 'smtp.163.com'  # 发邮件主机
EMAIL_PORT = 25  # 全世界默认邮件端口
EMAIL_HOST_USER = 'zhfeilong2008@163.com' # 授权的邮箱 #发送邮件的邮箱
# 在邮箱中设置的客户端授权密码 非注册登录密码
EMAIL_HOST_PASSWORD = 'woaini2017'
# 收件人看到的发件人
EMAIL_FROM = '行丰银拓办公商城<zhfeilong2008@163.com>'

# fastDFS 配置
FDFS_BASE_URL = 'http://192.168.243.132.:8888/'
# FDFS_BASE_URL = 'http://127.0.0.1.:8888/'
FDFS_CLIENT_CONF = os.path.join(BASE_DIR, 'utils/fastdfs/client.conf')
# 修改django文件默认存储
DEFAULT_FILE_STORAGE = 'meiduo_web_01.utils.fastdfs.fdfs_storage.FastDFSStorage'
# 富文本编辑器ckeditor配置
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',  # 工具条功能
        'height': 300,  # 编辑器高度
        # 'width': 300,  # 编辑器宽
    },
}
CKEDITOR_UPLOAD_PATH = ''  # 上传图片保存路径，使用了FastDFS，所以此处设为''
