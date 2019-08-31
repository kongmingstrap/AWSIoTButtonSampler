from logger.logger import Logger
from message_notifier import MessageNotifier

logger = Logger().getLogger(__name__)


def handler(event, context):
    try:
        logger.info(f'event: {event}')
        MessageNotifier().publish(event)
    except Exception as e:
        logger.error(f'Exception occurred: {e}', exc_info=True)
