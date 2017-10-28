import tornado.ioloop
import tornado.web
from routes import routes


def make_app():
    return tornado.web.Application(routes, debug=True)


if __name__ == "__main__":
    app = make_app()
    app.listen(9000)
    print('Start server')
    tornado.ioloop.IOLoop.current().start()