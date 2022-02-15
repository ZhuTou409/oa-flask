from flask import Flask, request, redirect, url_for, render_template, jsonify, g
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from DataBaseModels.user_models import User, query_user, GetUserDataByUserName
from login_token import auth as auth
import login_token as login_token
import json

app = Flask(__name__)
app.secret_key = '1234567'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = '请登录'
login_manager.init_app(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)


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


if __name__ == '__main__':
    app.run(debug=True)
