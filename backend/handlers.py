import tornado.web


class PipelinesHandler(tornado.web.RequestHandler):

    def get(self):
        self.finish({})


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

