import requests
from bs4 import BeautifulSoup


proxies=[]

def GetProxy():
    url=r'https://www.sslproxies.org'
    page=requests.get(url)
    soup=BeautifulSoup(page.text,'html.parser')
    Table=soup.findAll('table')[0].tbody.findAll('td')
    i=0
    AllProxy=''
    for i in range(0,len(Table),8):
        row=Table[i]
        AllProxy+=row.text+':'
        i+=1
        row=Table[i]
        AllProxy+=row.text+' '
    AllProxy=AllProxy.split(' ')
    AllProxy.remove('')
    return AllProxy







def checkProxies(listProxy):
    url=r'https://github.com'
    goodProxies=[]
    for proxy in listProxy:
        proxy="http://"+proxy
        proxy={'http':proxy}
        try:
            response=requests.get(url,proxies=proxy,timeout=5)
            print("~")
            if "Where the world" in str(response.text):
                goodProxies.append(proxy)
                print(str(response.text))
                response=''
        except:
            continue
    return goodProxies




proxies=GetProxy()
checkedProxies=checkProxies(proxies)
print(checkedProxies)