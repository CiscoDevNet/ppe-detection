from notification.provider import Provider


class Console(Provider):
    def __init__(self, config):
        self.room_id = config["room_id"]

    def send(self, msg):
        print("sending msg to", self.room_id)
        print(msg)
