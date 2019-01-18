import json

from botocore.vendored import requests


class SlackNotifier(object):
    def publish(self, api_endpoint, message):
        try:
            headers = {
                'Content-Type': 'application/json; charset=utf-8'
            }
            payload = self.make_payload(message)
            requests.post(api_endpoint, data=json.dumps(payload), headers=headers)
        except Exception as e:
            print(str(e))

    def make_payload(self, message):
        username = message['slack_username']
        text = message['slack_text']
        icon_emoji = message['slack_icon_emoji']

        return {
            'username': username,
            'text': text,
            'icon_emoji': icon_emoji
        }
