__author__ = 'luohua139'
import requests
import redis
import logging
import configparser

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s ： %(message)s')
logger = logging.getLogger(__name__)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}


class RedisClient():
    MAX_SCORE = 100
    MIN_SCORE = 0
    DECR_SCORE = -10
    INIT_SCORE = 50
    LIMITED = 10000

    def __init__(self, host="118.25.181.239", port=7778, password="1qaz@WSX", db=1):
        self.redis = redis.StrictRedis(host=host, port=port, password=password, db=db, decode_responses=True)

    def add(self, proxies, score=INIT_SCORE, name="proxies"):
        ret = self.redis.zadd(name=name, mapping={proxies: score})
        if ret == 1:
            logger.info("{} 代理添加成功".format(proxies))
        else:
            if score != self.INIT_SCORE:
                logger.info("{} 分值更新为{}".format(proxies, score))
            else:
                logger.info("{} 代理已存在！".format(proxies))

    def decr(self, proxies, score=DECR_SCORE, name="proxies"):
        ret = self.redis.zincrby(name, score, proxies, )
        if ret > 0:
            logger.info("{} 当前分数大于0".format(proxies))
        else:
            logger.info("{} 当前分数小于0，移除此ip".format(proxies))
            self.remove(proxies=proxies)

    def remove(self, proxies, name="proxies"):
        ret = self.redis.zrem(name, proxies)
        if ret > 0:
            logger.info("{}移除成功".format(proxies))
        else:
            logger.error("{}移除失败".format(proxies))


    def count(self, name="proxies"):
        _count = self.redis.zcard(name=name)
        return _count

    def countByScore(self, name="proxies", mins=MIN_SCORE, maxs=MAX_SCORE):
        ret = self.redis.zcount(name, mins, maxs)
        return ret

    def removeByScore(self, name="proxies", mins=MIN_SCORE, maxs=MAX_SCORE):
        ret = self.redis.zremrangebyscore(name, mins, maxs)
        if ret > 0:
            logger.info("移除成功{}个".format(ret))
        return ret


class BaseClass(type):
    def __new__(cls, name, base, attrs):
        attrs["cw_func"] = []
        count = 0
        for k, v in attrs.items():
            if "crawl_" in k:
                attrs["cw_func"].append(k)
                count += 1
        attrs["func_count"] = count
        return type.__new__(cls, name, base, attrs)


class Crawl(metaclass=BaseClass):
    def __init__(self):
        self.rc = RedisClient()

    def crawl_kuaidaili(self):
        pass

    def crawl_xici(self):
        pass

    def run(self):
        pass


class CheckValid():
    def __init__(self):
        self.test_url = "http://www.baidu.com"


if __name__ == '__main__':
    # cw = Crawl()
    # rc = RedisClient()
    # rc.add("10.255.445:80")
    cg = configparser.ConfigParser()
    cg.read("config.ini")
    sec = cg.sections()
    us = cg.get(sec[1], "user_agent")
    print(us)
