#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
import requests
from lxml import etree
import time

if __name__ == '__main__':
    chromedriver = "C:\Python38\chromedriver"
    driver = webdriver.Chrome(executable_path=chromedriver)
    home_url = "https://drugs.dxy.cn"
    driver.get(home_url)  # 打开网址
    cookie1 = {"name": "CLASS_CASTGC",
               "value": "59abc8e78c52098313bc349d45c5c9050adb83c281a3165f79016877480adcb45baf4bfc1e3b16b222064a51b3bad756966757757d19b9aef265690068c98212b0179181736a3075aaf7890a0ab6a9d8a28c3a5bb0d1316f2b2c1ad8fad515b8fbfb98731fa4831bc64ee33b31a015cff1aa3f97063832a3f43d53317f0f36a89ab0e72e7a42693a3e9e984f605e425d66e363aa77008f59f42de37c9552e33e2543a63f122922a47521d42cadbfa39e71d42cd199699c08d2d99c941ac95607038212cadf7d910654f7576ab863a24042ddadde88d548e65a83fcbb5fe2f09be0ad84a30316859fc303b3201385af77d83af1dfed328fe83f193f3594e1538e"}
    cookie2 = {"name": "dxy_da_cookie-id", "value": "2271a6bc57ad28abdc5e0d50bd03aa961619056600265"}
    time.sleep(4)
    driver.add_cookie(cookie1)
    driver.add_cookie(cookie2)
    driver.get(home_url)
    time.sleep(2)

    url = 'https://drugs.dxy.cn/drug/6TvOxP35itE1mepepmplsplsuFYmeJUg=='
    driver.get(url)
    time.sleep(1)
    detail_sel = etree.HTML(driver.page_source)
    t_name = detail_sel.xpath('//div[@class="drug-names__8L2q"]/p[contains(text(),"通用名称")]/text()')
    y_name = detail_sel.xpath('//div[@class="drug-names__8L2q"]/p[contains(text(),"英文名称")]/text()')
    s_name = detail_sel.xpath('//div[@class="drug-names__8L2q"]/p[contains(text(),"商品名称")]/text()')

    print(t_name)
    print(y_name)
    print(s_name)

    context = detail_sel.xpath('//div[@class="content__1KNL"]/p/text()')
    print(context)

    # 用法用量
    drug_tag = detail_sel.xpath('//div[@class="item__3ue7"]')
    info = detail_sel.xpath('//div[@class="content__1KNL"]')
    yfyl = ""
    for a in range(0, len(drug_tag)):
        print('a:'+str(a))
        type = drug_tag[a].xpath('./div[@class="cnName__3Kpx"]/text()')
        print(type)
        if type[1] == '用法用量':
            result = info[a].xpath('./p/text()')
            print(result)
            if (len(result)) > 0:
                yfyl = result[0]
            break
    print('yfyl:'+yfyl)


