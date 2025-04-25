import pandas as pd
import requests
import csv
import os
import re
import json
import time
import random
import pandas
from pymysql import *
from lxml import etree
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:123456@localhost:3306/db_movie')

class spider(object):
    def __init__(self):
        self.spiderUrl = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8'
        self.headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 Edg/133.0.0.0'
        }

    def init(self):
        if not os.path.exists('./tempData.csv'):
            with open('./tempData.csv','w',newline='') as writer_f:
                writer = csv.writer(writer_f)
                writer.writerow(['title','rate','directors', 'actors', 'cover','detailLink', 'year', 'types',
                                 'region', 'lang','releaseDate', 'duration', 'commentCount','stars', 'summary', 'comments',
                                 'imgList', 'movieUrl'])

        if not os.path.exists('./spiderPage.txt'):
            with open('./spiderPage.txt','w',encoding='utf8') as f:
                f.write('0\n')

        try:
            conn = connect(host='localhost',user='root',password='123456',database='db_movie',port=3306,
                           charset='utf8mb4')
            sql = '''
                    create table movie(
                        id int primary key auto_increment,
                        title varchar(255),
                        rate varchar(255),
                        directors varchar(255),
                        actors varchar(500),
                        cover varchar(255),
                        detailLink varchar(255),
                        year varchar(255),
                        types varchar(255),
                        region varchar(255),
                        lang varchar(255),
                        releaseDate varchar(255),
                        duration varchar(255),
                        commentCount varchar(255),
                        stars varchar(255),
                        summary varchar(2555),
                        comments text,
                        imgList varchar(2555),
                        movieUrl varchar(255)
                    )
            '''
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
        except:
            pass

    #得到当前爬虫页数
    def get_page(self):
        with open('./spiderPage.txt','r') as r_f:
            return r_f.readlines()[-1].strip()

    #建立新的一页
    def set_page(self,newPage):
        with open('./spiderPage.txt','a') as w_f:
            w_f.write(str(newPage) + '\n')

    def spiderMain(self):
        page = self.get_page()
        params = {
            'page_start':int(page) * 20
        }
        print('正在爬取第{}页'.format(int(page)+1))
        respJson = requests.get(self.spiderUrl, headers=self.headers, params=params).json()
        respJson = respJson['subjects']
        resList = []

        for index,movieData in enumerate(respJson):
            print('正在爬取第%d条'%(index+1))
            resData = []
            #电影名称（title）
            resData.append(movieData['title'])
            #电影评分（rate）
            resData.append(movieData['rate'])

            #向详情页发送请求
            respDetailHTML = requests.get(movieData['url'], headers=self.headers)
            respDetailHTMLXpath = etree.HTML(respDetailHTML.text)

            #电影导演（directors）
            directors = []
            for i in respDetailHTMLXpath.xpath('//*[@id="info"]/span[1]/span[@class="attrs"]/a'):
                directors.append(i.text)
            resData.append(','.join(directors))
            #电影演员（actors）
            actors = []
            for i in respDetailHTMLXpath.xpath('//*[@id="info"]/span[3]/span[@class="attrs"]/a'):
                actors.append(i.text)
            resData.append(','.join(actors))
            #电影封面（cover）
            resData.append(movieData['cover'])
            #电影详情链接（detailLink）
            resData.append(movieData['url'])
            #电影年份（year）
            year = re.search('\d+',respDetailHTMLXpath.xpath('//*[@id="content"]/h1/span[2]/text()')[0]).group()
            resData.append(year)
            #电影类型（types）
            types = []
            for i in respDetailHTMLXpath.xpath('//*[@id="info"]/span[@property="v:genre"]'):
                types.append(i.text)
            resData.append(','.join(types))
            #电影制片国家(region)
            textInfo = respDetailHTMLXpath.xpath('//*[@id="info"]/text()')
            texts = []
            for i in textInfo:
                if i.strip() and not i.strip() == '/':
                    texts.append(i)
            resData.append(','.join(texts[0].split(sep='/')))
            #语言（lang）
            resData.append(','.join(texts[1].split(sep='/')))
            #上映日期（releaseDate）
            resData.append(respDetailHTMLXpath.xpath('//*[@id="info"]/span[@property="v:initialReleaseDate"]/@content')[0][:10])
            #电影片长（duration）
            # resData.append(respDetailHTMLXpath.xpath('//*[@id="info"]/span[@property="v:runtime"]/@content')[0])
            try:
                # 尝试获取片长数据
                runtime = respDetailHTMLXpath.xpath('//*[@id="info"]/span[@property="v:runtime"]/@content')[0]
                resData.append(runtime)
            except IndexError:
                # 如果没有找到数据，添加说明
                resData.append(0)
            #短评个数（commentCount）
            commentCount = re.search('\d+',respDetailHTMLXpath.xpath('//*[@id="comments-section"]/div[@class="mod-hd"][1]/h2//a/text()')[0]).group()
            resData.append(commentCount)
            #电影星级占比
            stars = []
            for i in respDetailHTMLXpath.xpath('//*[@id="interest_sectl"]//div[@class="ratings-on-weight"]/div[@class="item"]'):
                stars.append(i.xpath('./span[@class="rating_per"]/text()')[0])
            resData.append(','.join(stars))
            #电影简介（summary）
            try:
                resData.append(respDetailHTMLXpath.xpath('//*[@id="link-report-intra"]//span[@property="v:summary"]/text()')[0].strip())
            except IndexError:
                # 如果没有找到数据，添加说明
                resData.append('暂无简介')
            #电影短评（comments）
            comments = []
            commentsList = respDetailHTMLXpath.xpath('//*[@id="hot-comments"]/div')
            for i in commentsList:
                user = i.xpath('.//h3/span[@class="comment-info"]/a/text()')[0]
                try:
                    star_class = i.xpath('.//h3/span[@class="comment-info"]/span[2]/@class')[0]
                    star = re.search(r'\d+', star_class).group()
                except (IndexError, AttributeError):
                    star = '未评分'
                postTime = i.xpath('.//h3/span[@class="comment-info"]/span[@class="comment-time "]/@title')[0]
                content = i.xpath('.//p[@class=" comment-content"]/span/text()')[0]
                comments.append({
                    'user':user,
                    'star':star,
                    'postTime':postTime,
                    'content':content
                })
            resData.append(json.dumps(comments))
            #图片列表（ImgList)
            imgList = []
            #这里有点电影图片url的分割问题！！！
            resData.append(','.join(respDetailHTMLXpath.xpath('//ul[@class="related-pic-bd  "]//img/@src')))
            #电影预告片链接
            try:
                movieUrl = respDetailHTMLXpath.xpath(
                    '//ul[@class="related-pic-bd  "]/li[@class="label-trailer"]/a/@href')[0]
                movieHTML = requests.get(movieUrl, headers=self.headers)
                movieHTMLXpath = etree.HTML(movieHTML.text)
                resData.append(movieHTMLXpath.xpath('//video/source/@src')[0])
            except:
                resData.append(0)
            resList.append(resData)
            time.sleep(random.uniform(2, 5))  # 随机等待1到5秒
            break

        self.save_to_csv(resList)
        self.set_page(int(page)+1)
        self.clear_csv()
        self.spiderMain()

    #保存为csv文件
    def save_to_csv(self,resList):
        with open('./tempData.csv','a',newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            for rowData in resList:
                writer.writerow(rowData)

    #数据清洗
    def clear_csv(self):
        df = pd.read_csv('./tempData.csv')
        df.dropna(inplace=True)    #删除缺失值
        df.drop_duplicates()  # 删除重复值
        self.save_to_sql(df)

    #存入数据库
    def save_to_sql(self,df):
        # 读取CSV文件
        pd.read_csv('./tempData.csv', encoding='utf-8')

        # 将DataFrame保存到MySQL数据库
        df.to_sql('movie', con=engine, index=False, if_exists='append')
        print('saved')



if __name__ == '__main__':
    spiderObj = spider()
    spiderObj.init()
    # spiderObj.spiderMain()
    # df = pd.read_csv('./tempData.csv', encoding='utf-8')
    # spiderObj.save_to_sql(df)




