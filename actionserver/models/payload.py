import json
from dataclasses import dataclass
from types import SimpleNamespace


@dataclass(init=True)
class Payload:
    job_id: str = None
    provider: str = None
    kind: str = None
    environment: str = None
    wait: bool = None
    break_on_error: bool = None
    action: str = None
    owner: str = None
    description: str = None
    resource_data: str = None
    provider_data: str = None
    uuid:str = None

    def __add__(self, other):
        data = {}
        for attr in self.getAttriburtes():
            if other.__getattribute__(attr) == None:
                data.update({attr: self.__getattribute__(attr)})
            else:
                data.update({attr: other.__getattribute__(attr)})
        return Payload(**data)

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

    def gen_gettersetters(self):
        for attr in self.getAttriburtes():
            print(f"""
    def set{attr.capitalize()}(self,{attr}: str):
        self.{attr} = {attr}
    def get{attr.capitalize()}(self) -> str:
        return self.{attr}""")

    def setAction(self, action: str):
        self.action = action

    def getAction(self) -> str:
        return self.action

    def setBreak_on_error(self, break_on_error: bool):
        self.break_on_error = break_on_error

    def getBreak_on_error(self) -> bool:
        return self.break_on_error

    def setDescription(self, description: str):
        self.description = description

    def getDescription(self) -> str:
        return self.description

    def setEnvironment(self, environment: str):
        self.environment = environment

    def getEnvironment(self) -> str:
        return self.environment

    def setJob_id(self, job_id: str):
        self.job_id = job_id

    def getJob_id(self) -> str:
        return self.job_id

    def setKind(self, kind: str):
        self.kind = kind

    def getKind(self) -> str:
        return self.kind

    def setOwner(self, owner: str):
        self.owner = owner

    def getOwner(self) -> str:
        return self.owner

    def setProvider(self, provider: str):
        self.provider = provider

    def getProvider(self) -> str:
        return self.provider

    def setProvider_data(self, provider_data: str):
        self.provider_data = provider_data

    def getProvider_data(self) -> str:
        return self.provider_data

    def setResource_data(self, resource_data: str):
        self.resource_data = resource_data

    def getResource_data(self) -> str:
        return self.resource_data

    def setWait(self, wait: bool):
        self.wait = wait

    def getWait(self) -> bool:
        return self.wait

    def setUuid(self, uuid: str):
        self.uuid = uuid

    def getUuid(self) -> str:
        return self.uuid

