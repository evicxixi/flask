from flask import Flask, render_template, request, redirect, Markup, session
import functools
import pymysql
from settings import Settings
from settings import STUDENT_DICT

# PEP8
app = Flask(__name__)  # 实例化flask对象
app.secret_key = Settings.SECRET_KEY
# app.DEBUG = True # 暂不起效

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root',
                       password='', db=Settings.DB, charset='utf8')
cursor = conn.cursor()


def get_student_dict(cursor):

    sql = 'select * from employee'
    cursor.execute(sql)  # 使用execute()防止sql注入
    student_set = cursor.fetchall()
    student_dict = {}
    for student in student_set:
        student_dict[student[0]] = {
            'name': student[1],
            'age': student[3],
            'gender': student[2],
        }
    return student_dict


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template('index.html', title='Students Manage System')


@app.route('/login/', methods=["POST", "GET"])
def login():

    if request.method == "GET":
        # print(STUDENT_DICT)
        return render_template('login.html')

    # print('request.form', request.form)
    # print('request.data', request.data)
    # print('request.args', request.args)
    # print('request.json', request.json)
    # print('request.values', request.values)
    # print('request', request)
    username = request.form.get("username")  # 获取POST请求时，FormData中的参数
    password = request.form.get("password")
    if username == 'nut' and password == '123':
        session['username'] = username
        return redirect('/student')
    else:
        return render_template('login.html', msg='用户名密码错误')


@app.route('/student/', methods=["POST", "GET"])
def student():
    if request.method == 'GET':
        student_dict = get_student_dict(cursor)
        return render_template('student.html', student_dict=student_dict)


@app.route('/student/add/', methods=["POST", "GET"])
def student_add():
    if request.method == 'GET':
        return render_template('student_edit.html')

    ret = (request.form.get('name'), int(request.form.get(
        'age')), '0000-00-00')
    # "insert into user(name,pwd,hire_date) values(%s,%s)"
    sql = 'insert into employee(name,age,hire_date) values(%s,%s,%s)'
    cursor.execute(sql, ret)
    return redirect('/student')


@app.route('/student/edit/<id>', methods=["POST", "GET"])
def student_edit(id):
    id = int(id)
    if request.method == 'GET':
        student_dict = get_student_dict(cursor)
        student = student_dict.get(id)
        return render_template('student_edit.html', student=student)

    ret = (request.form.get('name'), int(request.form.get(
        'age')), id)
    sql = 'update employee set name=%s,age=%s where id=%s'
    cursor.execute(sql, ret)
    return redirect('/student')


if __name__ == '__main__':
    app.run("0.0.0.0", 9527, debug=True)
