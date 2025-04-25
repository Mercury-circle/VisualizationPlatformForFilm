from utils import get_df,typeList

def getRegionData():
    regionList = [item.replace(" ", "") for item in typeList('region')]
    # 电影制片地区字典
    regionObj = {}
    # for i in regionList:
    #     regionObj[i] = regionObj.get(i, 0) + 1
    #
    # # 对字典按照值进行排序，如果值相同，则按键排序
    # sorted_regionObj = dict(sorted(regionObj.items(), key=lambda item: (item[1], item[0])))
    #
    # # 分别提取排序后的键和值
    # sorted_keys = list(sorted_regionObj.keys())
    # sorted_values = list(sorted_regionObj.values())
    #
    # return sorted_keys, sorted_values
    for i in regionList:
        if regionObj.get(i,-1) == -1:
            regionObj[i] = 1
        else:
            regionObj[i] = regionObj[i] + 1
    return list(regionObj.keys()),list(regionObj.values())

def getLangData():
    langList = [item.replace(" ", "") for item in typeList('lang')]
    # 电影制片地区字典
    langObj = {}
    for i in langList:
        if langObj.get(i,-1) == -1:
            langObj[i] = 1
        else:
            langObj[i] = langObj[i] + 1
    return list(langObj.keys()),list(langObj.values())