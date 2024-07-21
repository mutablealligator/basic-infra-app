import os
from redis import Redis


def create_redis_connection():
  redis_host = os.environ.get('REDIS_HOST', 'localhost')
  redis_port = int(os.environ.get('REDIS_PORT', 6379))
  return Redis(host=redis_host, port=redis_port)
