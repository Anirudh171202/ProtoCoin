import random
from hashlib import sha256

class Graph:
    def __init__(self, size):
        self.size = size
        self.adj_mat = [[False for _ in range(0, size)] for _ in range(0, size)]

    def from_hash(hash):
        graph = Graph(N)

        i = 0

        while i < 512:
            bytes = iter(hash.digest)
            for byte in bytes:
                graph.connect(byte, next(bytes))
                i += 1

            hash = sha256(hash.digest())

        return graph

    def connect(self, u: int, v: int):
        self.adj_mat[u][v] = True

    def is_connected(self, u: int, v: int) -> bool:
        if u == None:
            return True
        return self.adj_mat[u][v]

NOT_IN_STACK = -1

def dfs(u: int, graph: Graph, label: list[int], instack_count: int) -> bool:
    if instack_count == graph.size:
        return True

    for v in range(0, graph.size):
        if graph.is_connected(u, v) and label[v] == NOT_IN_STACK:
            label[v] = u

            if dfs(v, graph, label, instack_count + 1):
                return True

            label[v] = NOT_IN_STACK

    return False

def find_hamiltonian_path(graph: Graph) -> list[int]:
    path = [NOT_IN_STACK for _ in range(0, graph.size)]
    # is_connected returns True if u is None
    if dfs(None, graph, path, 0):
        return path
    else:
        return None

# TODO implement correct fields for Transaction and fix the hashing function
class Transaction:
    def hash(self, hasher):
        hasher.update(id(self))

class Block:
    def __init__(self, prev_hash: str, transactions: list[Transaction], proof_of_work: int,
            hash, hamiltonian_path: list[int]):
        self.prev_hash = prev_hash
        self.transactions = transactions
        self.proof_of_work = proof_of_work
        self.hash = hash
        self.hamiltonian_path = hamiltonian_path

    def validate(self) -> bool:
        graph = Graph.from_hash(self.hash)
        # is_connected returns True if u is None
        u = None
        for v in self.hamiltonian_path:
            if not graph.is_connected(u, v):
                return False
            u = v
        return True

N = 256


def proof_of_work(prev_hash: str, transactions: list[Transaction]):
    orig_hash = sha256(prev_hash.encode('utf-8'))

    for transaction in transactions:
        orig_hash.update(transaction)

    proof_of_work = random.randint(0, 2**64)

    while True:
        hash = orig_hash.copy()
        hash.update(proof_of_work)

        graph = Graph.from_hash(hash)

        hamiltonian_path = find_hamiltonian_path(graph)

        if hamiltonian_path != None:
            print("Found path", hamiltonian_path)
            return Block(prev_hash, transactions, proof_of_work, hash, hamiltonian_path)

    # TODO occasionally check if new blockchain should be taken as valid
    # TODO incorporate the computation here with the blockchain
