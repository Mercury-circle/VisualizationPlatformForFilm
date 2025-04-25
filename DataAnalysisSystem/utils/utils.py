import pandas as pd
from sqlalchemy import create_engine

# 定义数据库引擎创建函数
con = create_engine('mysql+pymysql://root:123456@localhost:3306/db_movie')
df = pd.read_sql('select * from movie', con=con)

def get_df():
    return df
def typeList(columnName):
    df = get_df()
    # 获取指定列的数据，并确保不是 None
    column_data = df[columnName].dropna().values
    # 将数据分割成列表
    type_list = []
    for item in column_data:
        if item is not None:
            type_list.extend(item.split(','))
    return type_list


