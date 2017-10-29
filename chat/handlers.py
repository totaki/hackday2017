import logging
import pprint
import urllib.parse
import uuid
import json

from datetime import datetime

import tornado.web
from os import getenv
from collections import Counter

from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop
from tornado.options import options, define
from attr_dict import AttrDict

define('count_accept', default=getenv('count_accept', 1), type=int)
define('WIT_TOKEN', default=getenv('WIT_TOKEN', 1), type=str)


MESSAGES_DEQUE = []
RESPONSES = {}


def json2data(response):
    if isinstance(response, bytes):
        response = response.decode()
    return json.loads(response)


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
    MESSAGES_DEQUE = []
    RESPONSES = {}


class BaseHandler(tornado.web.RequestHandler):

    @property
    def client(self):
        return self.application.settings['skype_client']


class DropStateHandler(BaseHandler):

    def get(self):
        clean_store()
        self.client.remove_token()
        self.finish({})


class StatusHandler(BaseHandler):

    def get(self):
        user_id = self.request.headers.get("userId", None)
        logging.warning(f'Request from userId: {user_id}')
        message = None
        logging.warning(f'Messages len {len(MESSAGES_DEQUE)}')
        if len(MESSAGES_DEQUE):
            index = -1
            while abs(index) <= len(MESSAGES_DEQUE):
                message_ = MESSAGES_DEQUE[index]
                responses = RESPONSES[message_['id']]
                if user_id not in responses['senders']:
                    message = MESSAGES_DEQUE.pop(index)
                    logging.warning(f'Messages len after take {len(MESSAGES_DEQUE)}')
                    break
                index -= 1
        logging.warning(f'Taken {user_id} for {message and message["id"]}')
        self.finish({'message': message})


class InWebhookHadler(BaseHandler):

    async def post(self):
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
                RESPONSES[id] = {
                    'activity': activity,
                    'responses': [],
                    'senders': [],
                    'created_at': datetime.utcnow().timestamp()
                }
                MESSAGES_DEQUE.extend([
                    {
                        'text': activity.text,
                        'suggests': (await self.get_suggests(activity.text)),
                        'id': id
                    }
                    for i in range(int(options.count_accept))
                ])
        self.finish({})

    @staticmethod
    async def get_suggests(text):
        client = AsyncHTTPClient()
        data = urllib.parse.urlencode({
            'q': text,
            'n': 2
        })
        response = await client.fetch(
            f'https://api.wit.ai/message?{data}',
            headers={'Authorization': f'Bearer {options.WIT_TOKEN}'}
        )
        return [i['value'] for i in json2data(response)['entities']['intent']]


class OutWebhookHadler(BaseHandler):

    def post(self):
        user_id = self.request.headers.get("userId", None)
        message = self.get_body_argument('response')
        id = self.get_body_argument('id')
        response = RESPONSES.get(id, None)
        if response:
            response['responses'].append(message)
            response['senders'].append(user_id)
            logging.warning(f'Response from {user_id} for {id}')
            if len(response['responses']) == int(options.count_accept):
                response_obj = RESPONSES.pop(id)
                counts = Counter(response_obj['responses'])
                max_possible = sorted(counts, key=lambda x: counts[x], reverse=True)
                IOLoop.current().add_callback(
                    self.client.send_message,
                    response_obj['activity'],
                    max_possible[0]
                )
        self.finish({})


