
import asyncio
import time
from bs4 import BeautifulSoup
import aiohttp
import requests
import os

proxy_type = r"http://"
test_url = r"https://min-api.cryptocompare.com/"
timeout_sec = 4
GoodProxiesHTTP = []
GoodProxiesHTTPS = []
AllProxyHTTP = []
AllProxyHTTPS = []
CurrentProxy = 0


def getallproxy():
    urls = ["https://www.socks-proxy.net/", "https://free-proxy-list.net/", "https://www.us-proxy.org/", "https://free-proxy-list.net/uk-proxy.html", "https://www.sslproxies.org/", "https://free-proxy-list.net/anonymous-proxy.html"]
    #urls = ["https://www.sslproxies.org/", "https://free-proxy-list.net/", "https://free-proxy-list.net/anonymous-proxy.html"]
    for url in urls:
        getproxy(url)


def getproxy(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    Table = soup.findAll('table')[0].tbody.findAll('td')
    for i in range(0, len(Table), 8):
        row = Table[i]
        Proxy = row.text + ':'
        i += 1
        row = Table[i]
        Proxy += row.text
        #print(Table[i+5].text)
        
        if Proxy not in AllProxyHTTP and Proxy not in AllProxyHTTPS:
            if Table[i+5].text == "no":
                AllProxyHTTP.append(Proxy)
            else:
                AllProxyHTTPS.append(Proxy)


async def checkproxyhttp(ipport):
     try:
         ipport = "http://" + ipport;
         session = aiohttp.ClientSession()
         resp = await session.get(test_url, proxy=ipport, timeout=timeout_sec)
         #print(1)
         await session.close()
         #print(resp.status)
         if resp.status != 200:
            raise "Error"
         GoodProxiesHTTP.append(ipport[7:])
     except:
         #print(2)
         await session.close()


def getdata(Proxies, CurrentProxy):
    #Proxies[CurrentProxy] = {"http": Proxies[CurrentProxy]};
    try:
        s = requests.session();
        s.proxies = {"http":Proxies[CurrentProxy]}
   
        resp = s.get("https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=RUB,USD,JPY,EUR")
        if r"You are over your rate limit please upgrade your account!" in resp.text:
            print(resp.text)
            return -1
        s.close();
        print(resp.text)
    except:
        print(0)
        print(Proxies[CurrentProxy])
        return -1




def checkproxy():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = []
    for item in AllProxyHTTP:
        tasks.append(asyncio.ensure_future(checkproxyhttp(item)))
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


timer = time.time()
getallproxy()
print(AllProxyHTTPS)
print(AllProxyHTTP)
checkproxy()
print(GoodProxiesHTTP)
t = time.time()
timeout = 60
CurrentProxy = 0
while True:
    if time.time() - t > timeout:
        print("timeout")
        print(time.time() - t)
        GoodProxiesHTTP = []
        AllProxy = []
        getallproxy()
        checkproxy()
        CurrentProxy = 0
        t = time.time()

    if len(GoodProxiesHTTP) == 0:
        t -= timeout
        continue
    if getdata(GoodProxiesHTTP, CurrentProxy) == -1:
        CurrentProxy += 1
        #t -= timeout
    if CurrentProxy >= len(GoodProxiesHTTP):
        t -= timeout
        continue
    print(GoodProxiesHTTP)
    print(time.time() - timer)



