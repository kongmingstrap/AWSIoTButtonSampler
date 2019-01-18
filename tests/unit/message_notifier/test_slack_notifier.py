import pytest

from botocore.vendored import requests

from slack_notifier import SlackNotifier


class TestPublish(object):
    @pytest.mark.parametrize(
        'api_endpoint, message, expected', [
            (
                'https://example.com',
                {
                    'slack_username': '',
                    'slack_text': '',
                    'slack_icon_emoji': ''
                },
                None
            )
        ])
    def test_expected_args(self, api_endpoint, message, expected, monkeypatch):
        monkeypatch.setattr(requests, 'post', lambda *_: None)

        f = SlackNotifier()

        assert f.publish(api_endpoint, message) == expected


class TestMakePayload(object):
    @pytest.mark.parametrize(
        'message, expected', [
            (
                {
                    'slack_username': 'slack_username',
                    'slack_text': 'slack_text',
                    'slack_icon_emoji': 'slack_icon_emoji'
                },
                {
                    'username': 'slack_username',
                    'text': 'slack_text',
                    'icon_emoji': 'slack_icon_emoji'
                }
            )
        ])
    def test_expected_args(self, message, expected, monkeypatch):
        f = SlackNotifier()
        actual = f.make_payload(message)

        assert actual == expected
