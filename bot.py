import os
import time
import sys
import re
import json
import urllib.request
import urllib.parse
from urllib.parse import unquote
from colorama import Fore, Style, init
from tqdm import tqdm

# Inisialisasi colorama
init(autoreset=True)

tix = 0
proxies = []
proxy_index = 0

def show_banner():
    """Menampilkan banner baru seperti Haha Wallet"""
    os.system("cls" if os.name == "nt" else "clear")
    print(f"""{Fore.YELLOW}{Style.BRIGHT}
╔══════════════════════════════════════════════╗
║      🚀 MIDAS BOT - Auto Task Completion     ║
║    Automate your MidasRWA account tasks!     ║
║  Developed by: https://t.me/sentineldiscus   ║
╚══════════════════════════════════════════════╝{Style.RESET_ALL}
""")

def load_proxies():
    """Membaca file proxy.txt dan memuat daftar proxy"""
    global proxies
    if os.path.exists("proxy.txt"):
        with open("proxy.txt", "r") as file:
            proxies = [line.strip() for line in file if line.strip()]
    
    if proxies:
        print(f"{Fore.GREEN}Proxy mode aktif: {len(proxies)} proxy dimuat.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Proxy tidak digunakan. Berjalan tanpa proxy.{Style.RESET_ALL}")

def get_next_proxy():
    """Mengambil proxy berikutnya secara bergilir"""
    global proxy_index
    if not proxies:
        return None  # Jika proxy kosong, jalankan tanpa proxy

    proxy = proxies[proxy_index]
    proxy_index = (proxy_index + 1) % len(proxies)  # Rotasi proxy
    return proxy

def log_header(title):
    """Menampilkan header untuk setiap akun"""
    print(f"\n{Fore.BLUE}{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}{Style.RESET_ALL}")

def log_step(step, status="OK"):
    """Menampilkan langkah-langkah dengan format berbeda"""
    color = Fore.GREEN if status == "OK" else Fore.RED
    print(f"{color}  ➜ {step} [{status}]{Style.RESET_ALL}")

def log_info(label, value):
    """Menampilkan informasi akun dalam satu blok"""
    print(f"  {Fore.CYAN}{label}: {Fore.WHITE}{value}{Style.RESET_ALL}")

def runforeva():
    """Loop utama script dengan tampilan log yang baru"""
    while True:
        try:
            with open('data.txt', 'r') as file:
                queries = file.read().splitlines()

            if not queries:
                print(f"{Fore.RED}Tidak ada akun ditemukan di `data.txt`!{Style.RESET_ALL}")
                time.sleep(10)
                continue

            print(f"\n{Fore.GREEN}>> Memproses {len(queries)} akun...{Style.RESET_ALL}")
            progress_bar = tqdm(total=len(queries), desc="Proses", ncols=80)

            for query_id in queries:
                log_header("MEMPROSES AKUN")
                proxy = get_next_proxy()
                if proxy:
                    log_info("Proxy digunakan", proxy)

                getname(query_id)
                token = gettoken(query_id, proxy)
                if token:
                    postrequest(token, proxy)
                progress_bar.update(1)

            progress_bar.close()
            print(f"\n{Fore.YELLOW}Menunggu 10 menit sebelum siklus berikutnya...{Style.RESET_ALL}")
            time.sleep(600)

        except Exception as e:
            print(f"{Fore.RED}[ERROR] {e}, restart dalam 10 detik...{Style.RESET_ALL}")
            time.sleep(10)

def gettoken(query, proxy=None):
    """Mengambil token login dengan proxy opsional"""
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json'
    }
    url = "https://api-tg-app.midas.app/api/auth/register"
    data = json.dumps({"initData": query}).encode('utf-8')

    proxy_handler = urllib.request.ProxyHandler({'http': proxy, 'https': proxy}) if proxy else None
    opener = urllib.request.build_opener(proxy_handler) if proxy else urllib.request.build_opener()

    try:
        req = urllib.request.Request(url, data, headers, method='POST')
        response = opener.open(req)

        if response.getcode() == 201:
            log_step("Login berhasil")
            return response.read().decode('utf-8')
        else:
            log_step("Login gagal", "FAILED")
            return None
    except Exception as e:
        log_step(f"Error login: {e}", "FAILED")
        return None

def getname(query):
    """Mendapatkan username dari query"""
    try:
        found = re.search('user=([^&]*)', query).group(1)
        user_data = json.loads(unquote(found))
        log_info("Username", f"@{user_data['username']}")
    except:
        log_step("Error parsing username", "FAILED")

def postrequest(token, proxy=None):
    """Memproses akun dengan berbagai aksi menggunakan proxy opsional"""
    getuser(token, proxy)
    checkin(token, proxy)

    if tix > 0:
        log_step("Memulai permainan...")
        playgame(token, proxy)

    gettasks(token, proxy)

def getuser(token, proxy=None):
    """Mengambil informasi akun dengan proxy opsional"""
    headers = {'Authorization': f'Bearer {token}', 'User-Agent': 'Mozilla/5.0'}
    url = "https://api-tg-app.midas.app/api/user"

    proxy_handler = urllib.request.ProxyHandler({'http': proxy, 'https': proxy}) if proxy else None
    opener = urllib.request.build_opener(proxy_handler) if proxy else urllib.request.build_opener()

    try:
        req = urllib.request.Request(url, None, headers, method='GET')
        response = opener.open(req)
        data = json.loads(response.read().decode('utf-8'))

        log_info("GM Points", data['points'])
        log_info("Check-in Days", data['streakDaysCount'])
        log_info("Tickets", data['tickets'])

        global tix
        tix = data['tickets']
    except Exception as e:
        log_step(f"Error mendapatkan data akun: {e}", "FAILED")

def checkin(token, proxy=None):
    """Melakukan check-in harian dengan proxy opsional"""
    headers = {'Authorization': f'Bearer {token}', 'User-Agent': 'Mozilla/5.0'}
    url = "https://api-tg-app.midas.app/api/streak"

    proxy_handler = urllib.request.ProxyHandler({'http': proxy, 'https': proxy}) if proxy else None
    opener = urllib.request.build_opener(proxy_handler) if proxy else urllib.request.build_opener()

    try:
        req = urllib.request.Request(url, None, headers, method='GET')
        response = opener.open(req)
        data = json.loads(response.read().decode('utf-8'))

        if data['claimable']:
            req = urllib.request.Request(url, None, headers, method='POST')
            opener.open(req)
            log_step("Check-in berhasil")
    except Exception as e:
        log_step(f"Error saat check-in: {e}", "FAILED")

# **Menjalankan script**
if __name__ == "__main__":
    try:
        show_banner()
        load_proxies()
        runforeva()
    except KeyboardInterrupt:
        sys.exit()