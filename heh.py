import os
import re
import urllib.request
import urllib
from collections import deque
from html.parser import HTMLParser

savePath = ''
imagevis = set()
cnt = 0
def getImage(addr):
    global cnt
    global imagevis
    try :
        data = urllib.request.urlopen(addr,timeout=10).read()
    except :
        print (addr)
        print ('sorry--------------------')
        return
    splitPath = addr.strip().split('/')
    fName = splitPath[-1]
    if fName == '' or fName in imagevis:
        return
    cnt = cnt +1
    imagevis |={fName}
    print ('saving %s' % fName)
    try :
        fp = open(savePath+fName,'wb')
    except:
        return
    print(savePath+fName)
    fp.write(data)
    fp.close()

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
        if tag =='img' :
            if len(attrs) ==0:
                pass
            for (name,value) in attrs:
                if (name == 'src'):
                    self.imglinks.append(value)


print ('ddddd')
url = 'http://www.941ni.com'
pattern = re.compile('http://www.941ni.com/xiaoshuo/')
queue = deque()
vis = set()
queue.append(url)
vis |={url}
while queue:
    url1 = queue.popleft()
    print(url1)
    try:
        data = urllib.request.urlopen(url1,timeout=10).read()
        data = data.decode('utf-8')
    except:
        print ('sorry,--'+url1)
        continue
    yk = MyHTMLParser()
    yk.feed(data)
    for link in yk.links:
        flink = link
        print(flink)
        if ('http' not in link):
            flink = url+flink
        if(flink in vis or not pattern.match(flink)):
            continue
        queue.append(flink)
        vis |={flink}
    
    savePath =os.getcwd()+'\image\\'
    if not os.path.exists(savePath):
        os.mkdir(savePath)
    for text in yk.urlText:
        print (text)
    continue
    for image in yk.imglinks:
        if ('http' in image):
            getImage(image)
        else :
            getImage(url+image)

