import requests, random, string, json, threading, time
from colorama import Fore, init
init(convert=True)
class stats():
    Valid = 1
    Invalid = 1          
with open("config.json") as config:
    data = json.load(config)
    thrd = data['threading']
    prox = data['proxies']
    lng = data['number']
config.close()

def check():
    try:
        
        name = ''.join(random.choices(string.ascii_letters + string.digits , k=lng))
        cookies = {
            'PHPSESSID': 'phpsessid',
        }
        
        headers = {
            'authority'        : 'www.chess.com',
            'accept'           : 'application/json, text/plain, */*',
            'accept-language'  : 'es-ES,es;q=0.9',
            'referer'          : 'https://www.chess.com/register',
            'user-agent'       : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        }

        params = {
            'username': name,
        }
        
        if prox == True:
            proxy = random.choice(open('proxies.txt', 'r').read().splitlines())
            response = requests.get('https://www.chess.com/callback/user/valid', params=params, headers=headers, proxies={'http': f'http://{proxy}', 'https': f'http://{proxy}'})
        else:
            response = requests.get('https://www.chess.com/callback/user/valid', params=params, headers=headers)
            
        if "Username is valid" in response.text:
            print(f"{Fore.BLUE}[ {Fore.GREEN}+ {Fore.BLUE}]{Fore.RESET} ({stats.Valid}) Valid | Name: {name}")
            with open("valids.txt", "a+") as f:
                f.write(f"{name}\n")
            stats.Valid += 1
            
        elif "That username is taken." in response.text:
            print(f"{Fore.BLUE}[ {Fore.RED}x {Fore.BLUE}]{Fore.RESET} ({stats.Invalid}) Taken | Name: {name}")
            stats.Invalid += 1
            
        else:
            print(f"{Fore.BLUE}[ {Fore.RED}x {Fore.BLUE}]{Fore.RESET} Unknown Error")
            
    except Exception as e:
        print(f"{Fore.BLUE}[ {Fore.RED}x {Fore.BLUE}]{Fore.RESET}Error: {e}")
        
response = requests.get('https://www.chess.com/login_and_go?returnUrl=https://www.chess.com/')
phpsessid = response.cookies.get('PHPSESSID')
print(f"{Fore.BLUE}[ {Fore.YELLOW}! {Fore.BLUE}]{Fore.RESET} PHPSESSID generated: {phpsessid}\n") 
       
threads = int(input(f"{Fore.BLUE}[ {Fore.YELLOW}> {Fore.BLUE}]{Fore.RESET} Threads > "))
time.sleep(1)
if thrd == True:
    for i in range(threads):
        threading.Thread(target=check).start()
else:
    for i in range(threads):
        check()
