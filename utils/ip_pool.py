import redis
import requests


class Crawl():
    def __init__(self,host="118.25.181.239",port=7778,db =1,password="1qaz@WSX"):
        self.redis = redis.StrictRedis(host=host,port=port,db=db,password=password,decode_responses=True)
        self.redis.set("test","中国")
        print(self.redis.get("test"))




if __name__ == "__main__":
    cw = Crawl()
