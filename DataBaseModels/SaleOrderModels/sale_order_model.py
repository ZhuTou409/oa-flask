from DataBaseInterface.database_func import DataFuncObj, OADatabaseForm
from DataBaseModels.CustomerModels.customer_model import CustomerModel, CustomerFormKey
from DataBaseModels.TransportInfoModels.voyage_model import VoyageModel, VoyageFormKey
from DataBaseModels.model_base import ModelBase
import time


class SaleOrderFormKey:
    ORDER_ID = "OrderID"
    SUBMIT_SALE_NAME = "SubmitSaleName"
    OPTION_NAME = "OptionName"
    CREATE_TIME = "CreateTime"
    DELEGATE_COMPANY_CUSTOMER = "DelegateCompanyCustomer"
    RECEIVE_COMPANY_CUSTOMER = "ReceiveCompanyCustomer"
    VOYAGE_INFO = "VoyageInfo"
    TRAILER_GROUP = "TrailerGroup"
    BAOGUAN_HANG = "BaoGuanHang"
    REGISTER = "Register"
    CONTAINER_TYPE = "ContainerSize"
    CONTAINER_COUNT = "ContainerCount"
    WEIGHT = "Weight"


SALE_ORDER_FORM_KEY_NUMBER = 4
SALE_ORDER_FORM_NAME = "SaleOrder"


class SaleOrderFormModel(ModelBase):
    """
    表单数据对象
    """
    def __init__(self, szOrderID, dictInfo=None):
        self.m_szOrderID = None
        self.m_szSubmitSaleName = None
        self.m_szOptionalName = None

        # 销售流程创建时间
        self.m_nCreateTime = None

        # 委托单位联系人
        self.m_DelegateCompanyCustomerModel = None
        # 收货单位联系人
        self.m_ReceiveCompanyCustomerModel = None
        # 货运航次
        self.m_VoyageModel = None
        # 拖车队
        self.m_szTrailerGroup = None
        # 报关行
        self.m_szBaoGuanHang = None
        # 代理
        self.m_szRegister = None
        # 柜型
        self.m_szContainerType = None
        # 方数
        self.m_nContainerCount = None
        # 重量
        self.m_szWeight = None

        super().__init__(szOrderID, dictInfo)

    def SetCreateTime(self, nCreateTime):
        self.m_nCreateTime = nCreateTime

    def InsertAllInfoToForm(self):
        dictPreInsertData = {
            SaleOrderFormKey.ORDER_ID: self.m_szOrderID,
            SaleOrderFormKey.SUBMIT_SALE_NAME: self.m_szSubmitSaleName,
            SaleOrderFormKey.OPTION_NAME: self.m_szOptionalName,
            SaleOrderFormKey.CREATE_TIME: self.m_nCreateTime
        }

        OrderFormObj = DataFuncObj.GetDataForm(SALE_ORDER_FORM_NAME)
        OrderFormObj.InsertOne(dictPreInsertData)

    def InitByMainKey(self, MainKeyObj):
        """
        初始化表单对象，通过表单ID
        :param MainKeyObj:
        :return:
        """
        OrderFormObj = DataFuncObj.GetDataForm(SALE_ORDER_FORM_NAME)
        FormDict = OrderFormObj.Find(SaleOrderFormKey.ORDER_ID, MainKeyObj)

        if FormDict is None:
            return False

        self.m_szOrderID = MainKeyObj
        self.m_szSubmitSaleName = FormDict.get(SaleOrderFormKey.SUBMIT_SALE_NAME)
        self.m_szOptionalName = FormDict.get(SaleOrderFormKey.OPTION_NAME)

        self.m_nCreateTime = time.time()

    def InitByDict(self, InfoDict):
        if len(InfoDict) != SALE_ORDER_FORM_KEY_NUMBER:
            return

        self.m_szOrderID = InfoDict.get(SaleOrderFormKey.ORDER_ID)
        self.m_szSubmitSaleName = InfoDict.get(SaleOrderFormKey.SUBMIT_SALE_NAME)
        self.m_szOptionalName = InfoDict.get(SaleOrderFormKey.OPTION_NAME)
        self.m_nCreateTime = time.time()
        # 拖车队
        self.m_szTrailerGroup = InfoDict.get(SaleOrderFormKey.TRAILER_GROUP)
        # 报关行
        self.m_szBaoGuanHang = InfoDict.get(SaleOrderFormKey.BAOGUAN_HANG)
        # 代理
        self.m_szRegister = InfoDict.get(SaleOrderFormKey.REGISTER)
        # 柜型
        self.m_szContainerType = InfoDict.get(SaleOrderFormKey.CONTAINER_TYPE)
        # 方数
        self.m_nContainerCount = InfoDict.get(SaleOrderFormKey.CONTAINER_COUNT)
        # 重量
        self.m_szWeight = InfoDict.get(SaleOrderFormKey.WEIGHT)

        # 主属性赋值
        self._InitMainAttrInfo(InfoDict)

    def _InitMainAttrInfo(self, dictInfo):
        # 委托单位联系人信息
        dictDelegateCustomerInfo = dictInfo.get(SaleOrderFormKey.DELEGATE_COMPANY_CUSTOMER)
        if dictDelegateCustomerInfo is None:
            return
        self.m_DelegateCompanyCustomerModel = self._InitCustomerModelInternal(dictDelegateCustomerInfo)

        # 收货单位联系人信息
        dictReceiveCustomerInfo = dictInfo.get(SaleOrderFormKey.RECEIVE_COMPANY_CUSTOMER)
        if dictReceiveCustomerInfo is None:
            return
        self.m_ReceiveCompanyCustomerModel = self._InitCustomerModelInternal(dictReceiveCustomerInfo)

        # 航次信息
        dictVoyageInfo = dictInfo.get(SaleOrderFormKey.VOYAGE_INFO)
        if dictVoyageInfo is None:
            return
        self.m_VoyageModel = self._InitVoyageModelInternal(dictVoyageInfo)

    def _InitCustomerModelInternal(self, CustomerInfoDict):
        szCustomerName = CustomerInfoDict.get(CustomerFormKey.CUSTOMER_NAME)
        if szCustomerName is not None:
            dictCustomerInfo = {
                CustomerFormKey.CUSTOMER_NAME: szCustomerName,
                CustomerFormKey.COMPANY: CustomerInfoDict.get(CustomerFormKey.COMPANY),
                CustomerFormKey.ADDRESS: CustomerInfoDict.get(CustomerFormKey.ADDRESS),
                CustomerFormKey.PHONE_NUMBER: CustomerInfoDict.get(CustomerFormKey.PHONE_NUMBER),
                CustomerFormKey.REGISTER_NAME: self.m_szSubmitSaleName
            }
            return CustomerModel(szCustomerName, dictCustomerInfo)
        return None

    def _InitVoyageModelInternal(self, VoyageInfoDict):
        szVoyageName = VoyageInfoDict.get(VoyageFormKey.VOYAGE_NAME)
        if szVoyageName is not None:
            dictCustomerInfo = {
                VoyageFormKey.VOYAGE_NAME: szVoyageName,
                VoyageFormKey.BOAT_NAME: VoyageInfoDict.get(VoyageFormKey.BOAT_NAME),
                VoyageFormKey.BOAT_COMPANY_NAME: VoyageInfoDict.get(VoyageFormKey.BOAT_COMPANY_NAME),
                VoyageFormKey.TARGET_PORT: VoyageInfoDict.get(VoyageFormKey.TARGET_PORT),
                VoyageFormKey.START_PORT: VoyageInfoDict.get(VoyageFormKey.START_PORT)
            }
            return VoyageModel(szVoyageName, dictCustomerInfo)
        return None
