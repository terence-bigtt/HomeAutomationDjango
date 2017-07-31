import uuid


class Device(object):
    def __init__(self, name, device_type, location, device_id=uuid.uuid4()):
        self.name = name
        self.device_type = device_type
        self.location = location
        self.device_id = device_id

    def run(self):
        pass
