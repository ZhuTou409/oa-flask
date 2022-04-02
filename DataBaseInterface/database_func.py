import pymongo
from Utils.static_def import MONGODB_CONNECT_URL


class DBFindConditionType:
    AND = '$and'
    OR = '$or'


class DatabaseFunc:
    """
    数据库中间层，隔离数据库方法
    """
    def __init__(self):
        self.bInitDBSuccess = True
        self.client = pymongo.MongoClient(host='127.0.0.1')
        if self.client is None:
            self.bInitDBSuccess = False

        self.mongoDBObj = self.client['oaSystem']
        # self.CollectionObj = self.mongoDBObj.zhu

    def GetDataForm(self, szFormName):
        """
        获取一个表格
        :param szFormName:
        :return:
        """
        return OADatabaseForm(self.mongoDBObj[szFormName])


class OADatabaseForm:
    """
    表格对象
    """
    def __init__(self, DatabaseFormObj):
        self.m_DatabaseFormObj = DatabaseFormObj

    def Find(self, Key, Value):
        Cursor = self.m_DatabaseFormObj.find({Key: Value})
        returnDict = []
        for Answer in Cursor:
            returnDict.append(Answer)
        return returnDict

    def FindAnd(self, dictKeyValue):
        Cursor = self._InternalFind(dictKeyValue, DBFindConditionType.AND)
        returnDict = []
        for Answer in Cursor:
            returnDict.append(Answer)
        return returnDict

    def FindOr(self, dictKeyValue):
        Cursor = self._InternalFind(dictKeyValue, DBFindConditionType.OR)
        returnDict = []
        for Answer in Cursor:
            returnDict.append(Answer)
        return returnDict

    def NormalFind(self, KeyValueObj):
        """
        直接利用数据库原始接口的find
        :param KeyValueObj:
        :return:
        """
        return self.m_DatabaseFormObj.find(KeyValueObj)

    def _InternalFind(self, ditKeyValue, szCondition):
        listKeyValue = []
        for key, value in ditKeyValue:
            listKeyValue.append({key: value})
        return self.m_DatabaseFormObj.find({szCondition: listKeyValue})

    def InsertOne(self, dictKeyValue):
        """
        插入单条数据
        :param dictKeyValue:
        :return:
        """
        return self.m_DatabaseFormObj.insert_one(dictKeyValue)

    def InsertMany(self, dictKeyValues):
        """
        插入多条数据
        :param dictKeyValue:
        :return:
        """
        return self.m_DatabaseFormObj.insert_many(dictKeyValues)


DataFuncObj = DatabaseFunc()




