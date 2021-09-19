from flask import Flask, request
from flask_cors import CORS, cross_origin
import json

miners = {}

app = Flask(__name__)
CORS(app)

def miner_list():
    return json.dumps(list(miners.values()))

@app.route("/register", methods=['POST'])
def register():
    miner = request.get_json()
    print("Got new miner", json.dumps(miner, sort_keys = True, indent = 2))
    res = miner_list()
    miners[miner["address"]] = miner["url"]
    return res

@app.route("/unregister", methods=['POST'])
def unregister():
    miner = request.get_json()
    print("Unregister miner", json.dumps(miner, sort_keys = True, indent = 2))
    miners.pop(miner["address"])

@app.route("/miners", methods=['GET'])
def get_miners():
    return miner_list()

if __name__ == "__main__":
    app.run(port = 5000)
