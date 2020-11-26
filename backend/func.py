import requests
import socket
from threading import Thread
import pymongo
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["database"]
col = db["proxies"]

def getProxies(url):
    arr = []
    r = requests.get(url, verify=False)
    proxies = r.text
    for proxy in proxies.split("\n"):
        arr.append(proxy.rstrip().lstrip())
    return arr

def checkProxy(ip, port):
    try:
        h = "GET http://example.org/ HTTP/1.1\nHost: example.org\r\n\r\n"
        chk = socket.socket()
        chk.settimeout(30)
        chk.connect((ip, port))
        chk.send(h.encode('utf-8'))
        #print("success: " + ip + ":" + str(port))
        col.insert_one({'ip': str(ip), 'port': str(port)})
        chk.close()
    except (socket.gaierror, socket.timeout, ConnectionRefusedError, ConnectionResetError, TimeoutError, OSError):
        #print("fail: " + ip + ":" + str(port))
        pass

def updateProxies():
    col.drop() #delete old entries (because proxies die fast)
    proxyList = [] #start with fresh list

    #get proxies from urls
    arr1 = getProxies("https://www.proxy-list.download/api/v1/get?type=socks5&anon=elite")
    arr2 = getProxies("https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=10000&country=all")

    proxyList = arr1 + arr2 #add proxies to list
    
    proxyList = list(dict.fromkeys(filter(None, proxyList))) #Remove empty list items and duplicates

    #check proxies
    for i in proxyList:
        try:
            proxy = i.split(":")
            t = Thread(target=checkProxy, args=(proxy[0], int(proxy[1])))
            t.start()
        except:
            pass

    t.join()
