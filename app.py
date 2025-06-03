from flask import Flask, render_template, request, redirect, flash
import json

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
        return redirect("/success")
    return render_template('index.html')

@app.route("/success")
def success():
    return "Configuration completed. Please run tweet_scheduler.py separately now."

if __name__=="__main__":
    app.run(debug=True)