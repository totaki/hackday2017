import logging
from os import getenv
import tornado.ioloop
import tornado.web
from routes import routes
from tornado.options import options, define

from client import SkypeClient


define('debug', default=getenv('debug', False), type=bool)
define('port', default=8000, type=int)

define('MICROSOFT_APP_ID',
       default=getenv('MICROSOFT_APP_ID', None), group='application')
define('MICROSOFT_APP_PASSWORD',
       default=getenv('MICROSOFT_APP_PASSWORD', None), group='application')
define(
    'MICROSOFT_OAUTH_URL',
    default='https://login.microsoftonline.com/botframework.com/oauth2/v2.0/token',
    group='application'
)
define(
    'MICROSOFT_OAUTH_SCOPE',
    default='https://api.botframework.com/.default',
    group='application'
)
define(
    'MICROSOFT_OPENID_URL',
    default='https://login.botframework.com/v1/.well-known/openidconfiguration',
    group='application'
)

def make_app():
    return tornado.web.Application(
        routes,
        debug=options.debug,
        skype_client=SkypeClient()
    )


if __name__ == "__main__":
    options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    logging.warning(f'Debug mode: {options.debug}')
    logging.warning(f'Start server port: {options.port}')
    logging.warning(f'Count accept: {options.count_accept}')
    tornado.ioloop.IOLoop.current().start()
