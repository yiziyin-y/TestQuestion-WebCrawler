# -*- coding: utf-8 -*-

from BS.items import QuestionItem
from lxml import etree
import requests
import urllib
import time
import os
import scrapy
import sys

from BS import glo
reload(sys)
sys.setdefaultencoding('utf-8')


class QuestionSpider(scrapy.Spider):

    global subject
    inputType = glo.inputType
    inputUrl = glo.inputUrl
    print("InputType:" + inputType)
    print("InputUrl:" + inputUrl)
    name = "BS"
    subject = inputType
    start_urls = [inputUrl]
    # subject = "test"
    # start_urls = [
    #     'https://tiku.21cnjy.com/tiku.php?mod=quest&channel=6&cid=0&type=5&xd=3',
    # ]

    def parse(self, response):
        global queImgName
        global awImgName
        global i
        i = 1

        for question in response.xpath('//div[@class="questions_col"]/ul/li'):
            time.sleep(0.6)
            # 解析网页源码， 替换去除img标签头尾保留img的超链接于文字之间
            page = response.text.decode('UTF-8')
            page = page.replace('<img src="', '')
            page = page.replace('" style="vertical-align:middle;"/>', '')
            page = page.replace('" style="vertical-align:middle;" />', '')
            selectorQ = etree.HTML(page)
            # 计数器转换为字符以插入xpath语句
            iStr = str(i)
            # 根据计数器确定题目所在格子
            q = selectorQ.xpath(
                'string(//div[@class="questions_col"]/ul/li[' + iStr + '])')

            # 依照response自带方法寻找标签 .extract()抽取为列表  .get()抽取为字符串
            # q = question.xpath('string(.)').get()
            i = question.xpath('./img/@src').extract()
            a = question.css('a.view_all::attr(href)').get()

            # 处理提取到的题目字符串，去除查看解析，添加到组卷等不必要字符
            que1 = q.strip()
            que2 = que1[:-11]
            que = "题目：" + que2
            print("que:" + que)

            #  保存问题图片(支持多个图片)
            if i is not None:
                for queImages in i:
                    print("queImages: " + queImages)
                    req = requests.get(url=queImages)
                    # 截取试题图片文件名
                    queImgName = queImages[38:]
                    queSavePath = r'D:\IntelliJ_IDEA2018.1.6\workspace\BS\queImages'
                    if not os.path.exists(queSavePath):
                        os.makedirs(queSavePath)
                    with open(queSavePath + '\\' + queImgName, "wb") as f:
                        f.write(req.content)
                    f.close()

            #  拼接答案页url
            awUrl = "https://tiku.21cnjy.com/" + str(a)
            #  打开并解析答案页url
            print("awUrl:" + awUrl)
            data = urllib.urlopen(awUrl).read()
            data2 = data.decode('UTF-8')
            selector = etree.HTML(data2)
            #  答案页xpath定位,自动解析为列表
            #  string()之后解析为字符串
            aw = selector.xpath(
                "string(/html/body/div[@class='content']/div[@class='shiti_answer']"
                "/div[@class='answer_detail']/dl/dd/p[1]/i)")
            analyze = selector.xpath(
                "string(/html/body/div[@class='content']/div[@class='shiti_answer']"
                "/div[@class='answer_detail']/dl/dd/p[2]/i)")
            awImage = selector.xpath(
                "/html/body/div[@class='content']/div[@class='shiti_answer']/"
                "div[@class='answer_detail']/dl/dd/p[1]/i/img/@src")


            #  保存答案图片(支持多张图片)
            if awImage is not None:
                #   从列表取出
                for awImages in awImage:
                    print("awimages: " + awImages)

                    req2 = requests.get(url=awImages)
                    awImgName = awImages[38:]                   # 截取答案图片文件名
                    awSavePath = r'D:\IntelliJ_IDEA2018.1.6\workspace\BS\awImages'
                    if not os.path.exists(awSavePath):
                        os.makedirs(awSavePath)
                    with open(awSavePath + '\\' + awImgName, "wb") as f:
                        f.write(req2.content)
                    f.close()

            item = QuestionItem()

            item["ques"] = que

            if i:
                i = str(i)
                print(i)
                item["quesImage"] = i
            else:
                i = ' '
                item["quesImage"] = i

            item["answer_url"] = awUrl

            item["answer"] = "答案：" + aw

            item["analyze"] = analyze
            if awImage:
                awImage1 = awImage[0].strip()
                awImage = "答案图片：" + awImage1
            else:
                awImage = ' '
            item["awImage"] = awImage

            yield item
            #  循环一次计数器+1
            i = int(iStr) + 1
        # 翻页
        next_page = response.css('a.nxt::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
            # 换页时计数器清零
            i = 1
            nextPage = "https://tiku.21cnjy.com/" + next_page
