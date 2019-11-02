# -*- coding: utf-8 -*-
from scrapy import cmdline
from BS import glo
#
# if __name__==  "__main__":
print("start:%s"%glo.inputType)
cmdline.execute("scrapy crawl BS ".split())
# execute("scrapy crawl BS -o test.csv".split())