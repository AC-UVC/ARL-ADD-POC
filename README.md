# ARL-ADD-POC

本仓库是一个用于 [ARL（资产侦察灯塔系统）](https://github.com/TophantTechnology/ARL) 的自定义 POC（概念验证）脚本集合，旨在帮助安全研究人员快速扩展 ARL 的漏洞检测能力。

## 📋 项目简介

ARL 默认的 POC 库主要覆盖常见 CVE 漏洞，但在实际渗透测试和攻防演练中，经常会遇到需要自定义检测逻辑的场景。本仓库收集了针对各类应用、框架和中间件的自定义 POC 脚本，可直接集成到 ARL 中使用。

### 特点

- 🔌 **即插即用**：所有 POC 均遵循 ARL 插件规范，复制到对应目录即可生效。
- 🆕 **持续更新**：追踪最新的安全公告和漏洞披露，及时添加新的 POC。
- 📁 **分类清晰**：按应用/框架分类，方便查找和管理。
- 🧪 **可本地调试**：支持使用 ARL-NPoC 框架在本地快速测试 POC 有效性。

## 🔗 上游依赖

本仓库的 POC 基于 [Aabyss-Team/ARL-NPoC](https://github.com/Aabyss-Team/ARL-NPoC) 框架开发，该仓库是原 `1c3z/ARL-NPoC` 的备份项目，提供了完整的 POC 开发环境和插件加载机制[reference:0]。

如需本地调试 POC，请先安装 ARL-NPoC：

```bash
git clone https://github.com/Aabyss-Team/ARL-NPoC.git
cd ARL-NPoC
pip3 install -r requirements.txt
pip3 install -e .
