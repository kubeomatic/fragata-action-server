from dataclasses import dataclass
from actionserver.models.payload import Payload
from actionserver.config.config import Config
from actionserver.service.message import Message
import time
import logging
import json
from types import SimpleNamespace


@dataclass(init=True, repr=True)
class ActionServer:
    provider: str = None
    kind: str = None
    message: str = None
    message_server: str = "tcp://127.0.0.1:5555"
    config = Config()
    logger = logging.getLogger(__name__)
    logger.setLevel(config.get_loglevel())
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=config.get_loglevel(),
        datefmt='%Y-%m-%d %H:%M:%S')

    def start(self):
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
                if str(msg.provider).lower() == str(self.provider).lower() and str(msg.kind).lower() == str(
                        self.kind).lower():
                    rc_msg = self.action(action=msg.action, payload=msg)
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
                self.logger.error(
                    f"provider={str(msg.provider).lower()}, king={str(msg.kind).lower()}, action={str(msg.action).lower()}")
                self.logger.debug(msg)
                rc_msg = {"status": "error", "message": f"Action Server, {str(e)}"}
                self.logger.error(rc_msg)
                self.message.send_data(json.dumps(rc_msg))
                self.logger.info(f"{self.__class__.__name__} Send data UUID={msg.uuid}")
            except Exception as e:
                self.logger.error(f"Action Server Fail to read message, {e}")
                self.logger.error(
                    f"prrovider={str(msg.provider).lower()}, kind={str(msg.kind).lower()}, action={str(msg.action).lower()}")
                self.logger.debug(msg)
                rc_msg = {"status": "error", "message": f"Action Server, {str(e)}."}
                self.logger.error(rc_msg)
                self.message.send_data(json.dumps(rc_msg))
                self.logger.info(f"{self.__class__.__name__} Send data UUID={msg.uuid}")

    def action(self, action: str, payload: SimpleNamespace) -> str:
        if hasattr(self, action) and callable(func := getattr(self, action)):
            return func(payload=payload)
        else:
            raise NotImplementedError(
                f'Could not cal method "{action}". Method "{action}" was not found in Class "{self.__class__.__name__}". Class "{self.__class__.__name__}" should implement method "{action}"')
