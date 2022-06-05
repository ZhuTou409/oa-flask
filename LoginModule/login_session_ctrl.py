import time
from werkzeug.security import generate_password_hash, check_password_hash

# 24小时
MAX_LOGIN_SAVE_TIME_SEC = 24 * 60 * 60
# 一个小时检查一次
CHECK_SAVE_SESSION_TO_FILE = 1 * 60 * 60


class LoginSessionController:
    def __init__(self):
        self.m_mapNowLoginSession = {}
        self.m_nLastCheckTime = time.time()

    def OnUpdate(self):
        nCreateTime = time.time()
        if nCreateTime - self.m_nLastCheckTime > CHECK_SAVE_SESSION_TO_FILE:
            dictNowLoginSessionCopy = self.m_mapNowLoginSession.copy()
            for Session, SessionObj in dictNowLoginSessionCopy.items():
                # 超过一定时间没有提交记录，则准备删除
                if self.m_nLastCheckTime - SessionObj.m_nCreateTime > MAX_LOGIN_SAVE_TIME_SEC:
                    self.m_mapNowLoginSession.pop(Session)

    def CreateNewSession(self, szUserName, szPassword):
        NewSessionInfoObj = SessionInfo.CreateNewSessionInfo(szUserName, szPassword)
        self.m_mapNowLoginSession[NewSessionInfoObj.m_szSession] = NewSessionInfoObj
        return NewSessionInfoObj.m_szSession

    def RefreshSession(self, szSession):
        SessionObject = self.m_mapNowLoginSession.get(szSession)
        if SessionObject is None:
            return False

        SessionObject.RefreshTime()

    def GetNowLoginUserList(self):
        pass

    def GetNowLoginSessionList(self):
        return self.m_mapNowLoginSession.keys()

    """
    根据时间检查是否需要从内存存储转到硬盘存储
    """
    def CheckCanStoreToFile(self):
        pass


class SessionInfo:
    def __init__(self, szSession, nCreateTime, szUserName):
        self.m_szSession = szSession
        self.m_nCreateTime = nCreateTime
        self.m_szUserName = szUserName
        self.m_bPreDelete = False

    """
    session信息是否相等
    """
    def IsEqual(self, InSessionInfoObj):
        if InSessionInfoObj.m_szSession != self.m_szSession:
            return False
        
        nNowTime = time.time()
        if InSessionInfoObj.m_nCreateTime - nNowTime > MAX_LOGIN_SAVE_TIME_SEC:
            return False
        
        return True

    def RefreshTime(self):
        self.m_nCreateTime = time.time()

    @staticmethod
    def CreateNewSessionInfo(szUserName, szPassword):
        nCreateTime = time.time()
        szPreSession = szUserName + szPassword + str(nCreateTime)
        szSession = generate_password_hash(szPreSession)
        NewSessionInfoObj = SessionInfo(szSession, nCreateTime, szUserName)
        return NewSessionInfoObj


LoginSession = LoginSessionController()



