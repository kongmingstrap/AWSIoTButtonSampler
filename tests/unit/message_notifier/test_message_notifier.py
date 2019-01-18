import pytest

from message_notifier import MessageNotifier
from slack_notifier import SlackNotifier


class TestPublish(object):
    @pytest.mark.parametrize(
        'dynamodb, expected', [
            (
                (
                    [
                        ['room_table', 'state unlocked']
                    ]
                ),
                {
                    'slack_icon_emoji': ':fukkeikun:',
                    'slack_text': 'place 01 locked.',
                    'slack_username': 'place 01'
                }
            ),
            (
                (
                    [
                        ['room_table', 'state locked']
                    ]
                ),
                {
                    'slack_icon_emoji': ':fukkeikun:',
                    'slack_text': 'place 01 unlocked.',
                    'slack_username': 'place 01'
                }
            ),
            (
                (
                    [
                        ['room_table', 'another device']
                    ]
                ),
                {}
            )
        ], indirect=['dynamodb']
    )
    def test_expected_args(self, dynamodb, expected, monkeypatch):
        monkeypatch.setattr(SlackNotifier, 'publish', lambda *_: True)

        f = MessageNotifier()
        f.dynamodb = dynamodb

        actual = f.publish()

        assert actual == expected
