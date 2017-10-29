import json

import tornado.web
from tornado import websocket, ioloop
from tornado.gen import coroutine

from mapper import mapper

live_web_sockets = set()

class PipelinesHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        text = self.get_argument('text')
        processors = self.get_arguments('processors')
        if not isinstance(processors, list):
            processors = [processors]
        async_processors = ['syntax_tagger', 'speller']
        processors = ['chars_replace', 'lowercase', 'word_tokenizer'] + processors
        text_object = {
            'text': text
        }
        for processor in processors:
            if processor in async_processors:
                text_object = yield mapper[processor].process(text_object)
            else:
                text_object = mapper[processor].process(text_object)
        result = json.dumps(text_object)
        ioloop.IOLoop.current().add_callback(
            PipelinesWebSocketHandler.web_socket_send_message, result)
        self.finish(result)


class PipelinesWebSocketHandler(websocket.WebSocketHandler):
    def open(self):
        self.set_nodelay(True)
        live_web_sockets.add(self)
        self.write_message("Welcome to TNLP")

    def on_message(self, message):
        print(message)

    def on_close(self):
        print("WebSocket closed")

    @staticmethod
    def web_socket_send_message(message):
        removable = set()
        for ws in live_web_sockets:
            if not ws.ws_connection or not ws.ws_connection.stream.socket:
                removable.add(ws)
            else:
                ws.write_message(message)
        for ws in removable:
            live_web_sockets.remove(ws)

    def check_origin(self, origin):
        return True
