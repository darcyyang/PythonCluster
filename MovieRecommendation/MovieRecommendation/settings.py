# -*- coding: utf-8 -*-

# Scrapy settings for MovieRecommendation project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'MovieRecommendation'

SPIDER_MODULES = ['MovieRecommendation.spiders']
NEWSPIDER_MODULE = 'MovieRecommendation.spiders'

FEED_EXPORTERS_BASE = {
    'json': 'scrapy.contrib.exporter.JsonItemExporter'
}


ITEM_PIPELINES = {
    'MovieRecommendation.itemProcessors.writer.JsonExportPipeline': 300}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'MovieRecommendation (+http://www.yourdomain.com)'

RETRY_TIMES = 5
# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]

DOWNLOADER_MIDDLEWARES = {
    # add fack bid on headers
    "MovieRecommendation.middlewares.douban_middlewares.CustomUserAgentMiddleware": 60,
    "MovieRecommendation.middlewares.douban_middlewares.CustomCookieMiddleware": 62,
    "MovieRecommendation.middlewares.douban_middlewares.CustomHeadersMiddleware": 66,


    # Fix path to this module
    # using proxy to avoid 403 forbidden issue
    # 'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 90,
    # 'MovieRecommendation.proxy.randomproxy.RandomProxy': 100,
    # 'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110
}
PROXY_LIST = 'list.txt'

DOWNLOAD_DELAY = 1.5

# AUTOTHROTTLE_ENABLED=True
