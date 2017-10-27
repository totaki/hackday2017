from handlers import *

routes = [
    (r'/api/v1/pipelines', PipelinesHandler),
    (r'/api/v1/test', TestHandler),
    (r'/api/v1/status', StatusHandler),
    (r'/api/v1/webhook/in', InWebhookHadler),
    (r'/api/v1/webhook/out', OutWebhookHadler),
]
