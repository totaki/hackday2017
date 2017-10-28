import json
import urllib.parse
from tornado.options import options
from tornado.httpclient import AsyncHTTPClient, HTTPRequest


CONVERSATION_PATH = '{}/v3/conversations/{}/activities'


def json2data(response):
    if isinstance(response, bytes):
        response = response.decode()
    return json.loads(response)


class SkypeClient(object):

    def __init__(self):
        self.auth_credentials = urllib.parse.urlencode({
            'grant_type': 'client_credentials',
            'client_id': options.MICROSOFT_APP_ID,
            'client_secret': options.MICROSOFT_APP_PASSWORD,
            'scope': options.MICROSOFT_OAUTH_SCOPE
        })
        self.oauth_url = options.MICROSOFT_OAUTH_URL
        self.access_token_data = {}

    def remove_token(self):
        self.access_token_data = {}

    async def send_message(self, activity, message):
        recipient = activity.from_
        from_ = activity.recipient
        activity.update({'from': from_.as_dict, 'recipient': recipient.as_dict})
        activity.text = message
        await self._post_json(
            CONVERSATION_PATH.format(activity.serviceUrl, activity.conversation.id),
            activity.to_json()
        )

    @property
    def access_token(self):
        return self.access_token_data.get('access_token', None)

    async def _post_json(self, url, json_data):
        if not self.access_token:
            self.access_token_data = await self._fetch_bot_token()
        client = AsyncHTTPClient()
        request = HTTPRequest(url, method='POST', body=json_data.encode(), headers={
            'Content-Type': 'application/json',
            'Authorization': '{} {}'.format(self.access_token_data['token_type'], self.access_token)
        })
        if options.debug:
            print(json_data)
            print('{} {}'.format(self.access_token_data['token_type'], self.access_token))
            print(options.MICROSOFT_APP_ID)
            print(options.MICROSOFT_APP_PASSWORD)
        response = await client.fetch(request=request)
        return json2data(response.body)

    async def _fetch_bot_token(self):
        client = AsyncHTTPClient()
        response = await client.fetch(
            self.oauth_url,
            method='POST',
            body=self.auth_credentials,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
        )
        return json2data(response.body)