import os
import re
import urllib.request
from urllib import request
from collections import deque
from html.parser import HTMLParser
from http import cookiejar 
savePath = ''
cnt = 0
class MyHTMLParser(HTMLParser):
    def __init__(self):   
        HTMLParser.__init__(self)   
        self.links = []
        self.imglinks = []
        self.urlText = []
    def handle_data(self, data):
        if data != '\n':
            self.urlText.append(data)
    def handle_starttag(self, tag, attrs):   
        #print "Encountered the beginning of a %s tag" % tag   
        if tag == "a":   
            if len(attrs) == 0:   
                pass   
            else:   
                for (variable, value) in attrs:   
                    if variable == "href":   
                        self.links.append(value)
print ('ddddd')
url = 'http://www.qb5.com/9_9508/'
pattern = re.compile('http://www.qb5.com/9_9508/\d*.html')

fp = open('盗墓笔记.txt','w')
vis = set()
vis |={url}
url1 = url
print(url1)

headers = {  
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'  
}  
req = request.Request(url1,  
    headers = headers  
)  



try:
    data = request.urlopen(req).read()
    data = data.decode('GBK')
except:
    print ('sorry,--'+url1)
yk = MyHTMLParser()
yk.feed(data)
for link in yk.links:
    flink = link
    if ('http' not in link):
        flink = url+flink
    if(flink in vis or not pattern.match(flink)):
        continue
    print(flink)
    vis.add(flink)

for url1 in vis:
    try:
        data = urllib.request.urlopen(url1,timeout=10).read()
        data = data.decode('GBK')
    except:
        print ('sorry,--'+url1)
        continue
    yk = MyHTMLParser()
    yk.feed(data)
    for text in yk.urlText:
        fp.write(text)
    print (url1)
fp.close()
print ('hhhhhhhh')
