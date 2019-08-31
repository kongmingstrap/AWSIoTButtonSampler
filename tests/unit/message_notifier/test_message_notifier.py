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
                {},
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
                {},
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
                {},
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
