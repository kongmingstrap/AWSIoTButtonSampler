from message_notifier import MessageNotifier


def handler(event, context):
    MessageNotifier().publish()
