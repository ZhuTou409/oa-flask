

class ModelBase:
    def __init__(self, MainKeyObj, dictInfo=None):
        if dictInfo is None:
            self.InitByMainKey(MainKeyObj)
        else:
            self.InitByDict(dictInfo)

    def InitByMainKey(self, MainKeyObj):
        """
        通过外部传入键值，从数据库中初始化数据
        :param MainKeyObj:
        :return:
        """
        pass

    def InitByDict(self, InfoDict):
        """
        通过外部传入数据字典，首次初始化
        :param InfoDict:
        :return:
        """
        pass

    def InsertAllInfoToForm(self):
        pass

    def CheckIsNewKeyValuePair(self, dictInfo):
        """
        检查是否是新属性
        :param dictInfo:
        :return:
        """
        pass



