import urllib.request

from bs4 import BeautifulSoup

import time

import os

import sys


# 请求url,返回html

def url_open(url):
    req = urllib.request.Request(url)

    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36')

    response = urllib.request.urlopen(req)

    html = response.read()

    return html


# 因为一个村的格式比较特殊，这里采用递归去拿数据

def getChild(domain, child, areaName, parentName):
    # 休眠0.5s

    time.sleep(0.5)

    # 根据class规则找数据，当下一个class找不到数据则表示处理完成，捕获异常直接return

    try:

        childClass = child['class']

    except BaseException:

        return

    # 根据样式判断是市还是区

    if 'cunnavtaga' == childClass[0]:

        if areaName != parentName:

            cityName = parentName + "-" + child.contents[0]

        else:

            cityName = areaName + "-" + child.contents[0]

        print(cityName)

        # 写入文件

        try:

            with open(writePath, 'a') as f:

                f.writelines(cityName + '\r\n')

        except Exception:

            print("插入失败", cityName)

        # 递归找下一个class，child.next_sibling是找下一个标签

        getChild(domain, child.next_sibling, cityName, parentName)

    elif 'cunnavtagb' == childClass[0]:

        districtName = areaName + "-" + child.contents[0].contents[0]

        # print(districtName)

        # 写入文件

        try:

            with open(writePath, 'a') as f:

                f.writelines(districtName + '\r\n')

        except Exception:

            print("插入失败", districtName)

        # 拿到a标签的url，获取区县的html内容。child.find("a")表示拿a标签,get('href')表示拿url

        try:

            districtHtml = url_open(domain + child.find("a").get('href'))

        except Exception:

            print("出异常啦，努力重试中")

            # 速度过快可能会被封掉，休息5S再重试

            time.sleep(5)

            districtHtml = url_open(domain + child.find("a").get('href'))

        # districtHtml = url_open(domain + child.find("a").get('href'))

        districtSoup = BeautifulSoup(districtHtml)

        districtChild = districtSoup.find("div", class_="cunnavtaga")

        getDistrictChild(domain, districtChild, districtName, districtName)

        getChild(domain, child.next_sibling, areaName, parentName)


def getDistrictChild(domain, districtChild, areaName, parentName):
    childClass = districtChild['class']

    # print(childClass)

    if 'cunnavtaga' == childClass[0]:

        districtName = areaName + "-" + districtChild.contents[0]

        # print(districtName)

        try:

            with open(writePath, 'a') as f:

                f.writelines(districtName + '\r\n')

        except Exception:

            print("插入失败", districtName)

        getDistrictChild(domain, districtChild.next_sibling, districtName, parentName)

    elif 'cunnavtagb' == childClass[0]:

        townName = areaName + "-" + districtChild.contents[0].contents[0]

        # print(townName)

        try:

            with open(writePath, 'a') as f:

                f.writelines(townName + '\r\n')

        except Exception:

            print("插入失败", townName)

        try:

            nextClass = districtChild.next_sibling['class']

        except BaseException:

            return

        if 'cunnavtaga' == nextClass[0]:

            getDistrictChild(domain, districtChild.next_sibling, parentName, parentName)

        elif 'cunnavtagb' == nextClass[0]:

            getDistrictChild(domain, districtChild.next_sibling, areaName, parentName)

        else:

            return

        # print(child.contents[0].a.get('href'))


def hand_logic(html, domain):
    print("---------开始抓取数据------------")

    # 根据html转换成bs格式

    provinceSoup = BeautifulSoup(html)

    # 这里是拿到所有的省再遍历，select(".cunpaddingl4")表示拿到所有class=cunpaddingl4的标签

    for provinceLink in provinceSoup.select(".cunpaddingl4"):

        # 获取省名字

        provinceName = provinceLink.contents[0]

        print(provinceName)

        # 存入文档

        try:

            with open(writePath, 'a') as f:

                f.writelines(provinceName + '\r\n')

        except Exception:

            print("插入失败", provinceName)

        # print(link.get('href'))

        # 拿到a标签的url，获取html内容。child.find("a")表示拿a标签,get('href')表示拿url

        try:

            cityHtml = url_open(domain + provinceLink.get('href'))

        except Exception:

            print("出异常啦，努力重试中")

            # 速度过快可能会被封掉，休息5S再重试

            time.sleep(5)

            cityHtml = url_open(domain + provinceLink.get('href'))

        citySoup = BeautifulSoup(cityHtml)

        # 拿到div标签中,class="cunnavtaga"样式的数据

        child = citySoup.find("div", class_="cunnavtaga")

        getChild(domain, child, provinceName, provinceName)

    print("----------数据抓取完成--------")


if __name__ == '__main__':
    # python的递归深度默认最大999，这里设置为1000000

    sys.setrecursionlimit(1000000)

    # 需要先在本地目录下面创建txt文件

    writePath = 'D:\Python\全国五级数据.txt'

    os.remove(writePath)

    url = "http://www.yigecun.com"

    html = url_open(url)

    hand_logic(html, url)

    # print(html)




