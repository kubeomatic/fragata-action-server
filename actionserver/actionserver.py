from dataclasses import dataclass
from actionserver.models.payload import Payload
from actionserver.models.payback import Payback
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
                payload = Payload(**json.loads(self.message.get_data()))
                payback = Payback(uuid=payload.getUuid(),job_id=payload.getJob_id())
                self.logger.info(f"{self.__class__.__name__} Received data UUID={payload.getUuid()}")
                time.sleep(1)
                if payload.getProvider().lower() == str(self.provider).lower() and payload.getKind().lower() == self.kind.lower():
                    rc_msg = self.action(action=payload.getAction(), payload=payload)
                    self.message.send_data(rc_msg)
                    self.logger.info(f"{self.__class__.__name__} Send data UUID={payload.getUuid()}")
                else:
                    self.logger.debug(payload)
                    payback.setStatus("error")
                    payback.setMessage("Action Server, kind or provider unknown")
                    # rc_msg = {"status": "error", "message": "Action Server, kind or provider unknown"}
                    self.logger.error(payback)
                    self.message.send_data(payback.toStr())
                    self.logger.info(f"{self.__class__.__name__} Send data UUID={payload.getUuid()}")
            except NotImplementedError as e:
                self.logger.error(f"Action Server, Missing method. Register missing method to fix this error. {e}")
                self.logger.error(
                    f"provider={payload.getProvider().lower()}, king={payload.getKind().lower()}, action={payload.getAction().lower()}")
                self.logger.debug(payload)
                payback.setStatus("error")
                payback.setMessage(f"Action Server, {str(e)}")
                # rc_msg = {"status": "error", "message": f"Action Server, {str(e)}"}
                self.logger.error(payback)
                self.message.send_data(payback.toStr())
                self.logger.info(f"{self.__class__.__name__} Send data UUID={payload.getUuid()}")
            except Exception as e:
                self.logger.error(f"Action Server Fail to read message, {e}")
                self.logger.error(
                    f"prrovider={payload.getProvider().lower()}, kind={payload.getKind().lower()}, action={payload.getAction().lower()}")
                self.logger.debug(payload)
                payback.setStatus("error")
                payback.setMessage(f"Action Server, {str(e)}.")
                # rc_msg = {"status": "error", "message": f"Action Server, {str(e)}."}
                self.logger.error(payback)
                self.message.send_data(payback.toStr())
                self.logger.info(f"{self.__class__.__name__} Send data UUID={payload.getUuid()}")

    def action(self, action: str, payload: SimpleNamespace) -> str:
        if hasattr(self, action) and callable(func := getattr(self, action)):
            return func(payload=payload)
        else:
            raise NotImplementedError(
                f'Could not cal method "{action}". Method "{action}" was not found in Class "{self.__class__.__name__}". Class "{self.__class__.__name__}" should implement method "{action}"')
