from DataBaseInterface.database_func import DataFuncObj, OADatabaseForm
import time


class SaleOrderFormKey:
    ORDER_ID = "OrderID"
    SUBMIT_SALE_NAME = "SubmitSaleName"
    OPTION_NAME = "OptionName"
    CREATE_TIME = "CreateTime"


SALE_ORDER_FORM_NAME = "SaleOrder"


class SaleOrderFormModel:
    """
    表单数据对象
    """
    def __init__(self):
        self.m_szOrderID = None
        self.m_szSubmitSaleName = None
        self.m_szOptionalName = None

        # 销售流程创建时间
        self.m_nCreateTime = None

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

    def InitByOrderID(self, szOrderID):
        """
        初始化表单对象，通过表单ID
        :param szOrderID:
        :return:
        """
        OrderFormObj = DataFuncObj.GetDataForm(SALE_ORDER_FORM_NAME)
        FormDict = OrderFormObj.Find(SaleOrderFormKey.ORDER_ID, szOrderID)

        if FormDict is None:
            return False

        self.m_szOrderID = szOrderID
        self.m_szSubmitSaleName = FormDict.get(SaleOrderFormKey.SUBMIT_SALE_NAME)
        self.m_szOptionalName = FormDict.get(SaleOrderFormKey.OPTION_NAME)

        self.m_nCreateTime = time.time()


