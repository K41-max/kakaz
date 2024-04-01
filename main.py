from flask import Flask, request, redirect, Response, render_template
import urllib.parse
import base64
import requests

app = Flask(__name__)

max_api_wait_time = 3
max_time = 10
url = requests.get('https://raw.githubusercontent.com/mochidukiyukimi/yuki-youtube-instance/main/instance.txt').text.rstrip()
version = "1.0"

def get_info(request):
    global version
    return json.dumps([version,os.environ.get('RENDER_EXTERNAL_URL'),str(request.headers),str(request.url)])

@app.get("/", response_class=HTMLResponse)
def home():
    return redirect("/bbs")

@app.get("/bbs", response_class=HTMLResponse)
def view_bbs():
    return render_template("bbs.html")

@app.get("/bbs/info", response_class=HTMLResponse)
def view_bbs_info():
    return requests.get(f"{url}bbs/info").text

@app.get("/bbs/api", response_class=HTMLResponse)
def view_bbs_api():
    t = requests.get(f"{url}bbs/api?t={urllib.parse.quote(str(int(time.time()*1000)))}&verify=false&channel=main", cookies={"yuki":"True"}, allow_redirects=False)
    if t.status_code != 307:
        return Response(t.text)
    return redirect("/bbs")

@app.get("/bbs/result")
def write_bbs():
    name = request.args.get("name", "")
    message = request.args.get("message", "")
    seed = request.args.get("seed", "")
    channel = request.args.get("channel", "main")
    verify = request.args.get("verify", "false")

    message = base64.b64decode(message).decode('utf-8')
    print(f"name:{name}, seed:{seed}, channel:{channel}, message:{message}")

    t = requests.get(f"{url}bbs/result?name={urllib.parse.quote(name)}&message={urllib.parse.quote(message)}&seed={urllib.parse.quote(seed)}&channel={urllib.parse.quote(channel)}&verify={urllib.parse.quote(verify)}&info={urllib.parse.quote(get_info(request))}", cookies={"yuki":"True"}, allow_redirects=False)
    if t.status_code != 307:
        return HTMLResponse(t.text)
    return redirect(f"/bbs?name={urllib.parse.quote(name)}&seed={urllib.parse.quote(seed)}&channel={urllib.parse.quote(channel)}&verify={urllib.parse.quote(verify)}")

@app.get("/bbs/how", response_class=PlainTextResponse)
def view_commonds():
    return requests.get(f"{url}bbs/how").text

@app.get("/load_instance")
def load_instance():
    global url
    url = requests.get('https://raw.githubusercontent.com/mochidukiyukimi/yuki-youtube-instance/main/instance.txt').text.rstrip()

@app.get("/bbs/howtouse", response_class=HTMLResponse)
def view_bbs_how_to_use():
    return render_template("bbshow.html")

if __name__ == "__main__":
    app.run()
