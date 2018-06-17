import time
import pandas as pd
class XiamenhousePipeline(object):
    house_list = []

    def process_item(self, item, spider):
        self.house_list.append(dict(item))
        return item

    def close_spider(self, spider):
        df = pd.DataFrame(self.house_list)
        df.to_excel("厦门房价数据(房天下版).xlsx",columns=[k for k in self.house_list[0].keys()])
        print("爬虫程序共运行{}秒".format(time.process_time()))