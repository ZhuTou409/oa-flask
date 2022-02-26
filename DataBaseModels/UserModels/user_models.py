from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import time

# 每个登录的对象最多存在时间
USER_EXIST_MAX_TIME = 60 * 60 * 24


class EmployeeModelKey:
    """
    雇员信息的key
    """
    OCCUPATION = "occupation"


class User(UserMixin):
    pass


users = [
    {'id':'Tom', 'username': 'Tom', 'password': '111111'},
    {'id':'Michael', 'username': 'Michael', 'password': '123456'},
    {'id': 'zhu', 'username': 'zhu', 'password': '123456'}
]


def query_user(user_id):
    for user in users:
        if user_id == user['id']:
            return user


def GetUserDataByUserName(szUserName):
    for user in users:
        if szUserName == user['username']:
            return user


class EmployeeModelBase(UserMixin):
    """
    用户信息，登录成功后创建
    """
    def __init__(self, szToken, szUserName, dictEmployInfo):
        self.m_szUserName = szUserName
        self.m_szToken = szToken
        self.m_szOccupation = dictEmployInfo.get(EmployeeModelKey.OCCUPATION)
        self.m_szCreateTime = time.time()
        self.m_szHashPassword = None

    def SetPassword(self, szPassword):
        """
        设置密码哈希值
        :param szPassword:
        :return:
        """
        self.m_szHashPassword = generate_password_hash(szPassword)

    def CheckPassword(self, szPassword):
        """
        校验密码
        :param szPassword:
        :return:
        """
        return check_password_hash(self.m_szHashPassword, szPassword)

    def IsModelCanDestroy(self):
        return self.m_szCreateTime > USER_EXIST_MAX_TIME

    def GetOccupation(self):
        return self.m_szOccupation

