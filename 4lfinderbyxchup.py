"""
instagram-4letter-username-finder

This project is dedicated to the public domain under the Creative Commons Zero (CC0) 1.0 Universal License.
Full license text: https://creativecommons.org/publicdomain/zero/1.0/legalcode
"""

# Banner
print("\033[1;33;40m  ~ Pяσɢяαммεя • ʙʀʏᴛ • -> ᴛɢ @xchup | Cнαиияℓ :  @bryyyyyt ~")
print("\x1b[1;39m", "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _  ")
print()

# ASCII logo
from pyfiglet import Figlet
V = '\033[1;36;40m'
fig = Figlet(font='poison')
logo = fig.renderText('BRYT')
print(V + logo)

# Open Telegram channel
import webbrowser
webbrowser.open("https://t.me/xchup")

# Imports
import os
import asyncio
import random
from uuid import uuid4

try:
    import string
    import aiohttp
except ModuleNotFoundError:
    os.system('pip install aiohttp')

# Colors
green_console = "\033[92m"
red_console = "\033[91m"
yellow_console = "\033[93m"

# Telegram Bot Setup
token = input('\033[1;32mTELEGRAM TOKEN : ')
telegram_user_id = input('\033[1;31mTELEGRAM ID : ')

# Username generator (4-letter usernames)
async def generate_username():
    characters = string.ascii_lowercase + string.digits
    separator = random.choice(['.', '_', ''])  # include empty string for no separator

    if separator:  # if a separator is chosen
        base = ''.join(random.choice(characters) for _ in range(3))  # 3 characters
        index = random.randint(1, 2)  # separator between 1 and 2
        username = base[:index] + separator + base[index:]  # add separator
    else:
        username = ''.join(random.choice(characters) for _ in range(4))  # 4 characters without separator

    return username

# Instagram checker
async def create_instagram_account(session):
    while True:
        username = await generate_username()
        headers = {
            "Host": "i.instagram.com",
            "cookie": "mid=Y16iBgABAAFggfUYwajggkGFz-hs",
            "x-ig-capabilities": "AQ==",
            "cookie2": "$Version=1",
            "x-ig-connection-type": "WIFI",
            "user-agent": "Instagram 6.12.1 Android (30/11; 480dpi; 1080x2298; HONOR; ANY-LX2; HNANY-Q1; qcom; en_IQ)",
            "content-type": "application/x-www-form-urlencoded",
            "accept-encoding": "gzip"
        }
        data = {
            "password": "zxcvbm1@",
            "device_id": f"android-{uuid4()}",
            "guid": str(uuid4()),
            "email": f"{username}@gmail.com",
            "username": username
        }

        async with session.post("https://i.instagram.com/api/v1/accounts/create/", headers=headers, data=data) as response:
            json_response = await response.json()
            error_type = json_response.get('error_type')

            if error_type == 'needs_upgrade':
                print(f'{green_console}GooD UserName : {username}   BY @xchup')
                await send_telegram_message(username)
            elif error_type == 'taken':
                print(f'{red_console}BaD UserName : {username}')
            else:
                print(f'{yellow_console}{error_type} : {username}')

# Send to Telegram
async def send_telegram_message(username):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        params = {"chat_id": telegram_user_id, "text": username}
        await session.get(url, params=params)

# Main loop
async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [create_instagram_account(session) for _ in range(10)]  # Modify loop range if needed
        await asyncio.gather(*tasks)

asyncio.run(main())
