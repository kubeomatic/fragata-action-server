from types import SimpleNamespace
from actionserver.actionserver import ActionServer
import json


class App(ActionServer):
    def create(self, payload: SimpleNamespace) -> str:
        rc = {
            "uuid": payload.uuid,
            "status": "success",
            "job_id": payload.job_id,
            "payload": [],
            "message": "abc"
        }
        self.logger.debug(payload)
        self.logger.debug(type(json.dumps(rc)))
        self.logger.debug(self.config.settings.test)
        return json.dumps(rc)


if __name__ == '__main__':
    app = App(provider="azure", kind="redis")
    app.start()