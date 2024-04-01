import json
import requests
import urllib.parse
import time
import datetime
import random
import os
import base64
from flask import Flask, request, Response, redirect, render_template, make_response

max_api_wait_time = 3
max_time = 10
url = requests.get('https://raw.githubusercontent.com/mochidukiyukimi/yuki-youtube-instance/main/instance.txt').text.rstrip()
version = "1.0"

app = Flask(__name__)

def get_info(request):
    global version
    return json.dumps([version, os.environ.get('RENDER_EXTERNAL_URL'), str(request.headers), str(request.url)])

@app.route("/")
def home():
    return redirect("/bbs")

@app.route("/bbs")
def view_bbs():
    return render_template("bbs.html")

@app.route("/bbs/info")
def view_bbs_info():
    res = requests.get(f"{url}bbs/info")
    return Response(res.text, content_type='text/html')

@app.route("/bbs/api")
def view_bbs_api():
    t = requests.get(f"{url}bbs/api?t={urllib.parse.quote(str(int(time.time()*1000)))}&verify={urllib.parse.quote('false')}&channel={urllib.parse.quote('main')}")
    return Response(t.text, content_type='text/html')

@app.route("/bbs/result")
def write_bbs():
    name = request.args.get('name', '')
    message = base64.b64decode(request.args.get('message', '')).decode('utf-8')
    seed = request.args.get('seed', '')
    channel = request.args.get('channel', 'main')
    verify = request.args.get('verify', 'false')
    info = get_info(request)
    t = requests.get(f"{url}bbs/result?name={urllib.parse.quote(name)}&message={urllib.parse.quote(message)}&seed={urllib.parse.quote(seed)}&channel={urllib.parse.quote(channel)}&verify={urllib.parse.quote(verify)}&info={urllib.parse.quote(info)}", cookies={"yuki": "True"}, allow_redirects=False)
    if t.status_code != 307:
        return Response(t.text, content_type='text/html')
    return redirect(f"/bbs?name={urllib.parse.quote(name)}&seed={urllib.parse.quote(seed)}&channel={urllib.parse.quote(channel)}&verify={urllib.parse.quote(verify)}")

@app.route("/bbs/how")
def view_commands():
    res = requests.get(f"{url}bbs/how")
    return Response(res.text, content_type='text/plain')

@app.route("/load_instance")
def load_instance():
    global url
    url = requests.get('https://raw.githubusercontent.com/mochidukiyukimi/yuki-youtube-instance/main/instance.txt').text.rstrip()
    return "Instance loaded successfully."

@app.route("/bbs/howtouse")
def view_bbs_how_to_use():
    return render_template("bbshow.html")

if __name__ == "__main__":
    app.run(debug=True)
