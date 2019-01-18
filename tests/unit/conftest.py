import os

import pytest

from utils import DynamoDBLocal

os.environ['CHATWORK_TOKEN'] = 'ChatWorkToken'
os.environ['CHATWORK_ROOM_ID'] = 'ChatworkRoomId'
os.environ['SLACK_WEBHOOK_URL'] = 'SlackWebhookURL'
os.environ['DATABASE_NAME'] = 'room_table'


@pytest.fixture(scope='function')
def dynamodb(request):
    dynamodb_objs = []

    for dynamodb_info in request.param:
        dynamodb_local = DynamoDBLocal(dynamodb_info[0])
        dynamodb_local.create_table()

        if len(dynamodb_info) > 1:
            dynamodb_local.put_items(dynamodb_info[1])

        dynamodb_objs.append(dynamodb_local)

    def delete_tables():
        for dynamodb_obj in dynamodb_objs:
            dynamodb_obj.dynamodb_table.delete()

    request.addfinalizer(delete_tables)

    return dynamodb_local.dynamodb
