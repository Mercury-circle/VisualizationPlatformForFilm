import numpy,copy
import pandas as pd

from flask import Flask, request, render_template, session, redirect, jsonify
from utils import query
from utils.getFilmData import *
from utils.getSearchData import *
from utils.getTimeData import *
from utils.getRateData import *
from utils.getRegionData import *
from utils.getDirActorData import *
from utils.getCommentsCloud import *
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'This is secret_key you know ?'



#路由，视图函数
#登录
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # 查询用户信息
        users = query.querys("SELECT * FROM user WHERE email = %s", (email,), 'select')

        # 检查是否找到了用户并且密码匹配
        user_found = False
        for user in users:
            if user[1] == email and user[2] == password:  # 直接比对邮箱和密码
                user_found = True
                session['email'] = email
                session['role'] = user[3]  # 假设角色字段是元组中的第四个元素

                if user[3] == 1:  # 如果角色为1，表示管理员
                    return redirect('/home')
                else:
                    return redirect('/userhome')  # 普通用户

        if not user_found:
            return render_template('error.html', message='邮箱或密码错误')

#退出登录
@app.route('/loginOut')
def loginOut():
    session.clear()
    return redirect('/login')

#生命周期
@app.before_request
def before_requre():
    pat = re.compile(r'^/static')
    if re.search(pat,request.path):
        return
    if request.path == '/login':
        return
    if request.path == '/register':
        return
    email = session.get('email')
    if email:
        return None

    return redirect('/login')

#注册
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        request.form = dict(request.form)
        print(request.form)
        if request.form['password'] != request.form['passwordChecked']:
            return render_template('error.html',message='两次密码不一致')
        def filter_fn(item):
            return request.form['email'] in item

        users = query.querys('select * from user',[],'select')
        filter_list = list(filter(filter_fn,users))
        if len(filter_list):
            return  render_template('error.html',message='该用户已被注册')
        else:
            query.querys('insert into user(email,password) values(%s,%s)',[request.form['email'],request.form['password']])
            return redirect('/login')


#电影从业用户端
#主页
@app.route('/home',methods=['GET','POST'])
def home():
    email = session.get('email')
    movieCount,maxRate,maxActors,maxRegion,typeCount,maxLang = getFilmData()
    typeDic = getTypesPieChart()
    row,columns = getRateLineChart()
    filmInfoTable = getFilmInfoTable()
    return render_template(
        'index.html',
        email = email,
        movieCount = movieCount,
        maxRate = maxRate,
        maxActors = maxActors,
        maxRegion = maxRegion,
        typeCount = typeCount,
        maxLang = maxLang,
        typeDic = typeDic,
        row = row,
        columns = columns,
        filmInfoTable = filmInfoTable,
    )

#电影预告片（By Id）
@app.route('/moviepre/<int:movieId>',methods=['GET','POST'])
def moviePre(movieId):
    movieUrl = getMovieUrlById(movieId)
    return render_template('movie.html',movieUrl=movieUrl)

#搜索（）
@app.route('/search/<int:movieId>',methods=['GET','POST'])
def search(movieId):
    email = session.get('email')
    if request.method == 'GET':
        movieDetails = getMovieDetialsById(movieId)
    else:
        request.form = dict(request.form)
        movieDetails = getMovieDetialsByWords(request.form['searchWords'])
    return  render_template(
        'search.html',
        email=email,
        movieDetails=movieDetails)

#时间分析表
@app.route('/chart/time')
def timeChart():
    email = session.get('email')
    durationData = getDurationData()
    return render_template(
        'timeChart.html',
        email = email,
        durationData = durationData)

#评分分析表
@app.route('/chart/rate/<type>',methods=['GET','POST'])
def rateChart(type):
    email = session.get('email')
    typeList = getAllTypes()
    row,columns = getRateDataByType(type)
    if request.method == 'GET':
        searchName,starsData = getStarsBy('猫猫的奇幻漂流')
    else:
        request.form = dict(request.form)
        searchName,starsData = getStarsBy(request.form['searchName'])
    return render_template(
        'rateChart.html',
        email = email,
        typeList = typeList,
        type = type,
        row = row,
        columns = columns,
        searchName = searchName,
        starsData = starsData
    )

#地区分析表
@app.route('/chart/region')
def regionChart():
    email = session.get('email')
    row, columns = getRegionData()
    langRow,langColumns = getLangData()
    return render_template(
        'regionChart.html',
        email = email,
        row = row,
        columns = columns,
        langRow = langRow,
        langColumns = langColumns
    )

#导演和演员分析表
@app.route('/chart/D&A')
def dirAndActorChart():
    email = session.get('email')
    dirRow,dirColumns = getDirectorsData()
    actorRow,actorColumns = getActorsData()
    getDirectorsData()
    return render_template(
        'dirAndActorChart.html',
        email = email,
        dirRow = dirRow,
        dirColumns = dirColumns,
        actorRow = actorRow,
        actorColumns = actorColumns
    )

#评论词云图
@app.route('/comment',methods=['GET','POST'])
def commentsWordCloud():
    email = session.get('email')
    if request.method == 'GET':
        return render_template('commentsCloud.html',email=email)
    else:
        searchName,resSrc = getComments(dict(request.form)['searchName'])
        return render_template(
        'commentsCloud.html',
        email = email,
        searchName = searchName,
        resSrc = resSrc
        )

#标题词云图
@app.route('/title',methods=['GET','POST'])
def titleWordCloud():
    email = session.get('email')
    return render_template('titleCloud.html',email=email)



#普通用户端
#主页
@app.route('/userhome',methods=['GET','POST'])
def userHome():
    email = session.get('email')
    movieCount,maxRate,maxActors,maxRegion,typeCount,maxLang = getFilmData()
    typeDic = getTypesPieChart()
    row,columns = getRateLineChart()
    filmInfoTable = getFilmInfoTable()
    typeList = getAllTypes()
    typeRow, typeColumns = getRateDataByType(type)
    return render_template(
        'userIndex.html',
        email = email,
        movieCount = movieCount,
        maxRate = maxRate,
        maxActors = maxActors,
        maxRegion = maxRegion,
        typeCount = typeCount,
        maxLang = maxLang,
        typeDic = typeDic,
        row = row,
        columns = columns,
        filmInfoTable = filmInfoTable,
        typeList = typeList,
        type = type,
        typeRow = typeRow,
        typeColumns = typeColumns
    )


@app.route('/category/', defaults={'type': 'all'})
@app.route('/category/<type>')
def category(type):
    # 获取所有电影数据
    all_films = getFilmInfoTable()

    # 初始化 sort_by 变量，默认为 rate
    sort_by = request.args.get("sort", "popular")

    # 过滤电影数据
    if type == 'all':
        film_list = all_films
    else:
        film_list = [film for film in all_films if type in film[8].split(',')]  # 类型在第8列

    # 深拷贝 film_list 防止污染原始数据
    sorted_film_list = copy.deepcopy(film_list)

    # 根据 sort_by 参数排序
    if sort_by == "rate":
        # 按评分降序排序（rate字段在索引2）
        def convert_rate(rate_str):
            try:
                return float(rate_str) if rate_str.strip() else 0.0
            except ValueError:
                return 0.0  # 如果转换失败，设置一个默认值

        sorted_film_list = sorted(
            sorted_film_list,
            key=lambda x: convert_rate(x[2]),
            reverse=True
        )
    elif sort_by == "releaseDate":
        # 按上映时间降序排序（假设日期字段在索引11）
        def parse_date(date_str):
            try:
                return datetime.strptime(date_str, '%Y-%m-%d')
            except (ValueError, TypeError):
                return datetime.min  # 或者使用其他默认日期

        sorted_film_list = sorted(
            sorted_film_list,
            key=lambda x: parse_date(x[11]) if x[11] not in (None, '') else datetime.min,
            reverse=True
        )

    return render_template(
        'category.html',
        film_list=sorted_film_list,
        current_type=type,
        type_list=getAllTypes(),
        movie_count=len(sorted_film_list),
        sort_by=sort_by
    )


# 电影详情页
@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    # 获取电影详细信息
    movie = getMovieById(movie_id)

    # 处理电影不存在的情况
    if not movie:
        return render_template('404.html'), 404

    # 解析评论数据
    comments = movie.get('comments', [])

    # 处理可能的字符串类型数据
    if isinstance(comments, str):
        try:
            comments = eval(comments)
        except:
            comments = []

    return render_template(
        'movieDetail.html',
        movie=movie,
        comments=comments
    )

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)
    # movie(1)