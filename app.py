from types import SimpleNamespace
from dataclasses import dataclass
from actionserver.actionserver import ActionServer, ActionServerInterface

import logging
import json

class App(ActionServerInterface):
    def create(self, payload: SimpleNamespace) -> str:
        self.logger.info(payload)
        rc = {
            "status":"success",
            "job_id": payload.job_id,
            "payload": [],
            "messasge": "abc"
        }
        self.logger.info(payload)
        self.logger.info(type(json.dumps(rc)))
        self.logger.info(self.config.settings.test)
        return json.dumps(rc)

if __name__ == '__main__':


    app = App()
    runapp = ActionServer(obj=app, provider="azure", kind="redis")
    runapp.start_message_server()