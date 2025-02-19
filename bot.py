import os
import time
import sys
import re
import json
import urllib.request
import urllib.parse
from urllib.parse import unquote
from colorama import Fore, Style
from onlylog import Log
from tqdm import tqdm
import concurrent.futures
import datetime
import random

tix = 0
proxies = []

def load_proxies():
    """Load proxies from proxy.txt file if it exists"""
    global proxies
    try:
        if os.path.exists('proxy.txt'):
            with open('proxy.txt', 'r') as file:
                proxy_list = file.read().splitlines()
                # Filter out empty lines and comments
                proxies = [p.strip() for p in proxy_list if p.strip() and not p.strip().startswith('#')]
                
                if proxies:
                    log_with_timestamp(f"Loaded {len(proxies)} proxies from proxy.txt", "SUCCESS")
                    # Validate proxy format
                    valid_proxies = []
                    for proxy in proxies:
                        if re.match(r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})$', proxy):
                            valid_proxies.append(proxy)
                        else:
                            log_with_timestamp(f"Invalid proxy format: {proxy}, expected format: ip:port", "WARN")
                    
                    proxies = valid_proxies
                    log_with_timestamp(f"{len(proxies)} valid proxies will be used", "INFO")
                    return True
                else:
                    log_with_timestamp("proxy.txt found but contains no valid proxies", "WARN")
                    return False
        else:
            log_with_timestamp("No proxy.txt file found, continuing without proxies", "INFO")
            return False
    except Exception as e:
        log_with_timestamp(f"Error loading proxies: {str(e)}", "ERROR")
        return False

def get_proxy_handler():
    """Get a proxy handler with a random proxy from the list"""
    if not proxies:
        return None
    
    proxy = random.choice(proxies)
    log_with_timestamp(f"Using proxy: {proxy}", "INFO")
    return urllib.request.ProxyHandler({
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    })

def create_opener():
    """Create URL opener with proxy if available"""
    proxy_handler = get_proxy_handler()
    if proxy_handler:
        opener = urllib.request.build_opener(proxy_handler)
        return opener
    return None

def banner():
    os.system("title MIDAS BOT" if os.name == "nt" else "clear")
    os.system("cls" if os.name == "nt" else "clear")
    print('')
    print(Fore.CYAN + "╔══════════════════════════════════════════════╗")
    print(Fore.CYAN + "║      🚀 MIDAS BOT - Auto Task Completion     ║")
    print(Fore.CYAN + "║    Automate your MidasRWA account tasks!     ║")
    print(Fore.CYAN + "║  Developed by: Your Team / Telegram Group    ║")
    print(Fore.CYAN + "╚══════════════════════════════════════════════╝" + Fore.RESET)
    print(Fore.CYAN + '[#] Enhanced with Progress Bar & Proxy Support' + Fore.RESET)
    print('')

def log_with_timestamp(message, type="INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if type == "SUCCESS":
        Log.success(f"[{timestamp}] {message}")
    elif type == "ERROR":
        Log.error(f"[{timestamp}] {message}")
    elif type == "WARN":
        Log.warn(f"[{timestamp}] {message}")
    else:
        print(f"[{timestamp}] {Fore.CYAN}[INFO]{Fore.RESET} {message}")

def runforeva():
    # Load proxies at startup
    load_proxies()
    
    while True:
        try:
            with open('data.txt', 'r') as file:
                queryh = file.read().splitlines()
            
            log_with_timestamp(f"Found {len(queryh)} accounts in data.txt", "INFO")
            
            while True:
                log_with_timestamp("Starting new processing cycle", "INFO")
                with tqdm(total=len(queryh), desc="Processing Accounts", 
                          bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.GREEN, Fore.RESET)) as pbar:
                    for index, query_id in enumerate(queryh, start=1):
                        try:
                            pbar.set_description(f"Processing Account [{index}/{len(queryh)}]")
                            getname(query_id)
                            token = gettoken(query_id)
                            if token:
                                postrequest(token)
                            pbar.update(1)
                        except Exception as e:
                            log_with_timestamp(f"Error processing account #{index}: {str(e)}", "ERROR")
                            continue
                
                # Sleep between cycles
                for i in tqdm(range(300), desc="Waiting for next cycle", 
                              bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.BLUE, Fore.RESET)):
                    time.sleep(1)
        
        except Exception as e:
            log_with_timestamp(f"Critical error in main loop: {str(e)}", "ERROR")
            time.sleep(10)
            log_with_timestamp("Restarting main process...", "WARN")

def gettoken(querybro):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
            }
    try:
        url = "https://api-tg-app.midas.app/api/auth/register"
        redrop = json.dumps({"initData":querybro}).encode('utf-8')
        
        req = urllib.request.Request(url, redrop, header, method='POST')
        
        # Use proxy if available
        opener = create_opener()
        if opener:
            response = opener.open(req)
        else:
            response = urllib.request.urlopen(req)
            
        if response.getcode() != 201:
            log_with_timestamp('Authentication failed - check your query_id/user_id (maybe expired)', "ERROR")
            return None
        elif response.getcode() == 500:
            log_with_timestamp('Server error - close all Midas mini-app!', "ERROR")
            time.sleep(30)
            return None
        else:
            log_with_timestamp('Login successful', "SUCCESS")
            cihuy = response.read().decode('utf-8')
            return cihuy
    except Exception as e:
        log_with_timestamp(f'Authentication error: {str(e)}', "ERROR")
        return None

def getuser(querybro):
    bear = 'Bearer '+querybro
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Authorization': bear
            }
    
    global tix

    try:
        url = "https://api-tg-app.midas.app/api/user"
        urlvisit = "https://api-tg-app.midas.app/api/user/visited"
        
        # Use proxy if available
        opener = create_opener()
        if opener:
            req = urllib.request.Request(url, None, header, method='GET')
            response = opener.open(req).read()
            
            reqv = urllib.request.Request(urlvisit, None, header, method='PATCH')
            opener.open(reqv)
        else:
            req = urllib.request.Request(url, None, header, method='GET')
            response = urllib.request.urlopen(req).read()
            
            reqv = urllib.request.Request(urlvisit, None, header, method='PATCH')
            urllib.request.urlopen(reqv)
            
        result = json.loads(response.decode('utf-8'))
        jData = result
        jsonpoints = jData['points']
        jsonsd = jData['streakDaysCount']
        jsontix = jData['tickets']
        
        # Enhanced formatted output
        print(f"\n{Fore.CYAN}══════ ACCOUNT STATUS ══════{Fore.RESET}")
        print(f"{Fore.WHITE}GM Points      : {Fore.YELLOW}{jsonpoints}{Fore.RESET}")
        print(f"{Fore.WHITE}Check-in Days  : {Fore.YELLOW}{jsonsd}{Fore.RESET}")
        print(f"{Fore.WHITE}Tickets        : {Fore.YELLOW}{jsontix}{Fore.RESET}")
        print(f"{Fore.CYAN}═════════════════════════{Fore.RESET}\n")
        
        tix = jsontix
        
        return True
    except Exception as e:
        log_with_timestamp(f'Failed to get user information: {str(e)}', "ERROR")
        return False

def getcheckin(querybro):
    bear = 'Bearer '+querybro
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Authorization': bear
        }
        
    url = "https://api-tg-app.midas.app/api/streak"
    
    try:
        # Use proxy if available
        opener = create_opener()
        if opener:
            req = urllib.request.Request(url, None, header, method='GET')
            response = opener.open(req).read()
        else:
            req = urllib.request.Request(url, None, header, method='GET')
            response = urllib.request.urlopen(req).read()
            
        result = json.loads(response.decode('utf-8'))
        jData = result
        jsonclaimable = jData['claimable']
        
        if jsonclaimable:
            try:
                with tqdm(total=1, desc="Claiming daily check-in", 
                          bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.MAGENTA, Fore.RESET)) as pbar:
                    req = urllib.request.Request(url, None, header, method='POST')
                    
                    if opener:
                        opener.open(req)
                    else:
                        urllib.request.urlopen(req)
                        
                    time.sleep(1)  # For visual effect
                    pbar.update(1)
                log_with_timestamp('Daily check-in successful! ✓', "SUCCESS")
                return True
            except Exception as e:
                log_with_timestamp(f'Failed to claim check-in: {str(e)}', "ERROR")
                return False
        else:
            log_with_timestamp('No check-in available today', "WARN")
            return True
    except Exception as e:
        log_with_timestamp(f'Check-in status check failed: {str(e)}', "ERROR")
        return False

def getname(querybro):
    try:
        found = re.search('user=([^&]*)', querybro).group(1)
        decodedUserPart = unquote(found)
        userObj = json.loads(decodedUserPart)
        username = userObj.get('username', 'Unknown')
        log_with_timestamp(f'Processing account: @{username}', "SUCCESS")
        print(f"{Fore.GREEN}{'='*40}{Fore.RESET}")
        print(f"{Fore.CYAN}▶ Now processing: {Fore.WHITE}@{username}{Fore.RESET}")
        print(f"{Fore.GREEN}{'='*40}{Fore.RESET}")
        return username
    except Exception as e:
        log_with_timestamp(f'Failed to decode username: {str(e)}', "ERROR")
        return "Unknown"

def playgame(tomket):
    bear = 'Bearer '+tomket
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Authorization': bear
    }

    n = tix
    total_rewards = 0
    opener = create_opener()

    if n > 0:
        with tqdm(total=n, desc="Playing Games", 
                  bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.YELLOW, Fore.RESET)) as pbar:
            for i in range(n):
                try:
                    url = "https://api-tg-app.midas.app/api/game/play"
                    req = urllib.request.Request(url, None, header, method='POST')
                    
                    if opener:
                        response = opener.open(req).read()
                    else:
                        response = urllib.request.urlopen(req).read()
                        
                    result = json.loads(response.decode('utf-8'))
                    jData = result
                    try:
                        jsonreward = jData.get('points', 0)
                        total_rewards += jsonreward
                        pbar.set_postfix(last_reward=jsonreward, total=total_rewards)
                        pbar.update(1)
                        time.sleep(3)  # Shorter wait between games
                    except:
                        pbar.update(1)
                except Exception as e:
                    log_with_timestamp(f'Game #{i+1} failed: {str(e)}', "ERROR")
                    pbar.update(1)
                    time.sleep(2)

        if total_rewards > 0:
            log_with_timestamp(f'Games completed! Total rewards: {total_rewards} points', "SUCCESS")
        return True
    return True

def gettask(tomket):
    bear = 'Bearer '+tomket
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': bear
        }
    
    opener = create_opener()

    try:
        log_with_timestamp("Checking available tasks...", "INFO")
        urltasks = "https://api-tg-app.midas.app/api/tasks/available"
        req = urllib.request.Request(urltasks, None, header, method='GET')
        
        if opener:
            response = opener.open(req).read()
        else:
            response = urllib.request.urlopen(req).read()
            
        result = json.loads(response.decode('utf-8'))
        jData = result
        
        waiting_tasks = [item for item in jData if item['state'] == 'WAITING']
        claimable_tasks = [item for item in jData if item['state'] == 'CLAIMABLE']
        
        if waiting_tasks:
            log_with_timestamp(f"Found {len(waiting_tasks)} tasks to start", "INFO")
            with tqdm(total=len(waiting_tasks), desc="Starting Tasks", 
                      bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.CYAN, Fore.RESET)) as pbar:
                for item in waiting_tasks:
                    try:
                        task_id = item['id']
                        task_name = item['name']
                        pbar.set_description(f"Starting Task: {task_name[:15]}...")
                        
                        urlstart = f'https://api-tg-app.midas.app/api/tasks/start/{task_id}'
                        req2 = urllib.request.Request(urlstart, None, header, method='POST')
                        
                        if opener:
                            opener.open(req2).read()
                        else:
                            urllib.request.urlopen(req2).read()
                            
                        time.sleep(0.5)
                        pbar.update(1)
                    except Exception as e:
                        log_with_timestamp(f"Failed to start task {item.get('name', 'unknown')}: {str(e)}", "ERROR")
                        pbar.update(1)
        
        if claimable_tasks:
            log_with_timestamp(f"Found {len(claimable_tasks)} tasks to claim", "INFO")
            total_claimed_points = 0
            
            with tqdm(total=len(claimable_tasks), desc="Claiming Task Rewards", 
                      bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.GREEN, Fore.RESET)) as pbar:
                for item in claimable_tasks:
                    try:
                        task_id = item['id']
                        task_name = item['name']
                        task_points = item['points']
                        
                        pbar.set_description(f"Claiming: {task_name[:15]}...")
                        
                        urlclaim = f'https://api-tg-app.midas.app/api/tasks/claim/{task_id}'
                        req3 = urllib.request.Request(urlclaim, None, header, method='POST')
                        
                        if opener:
                            responseclaim = opener.open(req3)
                        else:
                            responseclaim = urllib.request.urlopen(req3)
                        
                        if responseclaim.getcode() == 201:
                            total_claimed_points += task_points
                            pbar.set_postfix(points=f"+{task_points}", total=total_claimed_points)
                        
                        time.sleep(0.5)
                        pbar.update(1)
                    except Exception as e:
                        log_with_timestamp(f"Failed to claim task {item.get('name', 'unknown')}: {str(e)}", "ERROR")
                        pbar.update(1)
            
            if total_claimed_points > 0:
                log_with_timestamp(f"Successfully claimed {len(claimable_tasks)} tasks for total {total_claimed_points} GM Points", "SUCCESS")
        
        if not waiting_tasks and not claimable_tasks:
            log_with_timestamp("No tasks available to start or claim", "WARN")
        
        return True
    except Exception as e:
        log_with_timestamp(f'Task processing failed: {str(e)}', "ERROR")
        return False

def getreff(tomket):
    bear = 'Bearer '+tomket
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Authorization': bear
    }
    
    opener = create_opener()

    try:
        log_with_timestamp("Checking referral status...", "INFO")
        urlreff = "https://api-tg-app.midas.app/api/referral/status"
        urlclaimref = "https://api-tg-app.midas.app/api/referral/claim"
        req = urllib.request.Request(urlreff, None, header, method='GET')
        
        if opener:
            response = opener.open(req).read()
        else:
            response = urllib.request.urlopen(req).read()
            
        result = json.loads(response.decode('utf-8'))
        jData = result
        
        if jData['totalPoints'] > 0:
            jsoncanClaim = jData['canClaim']
            jsontotalPoints = jData['totalPoints']
            jsontotalTickets = jData['totalTickets']
            
            # Enhanced formatting
            print(f"\n{Fore.MAGENTA}════════ REFERRAL STATUS ════════{Fore.RESET}")
            print(f"{Fore.WHITE}Referral Points  : {Fore.YELLOW}{jsontotalPoints}{Fore.RESET}")
            print(f"{Fore.WHITE}Referral Tickets : {Fore.YELLOW}{jsontotalTickets}{Fore.RESET}")
            print(f"{Fore.WHITE}Can Claim        : {Fore.GREEN if jsoncanClaim else Fore.RED}{jsoncanClaim}{Fore.RESET}")
            print(f"{Fore.MAGENTA}═══════════════════════════════{Fore.RESET}\n")
            
            if jsoncanClaim:
                with tqdm(total=1, desc="Claiming Referral Rewards", 
                          bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.MAGENTA, Fore.RESET)) as pbar:
                    req = urllib.request.Request(urlclaimref, None, header, method='POST')
                    
                    if opener:
                        responseclaim = opener.open(req)
                    else:
                        responseclaim = urllib.request.urlopen(req)
                        
                    time.sleep(1)  # For visual effect
                    pbar.update(1)
                
                if responseclaim.getcode() =
