import requests
from bs4 import BeautifulSoup
import re
baseurl = 'http://www.941ni.com/xiaoshuo/xiaoyuanchunse/20140829/'
url = 'http://www.941ni.com/xiaoshuo/xiaoyuanchunse/20140829/13901.html'
url1 = 'http://www.zhihu.com'
headers = {
    'Cache-Control':'max-age=0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',  
}
response = requests.get(url,headers = headers)
print (response.encoding)
soup = BeautifulSoup(response.text.encode(response.encoding).decode('utf-8'))
fp = open(soup.find('h2').text+'.txt','w')
fp.write(soup.find('h2').text)
fp.write(soup.findAll('p')[1].text)
#print(soup.find('h2').text)
#print(soup.findAll('p')[1].text)
lis = soup.find('div','pagea').findAll('a')
vis =set()
comp = re.compile('.*html')
for item in lis:
    href = item.get('href')
    if (href == None or href in vis):
        continue
    vis |= {href}
    if(comp.match(href)):
        response = requests.get(baseurl+href,headers = headers)
        print (response.encoding)
        soup = BeautifulSoup(response.text.encode(response.encoding).decode('utf-8'))
        #print(soup.find('h2').text)
        #print(soup.findAll('p')[1].text)
        fp.write(soup.find('h2').text)
        fp.write(soup.findAll('p')[1].text)
fp.close()
