import sys
sys.path.append("/mnt/dailypops_spider/")
import requests,re,time,json,scrapy,hashlib,platform
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse
from database.mongodb import MongoDB
from items import eventItem,articleItem,hotwordItem,questionItem
now_node = platform.node()
if now_node=="WINDOWS-GI073J5":
    environment="local"
else:
    environment="server"
db_name='dailypops'
class Chinadaily(scrapy.Spider):
    name = "chinadaily"
    allowed_domain=[]
    custom_settings = { 'ROBOTSTXT_OBEY' : False,
        'LOG_LEVEL' : 'ERROR',
        'CONCURRENT_REQUESTS':1,
        'DOWNLOAD_DELAY' : 0.2,
        'CONCURRENT_REQUESTS_PER_DOMAIN' : 1,
        'ITEM_PIPELINES' : {'pipeline.pipeline.MongodbPipeline': 300}
    }
    def start_requests(self):
        self.client = MongoDB(environment=environment,db_name=db_name).client
        zds = self.client.dailypops.hotword.find({"article_state":0})
        for k in zds:
            parm = k.get("hotword","")
            url="http://newssearch.chinadaily.com.cn/rest/en/search?keywords={}&sort=dp&page=0&curType=story&type=&channel=&source=".format(parm)
            yield scrapy.Request(url=url,callback=self.parse,meta={"data":k})
    def parse(self,response):
        event_id=response.meta.get("data","").get("event_id","")
        hotword_id=response.meta.get("data","").get("hotword_id","")
        source=response.meta.get("data","").get("source","")
        cons_list = json.loads(response.text).get("content","")
        for k in cons_list:
            url = k.get("url","")
            yield scrapy.Request(url=url,callback=self.parse_detail,meta={"event_id":event_id,"hotword":hotword_id,"source":source})
    def parse_detail(self,response):
        items=articleItem()
        event_id=response.meta.get("event_id","")
        hotword_id=response.meta.get("hotword","")
        # source = response.meta.get("source","")
        title = response.xpath("//h1//text()").extract_first()
        if title!=None:
            titl = title.strip()
            content = response.xpath("//div[@id='Content']//p//text()").extract()
            cons = ''.join(content)
            if cons!='':
                items["article_id"]=self.md5_(response.url+hotword_id)
                items["hotword_id"]=hotword_id
                items["event_id"]=event_id
                items["title"]=titl
                items["content"]=cons
                items["images"]=""
                items["release_time"]=time.strftime("%Y-%m-%d")
                items["qa"]=""
                items["source"]=urlparse(response.url).netloc
                items["author"]=""
                items["url"]=response.url
                items["entity"]=""
                items["label"]=[]
                items["summary"]=[]
                items["time_stamp"]=int(time.time())
                items["priority"]=0
                items["nlp_state"]=0
                items["static_page"]=0
                s1 = {'hotword_id': hotword_id}
                s2 = {'$set': {'article_state': 1}}
                self.client.dailypops.hotword.update(s1,s2)
                yield items

    def md5_(self, str):
        md5 = hashlib.md5()
        data = str
        md5.update(data.encode('utf-8'))
        return md5.hexdigest()
if __name__ == '__main__':
    chinadaily=CrawlerProcess()
    chinadaily.crawl(Chinadaily)
    chinadaily.start()




