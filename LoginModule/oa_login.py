from flask import Flask, Response, redirect, url_for, request, session, abort, jsonify
from flask_login import LoginManager, UserMixin, \
    login_required, login_user, logout_user, current_user
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

# config
app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx'
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# silly user model
class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)


# create some users with ids 1 to 20
users = [User(id) for id in range(1, 21)]


# some protected url
@app.route('/home')
@login_required
def home():
    print("home")
    return Response("Hello World!")


# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        data = request.get_json(silent=True)
        print("post data:{}".format(str(data)))

        szRequestUserName = data.get('username')
        szRequestPassword = data.get('password')
        user = User(2)
        bSucceed = login_user(user)
        print("user form: {} {}".format(current_user, current_user.is_authenticated))
        returnData = {'code': 1, 'msg': 'succeed', 'data': {'tips': 'login succeed'}}
        return jsonify(returnData)
    else:
        print("user form: {} {}".format(current_user, current_user.is_authenticated))
        print("else")
        returnData = {'code': 1, 'msg': 'succeed', 'data': {'tips': 'login succeed'}}
        return jsonify(returnData)


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    print("logout!!!!!")
    returnData = {'code': 1, 'msg': 'succeed', 'data': {'tips': 'login succeed'}}
    return jsonify(returnData)


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    print("into user loader:{}".format(userid))
    return User(userid)


if __name__ == "__main__":
    app.run()

# import random
# import sys
# import datetime
# sys.path.append('..')
# sys.path.append('..\\LoginModule')
# sys.path.append('..\\oa-flask\\DataBaseModels')
# sys.path.append('..\\oa-flask\\DataBaseModels\\CustomerModels')
# sys.path.append('..\\oa-flask\\DataBaseModels\\UserModels')
#
# from flask import request, jsonify, session, Blueprint, redirect, Response
# from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
# from LoginModule.login_def import LoginFormKey
# # import login_token as login_token
# from FileDownloadModule.file_download_upload import DownloadCtrl
# from DataBaseModels.UserModels.user_models import EmployeeManager, EmployeeModelBase
#
# from flask import Flask
# # from router import app, cors
# from flask_cors import CORS, cross_origin
# from flask_login import LoginManager
#
# # auth_flask_login = Blueprint('auth_flask_login', __name__)
# DURATION_SEC = datetime.timedelta(seconds=60)
#
# # print("loginmanager:{}".format(ServerInstance.login_manager.login_view))
#
# FlaskApp = Flask(__name__)
# FlaskApp.secret_key = "FlaskOaSystem"
# cors = CORS(FlaskApp)
#
# login_manager = LoginManager()
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'
# login_manager.login_message = '请登录'
# login_manager.init_app(FlaskApp)
#
#
# # silly user model
# class User(UserMixin):
#
#     def __init__(self, id):
#         self.id = id
#         self.name = "user" + str(id)
#         self.password = self.name + "_secret"
#
#     def __repr__(self):
#         return "%d/%s/%s" % (self.id, self.name, self.password)
#
#
# @login_manager.user_loader
# def load_user(userid):
#     print("into user loader:{}".format(userid))
#     return User(userid)
#
#     EmployeeObj = EmployeeManager.GetUserModelByUserID(userid)
#     print("load_user: {}".format(userid))
#     if EmployeeObj is None:
#         print("yesr: {}".format(userid))
#         return EmployeeManager.CreateNewEmployeeModelByUserID(userid)
#     else:
#         print("no: {}".format(userid))
#         return EmployeeObj
#
#
# # handle login failed
# @FlaskApp.errorhandler(401)
# def page_not_found(e):
#     return Response('<p>Login failed</p>')
#
#
# @FlaskApp.route('/home', methods=['GET', 'POST'])
# @login_required
# def home():
#     print("home")
#     return Response('''
#     <form action="" method="post">
#         <p><input type=text name=username>
#         <p><input type=password name=password>
#         <p><input type=submit value=Login>
#     </form>
#     ''')
#
#
# # @app.route('/')
# # @login_required
# # def index():
# #     return 'Logged in as: %s' % current_user.get_id()
#
# @FlaskApp.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         data = request.get_json(silent=True)
#         print("post data:{}".format(str(data)))
#
#         szRequestUserName = data.get(LoginFormKey.EMPLOYEE_NAME)
#         szRequestPassword = data.get(LoginFormKey.EMPLOYEE_PASSWORD)
#         print("user form: {} {}".format(szRequestUserName, szRequestPassword))
#
#         user = User(1)
#         login_user(user)
#         returnData = {'code': 1, 'msg': 'succeed', 'data': {'tips': 'login succeed'}}
#         return jsonify(returnData)
#
#         # if szRequestPassword is None or szRequestUserName is None:
#         #     returnData = {'code': -1, 'msg': 'failed', 'data': {'tips': 'username or password is not correct'}}
#         #     return jsonify(returnData)
#         #
#         # LoginEmployeeObj = EmployeeManager.GetUserModelByNameAndPassword(szRequestUserName, szRequestPassword)
#         # if LoginEmployeeObj is None:
#         #     # 校验失败
#         #     returnData = {'code': -1, 'msg': 'failed', 'data': {'tips': 'username or password is not correct'}}
#         #     return jsonify(returnData)
#         # else:
#         #     bLoginSucceed = login_user(LoginEmployeeObj, remember=True) # , duration=DURATION_SEC)
#         #     print("login succeed: {}".format(bLoginSucceed))
#         #     returnData = {'code': 1, 'msg': 'succeed', 'data': {'tips': 'login succeed'}}
#         #     return jsonify(returnData)
#
#     # GET 请求
#     # return render_template('login.html')
#     # token = login_token.create_token(g.user_id)
#     # return jsonify({'token': token})
#     returnData = {'code': 1, 'msg': 'failed', 'data': {'tips': 'username or password is not correct'}}
#     return jsonify(returnData)
#
#
# @FlaskApp.route('/logout', methods=['GET', 'POST'])
# @login_required
# def logout():
#     # logout_user()
#     print("logout")
#     returnData = {'code': 1, 'msg': 'failed', 'succeed': {'tips': 'Logged out successfully!'}}
#     return jsonify(returnData)
#
#
# @FlaskApp.route('/register', methods=['GET', 'POST'])
# def NewEmployeeRegister():
#     """
#     对应注册页面
#     :return:
#     """
#     if request.method == 'POST':
#         data = request.get_json(silent=True)
#         print("register in ：{}".format(str(data)))
#         bRegisterSucceed, szContent = EmployeeManager.RegisterNewModel(data)
#         returnData = {'code': 1, 'msg': str(bRegisterSucceed), 'data': {'tips': szContent}}
#         print("tips:{}".format(szContent))
#
#         return jsonify(returnData)
#
#     returnData = {'code': -1, 'msg': 'failed', 'data': {'tips': 'register false'}}
#     return jsonify(returnData)
#
#
# @FlaskApp.route('/download', methods=['GET', 'POST'])
# def DownloadFile():
#     print("begin download")
#     szFileName = request.form.get('filename', None)
#     if szFileName is None:
#         # 默认下载文件
#         return DownloadCtrl.DownloadFile("29.mp4")
#
#     print("szFileName: {}".format(szFileName))
#     return DownloadCtrl.DownloadFile(szFileName)
#
#
# @FlaskApp.route('/upload', methods=['GET', 'POST'])
# def UploadFile():
#     print("begin upload")
#     name = request.form.get("name")
#     description = request.form.get("description")
#     fileObj = request.files.get("file")
#     fileObj.save("E://store.jpg")
#     print("szFileName: {}".format(fileObj.filename))
#     return jsonify({'tips': "succeed"})
#
#
# @FlaskApp.route('/autoroute/<username>', methods=['GET', 'POST'])
# def TestAutoRoute(username):
#     print("username:{}".format(username))
#
#
# if __name__ == '__main__':
#     FlaskApp.run(debug=True)
