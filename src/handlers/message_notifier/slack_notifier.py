import json

from botocore.vendored import requests
from logger.logger import Logger

logger = Logger().getLogger(__name__)


class SlackNotifier(object):
    def publish(self, api_endpoint: str, message: dict) -> dict:
        try:
            logger.info(f'message: {message}')
            headers = {
                'Content-Type': 'application/json; charset=utf-8'
            }
            payload = self.make_payload(message)
            logger.info(f'payload: {payload}')
            requests.post(api_endpoint, json.dumps(payload), headers)
            return payload
        except Exception as e:
            logger.error(f'Exception occurred: {e}', exc_info=True)
            raise e

    def make_payload(self, message: dict) -> dict:
        username = message['slack_username']
        text = message['slack_text']
        icon_emoji = message['slack_icon_emoji']

        return {
            'username': username,
            'text': text,
            'icon_emoji': icon_emoji
        }
