from DataBaseModels.model_base import ModelBase
from DataBaseInterface.database_func import DataFuncObj


class VoyageFormKey:
    VOYAGE_NAME = "VoyageName"
    BOAT_NAME = "BoatName"
    START_PORT = "StartPort"
    TARGET_PORT = "TargetPort"
    BOAT_COMPANY_NAME = "BoatCompanyName"


VOYAGE_FORM_NAME = "Voyage"


class VoyageModel(ModelBase):
    """
    客户信息数据类
    """
    def __init__(self, szVoyageName):
        super().__init__()
        self.m_szVoyageName = szVoyageName
        self.m_szBoatName = None
        self.m_szStartPort = None
        self.m_szTargetPort = None
        self.m_szBoatCompanyName = None

        self.InitByMainKey(szVoyageName)

    def InsertAllInfoToForm(self):
        dictPreInsertData = {
            VoyageFormKey.VOYAGE_NAME: self.m_szVoyageName,
            VoyageFormKey.BOAT_NAME: self.m_szBoatName,
            VoyageFormKey.START_PORT: self.m_szStartPort,
            VoyageFormKey.TARGET_PORT: self.m_szTargetPort,
            VoyageFormKey.BOAT_COMPANY_NAME: self.m_szBoatCompanyName
        }

        OrderFormObj = DataFuncObj.GetDataForm(VOYAGE_FORM_NAME)
        OrderFormObj.InsertOne(dictPreInsertData)

    def InitByMainKey(self, MainKeyObj):
        OrderFormObj = DataFuncObj.GetDataForm(VOYAGE_FORM_NAME)
        FormDict = OrderFormObj.Find(VoyageFormKey.VOYAGE_NAME, MainKeyObj)

        if FormDict is None:
            return False

        self.m_szVoyageName = MainKeyObj
        self.m_szBoatName = FormDict.get(VoyageFormKey.BOAT_NAME)
        self.m_szStartPort = FormDict.get(VoyageFormKey.START_PORT)
        self.m_szTargetPort = FormDict.get(VoyageFormKey.TARGET_PORT)
        self.m_szBoatCompanyName = FormDict.get(VoyageFormKey.BOAT_COMPANY_NAME)
        return True

    def GetVoyageName(self):
        return self.m_szVoyageName

    def GetBoatName(self):
        return self.m_szBoatName

    def GetStartPortName(self):
        return self.m_szStartPort

    def GetTargetPortName(self):
        return self.m_szTargetPort

    def GetBoatCompanyName(self):
        return self.m_szBoatCompanyName

