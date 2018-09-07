from flask import Flask, render_template, request, redirect, Markup, session
import functools

# PEP8
app = Flask(__name__)  # 实例化flask对象
app.secret_key = "123asdzxc"

STUDENT_DICT = {
    1: {'name': 'Old', 'age': 38, 'gender': '中'},
    2: {'name': 'Boy', 'age': 73, 'gender': '男'},
    3: {'name': 'EDU', 'age': 84, 'gender': '女'},
}


@app.route("/login", methods=["POST", "GET"])
def login():
    print(request.method)  # 获得当前请求的方式
    if request.method == "GET":
        # print(request.args["id"])  # 获取GET请求时，URL参数
        # print(request.args.get("username"))  # 获取GET请求时，URL参数
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]  # 获取POST请求时，FormData中的参数
        password = request.form.get("password")
        if username == "nut" and password == "123":
            session["username"] = username
            return redirect("/index")
        else:
            return render_template("login.html", msg="用户名密码错")

    # print(request.values.to_dict())  # 坑FormData参数会被URL参数覆盖
    print(request.data)  # Content-Type: None
    print(request.json)  # Content-Type: application/json
    print(request.headers)  # 请求头
    print(request.url)  # url地址：http://127.0.0.1:9527/login?id=123&username=dsb
    print(request.path)  # /login

    return render_template("login.html")


# def wrap(*args, **kwargs):
#     def wrapper(func):
#         @functools.wraps(func)
#         def inner(*args, **kwargs):
#             if session['username']:
#                 ret = func(*args, **kwargs)
#                 return ret
#             else:
#                 return redirect('/login')
#         return inner
#     return wrapper


def wai(func):
    def inner(*args, **kwargs):
        print('session.get("user")', session.get("user"))
        if session.get("user"):
            ret = func(*args, **kwargs)
            return ret
        else:
            return redirect("/login")

    return inner


@app.template_global()
def a_b(a, b):
    return a * b


@app.template_filter()
def a_b_c(a, b, c):
    return a * b * c


@app.route("/index")
@wai
def index():
    print('app.secret_key', app.secret_key)
    btn = "<a href='/add_stu'>添加学生</a>"
    btn = Markup(btn)
    return render_template("index.html", stu=STUDENT_DICT, btn=btn)


@app.route("/detail")
def detail():
    if request.method == "GET":
        id = request.args["id"]
        stu = STUDENT_DICT.get(int(id))
        return render_template("detail.html", stu=stu, id=id)


@app.route("/delete/<int:id>")
def delete(id):
    print(type(id), id)
    STUDENT_DICT.pop(id)

    return redirect("/index")


@app.route("/inc")
def inc():
    return render_template("inc.html", stu=STUDENT_DICT)


if __name__ == '__main__':
    app.run("0.0.0.0", 9527, debug=True)
