Telegram Profile Changer (TG批量改名工具)
一个基于 Python 开发的 Telegram 账号资料批量修改工具，支持批量更改用户名和显示名称。

🚀 功能特点

批量处理多个 Telegram 账号
随机生成用户名
随机组合中文姓名
内置延迟保护机制
简单的命令行操作界面

📋 环境要求
Python 3.7+
稳定的网络连接
Telegram API 凭据

🔧 安装步骤

克隆项目：

git clone 
cd telegram-profile-changer

安装依赖：

pip install -r requirements.txt

创建 session 目录：

放入.session文件

选择操作：
- 1️⃣ 修改用户名
- 2️⃣ 修改显示名称
- 3️⃣ 退出程序

## ⚙️ 配置说明

1. 获取 Telegram API 凭据配置api：
   - 访问 [Telegram API Development Tools](https://my.telegram.org/apps)
   - 登录您的 Telegram 账号
   - 创建新应用获取 `api_id` 和 `api_hash`

2. 准备数据文件：
   - 创建 `names.txt` 文件存放姓名组合
   - 创建 `usernames.txt` 文件存放用户名列表
   - 将 .session 文件放入 session 文件夹

3. 文件格式示例：

`names.txt`:
text
小明 王
小红 李
小华 张

`usernames.txt`:
text
user1234
tg5678
cool9012

运行程序：

python telegram_profile_changer.py

## ⚖️ 免责声明

本工具仅供学习和研究使用，使用者需：
- 遵守当地法律法规
- 遵守 Telegram 服务条款
- 对使用后果自行负责

禁止用于任何非法用途。