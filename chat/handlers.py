import pprint
import uuid

import tornado.web
from collections import deque, Counter
from tornado.ioloop import IOLoop
from tornado.options import options, define
from attr_dict import AttrDict

define('count_accept',default=1, type=1)


MESSAGES_DEQUE = deque()
RESPONSES = {}


def pretty_print(data):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data)


def check_is_hello(text):
    return text.lower() in {'/start', 'hi', 'hello', 'привет'}


class Activity(AttrDict):

    aliases = {
        'from_': 'from'
    }


def clean_store():
    global MESSAGES_DEQUE
    global RESPONSES
    MESSAGES_DEQUE = deque()
    RESPONSES = {}


class BaseHandler(tornado.web.RequestHandler):

    @property
    def client(self):
        return self.application.settings['skype_client']


class DropStateHandler(BaseHandler):

    def post(self):
        clean_store()
        self.client.clean_token()
        self.finish({})


class StatusHandler(BaseHandler):

    def get(self):
        try:
            message = MESSAGES_DEQUE.pop()
        except IndexError:
            message = None
        self.finish({'message': message})


class InWebhookHadler(BaseHandler):

    def post(self):
        activity = Activity.from_json(self.request.body)
        if options.debug:
            pretty_print(activity.as_dict)
        if activity.type == 'message':
            if check_is_hello(activity.text):
                IOLoop.current().add_callback(
                    self.client.send_message,
                    activity,
                    'Привет дорогой друг, давай пообщаемся'
                )
            else:
                id = uuid.uuid4().hex
                RESPONSES[id] = {'activity': activity, 'responses': []}
                message = {
                    'text': activity.text,
                    'suggests': self.get_suggests(activity.text),
                    'id': id
                }
                MESSAGES_DEQUE.extend([message] * options.count_accept)
        self.finish({})

    @staticmethod
    def get_suggests(text):
        return ['Suggest 1', 'Suggest 2']


class OutWebhookHadler(BaseHandler):

    def post(self):
        message = self.get_body_argument('response')
        id = self.get_body_argument('id')
        response = RESPONSES[id]
        response['responses'].append(message)
        if len(response['responses']) == options.count_accept:
            response_obj = RESPONSES.pop(id)
            counts = Counter(response_obj['responses'])
            max_possible = sorted(counts, key=lambda x: counts[x], reverse=True)
            IOLoop.current().add_callback(
                self.client.send_message,
                response_obj['activity'],
                max_possible[0]
            )
        self.finish({})


