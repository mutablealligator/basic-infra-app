# 🚀 TinyURL Maker: Your Friendly Neighborhood URL Shortener

Welcome to TinyURL Maker, where long URLs come to slim down! This project is a Flask-based web service that turns those pesky, lengthy URLs into bite-sized, shareable links. It's like a tailor for your URLs, but instead of fabric, we use Python magic! ✨

## 🌟 Features

- **URL Shortening**: Transform any long URL into a compact, TinyURL-style link.
- **Redis-Powered**: Lightning-fast storage and retrieval of your shortened URLs.
- **Docker-Ready**: Containerized for easy deployment and scaling.
- **RESTful API**: Simple and intuitive API for creating and retrieving shortened URLs.
- **Visit Counter**: Keep track of how many times the homepage is visited. Popularity contest, anyone?

## 🛠️ Technology Stack

- **Python 3.8**: Because we like our Python like we like our coffee - hot and energizing!
- **Flask**: A micro web framework that's small but mighty.
- **Redis**: Our speedy, in-memory data store. It's like a squirrel, but for your URLs.
- **Docker**: For containerizing our application. It's like a suitcase for your code!
- **pyshorteners**: The magic wand that transforms long URLs into short ones.

## 🚀 Quick Start

1. Clone this repository:
   ```
   git clone https://github.com/your-username/tinyurl-maker.git
   cd tinyurl-maker
   ```

2. Build and run with Docker Compose:
   ```
   docker-compose up --build
   ```

3. Your URL shortener is now running at `http://localhost:5253`!

## 🎯 API Endpoints

- `GET /`: Homepage. Shows visit count.
- `POST /create`: Create a shortened URL.
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"longUrl":"https://www.example.com"}' http://localhost:5253/create
  ```
- `GET /go/<short_code>`: Retrieve the original URL.
  ```bash
  curl http://localhost:5253/go/abc123
  ```
- `GET /username`: Get the current username.
- `PUT /username`: Update the username.
- `POST /username`: Set a new username.

## 💻 Code Highlights

Here's a sneak peek at some of the cool patterns and practices in this project:

1. **Environment Variables**: We use environment variables for configuration, making our app flexible and secure.

2. **Redis Integration**: Check out how we use Redis for both caching and as a lightweight database.

3. **Error Handling**: We've implemented comprehensive error handling to make our API robust and user-friendly.

4. **RESTful Design**: Our API follows RESTful principles, making it intuitive and easy to use.

5. **Docker Integration**: The project is fully dockerized, showcasing modern deployment practices.

## 🧪 Testing

To run tests (assuming you've written some, you diligent developer, you!):

```bash
python -m pytest tests/
```

## 🤝 Contributing

Contributions are welcome! Feel free to submit a Pull Request.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

If you want to contact me, you can reach me at `alligatorenterprisesinc.1992@gmail.com`.

## 🙏 Acknowledgements

- Thanks to the Flask team for their amazing framework.
- Shoutout to the Redis folks for making our data storage blazing fast.
- Hat tip to the Docker team for making deployment a breeze.

Remember, URL shorteners are like Neville Longbottom: they might seem small, but they're surprisingly powerful! 😉
