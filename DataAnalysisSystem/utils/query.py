from pymysql import *

conn = connect(host='localhost',user='root',password='123456',database='db_movie',port=3306)
cursor = conn.cursor()

def querys(sql,params,type='no_select'):
    params = tuple(params)
    #数据库传参
    cursor.execute(sql,params)
    #查询
    if type != 'no_select':
        data_list = cursor.fetchall()
        #提交
        conn.commit()
        #返回
        return data_list
    else:
        conn.commit()
        return '数据库语句执行成功'