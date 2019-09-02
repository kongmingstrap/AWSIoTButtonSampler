import os

import boto3

from boto3.dynamodb.conditions import Key

from logger.logger import Logger
from slack_notifier import SlackNotifier

logger = Logger().getLogger(__name__)


class MessageNotifier(object):
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')

    def publish(self, event: dict) -> dict:
        slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
        table_name = os.environ['DATABASE_NAME']

        try:
            device_id = self.get_device_id_from_event(event)
            table = self.dynamodb.Table(table_name)
            res = table.query(
                KeyConditionExpression=Key('device_id').eq(device_id)
            )['Items']

            if len(res) == 0:
                logger.info(f'{device_id} is not found.')
                return {}

            item = res[0]

            slack_username = item.get('slack_username', '')
            slack_text = item.get('slack_text', '')
            slack_icon_emoji = item.get('slack_icon_emoji', '')

            slack_message = {
                'slack_username': slack_username,
                'slack_text': slack_text,
                'slack_icon_emoji': slack_icon_emoji
            }

            SlackNotifier().publish(slack_webhook_url, slack_message)

            return slack_message
        except Exception as e:
            logger.error(f'Exception occurred: {e}', exc_info=True)
            raise e

    def get_device_id_from_event(self, event: dict) -> str:
        return event['deviceInfo']['deviceId']
