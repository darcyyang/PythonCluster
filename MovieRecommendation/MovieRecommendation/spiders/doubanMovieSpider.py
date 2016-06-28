import scrapy
from scrapy.http import Request
from MovieRecommendation.items import MovierecommendationItem
from MovieRecommendation import myConfig
class doubanMovieSpider(scrapy.Spider):
    name = "doubanMovie"
    # allowed_domains = ["dmoz.org"]
    start_urls = [
        "https://movie.douban.com/tag/2005",
        "https://movie.douban.com/tag/2006",
        "https://movie.douban.com/tag/2007",
        "https://movie.douban.com/tag/2008",
        "https://movie.douban.com/tag/2009",
        "https://movie.douban.com/tag/2010",
        "https://movie.douban.com/tag/2011",
        "https://movie.douban.com/tag/2012",
        "https://movie.douban.com/tag/2013",
        "https://movie.douban.com/tag/2014",
        "https://movie.douban.com/tag/2015",
        "https://movie.douban.com/tag/2016"
        # "http://www.baidu.com"
    ]

    def __init__(self):
        super(doubanMovieSpider, self).__init__()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                        'Connection': 'keep-alive',
                        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        # 'Cookie':'bid="+C+9xhDdviA"; __utma=30149280.1224461064.1435281944.1464587297.1464594976.7; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1464594974%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Dn5dIXOIZj94QFE0XY1JUEM5YYA8Y9YG3F7PrIBBVFxdTpVcA8eIqjero539ZeRcs%26wd%3D%26eqid%3D8b7a2eb6000534e40000000557470f0f%22%5D; _pk_id.100001.4cf6=b9a74c2e618bd6ce.1464274710.5.1464594996.1464587295.; ap=1; __utmc=30149280; __utmz=30149280.1464576168.4.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.1511161292.1464576168.1464587297.1464594976.4; __utmc=223695111; __utmz=223695111.1464576168.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _pk_ses.100001.4cf6=*; __utmb=30149280.0.10.1464594976; __utmb=223695111.0.10.1464594976; dbcl2="4020511:YIGQcP71V6Q"; ck=3CcL'
                        }
        # self.cookies = {'bid':' C 9xhDdviA','ck': '3CcL', 'dbcl2': '4020511:YIGQcP71V6Q','ue':'yangxin_xyx@163.com'}

    def make_requests_from_url(self, url):
        return Request(url, dont_filter=True
                       , headers=self.headers
                       # ,cookies=self.cookies
                       )

#https://movie.douban.com/tag/2016?start=20&type=T
    def parse(self, response):
        pageNum = self.get_last_page_number(response)
        currentBaseUrl = response._url
        for currentPageNum in range (0,pageNum):
            nextParseUrl = currentBaseUrl + '?start=' + str(20 * currentPageNum) + '&type=T'
            yield scrapy.Request(nextParseUrl,
                                 callback=self.parse_papg_content)


# paginator.last href
    def get_last_page_number(self,response):
        paginationNums = response.xpath(myConfig.lastPageNumRule)
        return int(paginationNums[0].extract())


    def parse_papg_content(self,response):
        for href in response.xpath(myConfig.movieDetailPageLinkRule):
            href = str(href.extract())
            request =scrapy.Request(href,
                                 callback=self.parse_detail_contents)
            request.meta['original-href'] = response._url
            yield request

    def parse_detail_contents(self, response):
            item = MovierecommendationItem()
            item['itemFrom'] = response.meta['original-href']
            item['link'] = response._url
            item['name'] = response.xpath(myConfig.movieTitleInDetailPageRule).extract()
            #item['keyword'] = sel.xpath(myConfig.keywordRule).extract()
            #item['downloadLink'] = sel.xpath(myConfig.downloadUrlRule).extract()
            #item['name'] = sel.xpath(myConfig.downloadUrlRule).extract()
            item['rating'] = response.xpath(myConfig.movieRating).extract()
            item['desc'] = response.xpath(myConfig.movieBriefDescription).extract()
            # item['tags'] = sel.xpath(myConfig.downloadUrlRule).extract()
            item['actors'] = response.xpath(myConfig.movieMainStars).extract()
            # item['longDesc'] = sel.xpath(myConfig.downloadUrlRule).extract()
            item['age'] = response.xpath(myConfig.movieYearInDetailPageRule).extract()
            item['genre'] = response.xpath(myConfig.movieGenre).extract()
            # item['area'] = sel.xpath(myConfig.downloadUrlRule).extract()
            # item['language'] = sel.xpath(myConfig.downloadUrlRule).extract()
            item['releaseDate'] = response.xpath(myConfig.movieReleaseDate).extract()
            item['runtime'] = response.xpath(myConfig.movieRuntime).extract()
            yield item

    def convertToUTF8(self,htmlUnicode):
            for element in htmlUnicode:
                element.encode('utf-8')