import json
import sys
sys.path.append('..')
from utils import get_df,typeList
from wordCloud import *
def getComments(searchName):
    df = get_df()
    searchName = list(df.loc[df['title'].str.contains(searchName)]['title'])[0]
    comments = json.loads(df[df['title'] == searchName]['comments'].values[0])
    resSrc = getCommentsImage(comments)
    print(resSrc)
    return searchName,resSrc

