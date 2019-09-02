import pytest

from message_notifier import MessageNotifier
from slack_notifier import SlackNotifier


class TestPublish(object):
    @pytest.mark.parametrize(
        'dynamodb, event, expected', [
            (
                (
                    [
                        ['room_table', 'exist device']
                    ]
                ),
                {
                    'deviceInfo': {
                        'deviceId': 'DEVICEIDEXAPMPLE',
                        'type': 'button',
                        'remainingLife': 80.00,
                        'attributes': {
                            'projectRegion': 'ap-northeast-1',
                            'projectName': 'office-notify',
                            'placementName': 'Office11',
                            'deviceTemplateName': 'OfficeNotify'
                        }
                    },
                    'deviceEvent': {
                        'buttonClicked': {
                            'clickType': 'SINGLE',
                            'reportedTime': '2019-09-02T00:00:00.744Z'
                        }
                    },
                    'placementInfo': {
                        'projectName': 'office-notify',
                        'placementName': 'Office11',
                        'attributes': {},
                        'devices': {
                            'OfficeNotify': 'DEVICEIDEXAPMPLE'
                        }
                    }
                },
                {
                    'slack_icon_emoji': ':fukkeikun:',
                    'slack_text': 'taped button 01',
                    'slack_username': 'user 01'
                }
            ),
            (
                (
                    [
                        ['room_table', 'not exist params']
                    ]
                ),
                {
                    'deviceInfo': {
                        'deviceId': 'DEVICEIDEXAPMPLE',
                        'type': 'button',
                        'remainingLife': 80.00,
                        'attributes': {
                            'projectRegion': 'ap-northeast-1',
                            'projectName': 'office-notify',
                            'placementName': 'Office11',
                            'deviceTemplateName': 'OfficeNotify'
                        }
                    },
                    'deviceEvent': {
                        'buttonClicked': {
                            'clickType': 'SINGLE',
                            'reportedTime': '2019-09-02T00:00:00.744Z'
                        }
                    },
                    'placementInfo': {
                        'projectName': 'office-notify',
                        'placementName': 'Office11',
                        'attributes': {},
                        'devices': {
                            'OfficeNotify': 'DEVICEIDEXAPMPLE'
                        }
                    }
                },
                {
                    'slack_icon_emoji': '',
                    'slack_text': '',
                    'slack_username': ''
                }
            ),
            (
                (
                    [
                        ['room_table', 'another device']
                    ]
                ),
                {
                    'deviceInfo': {
                        'deviceId': 'DEVICEIDEXAPMPLE',
                        'type': 'button',
                        'remainingLife': 80.00,
                        'attributes': {
                            'projectRegion': 'ap-northeast-1',
                            'projectName': 'office-notify',
                            'placementName': 'Office11',
                            'deviceTemplateName': 'OfficeNotify'
                        }
                    },
                    'deviceEvent': {
                        'buttonClicked': {
                            'clickType': 'SINGLE',
                            'reportedTime': '2019-09-02T00:00:00.744Z'
                        }
                    },
                    'placementInfo': {
                        'projectName': 'office-notify',
                        'placementName': 'Office11',
                        'attributes': {},
                        'devices': {
                            'OfficeNotify': 'DEVICEIDEXAPMPLE'
                        }
                    }
                },
                {}
            )
        ], indirect=['dynamodb'])
    def test_expected_args(self, dynamodb, event, expected, monkeypatch):
        monkeypatch.setattr(SlackNotifier, 'publish', lambda *_: True)

        f = MessageNotifier()
        f.dynamodb = dynamodb

        actual = f.publish(event)

        assert actual == expected

    @pytest.mark.parametrize(
        'dynamodb, event, expected', [
            (
                (
                    [
                        []
                    ]
                ),
                None,
                Exception
            )
        ])
    def test_exception_args(self, dynamodb, event, expected, monkeypatch):
        monkeypatch.setattr(SlackNotifier, 'publish', lambda *_: Exception)

        f = MessageNotifier()

        with pytest.raises(expected):
            f.publish(event)


class TestGetDeviceIdFromEvent(object):
    @pytest.mark.parametrize(
        'event, expected', [
            (
                {
                    'deviceInfo': {
                        'deviceId': 'DEVICEIDEXAPMPLE',
                        'type': 'button',
                        'remainingLife': 80.00,
                        'attributes': {
                            'projectRegion': 'ap-northeast-1',
                            'projectName': 'office-notify',
                            'placementName': 'Office11',
                            'deviceTemplateName': 'OfficeNotify'
                        }
                    },
                    'deviceEvent': {
                        'buttonClicked': {
                            'clickType': 'SINGLE',
                            'reportedTime': '2019-09-02T00:00:00.744Z'
                        }
                    },
                    'placementInfo': {
                        'projectName': 'office-notify',
                        'placementName': 'Office11',
                        'attributes': {},
                        'devices': {
                            'OfficeNotify': 'DEVICEIDEXAPMPLE'
                        }
                    }
                },
                'DEVICEIDEXAPMPLE'
            )
        ])
    def test_expected_args(self, event, expected):
        f = MessageNotifier()
        actual = f.get_device_id_from_event(event)
        assert actual == expected
