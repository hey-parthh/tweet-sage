from flask import Flask, render_template, request, redirect, jsonify
import json
import threading
from twitter_bot import run_scheduler
import os


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        config = {
            "api_key" : request.form["api_key"],
            "api_secret" : request.form["api_secret"],
            "access_token" : request.form["access_token"],
            "access_token_secret" : request.form["access_token_secret"],
            "file_path" : request.form["file_path"],
            "time_interval" : int(request.form["time_interval"]),
        }

        with open("config.json","w") as f:
            json.dump(config, f, indent = 4)

        thread = threading.Thread(target=run_scheduler, daemon=True)
        thread.start()
        return redirect("/dashboard")
    return render_template('index.html')

@app.route("/dashboard")
def success():
    return render_template('dashboard.html')

@app.route('/tweets')
def tweets():
    if not os.path.exists('posted_tweets.log'):
        return jsonify({"tweets": []})

    with open('posted_tweets.log', 'r', encoding='utf-8') as f:
        content = f.read()

    tweets_list = [t.strip() for t in content.split('---') if t.strip()]
    # Return last 5 tweets (most recent)
    last_tweets = tweets_list[-5:]
    return jsonify({"tweets": last_tweets})

if __name__=="__main__":
    app.run(debug=True)