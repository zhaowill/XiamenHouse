import scrapy
from scrapy import Field

class XiamenHouseItem(scrapy.Item):
    title = Field()
    price = Field()
    downPayment = Field()
    sizeType = Field()
    size = Field()
    unitPrice = Field()
    orientation = Field()
    floor = Field()
    decoration = Field()
    community = Field()
    region = Field()
    school = Field()
    houseDetail = Field()
    keySellingPoint = Field()
    equipment = Field()