from flask import request, jsonify, current_app, g
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from flask_httpauth import HTTPBasicAuth
from DataBaseModels import user_models as user_models
import re

auth = HTTPBasicAuth()


def create_token(api_user):
    '''
    生成token
    :param api_user:用户id
    :return: token
    '''

    # 第一个参数是内部的私钥，这里写在共用的配置信息里了，如果只是测试可以写死
    # 第二个参数是有效期(秒)
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=60)
    # 接收用户id转换与编码
    token = s.dumps({"id": api_user}).decode("ascii")
    return token


def verify_token(token):
    '''
    校验token
    :param token:
    :return: 用户信息 or None
    '''

    # 参数为私有秘钥，跟上面方法的秘钥保持一致
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        # 转换为字典
        data = s.loads(token)
        return data
        # token过期
    except SignatureExpired:
        return None
    # token错误
    except BadSignature:
        return None


# 验证token
@auth.verify_password
def verify_password(username_token, password):
    '''
    校验token
    :param token:
    :return: 用户信息 or None
    '''
    # 先验证token
    user_id = re.sub(r'^"|"$', '', username_token)
    user_id = verify_token(user_id)
    print("username" + str(username_token))
    # 如果token不存在，验证用户id与密码是否匹配
    # if not user_id:
    #     print("user_id:" + str(user_id))
    #     UserDataObj = user_models.query_user(user_id)
    #     if UserDataObj['password'] != password:
    #         return False
    #     # 如果用户id与密码对应不上，返回False
    #     if not user_id:
    #         return False
    g.user_id = user_id.get('username')
    return True

