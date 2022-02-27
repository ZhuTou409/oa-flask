import sys
sys.path.append('..')
sys.path.append('..\\LoginModule')
sys.path.append('..\\oa-flask\\DataBaseModels')
sys.path.append('..\\oa-flask\\DataBaseModels\\CustomerModels')
sys.path.append('..\\oa-flask\\DataBaseModels\\UserModels')

from flask import request, jsonify
from flask_login import LoginManager, logout_user, login_required
from DataBaseModels.UserModels.user_models import User, query_user, GetUserDataByUserName
import login_token as login_token
from router import app
from FileDownloadModule.file_download_upload import DownloadCtrl


# app = Flask(__name__)
# app.secret_key = '1234567'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = '请登录'
login_manager.init_app(app)

# enable CORS
# CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)


@login_manager.user_loader
def load_user(user_id):
    if query_user(user_id) is not None:
        curr_user = User()
        curr_user.id = user_id

        return curr_user


# @app.route('/')
# @login_required
# def index():
#     return 'Logged in as: %s' % current_user.get_id()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("post data:{}".format(str(request.form)))
        szUserName = request.form.get('userid')

        szRequestUserName = request.form.get("username", "")
        szRequestPassword = request.form.get("password", "")

        print("user form: {} {}".format(szRequestUserName, szRequestPassword))

        UserData = GetUserDataByUserName(szRequestUserName)
        if UserData is not None and UserData["password"] == szRequestPassword:
            print("校验成功")
            token = login_token.create_token(szRequestUserName)
            return jsonify({'token': token})
    #     if user is not None and request.form['password'] == user['password']:
    #
    #         curr_user = User()
    #         curr_user.id = user_id
    #
    #         # 通过Flask-Login的login_user方法登录用户
    #         login_user(curr_user)
    #
    #         return redirect(url_for('index'))

        # flash('Wrong username or password!')

    # GET 请求
    # return render_template('login.html')
    # token = login_token.create_token(g.user_id)
    # return jsonify({'token': token})
    returnData = {'code': 1, 'msg': 'failed', 'data': {'tips': 'username or password is not correct'}}
    return jsonify(returnData)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully!'


@app.route('/download', methods=['GET', 'POST'])
def DownloadFile():
    print("begin download")
    szFileName = request.form.get('filename', None)
    if szFileName is None:
        # 默认下载文件
        return DownloadCtrl.DownloadFile("29.mp4")

    print("szFileName: {}".format(szFileName))
    return DownloadCtrl.DownloadFile(szFileName)


@app.route('/upload', methods=['GET', 'POST'])
def UploadFile():
    print("begin upload")
    name = request.form.get("name")
    description = request.form.get("description")
    fileObj = request.files.get("file")
    fileObj.save("E://store.jpg")
    print("szFileName: {}".format(fileObj.filename))
    return jsonify({'tips': "succeed"})


@app.route('/autoroute/<username>', methods=['GET', 'POST'])
def TestAutoRoute(username):
    print("username:{}".format(username))


if __name__ == '__main__':
    app.run(debug=True)
