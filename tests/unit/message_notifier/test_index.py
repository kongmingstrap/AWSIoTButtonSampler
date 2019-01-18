import pytest

import index
from message_notifier import MessageNotifier


class TestHandler(object):
    @pytest.mark.parametrize(
        'event, context, expected', [
            (
                {}, {}, None
            )
        ])
    def test_expected_args(self, event, context, expected, monkeypatch):
        monkeypatch.setattr(MessageNotifier, 'publish', lambda *_: True)

        assert index.handler(event, context) == expected
