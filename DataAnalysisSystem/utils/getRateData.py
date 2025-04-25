from utils import get_df,typeList
import numpy,re

def getAllTypes():
    return list(set(typeList('types')))

def getRateDataByType(type):
    df = get_df()
    if type == 'all':
        rate_list = df['rate'].values
        rate_list.sort()
        # average_rating = rate_list.mean()  # 使用 numpy 的 mean 方法计算平均值
    else:
        type_list = df['types'].map(lambda x :x.split(sep=','))
        old_rate_list = df['rate'].values
        rate_list = []
        for i,item, in enumerate(type_list):
            if type in item:
                rate_list.append(old_rate_list[i])

    #电影评分字典
    rateObj = {}
    for i in rate_list:
        if rateObj.get(i,-1) == -1:
            rateObj[i] = 1
        else:
            rateObj[i] = rateObj[i] + 1
    return list(rateObj.keys()),list(rateObj.values())


def getStarsBy(searchName):
    df = get_df()
    stars = list(df.loc[df['title'].str.contains(searchName)]['stars'])[0].split(',')
    searchName = list(df.loc[df['title'].str.contains(searchName)]['title'])[0]
    starsData = [{
        'value':0,
        'name':'5☆'
    },{
        'value': 0,
        'name': '4☆'
    },{
        'value': 0,
        'name': '3☆'
    },{
        'value': 0,
        'name': '2☆'
    },{
        'value': 0,
        'name': '1☆'
    }]
    for i,item in enumerate(stars):
        starsData[i]['value'] = float(re.sub('%','',item))

    return searchName,starsData