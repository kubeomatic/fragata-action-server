from dataclasses import dataclass
import logging
import zmq

from actionserver.config.config import Config


@dataclass(init=True, repr=True)
class Message:
    server: str = "tcp://localhost:5555"
    context = zmq.Context()
    config = Config()
    logger = logging.getLogger(__name__)
    logger.setLevel(config.get_loglevel())
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=config.get_loglevel(),
        datefmt='%Y-%m-%d %H:%M:%S')



    def connect(self):
        try:
            self.socket = self.context.socket(zmq.REQ)
            self.socket.connect(self.server)
        except Exception as e:
            self.logger.error(f"ZMQ fail to connect to {self.server}, {e}")
        else:
            self.logger.debug(f"ZMQ connected to { self.server}")

    def listen(self):
        try:
            self.socket = self.context.socket(zmq.REP)
            self.socket.bind(self.server)
        except Exception as e:
            self.logger.error(f"ZMQ Fail to connect to {self.server}, {e}")
        else:
            self.logger.debug(f"ZMQ started listen as {self.server}")

    def get_data(self):
        try:
            response = self.socket.recv()
            self.logger.debug(f"ZMQ Received message=\"{response}\"")
        except Exception as e:
            self.logger.error(f"ZMQ Fail to get data, {e}")
            return response
        else:
            self.logger.debug(f"ZMQ DATA=\"{response}\" received")
            return response

    def send_data(self,data):
        try:
            self.socket.send(bytes(data,'utf-8'))
        except Exception as e:
            self.logger.error(f"ZMQ Fail to send data , {e}."
                f"Check if the returning message is a string. Cannot be an object")
        finally:
            self.logger.debug(f"ZMQ Fail to send data=\"{data}\"")

