from flask import Flask, render_template, request, redirect, Markup, session
import functools
import pymysql
from settings import Settings
from sqlheapler import inquiry, insert

# PEP8
app = Flask(__name__)  # 实例化flask对象
app.secret_key = Settings.SECRET_KEY
# app.DEBUG = True # 暂不起效


def get_student_dict():

    sql = 'select * from user'
    student_set = inquiry(sql, '', num='all')
    print('student_set', student_set)
    student_dict = {}
    for student in student_set:
        student_dict[student['id']] = {
            'id': student['id'],
            'name': student['name'],
            'age': student['age'],
            'sex': 'male' if student['sex'] == 1 else 'female',
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
        student_dict = get_student_dict()
        return render_template('student.html', student_dict=student_dict)


@app.route('/student/add/', methods=["POST", "GET"])
def student_add():
    if request.method == 'GET':
        return render_template('student_edit.html')

    args = (request.form.get('name'), int(request.form.get(
        'age')), int(request.form.get(
            'gender')))
    # print('args', args)
    sql = 'insert into user(name,age,sex) values(%s,%s,%s)'
    insert(sql, args)
    return redirect('/student')


@app.route('/student/edit/<id>', methods=["POST", "GET"])
def student_edit(id):
    id = int(id)
    if request.method == 'GET':
        student_dict = get_student_dict()
        student = student_dict.get(id)
        print('student', student)
        return render_template('student_edit.html', student=student)

    args = (
        request.form.get('name'),
        int(request.form.get('age')),
        int(request.form.get('sex')),
        id)
    print('args', args)

    sql = 'update user set name=%s,age=%s,sex=%s where id=%s'
    insert(sql, args)
    return redirect('/student')


if __name__ == '__main__':
    app.run("0.0.0.0", 9527, debug=True)
