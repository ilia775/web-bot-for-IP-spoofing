import asyncio
import time
from bs4 import BeautifulSoup
import aiohttp
import requests
import os
from fake_useragent import UserAgent
import random
import json
from proxy_checking import ProxyChecker

proxy_type = "http://"
test_url = 'http://example.com'
timeout_sec = 2
GoodProxies = []
CurrentProxy = 0

class Proxy:
    def __init__(self, ip:str, port:str, https:str):
        self.ip = ip
        self.port = port
        self.is_https = https == 'yes'

    def __eq__(self, other):
        return ((self.ip == other.ip) and (self.port == other.port) and (self.is_https == other.is_https))

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
                     if Proxy(i[0], i[1], i[6]) not in proxy_list:
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




async def checkproxyhttp(httpproxy):
     try:
         session = aiohttp.ClientSession()
         #print(UserAgent().random)
         resp = await session.get(test_url, proxy=httpproxy, headers = {'User-Agent' : UserAgent().random}, timeout=timeout_sec)
         await session.close()
         #print(resp.status)
         if resp.status != 200:
            raise "Error"
         GoodProxies.append(httpproxy)
     except:
         #print(2)
         await session.close()


def getdata(Query, Proxy):
    #Proxies[CurrentProxy] = {"http": Proxies[CurrentProxy]};
    try:
        s = requests.session();
        resp = s.get(Query, headers = {'User-Agent' : UserAgent().random}, proxies = {"http": Proxy, "https": Proxy}, timeout = timeout_sec * 2)
        if r"You are over your rate limit please upgrade your account!" in resp.text:
            #print(resp.text)
            #print(0)
            #print(Proxy)
            return -1
        s.close();
        print(resp.text)
    except:
        #print(0)
        #print(Proxy)
        return -1



def getquery():
    Query = "https://min-api.cryptocompare.com/data/price?fsym="
    while True:
        print("Выберите отсчётную валюту:")
        cc = input()
        response = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={cc}&tsyms=USD,JPY,EUR")
        if "market does not exist for this coin pair" not in response.text and "fsym param is empty or null" not in response.text:
            break
        else:
            print("Эта валюта не поддерживается")
    Query += cc + "&tsyms="
    while True:
        print("Выберите валюту для сравнения:(нажмите n чтобы закончить)")
        cc = input()
        if cc == 'n':
            break
        response = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms={cc}")
        if "market does not exist for this coin pair" not in response.text and "tsyms param is empty or null" not in response.text:
            Query += cc + ','
        else:
            print("Эта валюта не поддерживается")
    return Query


def checkproxy(proxy_list):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = []
    for item in proxy_list:
        #if item.is_https == 0:
            tasks.append(asyncio.ensure_future(checkproxyhttp(str(item))))
        #else:
            #tasks.append(asyncio.ensure_future(checkproxyhttps(str(item))))
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

if __name__ == "__main__":
    Query = getquery()
    #Query = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,JPY,EUR"
    timer = time.time()
    #Query = getquery();
    proxy_list = []
    getallproxy(proxy_list)
    #print(len(proxy_list))
    checkproxy(proxy_list)
    #print(GoodProxies)
    t = time.time()
    timeout = 60*60
    CurrentProxy = 0
    while True:
        if time.time() - t > timeout:
            print("timeout")
            print(time.time() - t)
            proxy_list = []
            GoodProxies = []
            getallproxy(proxy_list)
            checkproxy(proxy_list)
            #print(GoodProxies)
            CurrentProxy = 0
            t = time.time()

        if len(GoodProxies) == 0:
            t -= timeout
            continue
        if getdata(Query, str(GoodProxies[CurrentProxy])) == -1:
            CurrentProxy += 1
            if CurrentProxy >= len(GoodProxies):
                t -= timeout
                continue
            #t -= timeout
        if CurrentProxy >= len(proxy_list):
            t -= timeout
            continue
        #print(GoodProxiesHTTP)
        #print(time.time() - timer)
