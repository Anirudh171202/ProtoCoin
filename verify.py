from miner import *

config_file = sys.argv[-1]

port = 0
miner = None

with open(config_file) as f:
    config = json.load(f)
    address = config["address"]
    port = config["port"]
    url = "http://localhost:" + str(port)
    miner = Miner(address, url)

blockchain = miner.read_blockchain()

for block in blockchain[1:]:
    print(block.hash.hexdigest(), '->', block.validate())
