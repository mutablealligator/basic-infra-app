from flask import Flask
import os
from redis import Redis

app = Flask(__name__)
app.config['DEBUG'] = True
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = int(os.environ.get('REDIS_PORT', 6379))
redis = Redis(host=redis_host, port=redis_port)

from . import routes

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5253)