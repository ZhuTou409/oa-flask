from DataBaseModels.model_base import ModelBase
from DataBaseInterface.database_func import DataFuncObj


class CustomerFormKey:
    CUSTOMER_NAME = "CustomerName"
    PHONE_NUMBER = "PhoneNumber"
    ADDRESS = "Address"
    COMPANY = "Company"
    REGISTER_NAME = "RegisterName"


CUSTOMER_FORM_KEY_NUMBER = 5
CUSTOM_FORM_NAME = "Customer"


class CustomerModel(ModelBase):
    """
    客户信息数据类
    """
    def __init__(self, szCustomerName, szRegisterName, InfoDict=None):
        self.m_szCustomerName = szCustomerName
        self.m_szPhoneNumber = None
        self.m_szAddress = None
        self.m_szCompany = None
        # 登记这个信息的职员
        self.m_szRegisterName = szRegisterName

        # 初始化
        super().__init__(szCustomerName, InfoDict)

    def InsertAllInfoToForm(self):
        dictPreInsertData = {
            CustomerFormKey.CUSTOMER_NAME: self.m_szCustomerName,
            CustomerFormKey.PHONE_NUMBER: self.m_szPhoneNumber,
            CustomerFormKey.ADDRESS: self.m_szAddress,
            CustomerFormKey.COMPANY: self.m_szCompany,
            CustomerFormKey.REGISTER_NAME: self.m_szRegisterName
        }

        OrderFormObj = DataFuncObj.GetDataForm(CUSTOM_FORM_NAME)
        OrderFormObj.InsertOne(dictPreInsertData)

    def InitByMainKey(self, MainKeyObj):
        OrderFormObj = DataFuncObj.GetDataForm(CUSTOM_FORM_NAME)
        FormDict = OrderFormObj.Find(CustomerFormKey.CUSTOMER_NAME, MainKeyObj)

        if FormDict is None:
            return False

        self.m_szCustomerName = MainKeyObj
        self.m_szPhoneNumber = FormDict.get(CustomerFormKey.PHONE_NUMBER)
        self.m_szAddress = FormDict.get(CustomerFormKey.ADDRESS)
        self.m_szCompany = FormDict.get(CustomerFormKey.COMPANY)
        self.m_szRegisterName = FormDict.get(CustomerFormKey.REGISTER_NAME)
        return True

    def InitByDict(self, InfoDict):
        if len(InfoDict) != CUSTOMER_FORM_KEY_NUMBER:
            return

        self.m_szCustomerName = InfoDict.get(CustomerFormKey.CUSTOMER_NAME)
        self.m_szPhoneNumber = InfoDict.get(CustomerFormKey.PHONE_NUMBER)
        self.m_szAddress = InfoDict.get(CustomerFormKey.ADDRESS)
        self.m_szCompany = InfoDict.get(CustomerFormKey.COMPANY)
        self.m_szRegisterName = InfoDict.get(CustomerFormKey.REGISTER_NAME)

    def GetCompany(self):
        return self.m_szCompany

    def GetAddress(self):
        return self.m_szAddress

    def GetPhoneNumber(self):
        return self.m_szPhoneNumber
