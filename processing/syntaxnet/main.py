# coding=utf-8
import json
import logging
import os
import tornado.web
from tornado.concurrent import run_on_executor
from tornado.ioloop import IOLoop
from concurrent.futures import ThreadPoolExecutor


class SyntaxParseHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(max_workers=5)

    @run_on_executor
    def parse(self, text):
        res = os.system('echo "{}" | /opt/tensorflow/syntaxnet/syntaxnet/models/parsey_universal/parse.sh /opt/tensorflow/syntaxnet/russian > tmp'.format(text))
        # res = os.system('echo "{}" > tmp'.format(text))
        # res = os.system('echo "{}" | ./syntaxnet/models/parsey_universal/parse.sh ./russian/ > tmp'.format(text))
        return res

    @tornado.gen.coroutine
    def get(self):
        text = self.get_argument('text').encode('utf-8')
        data = yield self.parse(text)
        if data:
            raise OSError
        result = []
        with open('tmp') as f:
            lines = f.readlines()
            logging.error(lines)
            for line in lines[:-1]:
                logging.error(line)
                line = line.split()
                word_tagging = {
                    'index': line[0],
                    'POS': line[3],
                    'parent': line[6],
                    'RIS': line[7],
                }
                result.append(word_tagging)
        self.finish(json.dumps(result))


if __name__ == u'__main__':
    application = tornado.web.Application([
        (r"/parse", SyntaxParseHandler),
    ])
    application.listen(9999)
    IOLoop.current().start()
