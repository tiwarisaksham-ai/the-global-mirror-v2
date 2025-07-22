from flask import Flask, render_template
from news_fetcher import get_all_news, start_background_fetch

app = Flask(__name__, static_url_path='/static')  # ✅ Ensure static path is set

start_background_fetch()  # Start fetching in background

@app.route('/')
def homepage():
    all_news = get_all_news()
    return render_template("index.html", news_data=all_news)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # ✅ Required for Render (don't use debug=True)

