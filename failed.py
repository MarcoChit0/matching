from collections import deque
from copy import deepcopy
import random

import numpy as np

UNMATCHED = False
MATCHED = True
num_matches = 0
weight_sum = 0

def match(w):
    global num_matches, weight_sum
    num_matches += 1
    weight_sum += w

def unmatch(w):
    global num_matches, weight_sum
    num_matches -= 1
    weight_sum -= w

class Vertex:
    def __init__(self, id, label = 0) -> None:
        self.id = id
        self.label = label
        self.matched = UNMATCHED

    def is_matched(self):
        return self.matched

    def match(self):
        self.matched = MATCHED

    def unmatch(self):
        self.matched = UNMATCHED

    def __str__(self) -> str:
        return '''id={}; label={};'''.format(self.id, self.label)
    
    def set_label(self, l):
        self.label = l

class Edge:
    def __init__(self, id, src: Vertex, dst:Vertex, weight=0):
        self.id = id
        self.src = src
        self.dst = dst
        self.type = type
        self.weight = weight
        self.matched = UNMATCHED
    
    def can_match(self):
        if  self.is_equality_edge() and (not self.is_matched()) and (not self.src.is_matched() and not self.dst.is_matched()):
            return True
        else:
            return False

    def is_equality_edge(self):
        # label(src) + label(dst) must be equal weight(src, dst) to be an equality graph
        if self.src.label + self.dst.label == self.weight:
            return True
        else:
            return False

    def change_match(self):
        if self.is_matched():
            self.unmatch()
        else:
            self.match()

    def is_matched(self):
        return self.matched
    
    def match(self):
        match(self.weight)
        self.matched = MATCHED
        self.src.match()
        self.dst.match()

    def unmatch(self):
        unmatch(self.weight)
        self.matched = UNMATCHED
        self.src.unmatch()
        self.dst.unmatch()

    def __str__(self) -> str:
        return '''id={}; src=[{}]; dst=[{}]; w={};'''.format(self.id, self.src,self.dst,self.weight)
    
class Graph:
    def __init__(self) -> None:
        self.vertex = []
        self.vset1 = []
        self.vset2 = []
        self.edges = []
        self.match = []
        self.value = 0
        self.num_vertex = 0

    def is_perfect(self):
        if num_matches == self.num_vertex/2:
            return True
        else:
            return False

    def from_cmd(self, operation='min'):
        n = int(input())
        self.num_vertex = 2*n
        self.vertex = [Vertex(i) for i in range(self.num_vertex)]
        self.vset1 = [v for v in self.vertex if v.id < n]
        self.vset2 = [v for v in self.vertex if v.id >= n]
        self.edges = [[] for i in range(self.num_vertex)]
        self.free_vset1 = []
        self.free_vset2 = []
        for r in range(n):
            line = input()
            splitline = line.split(' ')
            c = 0
            for w in splitline:
                if not w == '':
                    if operation == 'min':
                        e = Edge(
                            (r, c+n), 
                            self.vertex[r], 
                            self.vertex[c+n],
                            -int(w))
                    else:
                        e = Edge(
                            (r, c+n), 
                            self.vertex[r], 
                            self.vertex[c+n],
                            int(w))
                    self.edges[r].append(e)
                    self.edges[c+n].append(e) 
                    c += 1

        self.value = int(input())

    def equality_neighbors(self, vertex:Vertex):
        neighbors = set()
        for e in self.edges[vertex.id]:
            if e.is_equality_edge():
                if e.src.id == vertex.id:
                    neighbors.add(e.dst)
                else:
                    neighbors.add(e.src)
        return neighbors
    
    def set_of_equality_neighbors(self, s):
        Nl = set()
        for v in s:
            Nl.update(self.equality_neighbors(v))
        return Nl
    
    def print(self):
        print('n={}\nv={}\n'.format(self.num_vertex, self.value))
        print('---- vset1: ----')
        for v in self.vset1:
            print(v)
            for e in self.edges[v.id]:
                print(e)
        print('---- vset2: ----')
        for v in self.vset2:
            print(v)
            for e in self.edges[v.id]:
                print(e)

    def improve_labeling(self, S:set, T:set):
        print('\n\nIMPROVING LABELS\n\n')
        # alpha = min l(x) + l(y) - w(x,y), for x in S, y in Y/T
        alpha = float('inf') 
        for x in S:
            for y in self.vset2:
                if not y in T:
                    xy = self.edges[x.id][y.id - int(self.num_vertex/2)]
                    print(xy)
                    v = x.label + y.label - xy.weight
                    if alpha > v:
                        alpha = v
        print(alpha)
        if alpha > 0:
            print('\nS:')
            for x in S:
                x.set_label(x.label - alpha)
                print(x)
            print('\nT:')
            for y in T:
                y.set_label(y.label + alpha)
                print(y)
            

    def bfs(self, vertex:Vertex):
        discovered = [False for v in range(self.num_vertex)]
        path = deque()
        q = deque()
        q.append(vertex)
        discovered[vertex.id] = True
        while q:
            u = q.popleft()
            path.append(u)
            for v in self.neighbors(u):
                if not discovered[v.id]:
                    discovered[v.id] = True
                    q.append(v)
        return path

    def matched_edges(self):
        for v in self.vset1:
            for e in self.edges[v.id]:
                if e.is_matched():
                    print(e)

    def hungarian_algorithm(self):
        S = set()
        T = set()
        path = []
        go_directly_to_improve_labeling = False
        # set initial labels
        for x in self.vset1:
            x.set_label(max([e.weight for e in self.edges[x.id]]))
        for y in self.vset2:
            y.set_label(0)
        # create first match
        for x in self.vset1:
            for edge in self.edges[x.id]:
                if edge.can_match():
                    edge.match()
                    self.match.append(edge)
        g.matched_edges()
        go_directly_to_improve_labeling = False
        while not self.is_perfect():
            print('ENTREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEI')
            if not go_directly_to_improve_labeling:
                # randomly select a vertex to be on S set
                for x in self.vset1:
                    if not x.is_matched():
                        self.free_vset1.append(x)
                x = np.random.choice(self.free_vset1, size=1)[0]
                print()
                print('x:')
                print(x)
                S.add(x)
                path.append(x)
                Nl = self.set_of_equality_neighbors(S)
                print('\n\nNl:')
                for n in Nl:
                    print(n)
            # reset Flag
            go_directly_to_improve_labeling = False
            if  Nl == T:
                self.improve_labeling(S, T)
                Nl = self.set_of_equality_neighbors(S)
            y = random.choice(tuple(Nl.difference(T)))
            print()
            print('y:')
            print(y)
            if not y.is_matched():
                self.edges[x.id][y.id-int(self.num_vertex/2)].match()
                self.match.append(self.edges[x.id][y.id-int(self.num_vertex/2)])
            else:
                z = None
                for e in self.edges[y.id]:
                    if e.is_matched:
                        if e.src.id == y.id:
                            z = e.dst
                        else:
                            z = e.src
                        break
                path.append(y)
                T.add(y)
                path.append(z)
                S.add(z)
                print('\nS:')
                for s in S:
                    print(s)
                print('\nT:')
                for t in T:
                    print(t)
                go_directly_to_improve_labeling = True

g = Graph()
g.from_cmd('min')
g.hungarian_algorithm()
print('\n\n\n#########')
g.matched_edges()