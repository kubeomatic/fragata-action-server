from dataclasses import dataclass

from actionserver.config.config import Config
from actionserver.service.message import Message
import time
import logging
import inspect
import json
from types import SimpleNamespace

@dataclass(init=True, repr=True)
class ActionServerObjInterface:
    obj: object
    config = Config()
    logger = logging.getLogger(__name__)
    logger.setLevel(config.get_loglevel())
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=config.get_loglevel(),
        datefmt='%Y-%m-%d %H:%M:%S')

    # def _status(self, payload: SimpleNamespace) -> str:
    #     return self.obj.status(payload=payload)
    # def _start(self, payload: SimpleNamespace) -> str:
    #     return self.obj.start(payload=payload)
    # def _stop(self, payload: SimpleNamespace) -> str:
    #     return self.obj.stop(payload=payload)
    # def _restart(self, payload: SimpleNamespace) -> str:
    #     return self.obj.restart(payload=payload)
    # def _list(self, payload: SimpleNamespace) -> str:
    #     return self.obj.list(payload=payload)
    # def _create(self, payload: SimpleNamespace) -> str:
    #     return self.obj.create(payload=payload)
    # def _delete(self, payload: SimpleNamespace) -> str:
    #     return self.obj.delete(payload=payload)
    # def _update(self, payload: SimpleNamespace) -> str:
    #     return self.obj.update(payload=payload)
    # def _recreate(self, payload: SimpleNamespace) -> str:
    #     return self.obj.recreate(payload=payload)
    # def _docs(self, payload: SimpleNamespace) -> str:
    #     return self.obj.docs(payload=payload)
    # def _show(self, payload: SimpleNamespace) -> str:
    #     return self.obj.show(payload=payload)
    def action(self,action: str, payload: SimpleNamespace) -> str:
        if hasattr(self,action) and callable(func := getattr(self, action)):
            return func(payload=payload)

@dataclass(init=True, repr=True)
class ActionServerInterface:
    config = Config()
    logger = logging.getLogger(__name__)
    logger.setLevel(config.get_loglevel())
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=config.get_loglevel(),
        datefmt='%Y-%m-%d %H:%M:%S')
    logger.info("Action Server Start")

    def make_action(self,action):
        def inneraction(payload: SimpleNamespace) -> str:
            raise NotImplementedError(f"Subclass, {self.__class__.__name__}, should implement method \"{action}\"")
        inneraction.__doc__ = f"docstring for {action}"
        inneraction.__name__ = action
        setattr(self,inneraction.__name__,inneraction)

    def status(self, payload: SimpleNamespace) -> str:
        raise NotImplementedError(
            f"Subclas, {self.__class__.__name__}, should implement method \"{inspect.currentframe().f_code.co_name}")
    def start(self,payload: SimpleNamespace) -> str:
        raise NotImplementedError(f"Subclas, {self.__class__.__name__}, should implement method \"{inspect.currentframe().f_code.co_name}")
    def stop(self,payload: SimpleNamespace) -> str:
        raise NotImplementedError(f"Subclas, {self.__class__.__name__}, should implement method \"{inspect.currentframe().f_code.co_name}")
    def restart(self,payload: SimpleNamespace) -> str:
        raise NotImplementedError(f"Subclas, {self.__class__.__name__}, should implement method \"{inspect.currentframe().f_code.co_name}")
    def list(self,payload: SimpleNamespace) -> str:
        raise NotImplementedError(f"Subclas, {self.__class__.__name__}, should implement method \"{inspect.currentframe().f_code.co_name}")
    def create(self,payload: SimpleNamespace) -> str:
        raise NotImplementedError(f"Subclas, {self.__class__.__name__}, should implement method \"{inspect.currentframe().f_code.co_name}")
    def delete(self,payload: SimpleNamespace) -> str:
        raise NotImplementedError(f"Subclas, {self.__class__.__name__}, should implement method \"{inspect.currentframe().f_code.co_name}")
    def update(self,payload: SimpleNamespace) -> str:
        raise NotImplementedError(f"Subclas, {self.__class__.__name__}, should implement method \"{inspect.currentframe().f_code.co_name}")
    def recreate(self,payload: SimpleNamespace) -> str:
        raise NotImplementedError(f"Subclas, {self.__class__.__name__}, should implement method \"{inspect.currentframe().f_code.co_name}")
    def docs(self,payload: SimpleNamespace) -> str:
        raise NotImplementedError(f"Subclas, {self.__class__.__name__}, should implement method \"{inspect.currentframe().f_code.co_name}")
    def show(self,payload: SimpleNamespace) -> str:
        raise NotImplementedError(f"Subclas, {self.__class__.__name__}, should implement method \"{inspect.currentframe().f_code.co_name}")

@dataclass(init=True, repr=True)
class ActionServer(ActionServerObjInterface):
    provider: str
    kind: str
    message_server: str = "tcp://127.0.0.1:5555"
    def start_message_server(self) -> bool:
        try:
            self.message = Message(server=self.message_server)
            self.message.listen()
        except Exception as e:
            self.logger.error(f"Action Server fail to start message, {e}")
        else:
            self.logger.info(f"Action Server message started at {self.message_server}")
        while True:
            try:
                msg = json.loads(self.message.get_data(), object_hook=lambda d: SimpleNamespace(**d))
                self.logger.info(f"{self.__class__.__name__} Received data UUID={msg.uuid}")
                time.sleep(1)
                if str(msg.provider).lower() == str(self.provider).lower() and str(msg.kind).lower() == str(self.kind).lower():
                    rc_msg = self.start_action(action=msg.action, payload=msg)
                    self.message.send_data(rc_msg)
                    self.logger.info(f"{self.__class__.__name__} Send data UUID={msg.uuid}")
                else:
                    self.logger.debug(msg)
                    rc_msg = {"status": "error", "message": "Action Server, kind or provider unknown"}
                    self.logger.error(rc_msg)
                    self.message.send_data(json.dumps(rc_msg))
                    self.logger.info(f"{self.__class__.__name__} Send data UUID={msg.uuid}")
            except NotImplementedError as e:
                self.logger.error(f"Action Server, Missing method. Register missing method to fix this error. {e}")
                self.logger.error(f"provider={str(msg.provider).lower()}, king={str(msg.kind).lower()}, action={str(msg.action).lower()}")
                self.logger.debug(msg)
                rc_msg = { "status": "error", "message": f"Action Server, {str(e)}"}
                self.logger.error(rc_msg)
                self.message.send_data(json.dumps(rc_msg))
                self.logger.info(f"{self.__class__.__name__} Send data UUID={msg.uuid}")
            except Exception as e:
                self.logger.error(f"Action Server Fail to read message, {e}")
                self.logger.error(f"prrovider={str(msg.provider).lower()}, kind={str(msg.kind).lower()}, action={str(msg.action).lower()}")
                self.logger.debug(msg)
                rc_msg = { "status": "error", "message": f"Action Server, {str(e)}."}
                self.logger.error(rc_msg)
                self.message.send_data(json.dumps(rc_msg))
                self.logger.info(f"{self.__class__.__name__} Send data UUID={msg.uuid}")
    def start_action(self, action: str, payload: SimpleNamespace) -> str:
        return self.action(action=action, payload=payload)
        # if action == "status":
        #     return self._status(payload=payload)
        # elif action == "start":
        #     return self._start(payload=payload)
        # elif action == "stop":
        #     return self._stop(payload=payload)
        # elif action == "restart":
        #     return self._restart(payload=payload)
        # elif action == "list":
        #     return self._list(payload=payload)
        # elif action == "create":
        #     return self._create(payload=payload)
        # elif action == "delete":
        #     return self._delete(payload=payload)
        # elif action == "update":
        #     return self._update(payload=payload)
        # elif action == "recreate":
        #     return self._recreate(payload=payload)
        # elif action == "docs":
        #     return self._docs(payload=payload)
        # elif action == "show":
        #     return self._show(payload=payload)

# class ActionServerError(Exception):
#     pass

