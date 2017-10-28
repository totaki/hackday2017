import tornado.web
from tornado import gen

from mapper import mapper

class PipelinesHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        text_object = {
            'text': """ Моя доргая !ненастная ПОГОДА как) ты уже мне надоела"""
        }
        processors = ['punctuation_cleaner', 'alphabet_cleaner', 'speller', 'lemmatizer']
        for processor in processors:
            text_object = mapper[processor].process(text_object)
        print(text_object['prep_text'])
        self.finish(text_object)


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

