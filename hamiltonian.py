import random, json, requests
from hashlib import sha256

N = 16

class Graph:
    def __init__(self, size):
        self.size = size
        self.adj_mat = [[False for _ in range(0, size)] for _ in range(0, size)]

    def from_hash(hash):
        graph = Graph(N)

        for byte in hash.digest():
            u = byte >> 4
            v = byte & 0xf
            # u = (byte & 0b111000) >> 3
            # v = byte & 0b000111
            # print(bin(byte), u, v)
            # Use four bit sized numbers to represent nodes
            graph.connect(u, v)

        return graph

    def verify_path(self, path: list[int]) -> bool:
        # is_connected returns True if u is None
        u = None
        for v in path:
            if not self.is_connected(u, v):
                return False
            u = v
        return True

    def print(self):
        for i in range(0, N):
            print(i, '->', end = ' ')
            for j in range(0, N):
                if i != j and self.is_connected(i, j):
                    print(j, end = ' ')
            print()


    def connect(self, u: int, v: int):
        self.adj_mat[u][v] = True

    def is_connected(self, u: int, v: int) -> bool:
        if u == None:
            return True
        return self.adj_mat[u][v]

NOT_IN_STACK = -1

def dfs(u: int, graph: Graph, label: list[int], instack_count: int) -> int:
    if instack_count == graph.size:
        return u

    for v in range(0, graph.size):
        if graph.is_connected(u, v) and label[v] == NOT_IN_STACK:
            label[v] = u

            res = dfs(v, graph, label, instack_count + 1)
            if res >= 0:
                return res

            label[v] = NOT_IN_STACK

    return -1

def find_hamiltonian_path(graph: Graph) -> list[int]:
    path = [NOT_IN_STACK for _ in range(0, graph.size)]
    end = dfs(None, graph, path, 0)
    # is_connected returns True if u is None

    # print('PARENT PATH:', path)

    if end < 0:
        return None

    sequence = [None for _ in range(0, graph.size)]

    for i in range(graph.size - 1, -1, -1):
        sequence[i] = end
        end = path[end]

    return sequence
