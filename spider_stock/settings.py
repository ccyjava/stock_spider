# -*- coding: utf-8 -*-

# Scrapy settings for spider_stock project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'spider_stock'

SPIDER_MODULES = ['spider_stock.spiders']
NEWSPIDER_MODULE = 'spider_stock.spiders'



download_delay=1
#ITEM_PIPELINES={'spider_stock.pipelines.SpiderStockPipeline':300}
COOKIES_ENABLED=False
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'TTJJ (+http://www.yourdomain.com)'
#取消默认的useragent,使用新的useragent
DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'spider_stock.spiders.ua_middle.UserAgentMiddle':400
    }

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'spider_stock (+http://www.yourdomain.com)'
