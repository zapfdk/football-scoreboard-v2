from channels.generic.websocket import WebsocketConsumer
import json

class DisplayConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        print(text_data_json["command"], text_data_json["value"])