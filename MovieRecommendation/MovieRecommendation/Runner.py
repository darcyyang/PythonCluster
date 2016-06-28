from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log
from MovieRecommendation.spiders.doubanMovieSpider import doubanMovieSpider
from MovieRecommendation.loadAgent import agentLoader
from scrapy.utils.project import get_project_settings

def setup_crawler():
    spider = doubanMovieSpider()
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()

# agentLoader().checkProxy('59.58.162.141:888','https://movie.douban.com/tag/2016')

setup_crawler()
# #start crawler log
log.start()
# #start reactor loop.
reactor.run()