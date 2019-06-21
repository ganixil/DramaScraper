#import the scraper 
from scraper import MeijuSetSpider

#scrapy api
from scrapy.import signals,log
from twisted.internet import reactor
from scrapy.crawler import Crawler

def spider_closing(spider):
    """Activates on closing signal of the spider"""
    log.msg("Closing spider", level=log.INFO)
    reactor.stop()

log.start(loglevel = log.DEBUG)

crawler.signals.connect(spider_closing, signal=signals.spider_closed)
crawler.configure()
crawler.crawl(MeijuSetSpider())
crawler.start()
reactor.run()
