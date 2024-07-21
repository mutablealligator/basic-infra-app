import pyshorteners

from . import app, redis
from flask import request, jsonify
from logging import getLogger
from urllib.parse import urlparse


logger = getLogger(__name__)


@app.route('/')
def index():
    redis.incr('homepage-hits')
    hits = redis.get('homepage-hits')
    return f'This page has been visited {hits.decode("utf-8")} times'


@app.route('/username', methods=['GET'])
def get():
    username = redis.get('username')
    if username:
        return f'Username: {username.decode("utf-8")}'
    else:
        return 'No username set', 404


@app.route('/username', methods=['PUT'])
def put():
    data = request.get_json()
    if not data or 'username' not in data:
        return jsonify({"error": "No username provided"}), 400

    logger.debug(data)
    username = data['username']
    redis.set('username', username)
    return jsonify({"message": f"Successfully inserted username: {username}"}), 200


@app.route('/username', methods=['POST'])
def post():
    data = request.get_json()
    if not data or 'username' not in data:
        return jsonify({"error": "No username provided"}), 400

    logger.debug(data)
    redis.set('username', data['username'])
    return jsonify({"message": f"Successfully inserted username: {data['username']}"}), 200


@app.route('/create', methods=['POST'])
def create():
    request_data = request.get_json()
    if 'longUrl' in request_data:
        long_url = request_data['longUrl']
        short_url = pyshorteners.Shortener().tinyurl.short(long_url)
        short_code = urlparse(short_url).path.lstrip('/')
        redis.set(long_url, short_url)
        redis.set(short_code, long_url)

        return jsonify({"message": f"Successfully inserted long_url: {long_url} with short_url: {short_url}, short_code: {short_code}"}), 200
    else:
        return jsonify({"error": "No longUrl provided"}), 400

@app.route('/go/<short_code>', methods=['GET'])
def go(short_code):
    long_url = redis.get(short_code)
    long_url = long_url.decode("utf-8")
    if long_url:
        return jsonify({"message": f"Successfully retrieved long_url: {long_url}"}), 200
    else:
        return jsonify({"error": f"No longUrl found for short_code: ${short_code}"}), 404
