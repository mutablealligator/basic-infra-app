import pyshorteners
from app import redis_connection

from . import app
from flask import request, jsonify
from logging import getLogger
from urllib.parse import urlparse
from util import url_validator


logger = getLogger(__name__)
app.redis = redis_connection.create_redis_connection()

@app.route('/')
def index():
    app.redis.incr('homepage-hits')
    hits = app.redis.get('homepage-hits')
    return f'This page has been visited {hits.decode("utf-8")} times'


@app.route('/username', methods=['GET'])
def get():
    username = app.redis.get('username')
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
    app.redis.set('username', username)
    return jsonify({"message": f"Successfully inserted username: {username}"}), 200


@app.route('/username', methods=['POST'])
def post():
    data = request.get_json()
    if not data or 'username' not in data:
        return jsonify({"error": "No username provided"}), 400

    logger.debug(data)
    app.redis.set('username', data['username'])
    return jsonify({"message": f"Successfully inserted username: {data['username']}"}), 200


@app.route('/create', methods=['POST'])
def create():
    request_data = request.get_json()
    if 'longUrl' in request_data:
        long_url = request_data['longUrl']

        # Validate URL
        if not url_validator.is_valid_url(long_url):
            return jsonify({"error": "Invalid URL"}), 400

        # Validate if it already exists
        if app.redis.exists(long_url):
            return jsonify({"error": f"Shortened URL for long_url: {long_url} already exists. Short URL: {app.redis.get(long_url)}"}), 400

        # Shorten the URL and persist the state
        short_url = pyshorteners.Shortener().tinyurl.short(long_url)
        short_code = urlparse(short_url).path.lstrip('/')
        app.redis.set(long_url, short_url)
        app.redis.set(short_code, long_url)

        # Return the response
        return jsonify({"message": f"Successfully inserted long_url: {long_url} with short_url: {short_url}, short_code: {short_code}"}), 200
    else:
        return jsonify({"error": "No longUrl provided"}), 400

@app.route('/go/<short_code>', methods=['GET'])
def go(short_code):
    if not short_code or not app.redis.exists(short_code):
        return jsonify({"error": f"No such short code found in the system: {short_code}"}), 404
    if not url_validator.is_valid_short_code(short_code):
        return jsonify({"error": f"Invalid short code found in the system: {short_code}"}), 404

    long_url = app.redis.get(short_code)
    long_url = long_url.decode("utf-8")
    if not url_validator.is_valid_url(long_url):
        return jsonify({"error": f"Invalid long_url: {long_url} found for short_code: {short_code}"}), 400

    if long_url:
        return jsonify({"message": f"Successfully retrieved long_url: {long_url}"}), 200
    else:
        return jsonify({"error": f"No longUrl found for short_code: ${short_code}"}), 404
