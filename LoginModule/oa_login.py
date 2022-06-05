import random
import sys
import datetime
from functools import wraps
import threading
import _thread
import time
sys.path.append('..')
sys.path.append('..\\LoginModule')
sys.path.append('..\\oa-flask\\DataBaseModels')
sys.path.append('..\\oa-flask\\DataBaseModels\\CustomerModels')
sys.path.append('..\\oa-flask\\DataBaseModels\\UserModels')

from flask import request, jsonify, session, Blueprint, redirect, Response
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from LoginModule.login_def import LoginFormKey
from LoginModule.login_session_ctrl import LoginSession
# import login_token as login_token
from FileDownloadModule.file_download_upload import DownloadCtrl
from DataBaseModels.UserModels.user_models import EmployeeManager, EmployeeModelBase

from flask import Flask
# from router import app, cors
from flask_cors import CORS, cross_origin
from flask_login import LoginManager

# auth_flask_login = Blueprint('auth_flask_login', __name__)
DURATION_SEC = datetime.timedelta(seconds=60)

# print("loginmanager:{}".format(ServerInstance.login_manager.login_view))

FlaskApp = Flask(__name__)
FlaskApp.secret_key = "FlaskOaSystem"
cors = CORS(FlaskApp)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = '请登录'
login_manager.init_app(FlaskApp)


def oa_login_required(func):  # pylint:disable=invalid-name
    @wraps(func)
    def decorated_view(*args, **kwargs):
        data = request.get_json(silent=True)
        szSession = data.get("Session")
        returnData = {'tips': 'username or password is not correct'}
        if szSession is None:
            print("invalid session{}\nlist: {}".format(szSession, LoginSession.GetNowLoginSessionList()))
            return jsonify(returnData)
        if not LoginSession.RefreshSession(szSession):
            print("invalid session{}\nlist: {}".format(szSession, LoginSession.GetNowLoginSessionList()))
            return jsonify(returnData)
        return func(*args, **kwargs)

    print(5555555)
    return decorated_view


# handle login failed
@FlaskApp.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


@FlaskApp.route('/home', methods=['GET', 'POST'])
@oa_login_required
def home():
    print("home")
    returnData = {'code': -1, 'msg': 'failed', 'data': {'tips': 'username or password is not correct'}}
    return jsonify(returnData)


# @app.route('/')
# @login_required
# def index():
#     return 'Logged in as: %s' % current_user.get_id()

@FlaskApp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json(silent=True)
        print("post data:{}".format(str(data)))

        szRequestUserName = data.get(LoginFormKey.EMPLOYEE_NAME)
        szRequestPassword = data.get(LoginFormKey.EMPLOYEE_PASSWORD)
        print("user form: {} {}".format(szRequestUserName, szRequestPassword))

        if szRequestPassword is None or szRequestUserName is None:
            returnData = {'code': -1, 'msg': 'failed', 'data': {'tips': 'username or password is not correct'}}
            return jsonify(returnData)

        LoginEmployeeObj = EmployeeManager.GetUserModelByNameAndPassword(szRequestUserName, szRequestPassword)
        if LoginEmployeeObj is None:
            # 校验失败
            returnData = {'code': -1, 'msg': 'failed', 'data': {'tips': 'username or password is not correct'}}
            return jsonify(returnData)
        else:
            # 创建新的session
            # bLoginSucceed = login_user(LoginEmployeeObj, remember=True) # , duration=DURATION_SEC)
            # print("login succeed: {}".format(bLoginSucceed))
            szNewSession = LoginSession.CreateNewSession(szRequestUserName, szRequestPassword)
            print("create new session: {}".format(szNewSession))
            returnData = {'tips': 'login succeed', 'Session': szNewSession}
            return jsonify(returnData)

    # GET 请求
    # return render_template('login.html')
    # token = login_token.create_token(g.user_id)
    # return jsonify({'token': token})
    returnData = {'code': 1, 'msg': 'failed', 'data': {'tips': 'username or password is not correct'}}
    return jsonify(returnData)


@FlaskApp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    # logout_user()
    print("logout")
    returnData = {'code': 1, 'msg': 'failed', 'succeed': {'tips': 'Logged out successfully!'}}
    return jsonify(returnData)


@FlaskApp.route('/register', methods=['GET', 'POST'])
def NewEmployeeRegister():
    """
    对应注册页面
    :return:
    """
    if request.method == 'POST':
        data = request.get_json(silent=True)
        print("register in ：{}".format(str(data)))
        bRegisterSucceed, szContent = EmployeeManager.RegisterNewModel(data)
        returnData = {'code': 1, 'msg': str(bRegisterSucceed), 'data': {'tips': szContent}}
        print("tips:{}".format(szContent))

        return jsonify(returnData)

    returnData = {'code': -1, 'msg': 'failed', 'data': {'tips': 'register false'}}
    return jsonify(returnData)


@FlaskApp.route('/download', methods=['GET', 'POST'])
def DownloadFile():
    print("begin download")
    szFileName = request.form.get('filename', None)
    if szFileName is None:
        # 默认下载文件
        return DownloadCtrl.DownloadFile("29.mp4")

    print("szFileName: {}".format(szFileName))
    return DownloadCtrl.DownloadFile(szFileName)


@FlaskApp.route('/upload', methods=['GET', 'POST'])
def UploadFile():
    print("begin upload")
    name = request.form.get("name")
    description = request.form.get("description")
    fileObj = request.files.get("file")
    fileObj.save("E://store.jpg")
    print("szFileName: {}".format(fileObj.filename))
    return jsonify({'tips': "succeed"})


@FlaskApp.route('/autoroute/<username>', methods=['GET', 'POST'])
def TestAutoRoute(username):
    print("username:{}".format(username))


def DefendThread(sleepTimeSec):
    while 1:
        time.sleep(sleepTimeSec)
        print("DefendThread Wake Up")


def ServerThread():
    FlaskApp.run(debug=True)


class DefendThreadClass(threading.Thread):
    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay

    def run(self):
        print("开始线程：" + self.name)
        DefendThread(self.delay)
        print("退出线程：" + self.name)


class ServerClass(threading.Thread):
    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay

    def run(self):
        print("开始线程：" + self.name)
        ServerThread()
        print("退出线程：" + self.name)


if __name__ == '__main__':
    _thread.start_new_thread(DefendThread, (2,))
    # thread1 = DefendThreadClass(1, "Thread-1", 2)
    # thread1.start()
    # thread1.join()
    FlaskApp.run(debug=True)
