import requests
from lxml import etree
import time
import csv


def Get(url):
    url = url
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Requests": "https://movie.douban.com/cinema/nowplaying/harbin/"
    }
    response = requests.get(url=url, headers=headers)
    tree = etree.HTML(response.text)
    return tree


def Value(tree):
    value = {}
    name = tree.xpath('//*[@id="content"]/h1/span[1]/text()')[0].strip()  # 片面
    value['片名'] = name
    year = tree.xpath('/html/body/div[3]/div[1]/h1/span[2]/text()')[0].strip()[1:-1]  # 上映的时间
    value['上映时间'] = year
    director = tree.xpath('/html/body/div[3]/div[1]/div/div[1]/div[1]/div[1]/div[1]/div[2]/span[1]/span[2]/a/text()')[
        0].strip()  # 导演
    value['导演'] = director
    try:
        scoer = tree.xpath('/html/body/div[3]/div[1]/div/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/strong/text()')[
            0].strip()
        value['评分'] = scoer
    except:
        value['评分'] = "暂无评分"
    actors_F = tree.xpath('/html/body/div[3]/div[1]/div/div[1]/div[1]/div[1]/div[1]/div[2]/span[3]/span[2]//text()')
    actors = [i for i in (actors_F) if actors_F.index(i) % 2 == 0]
    value['主演'] = actors
    try:
        property_value = tree.xpath('//span[@property="v:runtime"]/text()')[0]
        value['片长'] = property_value
    except:
        value['片长'] = "暂无信息"
    try:
        specific_time = tree.xpath('//span[@property="v:initialReleaseDate"]/text()')[0]
        value['具体上映日期'] = specific_time
    except:
        value['具体上映日期'] = "暂无信息"

    return value


# 写入信息
f = open("nowplaying.csv", "w", newline="", encoding="utf-8")
write = csv.DictWriter(f, ['片名', '上映时间', '导演', '评分', '主演', '片长', '具体上映日期'])
write.writeheader()

tree = Get("https://movie.douban.com/cinema/nowplaying/shantou/")
lis = tree.xpath('//div[@id="nowplaying"]/div[2]/ul/li')  # 找到正在上映的标签下的所有值
# print(lis)
href_s = lis[0].xpath('//li[@class="stitle"]/a/@href')  # 获取所有的标签
for href in range(len(href_s)):
    href_s[href] = href_s[href].strip()
    print(f"第 {href + 1} 部电影的信息如下")
    result_value = Value(Get(href_s[href]))
    print(result_value)
    write.writerow(result_value)
    print("=" * 8)
    time.sleep(5)

f.close()
