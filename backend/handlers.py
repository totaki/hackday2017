import json

import tornado.web

from mapper import mapper


class PipelinesHandler(tornado.web.RequestHandler):
    async def get(self):
        text = self.get_argument('text')
        processors = self.get_argument('processors')
        if not isinstance(processors, list):
            processors = [processors]
        processors = ['chars_replace', 'lowercase'] + processors
        text_object = {
            'text': text
        }
        # Reset
        for processor in processors:
            text_object = mapper[processor].process(text_object)

        self.finish(json.dumps(text_object))


