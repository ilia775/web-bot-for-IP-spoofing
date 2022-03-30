import requests
from bs4 import BeautifulSoup


def GetProxyList():
    url = r'https://www.sslproxies.org/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    Table = soup.findAll('table')[0].tbody.findAll('td')
    AllProxy = ''
    for i in range(0, len(Table), 8):
        row = Table[i]
        AllProxy += row.text + ':'
        i += 1
        row = Table[i]
        if i + 8 <= len(Table):
            AllProxy += row.text + ' '
        else:
            AllProxy += row.text
    AllProxy = AllProxy.split(' ')
    return AllProxy
