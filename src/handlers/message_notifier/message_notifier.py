import os

import boto3

from boto3.dynamodb.conditions import Key

from chatwork_notifier import ChatworkNotifier
from slack_notifier import SlackNotifier


class MessageNotifier(object):
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')

    def publish(self):
        chatwork_token = os.environ['CHATWORK_TOKEN']
        chatwork_room_id = os.environ['CHATWORK_ROOM_ID']
        slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
        table_name = os.environ['DATABASE_NAME']

        try:
            table = self.dynamodb.Table(table_name)
            res = table.query(
                KeyConditionExpression=Key('device_id').eq('1')
            )['Items'][0]

            place_name = res.get('place_name')
            message = res.get('message')
            state = res.get('state')

            if state == 'locked':
                message = f'{place_name} unlocked.'
                state = 'unlocked'
            else:
                message = f'{place_name} locked.'
                state = 'locked'

            table.put_item(
                Item={
                    'device_id': '1',
                    'state': state,
                    'message': message,
                    'place_name': place_name
                }
            )

            slack_message = {
                'slack_username': f'{place_name}',
                'slack_text': message,
                'slack_icon_emoji': ':fukkeikun:'
            }

            chatwork_message = {
                'chatwork_text': message
            }

            SlackNotifier().publish(slack_webhook_url, slack_message)
            ChatworkNotifier().publish(chatwork_token, chatwork_room_id, chatwork_message)
        except Exception as e:
            print(str(e))
