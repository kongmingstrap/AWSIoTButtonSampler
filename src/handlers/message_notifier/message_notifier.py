import os

import boto3

from boto3.dynamodb.conditions import Key

from slack_notifier import SlackNotifier


class MessageNotifier(object):
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')

    def publish(self):
        slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
        table_name = os.environ['DATABASE_NAME']

        try:
            table = self.dynamodb.Table(table_name)
            res = table.query(
                KeyConditionExpression=Key('device_id').eq('1')
            )['Items']

            if len(res) == 0:
                return {}

            item = res[0]

            place_name = item.get('place_name')
            message = item.get('message')
            state = item.get('state')

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

            SlackNotifier().publish(slack_webhook_url, slack_message)

            return slack_message
        except Exception as e:
            print(str(e))
