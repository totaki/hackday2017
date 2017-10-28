import json

import tornado.web

from mapper import mapper


class PipelinesHandler(tornado.web.RequestHandler):
    async def get(self):
        text = self.get_argument('text')
        processors = self.get_argument('processors')
        if not isinstance(processors, list):
            processors = [processors]
        async_processors = ['syntax_tagger']
        processors = ['chars_replace', 'lowercase'] + processors
        text_object = {
            'text': text
        }
        # Reset
        for processor in processors:
            if processor in async_processors:
                text_object = await mapper[processor].process(text_object)
            else:
                text_object = mapper[processor].process(text_object)

        self.finish(json.dumps(text_object))
