# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from XiamenHouse.items import XiamenHouseItem
import json
class HouseSpider(scrapy.Spider):
    name = 'house'
    allowed_domains = ['esf.xm.fang.com']
    start_urls = []
    region_dict = dict(
        集美 = "house-a0354",
        翔安 = "house-a0350",
        同安 = "house-a0353",
        海沧 = "house-a0355",
        湖里 = "house-a0351",
        思明 = "house-a0352"
    )
    price_dict = dict(
        d100 = "d2100",
        c100d200 = "c2100-d2200",
        c200d250 = "c2200-d2250",
        c250d300 = "c2250-d2300",
        c300d400 = "c2300-d2400",
        c400d500 = "c2400-d2500",
        c500d600 = "c2500-d2600",
        c600 = "c2600"
    )
    for region in list(region_dict.keys()):
        for price in list(price_dict.keys()):
            url = "http://esf.xm.fang.com/{}/{}/".format(region_dict[region],price_dict[price])
            start_urls.append(url)
    #start_urls共有48个，parse函数的作用是找出这48个分类中每个分类的最大页数
    def parse(self, response):
        pageNum = response.xpath("//span[@class='txt']/text()").extract()[0].strip('共').strip('页')
        for i in range(1,int(pageNum)+1):
            url = "{}-i3{}/".format(response.url.strip('/'),i)
            yield Request(url,callback=self.parse1)

    def parse1(self, response):
        house_list = response.xpath("//div[@class='houseList']/dl")
        for house in house_list:
            if "list" in house.xpath("@id").extract()[0]:
                detailUrl = "http://esf.xm.fang.com" + house.xpath("dd[1]/p/a/@href").extract()[0]
                yield Request(detailUrl,callback=self.parse2)

    def parse2(self, response):
        def find(xpath,pNode=response):
            if len(pNode.xpath(xpath)):
                return pNode.xpath(xpath).extract()[0]
            else:
                return ''
        item = XiamenHouseItem()
        item['title'] = find("//h1[@class='title floatl']/text()").strip()
        item['price'] = find("//div[@class='trl-item_top']/div[1]/i/text()") + "万"
        item['downPayment'] = find("//div[@class='trl-item']/text()").strip().strip("首付约 ")
        item['sizeType'] = find("//div[@class='tab-cont-right']/div[2]/div[1]/div[1]/text()").strip()
        item['size'] = find("//div[@class='tab-cont-right']/div[2]/div[2]/div[1]/text()")
        item['unitPrice'] = find("//div[@class='tab-cont-right']/div[2]/div[3]/div[1]/text()")
        item['orientation'] = find("//div[@class='tab-cont-right']/div[3]/div[1]/div[1]/text()")
        item['floor'] = find("//div[@class='tab-cont-right']/div[3]/div[2]/div[1]/text()") + ' ' + \
                        find("//div[@class='tab-cont-right']/div[3]/div[2]/div[2]/text()")
        item['decoration'] = find("//div[@class='tab-cont-right']/div[3]/div[3]/div[1]/text()")
        item['community'] = find("//div[@class='tab-cont-right']/div[4]/div[1]/div[2]/a/text()")
        item['region'] = find("//div[@class='tab-cont-right']/div[4]/div[2]/div[2]/a[1]/text()").strip() + \
                         '-' + find("//div[@class='tab-cont-right']/div[4]/div[2]/div[2]/a[2]/text()").strip()
        item['school'] = find("//div[@class='tab-cont-right']/div[4]/div[3]/div[2]/a[1]/text()")
        detail_list = response.xpath("//div[@class='content-item fydes-item']/div[2]/div")
        detail_dict = {}
        for detail in detail_list:
            key = find("span[1]/text()",detail)
            value = find("span[2]/text()",detail).strip()
            detail_dict[key] = value
        item['houseDetail'] = json.dumps(detail_dict,ensure_ascii=False)
        item['keySellingPoint'] = '\n'.join(response.xpath("//div[text()='核心卖点']/../div[2]/div/text()").extract()).strip()
        item['equipment'] = '\n'.join(response.xpath("//div[text()='小区配套']/../div[2]/text()").extract()).strip()
        yield item