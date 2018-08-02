from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from fdfs_client.client import Fdfs_client


class FastDFSStorage(Storage):
    '''自定义文件存储方案，转存到fdfs'''

    def __init__(self, client_conf=None, base_url=None):
        """
        初始化
        :param base_url: 用于构造图片完整路径使用，图片服务器的域名
        :param client_conf: FastDFS客户端配置文件的路径
        """
        self.client_conf = client_conf or settings.FDFS_CLIENT_CONF
        self.base_url = base_url or settings.FDFS_BASE_URL

    def exists(self, name):
        """
        如果文件已经存在,就返回True,那么该文件不再存储，save()方法不再被调用了
        :param name: 判断是否存在的文件的名字
        :return: False；告诉Django,要保存的name对应的文件不存在，就会调用save()
        """
        return False

    def _open(self, name, mode='rb'):
        """
        用不到打开文件，所以省略
        """
        pass

    def _save(self, name, content):
        """
        在FastDFS中保存文件
        :param name: 传入的文件名
        :param content: 文件内容
        :return: 保存到数据库中的FastDFS的文件名
        """
        # 创建client对象
        client = Fdfs_client(self.client_conf)
        # 调用上传方法
        ret = client.upload_by_buffer(content.read())
        if ret.get("Status") != "Upload successed.":
            raise Exception("上传文件失败upload file failed")
        file_id = ret.get("Remote file_id")
        return file_id

    def url(self, name):
        """
        返回文件的完整URL路径
        :param name: 数据库中保存的文件名
        :return: 完整的URL
        """
        return self.base_url + name
