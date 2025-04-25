import numpy
from flask import Flask,request,render_template,session,redirect
from utils import query
from utils.getFilmData import *
from utils.getSearchData import *
from utils.getTimeData import *
from utils.getRateData import *
from utils.getRegionData import *
from utils.getDirActorData import *
from utils.getCommentsCloud import *

app = Flask(__name__)
app.secret_key = 'This is secret_key you know ?'

#路由，视图函数
#登录
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return  render_template('login.html')
    elif request.method == 'POST':
        request.form = dict(request.form)
        def filter_fn(item):
            return request.form['email'] in item and request.form['password'] in item

        users = query.querys('select * from user',[],'select')
        filter_user = list(filter(filter_fn,users))

        session['email'] = request.form['email']
        if len(filter_user):
            return redirect('/home')
        else:
            return render_template('error.html',message='邮箱或密码错误')

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
@app.route('/movie/<int:movieId>',methods=['GET','POST'])
def movie(movieId):
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


if __name__ == '__main__':
    app.run(debug=True)
    movie(1)