import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
def init(update, context):
    logger.warning('[LOG] errore: {}'.format(context.error))