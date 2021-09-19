import random, json, requests, time, base64, ecdsa, sys, os
from hashlib import sha256
from flask import Flask, request
from flask_cors import CORS, cross_origin
from multiprocessing import Process

from hamiltonian import *

class Transaction:
    def __init__(self, sender: str, receiver: str, amount: int):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def hash(self, hasher):
        hasher.update(self.sender.encode('utf-8'))
        hasher.update(self.receiver.encode('utf-8'))
        hasher.update(str(self.amount).encode('utf-8'))

    def to_json(self):
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
        }

    def from_json(json):
        return Transaction(json['sender'], json['receiver'], json['amount'])

class Block:
    def __init__(self, prev_hash: str, transactions: list[Transaction], proof_of_work: int,
            hash, hamiltonian_path: list[int]):
        self.prev_hash = prev_hash
        self.transactions = transactions
        self.proof_of_work = proof_of_work
        self.hash = hash
        self.hamiltonian_path = hamiltonian_path

    def genesis():
        return Block('0', [], 0, sha256(), [])

    def validate(self) -> bool:
        graph = Graph.from_hash(self.hash)
        return graph.verify_path(self.hamiltonian_path)

    def to_json(self):
        return {
            'prev_hash': self.prev_hash,
            'transactions': [transaction.to_json() for transaction in self.transactions],
            'proof_of_work': self.proof_of_work,
            'hamiltonian_path': self.hamiltonian_path,
        }

    def from_json(json):
        prev_hash = json['prev_hash']
        transactions = json['transactions']
        proof_of_work = json['proof_of_work']
        hamiltonian_path = json['hamiltonian_path']

        hash = sha256(prev_hash.encode('utf-8'))

        for i in range(0, len(transactions)):
            transactions[i] = Transaction.from_json(transactions[i])
            if transactions[i].sender != 'network':
                transactions[i].hash(hash)

        hash.update(str(proof_of_work).encode('utf-8'))

        return Block(prev_hash, transactions, proof_of_work, hash, hamiltonian_path)

class Miner:
    def __init__(self, address: str, url: str):
        self.address = address
        self.url = url

    def save_blockchain(self, blockchain: list[Block]):
        with open(self.address + '-blockchain.json', 'w') as f:
            json.dump([block.to_json() for block in blockchain], f)

    def read_blockchain_json(self):
        with open(self.address + '-blockchain.json') as f:
            return json.load(f)

    def read_blockchain(self) -> list[Block]:
        return [Block.from_json(block) for block in self.read_blockchain_json()]

    def save_transactions(self, transactions: list[Transaction]):
        with open(self.address + '-transactions.json', 'w') as f:
            json.dump([transaction.to_json() for transaction in transactions], f)

    def read_transactions(self) -> list[Transaction]:
        with open(self.address + '-transactions.json') as f:
            return [Transaction.from_json(transaction) for transaction in json.load(f)]

    def save_peers(self, peers: list[str]):
        with open(self.address + '-peers.json', 'w') as f:
            json.dump(peers, f)

    def read_peers(self) -> list[str]:
        with open(self.address + '-peers.json') as f:
            return json.load(f)

    def to_json(self):
        return { 'address': self.address, 'url': self.url }

    def find_new_chains(self):
        # Get the blockchains of every other node
        other_chains = []

        peers = self.read_peers()

        for node_url in peers:
            # Get their chains using a GET request
            block = requests.get(
                url = node_url + '/blocks',
                params = self.to_json(),
            ).content
            # Convert the JSON object to a Python dictionary
            block = Block.from_json(json.loads(block))
            # Verify other node block is correct
            if block.validate():
                other_chains.append(block)

        return other_chains

def proof_of_work(miner: Miner, blockchain: list[Block]) -> (bool, list[Block]):
    prev_hash = blockchain[-1].hash.hexdigest()
    orig_hash = sha256(prev_hash.encode('utf-8'))

    # FIXME: Race condition here, server process can update the transaction in
    # between transactions being read and cleared
    transactions = miner.read_transactions()
    miner.save_transactions([])

    for transaction in transactions:
        transaction.hash(orig_hash)

    proof_of_work = random.randint(0, 2**N)

    # print('Orig: ', orig_hash.hexdigest())

    while True:
        hash = orig_hash.copy()
        hash.update(str(proof_of_work).encode('utf-8'))


        graph = Graph.from_hash(hash)

        # print('Checking new graph', graph.adj_mat)

        hamiltonian_path = find_hamiltonian_path(graph)

        new_longest = consensus(miner, blockchain)
        if new_longest != None:
            return (False, blockchain)

        if hamiltonian_path != None:
            # print('--- Graph ---')
            # for i in range(0, N):
            #     print(i, '->', end = '')
            #     for j in range(0, N):
            #         if i != j and graph.is_connected(i, j):
            #             print(j, end = ' ')
            #     print()
            # print('-------------')

            print(f'Found path ({hash.hexdigest()}): {hamiltonian_path}')

            blockchain.append(Block(prev_hash, transactions, proof_of_work, hash, hamiltonian_path))
            return (True, blockchain)
        # else:
        #     print('No path found')

        proof_of_work += 1

def consensus(miner: Miner, blockchain: list[Block]):
    # Get the blocks from other nodes
    other_chains = miner.find_new_chains()

    longest_chain = blockchain
    updated_longest = False

    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain
            updated_longest = True

    # If the longest chain wasn't ours, then we set our chain to the longest
    if updated_longest:
        return longest_chain

def mine(miner: Miner):
    blockchain = miner.read_blockchain()

    peers = json.loads(requests.post(
        'http://localhost:5000/register',
        json = miner.to_json(),
        headers = {'Content-Type': 'application/json'}
    ).content)
    miner.save_peers(peers)

    print('Registered self. Peers: ', peers)

    a = True

    while True:
        proof = proof_of_work(miner, blockchain)

        blockchain = proof[1]

        if proof[0]:
            blockchain[-1].transactions.append(Transaction('network', miner.address, 1))

        miner.save_blockchain(blockchain)

        a = False

node = Flask(__name__)
CORS(node)

MINER = Miner('', '')

@node.route('/blocks', methods=['GET'])
def get_blocks():
    print(MINER)
    peers = MINER.read_peers()

    # Load current blockchain. Only you should update your blockchain
    if "address" in request.args:
        url = request.args["url"]

        if url not in peers:
            peers[url] = url
            print(f"Adding new peer node at {url}")

    return json.dumps(MINER.read_blockchain_json())


@node.route('/txion', methods=['POST'])
def transaction():
    # On each new POST request, we extract the transaction data
    new_txion = request.get_json()
    pending = MINER.read_transactions()

    # Then we add the transaction to our list
    if validate_signature(new_txion['sender'], new_txion['signature'], new_txion['message']):
        transaction = Transaction.from_json(new_txion)
        pending.append(transaction)
        # Because the transaction was successfully
        # submitted, we log it to our console
        print("New transaction")
        print("FROM: {0}".format(transaction.sender))
        print("TO: {0}".format(transaction.receiver))
        print("AMOUNT: {0}\n".format(transaction.amount))
        MINER.save_transactions(pending)
        # Then we let the client know it worked out
        return "Transaction submission successful\n"
    else:
        return "Transaction submission failed. Wrong signature\n"

def validate_signature(public_key, signature, message):
    """Verifies if the signature is correct. This is used to prove
    it's you (and not someone else) trying to do a transaction with your
    address. Called when a user tries to submit a new transaction.
    """
    return True
    # public_key = (base64.b64decode(public_key)).hex()
    # signature = base64.b64decode(signature)
    # vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key), curve=ecdsa.SECP256k1)

    # # Try changing into an if/else statement as except is too broad.
    # try:
    #     return vk.verify(signature, message.encode())
    # except:
    #     return False

if __name__ == '__main__':
    config_file = sys.argv[-1]

    port = 0

    with open(config_file) as f:
        config = json.load(f)
        address = config["address"]
        port = config["port"]
        url = "http://localhost:" + str(port)
        MINER = Miner(address, url)

    if not os.path.exists(MINER.address + '-blockchain.json'):
        MINER.save_blockchain([Block.genesis()])
    MINER.save_peers([])
    MINER.save_transactions([])

    p1 = Process(target=mine, args=(MINER,))
    p1.start()

    # Start server to receive transactions
    p2 = Process(target=node.run(port = port))
    p2.start()
