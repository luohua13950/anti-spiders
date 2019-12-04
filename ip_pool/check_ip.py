__author__ = 'luohua139'
from .crawl_ip import RedisClient,Config
import asyncio,aiohttp

class TestIpValid():
    def __init__(self):
        self.test_url = "http://www.baidu.com"
        self.db_config = Config().db_config
        self.redis = RedisClient(**self.db_config)