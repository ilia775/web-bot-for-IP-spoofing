
import asyncio
import time
from bs4 import BeautifulSoup
import aiohttp
import requests
import os
from fake_useragent import UserAgent
import random

proxy_type = "http://"
test_url = 'http://example.com'
timeout_sec = 4
GoodProxiesHTTP = []
GoodProxiesHTTPS = []
AllProxyHTTP = []
AllProxyHTTPS = []
CurrentProxy = 0

class Proxy:
    def __init__(self, ip:str, port:str, https:str):
        self.ip = ip
        self.port = port
        self.is_https = https == 'yes'

    def __str__(self):
        return f"{'https' if self.is_https else 'http'}://{self.ip}:{self.port}"


def getallproxy(proxy_list):
    urls = ["https://www.socks-proxy.net/", "https://free-proxy-list.net/", "https://www.us-proxy.org/", "https://free-proxy-list.net/uk-proxy.html", "https://www.sslproxies.org/", "https://free-proxy-list.net/anonymous-proxy.html"]
    #urls = ["https://www.sslproxies.org/", "https://free-proxy-list.net/", "https://free-proxy-list.net/anonymous-proxy.html"]
    for url in urls:
        getproxy(url, proxy_list)


def getproxy(url, proxy_list):
     response = requests.get(url)
     soup = BeautifulSoup(response.content, 'html.parser')
     for table in soup.find_all('table'):
             if 'table-striped' in table['class']:
                 tempt = table.find_all('td')
                 #for i in [ [el.text for el in tempt[i:i+8]] for i in range(0,len(tempt),8)]:
                      #print(str(Proxy(i[0],i[1], i[6]))) 
                 #return [ str(Proxy(x[0], x[1], x[6])) for x in [ [el.text for el in tempt[i:i+8]] for i in range(0,len(tempt),8)]]
                 for i in [ [el.text for el in tempt[i:i+8]] for i in range(0,len(tempt),8)]:
                     proxy_list.append(Proxy(i[0], i[1], i[6]))

def getproxy1(url):

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
         #ipport = "http://" + ipport;
         session = aiohttp.ClientSession()
         #print(UserAgent().random)
         resp = await session.get(test_url, proxy=ipport, headers = {'User-Agent' : UserAgent().random}, timeout=timeout_sec)
         await session.close()
         #print(resp.status)
         if resp.status != 200:
            raise "Error"
         GoodProxiesHTTP.append(ipport[7:])
     except:
         print(2)
         await session.close()


def getdata(Proxy):
    #Proxies[CurrentProxy] = {"http": Proxies[CurrentProxy]};
    try:
        s = requests.session();
        s.proxies = {"http":Proxy}
   
        resp = s.get("https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=RUB,USD,JPY,EUR", headers = {'User-Agent' : UserAgent().random})
        if r"You are over your rate limit please upgrade your account!" in resp.text:
            #print(resp.text)
            return -1
        s.close();
        print(resp.text)
    except:
        print(0)
        print(Proxy)
        return -1




def checkproxy(proxy_list):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = []
    for item in proxy_list:
        if item.is_https == 0:
            tasks.append(asyncio.ensure_future(checkproxyhttp(str(item))))
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

if __name__ == "__main__":

    timer = time.time()
    proxy_list = []
    getallproxy(proxy_list)
    #print(len(proxy_list))
    checkproxy(proxy_list)
    print(GoodProxiesHTTP)
    t = time.time()
    timeout = 60
    CurrentProxy = 0
    while True:
        if time.time() - t > timeout:
            print("timeout")
            print(time.time() - t)
            proxy_list = []
            GoodProxiesHTTP = []
            getallproxy(proxy_list)
            checkproxy(proxy_list)
            CurrentProxy = 0
            t = time.time()

        if len(GoodProxiesHTTP) == 0:
            t -= timeout
            print("pizda")
            continue
        if getdata(str(GoodProxiesHTTP[CurrentProxy])) == -1:
            CurrentProxy += 1
            if CurrentProxy >= len(GoodProxiesHTTP):
                continue
            #t -= timeout
        if CurrentProxy >= len(proxy_list):
            t -= timeout
            continue
        #print(GoodProxiesHTTP)
        print(time.time() - timer)



