from flask import Flask, render_template, request, redirect, url_for, session
from news_fetcher import get_all_news, start_background_fetch

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key_here'  # ✅ Needed for session handling

start_background_fetch()  # Background news fetch

@app.route('/')
def homepage():
    all_news = get_all_news()
    return render_template("index.html", news_data=all_news, username=session.get('username'))
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # You can replace this with database logic
    if username == 'admin' and password == '1234':
        return redirect(url_for('homepage'))
    else:
        return "Invalid credentials. <a href='/'>Try again</a>"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('homepage'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


