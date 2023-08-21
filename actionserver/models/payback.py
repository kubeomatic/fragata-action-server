import json
from dataclasses import dataclass
from types import SimpleNamespace

@dataclass(init=True)
class Payback:
    status: str = None
    message: str = None
    uuid: str = None
    job_id: str = None

    def __add__(self, other):
        data = {}
        for attr in self.getAttriburtes():
            if other.__getattribute__(attr) == None:
                data.update({attr: self.__getattribute__(attr)})
            else:
                data.update({attr: other.__getattribute__(attr)})
        return Payback(**data)

    def __repr__(self):
        data = {}
        for attr in self.getAttriburtes():
            data.update({attr: self.__getattribute__(attr)})
        return data

    def __str__(self):
        return json.dumps(self.__repr__())

    def __len__(self):
        count = 0
        for attr in self.getAttriburtes():
            if self.__getattribute__(attr) != None:
                count = count + 1
        return count

    def toDict(self):
        return self.__repr__()

    def getAttriburtes(self):
        return [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]

    def getMethods(self):
        return [attr for attr in dir(self) if callable(getattr(self, attr)) and not attr.startswith("__")]

    def toSimpleNamespace(self):
        return json.loads(self.__str__(), object_hook=lambda d: SimpleNamespace(**d))

    def toStr(self):
        return self.__str__()

    def gen_gettersetters(self):
        for attr in self.getAttriburtes():
            attr_type = str(type(getattr(self, attr))).split("'")[1]
            print(f"""
    def set{attr.capitalize()}(self, {attr}: {attr_type}):
        self.{attr} = {attr}
    def get{attr.capitalize()}(self) -> {attr_type}:
        return self.{attr}""")

    def setJob_id(self, job_id: str):
        self.job_id = job_id
    def getJob_id(self) -> str:
        return self.job_id

    def setMessage(self, message: str):
        self.message = message
    def getMessage(self) -> str:
        return self.message

    def setStatus(self, status: str):
        self.status = status
    def getStatus(self) -> str:
        return self.status

    def setUuid(self, uuid: str):
        self.uuid = uuid
    def getUuid(self) -> str:
        return self.uuid