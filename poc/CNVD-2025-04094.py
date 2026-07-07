from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req
from xing.core import PluginType, SchemeType


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "Ollama 未授权访问 (CNVD-2025-04094)"
        self.app_name = 'Ollama'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

    def verify(self, target):
        # 构造验证URL，访问 /api/tags 接口
        test_url = target.rstrip('/') + '/api/tags'

        try:
            resp = http_req(test_url, timeout=10)

            # 检测逻辑：
            # 1. 状态码必须为 200
            # 2. 响应内容包含 "models" 字段，这是 /api/tags 成功响应的特征
            if resp.status_code == 200:
                try:
                    json_data = resp.json()
                    if isinstance(json_data, dict) and 'models' in json_data:
                        self.logger.info("发现 Ollama 未授权访问漏洞 (CNVD-2025-04094)")
                        return test_url
                except:
                    pass
        except Exception:
            pass

        return None