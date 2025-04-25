from utils import get_df,typeList

def getDirectorsData():
    dirList = typeList('directors')
    dirObj = {}
    for i in dirList:
        if dirObj.get(i,-1) == -1:
            dirObj[i] = 1
        else:
            dirObj[i] += 1
    dirObj = sorted(dirObj.items(),key=lambda x :x[1],reverse=True)[:20]
    dirRow = []
    dirColumns = []
    for i in dirObj:
        dirRow.append(i[0])
        dirColumns.append(i[1])
    return dirRow,dirColumns


def getActorsData():
    actorList = typeList('actors')
    actorObj = {}
    for i in actorList:
        if actorObj.get(i,-1) == -1:
            actorObj[i] = 1
        else:
            actorObj[i] += 1
    actorObj = sorted(actorObj.items(),key=lambda x :x[1],reverse=True)[:20]
    actorRow = []
    actorColumns = []
    for i in actorObj:
        actorRow.append(i[0])
        actorColumns.append(i[1])
    return actorRow,actorColumns