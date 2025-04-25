from utils import get_df,typeList

def getFilmData():
    df = get_df()
    # 电影总个数+
    movieCount = len(df.values)
    # 电影最高评分
    maxRate = df['rate'].max()
    # 出场最多演员
    actorsList = typeList('actors')
    maxActors = max(actorsList, key=actorsList.count)
    #制片国家最多数
    regionList = typeList('region')
    maxRegion = max(regionList, key=regionList.count)
    #电影种类数量
    type_list = typeList('types')
    typeCount = len(set(type_list))
    #电影语言最多数
    langList = typeList('lang')
    maxLang = max(langList, key=langList.count)
    return movieCount,maxRate,maxActors,maxRegion,typeCount,maxLang

#热门电影种类饼状图数据
def getTypesPieChart():
    type_list = typeList('types')
    #电影种类字典
    typeObj = {}
    for i in type_list:
        if typeObj.get(i,-1) == -1:
            typeObj[i] = 1
        else:
            typeObj[i] = typeObj[i] + 1
    typeDic = []
    for key,value in typeObj.items():
        typeDic.append({
            'name':key,
            'value':value
        })
    return typeDic

#电影评分折线图数据
def getRateLineChart():
    df = get_df()
    rate_list = df['rate'].map(lambda x :float(x)).values
    rate_list.sort()
    #电影评分字典
    rateObj = {}
    for i in rate_list:
        if rateObj.get(i,-1) == -1:
            rateObj[i] = 1
        else:
            rateObj[i] = rateObj[i] + 1
    return list(rateObj.keys()),list(rateObj.values())

def getFilmInfoTable():
    df = get_df()
    filmInfoTable = df.values
    for i,item in enumerate(filmInfoTable):
        try:
            item[17] = item[17].split(sep=',')
        except:
            pass
    return filmInfoTable

def getMovieUrlById(id):
    df = get_df()
    filmInfoTable = df.values
    return filmInfoTable[id-1][-1]

