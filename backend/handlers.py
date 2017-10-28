import json

import tornado.web
from tornado import gen

from mapper import mapper


class PipelinesHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        text = self.get_argument('text')
        processors = self.get_argument('processors')
        if not isinstance(processors, list):
            processors = [processors]
        processors = ['chars_replace', 'lowercase'] + processors
        text_object = {
            'text': text
        }
        for processor in processors:
            text_object = mapper[processor].process(text_object)

        self.finish(json.dumps(text_object))


class TestHandler(tornado.web.RequestHandler):

    def post(self):
        self.finish({})


class StatusHandler(tornado.web.RequestHandler):

    def get(self):
        self.finish({})


class InWebhookHadler(tornado.web.RequestHandler):

    def post(self):
        self.finish({})


class OutWebhookHadler(tornado.web.RequestHandler):

    def post(self):
        self.finish({})

