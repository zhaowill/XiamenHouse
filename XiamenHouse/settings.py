BOT_NAME = 'XiamenHouse'
SPIDER_MODULES = ['XiamenHouse.spiders']
NEWSPIDER_MODULE = 'XiamenHouse.spiders'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 96
ITEM_PIPELINES = {
   'XiamenHouse.pipelines.XiamenhousePipeline': 300,
}