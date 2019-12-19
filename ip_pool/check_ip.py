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

    def get_proxies(self,start,end,http_type = "https"):
        _proxies_list = self.redis.batch(start=start,end=end)
        if not _proxies_list:
            logger.error("{}到{}的代理不存在，请重新输入".format(start,end))
            return
        def format_proxies(_proxies):
            _http_type = _proxies.split(":")[0]
            proxies = { _http_type : _proxies}
            return proxies
        proxies_list = list(map(format_proxies,_proxies_list))
        filter_proxies_list = [v for prxy in proxies_list for k,v in prxy.items() if k == http_type]
        print()
        return filter_proxies_list

    async def get_response(self,url,proxies):
        conn = aiohttp.TCPConnector(limit=50)
        async with aiohttp.ClientSession(connector=conn) as session:
            agent = random.choice(USER_AGENT)
            headers = {"User-Agent":agent}
            try:
                async with session.get(url, headers=headers,timeout = 5,proxy = proxies) as resp:
                    if resp.status == 200:
                        self.redis.add(proxies)
                        logger.info("{} is success to connect test url,update score!".format(proxies))
                        self.count +=1
            except asyncio.TimeoutError:
                logger.warning("{} is timeout".format(proxies))
                self.redis.decr(proxies)
            # except aiohttp.client_exceptions.ClientProxyConnectionError as e:
            #     logger.error("{} is {}".format(proxies,e))
            #     self.redis.decr(proxies)
            # except ConnectionRefusedError as e:
            #     logger.error("{} is {}".format(proxies,e))
            #     self.redis.decr(proxies)
            except Exception as e:
                self.redis.decr(proxies)
                logger.warning("{} is {}".format(proxies,e))

    @staticmethod
    def get_str_type_proxies(prx_batch):
        str_proxies = list(map(lambda x:list(x.values())[0],prx_batch))
        return str_proxies

    def run_loop(self):
        prx_batch = self.get_proxies(8000,8010)
        print(prx_batch)
        str_type_proxies = self.get_str_type_proxies(prx_batch)
        loop = asyncio.get_event_loop()
        task = [self.get_response(self.test_url,prx) for prx in str_type_proxies]
        loop.run_until_complete(asyncio.gather(*task))
        logger.info("{} proxy live!".format(self.count))

if __name__ == '__main__':
    tiv = CheckIpValid()
    tiv.run_loop()
    import requests
    agent = random.choice(USER_AGENT)
    headers = {"User-Agent":agent}
    # resp = requests.get(tiv.test_url,headers = headers,proxies={"http":"http://1.197.10.34:9999"})
    # print(resp)
    #ret = tiv.redis.score("https://171.11.32.128:9999")
    # ret = tiv.redis.decr("https://171.11.32.128:9999")
    # print(ret)