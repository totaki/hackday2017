import json

import tornado.web
from tornado.gen import coroutine

from mapper import mapper


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
        print(text_object)
        self.finish(json.dumps(text_object))
