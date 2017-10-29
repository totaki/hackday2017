from handlers import *

routes = [
    (r'/api/v1/pipelines', PipelinesHandler),
    (r'/api/v1/websocket', PipelinesWebSocketHandler),
]
