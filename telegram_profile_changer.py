from pyrogram import Client
import time
import random
import asyncio
import os
from typing import List

class TelegramProfileChanger:
    def __init__(self):
        # 配置信息
        self.api_id = "YOUR_API_ID"
        self.api_hash = "YOUR_API_HASH"
        
        # 名字库
        self.first_names = []
        self.last_names = []
        self.usernames = []
        self.session_dir = "sessions"
        self.names_file = "names.txt"
        self.usernames_file = "usernames.txt"
        
        # 从文件加载名字和用户名
        self.load_data()

    def load_data(self):
        """从文件加载名字和用户名数据"""
        try:
            # 加载名字
            if os.path.exists(self.names_file):
                with open(self.names_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        first, last = line.strip().split()
                        self.first_names.append(first)
                        self.last_names.append(last)
            
            # 加载用户名
            if os.path.exists(self.usernames_file):
                with open(self.usernames_file, 'r', encoding='utf-8') as f:
                    self.usernames = [line.strip() for line in f if line.strip()]
                    
        except Exception as e:
            print(f"加载数据文件时出错: {str(e)}")

    async def generate_random_username(self) -> str:
        """从用户名列表中随机选择一个"""
        if not self.usernames:
            return super().generate_random_username()
        return random.choice(self.usernames)

    async def get_session_files(self) -> List[str]:
        """获取session文件夹中的所有session文件"""
        session_files = []
        for file in os.listdir(self.session_dir):
            if file.endswith('.session'):
                session_files.append(os.path.splitext(file)[0])
        return session_files

    async def change_username(self, app: Client) -> None:
        """修改用户名，如果被占用则立即尝试新的用户名"""
        max_attempts = 5
        
        for _ in range(max_attempts):
            username = await self.generate_random_username()
            try:
                await app.set_username(username)
                print(f"成功更新用户名: {username}")
                return
            except Exception as e:
                if "USERNAME_OCCUPIED" in str(e):
                    continue  # 用户名被占用时立即尝试下一个
                else:
                    print(f"设置用户名失败: {str(e)}")
                    return
        
        print("已达到最大尝试次数，无法设置用户名")

    async def change_name(self, app: Client) -> None:
        """仅修改名字"""
        first_name = random.choice(self.first_names)
        last_name = random.choice(self.last_names)
        try:
            await app.update_profile(
                first_name=first_name,
                last_name=last_name
            )
            print(f"成功更新名字: {first_name} {last_name}")
        except Exception as e:
            print(f"设置名字失败: {str(e)}")

    async def process_accounts(self, change_type: str):
        """并发处理所有账户"""
        # 根据操作类型设置不同的延迟
        if change_type == "username":
            delay_min, delay_max = 10, 15  # 用户名修改用更长延迟
        else:
            delay_min, delay_max = 5, 8    # 名字修改用较短延迟
        
        async def process_single_account(session_name):
            try:
                async with Client(
                    name=session_name,
                    api_id=self.api_id,
                    api_hash=self.api_hash,
                    workdir=self.session_dir,
                    proxy=dict(
                        scheme="socks5",
                        hostname="YOUR_PROXY_IP",
                        port=1234,
                        username="YOUR_PROXY_USERNAME",
                        password="YOUR_PROXY_PASSWORD"
                    )
                ) as app:
                    print(f"\n处理账户: {session_name}")
                    
                    if change_type == "username":
                        await self.change_username(app)
                    elif change_type == "name":
                        await self.change_name(app)
                    
                    # 使用根据操作类型确定的延迟
                    await asyncio.sleep(random.uniform(delay_min, delay_max))
                    
            except Exception as e:
                if "FLOOD_WAIT" in str(e):
                    wait_time = int(str(e).split()[1])
                    print(f"账号 {session_name} 触发限制，需要等待 {wait_time} 秒")
                    await asyncio.sleep(wait_time)
                else:
                    print(f"处理账户 {session_name} 时出错: {str(e)}")

        # 并发执行所有账户的处理
        session_files = await self.get_session_files()
        tasks = [process_single_account(session) for session in session_files]
        await asyncio.gather(*tasks)

async def main():
    changer = TelegramProfileChanger()
    
    while True:
        print("\n请选择要执行的操作：")
        print("1. 修改用户名")
        print("2. 修改名字")
        print("3. 退出程序")
        
        choice = input("请输入选项（1/2/3）: ")
        
        if choice == "1":
            await changer.process_accounts("username")
        elif choice == "2":
            await changer.process_accounts("name")
        elif choice == "3":
            print("程序已退出")
            break
        else:
            print("无效的选择，请重新输入")

if __name__ == "__main__":
    asyncio.run(main()) 