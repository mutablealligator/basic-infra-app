from flask import Flask
import os
from redis import Redis

app = Flask(__name__)
app.config['DEBUG'] = True


from . import routes

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5253)