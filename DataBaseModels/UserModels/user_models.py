from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from DataBaseInterface.database_func import DataFuncObj
from DataBaseModels.model_base import ModelBase
from LoginModule.login_def import LoginFormKey
import time

EMPLOYEE_FORM_KEY_NUMBER = 5
EMPLOYEE_FORM_NAME = "Employee"


class EmployeeFormKey:
    """
    雇员信息的key
    """
    IDENTIFY_USER_ID = "IdentifyUserID"
    EMPLOYEE_NAME = "EmployeeName"
    PASSWORD = "Password"
    OCCUPATION = "Occupation"
    CREATE_TIME = "CreateTime"


# 每个登录的对象最多存在时间
USER_EXIST_MAX_TIME = 60 * 60 * 24


class UserManager:
    @staticmethod
    def CreatePasswordByMD5(szPassword):
        return generate_password_hash(szPassword)

    @staticmethod
    def _CreateIdentifyUserID(szUserName, szCreateTime):
        # md5生成用户唯一标识符（username + createTime）,做为数据库的mainKey
        return generate_password_hash(szUserName + str(szCreateTime))

    @staticmethod
    def RegisterNewModel(dictRegisterForm):
        """
        添加一个新用户
        :param dictRegisterForm:
        :return:
        """
        szPassword = dictRegisterForm.get(LoginFormKey.EMPLOYEE_PASSWORD)
        szEmployeeName = dictRegisterForm.get(LoginFormKey.EMPLOYEE_NAME)
        print("password: {}, name: {}".format(szPassword, szEmployeeName))
        if szEmployeeName is not None:

            nNowTime = time.time()
            szNewIdentifyUserID = UserManager._CreateIdentifyUserID(szEmployeeName, nNowTime)
            EmployeeFormObj = DataFuncObj.GetDataForm(EMPLOYEE_FORM_NAME)
            # 检查是否有同名的人
            listFindNameFormDict = EmployeeFormObj.Find(EmployeeFormKey.EMPLOYEE_NAME, szEmployeeName)
            if len(listFindNameFormDict) != 0:
                return False, str("userName is already existed!:{}".format(str(listFindNameFormDict[0].get(EmployeeFormKey.EMPLOYEE_NAME))))

            # 检查是否有重复的ID
            listFormDict = EmployeeFormObj.Find(EmployeeFormKey.IDENTIFY_USER_ID, szNewIdentifyUserID)
            print("FormDict: {}, EmployeeFormKey.IDENTIFY_USER_ID: {}".format(listFormDict, EmployeeFormKey.IDENTIFY_USER_ID))
            if len(listFormDict) != 0:
                return False, str("userName is already existed!:{}".format(str(listFormDict[EmployeeFormKey.EMPLOYEE_NAME])))
            else:
                # 正式创建model
                dictInitEmployee = {
                    EmployeeFormKey.IDENTIFY_USER_ID: szNewIdentifyUserID,
                    EmployeeFormKey.EMPLOYEE_NAME: szEmployeeName,
                    EmployeeFormKey.CREATE_TIME: nNowTime,
                    EmployeeFormKey.OCCUPATION: dictRegisterForm.get(LoginFormKey.OCCUPATION),
                    EmployeeFormKey.PASSWORD: UserManager.CreatePasswordByMD5(szPassword)
                }
                NewModel = EmployeeModelBase(None, dictInitEmployee)
                # 存入数据库
                NewModel.InsertAllInfoToForm()
                return True, str("create New Employee succeed!")

        return False, str("szEmployeeName is None!")

    @staticmethod
    def GetUserModelByNameAndPassword(szEmployeeName, szPassword):
        """
        根据名字和密码查询是否有这个人
        :param self:
        :param szEmployeeName:
        :param szPassword:
        :return:
        """
        EmployeeFormObj = DataFuncObj.GetDataForm(EMPLOYEE_FORM_NAME)
        listFormDict = EmployeeFormObj.Find(EmployeeFormKey.EMPLOYEE_NAME, szEmployeeName)
        if len(listFormDict) != 1:
            print("数据库出错：{}".format(listFormDict))
            return None
        for dictEmployeeInfo in listFormDict:
            szCheckPassword = dictEmployeeInfo.get(EmployeeFormKey.PASSWORD)
            if check_password_hash(szCheckPassword, szPassword):
                return EmployeeModelBase(None, dictEmployeeInfo)

        return None

    @staticmethod
    def GetUserModelByUserID(szIdentifyUserID):
        """
        根据UID获取用户
        :param szIdentifyUserID:
        :return:
        """
        EmployeeFormObj = DataFuncObj.GetDataForm(EMPLOYEE_FORM_NAME)
        FormDict = EmployeeFormObj.Find(EmployeeFormKey.IDENTIFY_USER_ID, szIdentifyUserID)

        if FormDict is None:
            return None

        return EmployeeModelBase(None, FormDict[0])

    @staticmethod
    def CreateNewEmployeeModelByUserID(szIdentifyUserID):
        """
        根据UID创建对象
        :param szIdentifyUserID:
        :return:
        """
        dictInitEmployee = {
            EmployeeFormKey.IDENTIFY_USER_ID: szIdentifyUserID,
            EmployeeFormKey.EMPLOYEE_NAME: None,
            EmployeeFormKey.CREATE_TIME: time.time(),
            EmployeeFormKey.OCCUPATION: None,
            EmployeeFormKey.PASSWORD: None
        }

        return EmployeeModelBase(None, dictInitEmployee)


EmployeeManager = UserManager()


class EmployeeModelBase(UserMixin, ModelBase):
    """
    用户信息，登录成功后创建
    """
    def __init__(self, szIdentifyUserID, dictInfo):
        self.m_szUserName = None
        self.m_szOccupation = None
        self.m_szCreateTime = None
        self.m_szHashPassword = None
        self.m_szIdentifyUserID = None

        super().__init__(szIdentifyUserID, dictInfo)

    def InsertAllInfoToForm(self):
        dictPreInsertData = {
            EmployeeFormKey.IDENTIFY_USER_ID: self.m_szIdentifyUserID,
            EmployeeFormKey.EMPLOYEE_NAME: self.m_szUserName,
            EmployeeFormKey.CREATE_TIME: self.m_szCreateTime,
            EmployeeFormKey.OCCUPATION: self.m_szOccupation,
            EmployeeFormKey.PASSWORD: self.m_szHashPassword
        }

        OrderFormObj = DataFuncObj.GetDataForm(EMPLOYEE_FORM_NAME)
        OrderFormObj.InsertOne(dictPreInsertData)

    def InitByMainKey(self, MainKeyObj):
        OrderFormObj = DataFuncObj.GetDataForm(EMPLOYEE_FORM_NAME)
        FormDict = OrderFormObj.Find(EmployeeFormKey.IDENTIFY_USER_ID, MainKeyObj)

        if FormDict is None:
            return False

        self.m_szIdentifyUserID = MainKeyObj
        self.m_szUserName = FormDict.get(EmployeeFormKey.EMPLOYEE_NAME)
        self.m_szOccupation = FormDict.get(EmployeeFormKey.OCCUPATION)
        self.m_szCreateTime = FormDict.get(EmployeeFormKey.CREATE_TIME)
        self.m_szHashPassword = FormDict.get(EmployeeFormKey.PASSWORD)
        return True

    def InitByDict(self, InfoDict):
        if len(InfoDict) != EMPLOYEE_FORM_KEY_NUMBER:
            return

        self.m_szIdentifyUserID = InfoDict.get(EmployeeFormKey.IDENTIFY_USER_ID)
        self.m_szUserName = InfoDict.get(EmployeeFormKey.EMPLOYEE_NAME)
        self.m_szOccupation = InfoDict.get(EmployeeFormKey.OCCUPATION)
        self.m_szCreateTime = InfoDict.get(EmployeeFormKey.CREATE_TIME)
        self.m_szHashPassword = InfoDict.get(EmployeeFormKey.PASSWORD)

    def get_id(self):
        return self.m_szIdentifyUserID

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

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

