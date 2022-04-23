
import asyncio
import time
from bs4 import BeautifulSoup
import aiohttp
import requests




proxy_type = "http"
test_url = r"https://github.com/"
timeout_sec = 4
GoodProxies = []
AllProxy = []
CurrentProxy = 0

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def GetAllProxy():
    urls=["https://www.socks-proxy.net/", "https://free-proxy-list.net/", "https://www.us-proxy.org/", "https://free-proxy-list.net/uk-proxy.html", "https://www.sslproxies.org/", "https://free-proxy-list.net/anonymous-proxy.html"]
    for url in urls:
        GetProxy(url)


def GetProxy(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    Table = soup.findAll('table')[0].tbody.findAll('td')
    for i in range(0, len(Table), 8):
        row = Table[i]
        Proxy = 'http://'
        Proxy += row.text + ':'
        i += 1
        row = Table[i]
        Proxy += row.text
        if Proxy not in AllProxy:
            AllProxy.append(Proxy)
    return


async def is_bad_proxy(ipport):
     try:
         session = aiohttp.ClientSession()
         resp = await session.get(test_url, proxy=ipport, timeout=timeout_sec)
         print(1)
         await session.close()
         #print(resp.status)
         if resp.status != 200:
            raise "Error"
         #print(bcolors.OKBLUE + "Working:", ipport + bcolors.ENDC)
         GoodProxies.append(ipport)
     except:
         print(2)
         await session.close()
         #print(bcolors.FAIL + "Not Working:", ipport + bcolors.ENDC)


async def GetData():
    global CurrentProxy
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,RUB,JPY,EUR", proxy = GoodProxies[CurrentProxy], timeout = 5 ) as resp:
                print(resp.status)
        #print(3)
        await session.close()
    except:
        print(0)
        CurrentProxy += 1
        await session.close()
        if CurrentProxy > len(GoodProxies):
            return -1



def CheckProxies():
    loop = asyncio.get_event_loop()
    tasks = []
    for item in AllProxy:
        tasks.append(asyncio.ensure_future(is_bad_proxy(item)))
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
#GetAllProxy()
#loop = asyncio.get_event_loop()
#tasks = []
#for item in AllProxy:
#    tasks.append(asyncio.ensure_future(is_bad_proxy(item)))
#print(bcolors.HEADER + "Starting... \n" + bcolors.ENDC)
#oop.run_until_complete(asyncio.wait(tasks))
#print(bcolors.HEADER + "\n...Finished" + bcolors.ENDC)
#print(AllProxy)
#print(GoodProxies)
#loop.close()
GetAllProxy()
CheckProxies()
t = time.time()
timeout = 100
while True :
    if time.time() - t > timeout:
        GetAllProxy()
        CheckProxies()
        CurrentProxy = 0
        t = time.time()
    if asyncio.run(GetData()) == -1:
        t -= timeout



