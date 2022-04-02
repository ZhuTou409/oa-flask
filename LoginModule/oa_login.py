import sys
import datetime
sys.path.append('..')
sys.path.append('..\\LoginModule')
sys.path.append('..\\oa-flask\\DataBaseModels')
sys.path.append('..\\oa-flask\\DataBaseModels\\CustomerModels')
sys.path.append('..\\oa-flask\\DataBaseModels\\UserModels')

from flask import request, jsonify, session, Blueprint
from flask_login import LoginManager, login_user, logout_user, login_required
from LoginModule.login_def import LoginFormKey
# import login_token as login_token
from FileDownloadModule.file_download_upload import DownloadCtrl
from DataBaseModels.UserModels.user_models import EmployeeManager, EmployeeModelBase
from app import ServerInstance

auth_flask_login = Blueprint('auth_flask_login', __name__)
DURATION_SEC = datetime.timedelta(seconds=60)


@ServerInstance.login_manager.user_loader
def load_user(user_id):
    EmployeeObj = EmployeeManager.GetUserModelByUserID(user_id)
    print("load_user: {}".format(user_id))
    if EmployeeObj is None:
        print("yesr: {}".format(user_id))
        return EmployeeManager.CreateNewEmployeeModelByUserID(user_id)
    else:
        print("no: {}".format(user_id))
        return EmployeeObj


# @app.route('/')
# @login_required
# def index():
#     return 'Logged in as: %s' % current_user.get_id()

@auth_flask_login.route('/login', methods=['GET', 'POST'])
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
            bLoginSucceed = login_user(LoginEmployeeObj, remember=True, duration=DURATION_SEC)
            print("login succeed: {}".format(bLoginSucceed))
            returnData = {'code': 1, 'msg': 'succeed', 'data': {'tips': 'login succeed'}}
            return jsonify(returnData)

    # GET 请求
    # return render_template('login.html')
    # token = login_token.create_token(g.user_id)
    # return jsonify({'token': token})
    returnData = {'code': 1, 'msg': 'failed', 'data': {'tips': 'username or password is not correct'}}
    return jsonify(returnData)


@ServerInstance.App.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    # logout_user()
    print("logout")
    returnData = {'code': 1, 'msg': 'failed', 'succeed': {'tips': 'Logged out successfully!'}}
    return jsonify(returnData)


@auth_flask_login.route('/register', methods=['GET', 'POST'])
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


@auth_flask_login.route('/download', methods=['GET', 'POST'])
def DownloadFile():
    print("begin download")
    szFileName = request.form.get('filename', None)
    if szFileName is None:
        # 默认下载文件
        return DownloadCtrl.DownloadFile("29.mp4")

    print("szFileName: {}".format(szFileName))
    return DownloadCtrl.DownloadFile(szFileName)


@auth_flask_login.route('/upload', methods=['GET', 'POST'])
def UploadFile():
    print("begin upload")
    name = request.form.get("name")
    description = request.form.get("description")
    fileObj = request.files.get("file")
    fileObj.save("E://store.jpg")
    print("szFileName: {}".format(fileObj.filename))
    return jsonify({'tips': "succeed"})


@auth_flask_login.route('/autoroute/<username>', methods=['GET', 'POST'])
def TestAutoRoute(username):
    print("username:{}".format(username))


# if __name__ == '__main__':
#     app.run(debug=True)
