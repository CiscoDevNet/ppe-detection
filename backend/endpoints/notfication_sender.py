from common import logger
from config import config
from services.spark import Spark


def send_process(queue):
    spark_cli = Spark(config)
    while True:
        msg, files = queue.get(True)
        logger.info("getting msg and send in async mode")
        spark_cli.send_msg(msg, files)
