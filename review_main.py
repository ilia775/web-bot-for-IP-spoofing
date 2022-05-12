import asyncio
from http import HTTPStatus
import time
from urllib import response
from bs4 import BeautifulSoup
import aiohttp
from matplotlib.pyplot import table
import requests
import typing
import os

proxy_type = r"http://"
test_url = r"https://min-api.cryptocompare.com/"
# интересный факт, тут у вас с r"", а ниже в getallproxy() просто ""
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


# global AllProxy тут вообще не нужно, на будущее
# глобальные переменные исользуют чаще всего для всяких констант, наименований, директорий итд 
# если видели когданибудь в проекта config.py, то это и есть хороший пример того,
# что можно использовать как глобал 
# Далее - стиль верблюд как я уже сказал чаще всего используется в названии классов, на вашем месте я бы писал 
# get_all_proxy() - с точки зрения оформления так намного правильнее

# вот то как обычно делается и то о чем я вам писал в тг

# def getallproxy():
#     urls = ["https://www.socks-proxy.net/", "https://free-proxy-list.net/", "https://www.us-proxy.org/", "https://free-proxy-list.net/uk-proxy.html", "https://www.sslproxies.org/", "https://free-proxy-list.net/anonymous-proxy.html"]
#     return set([prox for proxs in [getproxy(url) for url in urls] for prox in proxs])

# set() сразу избавит вас от дубликатов

# Далее, если вам нужно для чего то присвоить результат, достаточно сделать вот так 

# proxy_list = get_all_proxy() обратите внимание, перменные так же без заглавных букв
            

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

# "page" было бы правильнее назвать response 
# soup = BeautifulSoup(page.text, 'html.parser') не .text a .content скорее всего
# сам код я бы написал далее приблизительно вот так

# class Proxy:
#     def __init__(self, ip:str, port:str, https:str):
#         self.ip = ip
#         self.port = int(port)
#         self.is_https = https == 'yes'
    
#     def __str__(self):
#         return f"{'https' if self.is_https else 'http'}://{self.ip}:{self.port}"

# print(Proxy('129.14.12.2','555','yes')) - можете посмотреть как работает 
#  is_https - стандарт по названиям (is_empty, is_null... etc)

# def getproxy(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     for table in soup.find_all('table'):    
#             if 'table-striped' in table['class']:
#                 tempt = table.find_all('td')
#                 # for i in [ [el.text for el in tempt[i:i+8]] for i in range(0,len(tempt),8)]:
#                 #     print(str(Proxy(i[0],i[1], i[6]))) оставляю вам принт, чтобы тоже могли посомтреть что там возвращается
#                 return [ str(Proxy(x[0], x[1], x[6])) for x in [ [el.text for el in tempt[i:i+8]] for i in range(0,len(tempt),8)]]    

# суть происходящего заключается в том что вы делаете проверку 
# на то находится ли класс 'table-striped' в классе таблицaх обозначающихся как 'table' 
# если вы залезите в htmlку страницы, то вы увидете, что все 
# прокси лежат именно в классе таблицы table-striped 
# Далее суть такова, что мы получаем каждую строку в таблице - буквально
# вот что у нас лежит в [ [el.text for el in tempt[i:i+8]] for i in range(0,len(tempt),8)] 
# [['3.95.61.16', '80', 'US', 'United States', 'anonymous', 'no', 'yes', '12 secs ago'], ...]
# Class Proxy() выше отвечает за то что ему на вход поступют 3 параметра:
# ip, port, и https это или нет
# Соответственно в ретурне у вас сразу готовые к проверке прокси, которые обрабатывает class Proxy
# вот что у вас теперь возвращает getproxy(url):
# ['http://109.94.172.194:8085', 'http://78.38.108.194:1080', 'http://78.31.94.118:1080', 'https://31.192.128.203:53281', 'https://186.67.230.45:3128']



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
# обратите внимание, у вас стоит пробел, пользуйтесь ТАБАМИ
# и приучайтесь сразу, это прям стандарт


# чисто визуальный момент, у вас getdata()
# Вызывается в самый последний момент
# Даже чисто визуально таски удобно делать прямо под async
def checkproxy():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = []
    for item in AllProxyHTTP:
        tasks.append(asyncio.ensure_future(checkproxyhttp(item)))
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

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






#Запомните, вызов программы осуществляется вот так
# if __name__ == "__main__":
# И сделайте gitignore файл, закиньте туда все, что 
# не используете в проекте

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
    # мне поплохело
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