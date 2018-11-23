import os

import boto3

from boto3.dynamodb.conditions import Key
from botocore.vendored import requests


dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    chatwork_token = os.environ['CHATWORK_TOKEN']
    chatwork_room_id = os.environ['CHATWORK_ROOM_ID']
    table_name = os.environ['DATABASE_NAME']

    table = dynamodb.Table(table_name)

    res = table.query(
        KeyConditionExpression=Key('device_id').eq('1')
    )['Items'][0]

    message = res.get('message')
    state = res.get('state')

    if state == 'locked':
        message = 'office 7 unlocked.'
        state = 'unlocked'
    else:
        message = 'office 7 locked.'
        state = 'locked'

    res = table.put_item(
        Item={
            'device_id': '1',
            'state': state,
            'message': message
        }
    )

    payload = {'body': message}
    headers = {'X-ChatWorkToken': chatwork_token, 'Content-Type': 'application/json'}
    response = requests.post(f'https://api.chatwork.com/v2/rooms/{chatwork_room_id}/messages',
                             params=payload,
                             headers=headers)


    print(response)
