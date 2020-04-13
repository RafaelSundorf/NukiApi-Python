from typing import List
import datetime

class Pin(dict):

    id = ""
    smartlockId = ""
    authId = ""
    type = 0
    name = ""
    enabled = True
    remoteAllowed = True
    lockCount = 0
    lastActiveDate = datetime.datetime(2020, 1, 1)
    creationDate = datetime.datetime(2020, 1, 1)
    updateDate = datetime.datetime(2020, 1, 1)
    code = ""
    raw = {}

    def __init__(self, id: str, smartlockId: str, authId: str, type: int, name: str, enabled: bool, remoteAllowed: bool, lockCount: int, lastActiveDate: datetime.datetime, creationDate: datetime.datetime, updateDate: datetime.datetime, code: str, raw: dict):
        self.id = id
        self.smartlockId = smartlockId
        self.authId = authId
        self.type = type
        self.name = name
        self.enabled = enabled
        self.remoteAllowed = remoteAllowed
        self.lockCount = lockCount
        self.lastActiveDate = lastActiveDate
        self.creationDate = creationDate
        self.updateDate = updateDate
        self.code = code
        self.raw = raw
        self.extended_infos = False
        if "allowedUntilDate" in raw:
            self.extended_infos = True
            self.allowedFromDate = raw["allowedFromDate"]
            self.allowedUntilDate = raw["allowedUntilDate"]
            self.allowedWeekDays = raw["allowedWeekDays"]
            self.allowedFromTime = raw["allowedFromTime"]
            self.allowedUntilTime = raw["allowedUntilTime"]
            dict.__init__(self, id=self.id, smartlockId=self.smartlockId, authId=self.authId, type=self.type,
                        name=self.name, enabled=self.enabled, remoteAllowed=self.remoteAllowed, lockCount=self.lockCount,
                        lastActiveDate=self.lastActiveDate, creationDate=self.creationDate, updateDate=self.updateDate,
                        code=self.code, raw=self.raw, extended_infos=self.extended_infos, allowedFromDate=self.allowedFromDate,
                        allowedUntilDate=self.allowedUntilDate, allowedWeekDays=self.allowedWeekDays, allowedFromTime=self.allowedFromTime,
                        allowedUntilTime=self.allowedUntilTime)
        else:
            dict.__init__(self, id=self.id, smartlockId=self.smartlockId, authId=self.authId, type=self.type,
                        name=self.name, enabled=self.enabled, remoteAllowed=self.remoteAllowed, lockCount=self.lockCount,
                        lastActiveDate=self.lastActiveDate, creationDate=self.creationDate, updateDate=self.updateDate,
                        code=self.code, raw=self.raw, extended_infos=self.extended_infos)

    def __eq__(self, other) -> bool:
        if type(other) == Pin:
            if other.id == self.id:
                return True
            else:
                return False
        else:
            return False

    def __repr__(self) -> dict:
        ret = {
            "id": self.id,
            "smartlockId": self.smartlockId,
            "authId": self.authId,
            "type": self.type,
            "name": self.name,
            "enabled": self.enabled,
            "remoteAllowed": self.remoteAllowed,
            "lockCount": self.lockCount,
            "lastActiveDate": self.lastActiveDate,
            "creationDate": self.creationDate,
            "updateDate": self.updateDate,
            "raw": self.raw
        }
        return ret

    def __str__(self) -> str:
        return "smartlock.Pin(id={id},smartlockId={smartlockId},authId={authId},type={type},name={name},enabled={enabled},remoteAllowed={remoteAllowed},lockCount={lockCount},lastActiveDate={lastActiveDate},creationDate={creationDate},updateDate={updateDate}".format(id=self.id, smartlockId=self.smartlockId, authId=self.authId, type=self.type, name=self.name, enabled=self.enabled, remoteAllowed=self.remoteAllowed, lockCount=self.lockCount, lastActiveDate=self.lastActiveDate, creationDate=self.creationDate, updateDate=self.updateDate)


class Smartlock(dict):
    """This class represents a smartlock, it has an id and name"""
    id = ""
    name = ""

    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        dict.__init__(self, id=self.id, name=self.name)

    def getPins(self, api) -> List[Pin]:
        return api.getAllPins(self.id)

    def __eq__(self, other):
        if isinstance(other, Smartlock):
            if self.id == other.id:
                return True
            else:
                return False
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, Smartlock):
            if self.id == other.id:
                return False
            else:
                return True
        else:
            return True

    def __repr__(self) -> str:
        return ("smartlock.Smartlock(name=" + self.name + ", id=" + self.id + ")")

    def __str__(self) -> str:
        return ("smartlock.Smartlock(name=" + self.name + ", id=" + self.id + ")")

    def __lt__(self, other):
        import utils
        me = utils.findApartNum(self.name)
        ot = utils.findApartNum(other.name)
        return me < ot

    def __le__(self, other):
        import utils
        me = utils.findApartNum(self.name)
        ot = utils.findApartNum(other.name)
        return me < ot