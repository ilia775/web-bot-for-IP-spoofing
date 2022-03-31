import requests
from bs4 import BeautifulSoup


#proxies=[]

def GetProxy():
    url=r'https://www.sslproxies.org'
    page=requests.get(url)
    soup=BeautifulSoup(page.text,'html.parser')
    Table=soup.findAll('table')[0].tbody.findAll('td')
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
