import json

from botocore.vendored import requests


class ChatworkNotifier(object):
    def publish(self, chatwork_token, chatwork_room_id, message):
        try:
            headers = {
                'X-ChatWorkToken': chatwork_token,
                'Content-Type': 'application/json'
            }
            payload = self.make_payload(message)
            requests.post(f'https://api.chatwork.com/v2/rooms/{chatwork_room_id}/messages',
                          params=payload,
                          headers=headers)
        except Exception as e:
            print(str(e))

    def make_payload(self, message):
        text = message['chatwork_text']

        return {
            'body': text
        }
