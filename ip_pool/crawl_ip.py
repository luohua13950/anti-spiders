__author__ = 'luohua139'
import requests
import redis
import logging
import configparser
import datetime
import time
from lxml import etree
from threading import Thread
import threading
from multiprocessing import Process


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s ： %(message)s')
logger = logging.getLogger(__name__)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}


class Config():
    def __init__(self):
        self.cg = configparser.ConfigParser()
        self.cg.read("config.ini")

    @property
    def db_config(self):
        sec = self.cg._sections
        db_info = dict(sec["db_config"])
        return db_info


class RedisClient():
    MAX_SCORE = 100
    MIN_SCORE = 0
    DECR_SCORE = -5
    INIT_SCORE = 100
    LIMITED = 10000

    def __init__(self, host, port, password, db, ):
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
        return ret

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
        return ret

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
            #if "crawl_" in k:
            if k.startswith("crawl_"):
                attrs["cw_func"].append(k)
                count += 1
        attrs["func_count"] = count
        return type.__new__(cls, name, base, attrs)


class Crawl(metaclass=BaseClass):
    def __init__(self, valid_period=20):
        db_info = Config().db_config
        self.rc = RedisClient(**db_info)
        self.valid_period = valid_period
        self.base = datetime.timedelta(days=valid_period)
        self.sleep_sec = 30

    def check_invalid_day(self, str_time):
        try:
            day = datetime.datetime.now()
            dt = datetime.datetime.strptime(str_time.split()[0], "%Y-%m-%d")
        except Exception as e:
            logger.error("转换时间发生错误:{}".format(e))
            return False
        logger.info("此ip上次验证时间为{}前".format(day.date() - dt.date()))
        return day.date() - dt.date() < self.base

    @staticmethod
    def get_page(url, page):
        resp = requests.get(url=url.format(page), headers=headers)
        logger.info("{}:当前爬取第{}页".format(threading.current_thread().name,page))
        x_page = etree.HTML(resp.text)
        x_tr = x_page.xpath("//tbody//tr")
        if len(x_tr) <1:
          x_tr = x_page.xpath("//table//tr")
        return x_tr

    def add_proxies(self, ip, port, http, str_time):
        try:
            http = http.lower()
            if self.check_invalid_day(str_time):
                proxies = "{}://{}:{}".format(http, ip, port)
                self.rc.add(proxies)
                return True
            else:
                return False
        except Exception as e:
            logger.error("存储过程发生异常:{}".format(e))


    def crawl_kuaidaili(self):
        url = "https://www.kuaidaili.com/free/inha/{}/"
        page = 1
        while True:
            try:
                x_tr = self.get_page(url, page)
                if not self._crawl_kuaidaili(x_tr):
                    logger.info("{}:当前ip校验时间已超过{}天,不再继续爬取后面！".format(threading.current_thread().name,self.valid_period))
                    break
                page += 1
                logger.info("快代理睡眠{}秒".format(self.sleep_sec))
                time.sleep(self.sleep_sec)

            except Exception as e:
                logger.error(e)
                break


    def _crawl_kuaidaili(self, x_tr):
        for tr in x_tr:
            try:
                _ip = tr.xpath("td[1]/text()")
                ip = _ip[0] if _ip else ""
                _port = tr.xpath("td[2]/text()")
                port = _port[0] if _port else ""
                _http = tr.xpath("td[4]/text()")
                http = _http[0] if _http else ""
                _str_time = tr.xpath("td[7]/text()")
                str_time = _str_time[0] if _str_time else ""
                if not all([ip, port, http]):
                    continue
                if not self.add_proxies(ip, port, http, str_time):
                    return False
            except Exception as e:
                logger.error(e)
                continue
        return True

    def crawl_xici(self):
        url = "https://www.xicidaili.com/nn/{}"
        page = 1
        while True:
            try:
                x_tr = self.get_page(url, page)
                if not self._crawl_xici(x_tr):
                    logger.info("{}:当前ip校验时间已超过{}天,不再继续爬取后面！".format(threading.current_thread().name,self.valid_period))
                    break
                page += 1
                logger.info("西刺睡眠{}秒".format(self.sleep_sec))
                time.sleep(self.sleep_sec)
            except Exception as e:
                logger.error(e)
                break

    def _crawl_xici(self, x_tr):
        for tr in x_tr[1:]:
            try:
                _ip = tr.xpath("td[2]/text()")
                ip = _ip[0] if _ip else ""
                _port = tr.xpath("td[3]/text()")
                port = _port[0] if _port else ""
                _http = tr.xpath("td[6]/text()")
                http = _http[0] if _http else ""
                _str_time = tr.xpath("td[10]/text()")
                str_time = _str_time[0] if _str_time else ""
                if not all([ip, port, http]):
                    continue
                str_time = "20" +str_time
                if not self.add_proxies(ip, port, http, str_time):
                    logger.info("当前ip验证时间为{}".format(str_time))
                    return False

            except Exception as e:
                logger.error(e)
                continue
        return True

    def run(self):
        #th_kuaidali = Thread(target=self.crawl_kuaidaili,args=())
        th_list = []
        for cw in self.cw_func:
            fn = eval("self.{}".format(cw))
            th_list.append(Thread(target=fn,args=(),name="thread-{}".format(cw)))
            logger.info("创建线程...")
        for th in th_list:
            logger.info("启动线程:{}...".format(th.name))
            th.start()

class CheckValid():
    def __init__(self):
        self.test_url = "http://www.baidu.com"


if __name__ == '__main__':
    cw = Crawl()
    # cw.crawl_kuaidaili()
    cw.run()


