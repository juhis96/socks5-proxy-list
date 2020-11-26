from apscheduler.schedulers.background import BackgroundScheduler
import flask
from flask import request, jsonify
import requests
import pymongo
from flask_cors import CORS
from func import updateProxies

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app, resources={r"/*": {"origins": "*"}})

#update proxies every 2 hours
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(updateProxies,'interval',minutes=120)
scheduler.start()

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["database"]
col = db["proxies"]

@app.route('/api/proxies', methods=['GET'])
def api():
    proxies = []
    for proxy in col.find({}, {"_id":0, "ip": 1, "port": 1 }):  
        proxies.append(proxy)
    return jsonify(proxies)

@app.route('/', methods=['GET'])
def home():
    return 'SOCKS5 Proxy API'

if __name__ == "__main__":
    app.run()
