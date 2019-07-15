from config import config
from services.redis_client import RedisClient

redis_cli = RedisClient(config)

abnormal_count_map = {}  # cameraId: count
