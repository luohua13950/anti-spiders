__author__ = 'luohua139'
import asyncio
import os
import requests
import time
import aiohttp

@asyncio.coroutine
def asyn():
    print("开始asyn")
    for dirs in os.listdir("..\\"):
        #print(dirs)
        asyncio.ensure_future(task(dirs))
    #yield from asyncio.sleep(2)
    print("fafafa")
    asyncio.ensure_future(opens())

@asyncio.coroutine
def task(dirs):
    print("开始task")
    print(dirs)
    #yield from asyncio.sleep(2)

@asyncio.coroutine
def opens():
    #yield from asyncio.sleep(2)
    print("this func is open file")

@asyncio.coroutine
def get_url(url):
    print(url.split("/")[-1])
    #done,response = asyncio.ensure_future(real(url))
    response = yield  from  real(url)
    while True:
        print(url.split("/")[-1])
        status_code = yield from response.status_code
        if url.split("/")[-1] == "107101922065.html":
            break
        print(status_code)

@asyncio.coroutine
def real(url):
    ua = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
    response = requests.get(url,headers=ua)
    return response


async def aio(url,index):
    connect = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connect) as session:
        async with session.get(url) as resp:
            print(index,":",resp.status)
            #print(session.cookie_jar.filter_cookies(url))

if __name__ == "__main__":
    st = time.perf_counter()
    url_l = ["https://sh.lianjia.com/ershoufang/107101498934.html",
             "https://sh.lianjia.com/ershoufang/107101534657.html",
             "https://sh.lianjia.com/ershoufang/107101377032.html",
             "https://sh.lianjia.com/ershoufang/107101936820.html",
             "https://sh.lianjia.com/ershoufang/107101739271.html",
             "https://sh.lianjia.com/ershoufang/107101637990.html",
             "https://sh.lianjia.com/ershoufang/107101748799.html",
             "https://sh.lianjia.com/ershoufang/107101922063.html",
             "https://sh.lianjia.com/ershoufang/107101922064.html",
             "https://sh.lianjia.com/ershoufang/107101922061.html",
             "https://sh.lianjia.com/ershoufang/107101922060.html",
             "https://sh.lianjia.com/ershoufang/107101922025.html",
             "https://sh.lianjia.com/ershoufang/107101922015.html",
             "https://sh.lianjia.com/ershoufang/107101922075.html",
             "https://sh.lianjia.com/ershoufang/107101922045.html",
             "https://sh.lianjia.com/ershoufang/107101922085.html",
             "https://sh.lianjia.com/ershoufang/107101922065.html",
             "https://sh.lianjia.com/ershoufang/107101922036.html",
             "https://sh.lianjia.com/ershoufang/107101922058.html",
             ]
    loop = asyncio.get_event_loop()
    baidu = "https://www.baidu.com"
    #task = [aio(_url) for _url in url_l[:1]]
    task = [aio(baidu,i) for i in range(60)]
    loop.run_until_complete(asyncio.gather(*task))
    end = time.perf_counter()
    loop.close()
    print("耗时%s" %(end-st))
