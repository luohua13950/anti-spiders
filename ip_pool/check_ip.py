__author__ = 'luohua139'

import asyncio, aiohttp
import random

from ip_pool.crawl_ip import RedisClient, Config,logger
from ip_pool import USER_AGENT


class CheckIpValid():
    def __init__(self):
        self.test_url = "http://www.baidu.com"
        self.count = 0
        self.db_config = Config().db_config
        self.redis = RedisClient(**self.db_config)

    def get_proxies(self,start,end):
        _proxies_list = self.redis.batch(start=start,end=end)
        if not _proxies_list:
            logger.error("{}到{}的代理不存在，请重新输入".format(start,end))
            return
        def format_proxies(_proxies):
            http_type = _proxies.split(":")[0]
            proxies = { http_type : _proxies}
            return proxies
        proxies_list = list(map(format_proxies,_proxies_list))
        return proxies_list

    async def get_response(self,url,proxies):
        conn = aiohttp.TCPConnector(limit=10)
        async with aiohttp.ClientSession(connector=conn) as session:
            agent = random.choice(USER_AGENT)
            headers = {"User-Agent":agent}
            try:
                async with session.get(url, headers=headers,timeout = 5) as resp:
                    print(self.count)
                    if resp.status == 200:
                        print("200")
                    self.count +=1
            except asyncio.TimeoutError:
                print("timeout")

    def run_loop(self):
        loop = asyncio.get_event_loop()
        task = [self.get_response(self.test_url) for i in range(60)]
        loop.run_until_complete(asyncio.gather(*task))

if __name__ == '__main__':
    tiv = CheckIpValid()
    tiv.get_proxies(10000,10001)