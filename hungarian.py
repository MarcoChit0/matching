import heapq


class Vertex:
    def __init__(self, id, p=0) -> None:
        self.id = id
        self.potential = p
        self.matched = False
    
    def is_free(self):
        if not self.matched:
            return True
        else:
            return False
    
    def __str__(self) -> str:
        return 'id:{}, p:{}, m:{}'.format(self.id, self.potential, self.matched)
    
    def set_potential(self, p):
        self.potential = p

    def update_potential(self, augmenting_path_value):
        self.potential = self.potential + augmenting_path_value

    
    def free(self):
        self.matched = False

    def match(self):
        self.matched = True

class Edge:
    def __init__(self, id, s, t, weight, matched=False) -> None:
        self.id = id
        self.s = s
        self.t = t
        self.weight = weight
        self.matched = matched
    
    def __str__(self) -> str:
        return 'Edge: {}, s: [{}], t: [{}], w: {}, m: {}'.format(        
            self.id,
            self.s,
            self.t,
            self.weight,
            self.matched)
    
    def free(self):
        self.matched = False

    def match(self):
        self.matched = True

class Arc(Edge):
    def __init__(self, id, s, t, weight, matched=False) -> None:
        super().__init__(id, s, t, weight, matched)
        if self.matched:
            # if e = {s,t} is matched, create arc ts, whose distance = weight{s,t}
            self.id = (self.id[1], self.id[0])
            self.src = t
            self.dst = s
            self.distance = self.weight
        else:
             # if e = {s,t} is free, create arc st, whose distance = - weight{s,t}
            self.src = s
            self.dst = t
            self.distance = - self.weight
    
    def __str__(self) -> str:
        return "Arc: {}, src: [{}], dst: [{}], w: {}, m: {}, d: {}, d': {}".format(        
            self.id,
            self.src,
            self.dst,
            self.weight,
            self.matched,
            self.distance,
            self.get_distance())

    def get_distance(self):
        # dist'(u, v) = dist(u, v) - (p(v) - p(u))
        # print('{} - ({} - {})'.format(self.distance,self.dst.potential,self.src.potential))
        return self.distance - (self.dst.potential - self.src.potential)

class Graph:
    def __init__(self, V, S, T, E, expectedvalue):
        self.V = V
        self.S = S
        self.T = T
        self.E = E
        assert len(S) + len(T) == len(V)
        self.num_vertex = len(V)
        self.expectedvalue = expectedvalue
    
    def print(self):
        print('\nS:')
        for s in self.S:
            print(s)
        print('\nT:')
        for t in self.T:
            print(t)
        print('\nE:')
        for v in self.V:
            print('\nv: {}'.format(v.id))
            for e in self.E[v.id]:
                print(e)

def hungarian(g: Graph, operation:str='min'):
    num_matches = 0
    M = [None for v in range(g.num_vertex)]
    maxwe = float('-inf')
    for edges in g.E:
        for edge in edges:
            if edge.weight > maxwe:
                maxwe = edge.weight
    # p(s) = max we for e in E, for s in S
    for s in g.S:
        s.set_potential(0)
    # p(t) = 0, for t in T
    for t in g.T:
        t.set_potential(-maxwe)
    cont = 1
    while num_matches < g.num_vertex:
        # print('##############################')
        # print(cont)
        # print('##############################')
        cont += 1
        A = [[] for v in g.V]
        for ind in range(int(g.num_vertex/2)):
            for edge in g.E[ind]:
                a = Arc(edge.id, edge.s, edge.t, edge.weight, edge.matched)
                if edge.matched:
                    # ts arc, whose dist = weight
                    A[edge.t.id].append(a)
                else:
                    # st arc, whose dist = - weight
                    A[edge.s.id].append(a)
        # print('\nHungarian Tree Arcs:')
        # for arcs in A:
        #     print()
        #     for a in arcs:
        #         print(a)
        # apply dijkstra to obtain shortest path
        dist, prev = dijkstra([s for s in g.S if s.is_free()], g.V, A)
        # print('\ndijkstra distances: {}'.format(dist))
        # print('dijkstra previous:')
        # for key in prev:
        #     print('prev[ {} ] = {}'.format(key, prev[key]))
        distances = sorted([
            (dist[ind+int(g.num_vertex/2)], ind+int(g.num_vertex/2)) 
            for ind in range(int(g.num_vertex/2)) 
            if g.V[ind+int(g.num_vertex/2)].is_free()
            ],key=lambda tup: tup[0])
        # print('\ndistances: {}'.format(distances))
        # recover shortest augmenting path
        augmenting_path = make_augmenting_path(distances, prev) 
        # print('\npath: {}'.format(augmenting_path))
        lenP = path_value(augmenting_path, A)
        if lenP < 0 and operation=='min':
            return M
        elif lenP >= 0 and operation=='max':
            return M
        else:
            num_matches = augment_path(num_matches, M, augmenting_path, g)
            # print('\nAfter augmenting:')
            # print('num_matches: {}'.format(num_matches))
            # print('M: {}'.format(M))
            # print('S:')
            # for s in g.S:
            #     print(s)
            # print('T:')
            # for t in g.T:
            #     print(t)
            update_potentials(g, dist)
            # print('\nAfter update potentials:')
            # print('S:')
            # for s in g.S:
            #     print(s)
            # print('T:')
            # for t in g.T:
            #     print(t)

    return M


def augment_path(num_matches, matches, augmenting_path, g):
    g.V[augmenting_path[0]].match()
    g.V[augmenting_path[-1]].match()
    num_matches += 2
    for i in range(len(augmenting_path)-1):
        # even -> match
        if i%2 == 0:
            matches[augmenting_path[i]] = augmenting_path[i+1]
            matches[augmenting_path[i+1]] = augmenting_path[i]
            g.E[augmenting_path[i]][augmenting_path[i+1]-int(g.num_vertex/2)].match()
        # odd -> free
        else:
            g.E[augmenting_path[i]][augmenting_path[i+1]].free()
    return num_matches


def update_potentials(g, dist):
    # s0 t0 s1 t1 ... sN tN
    for v in g.V:
        g.V[v.id].update_potential(dist[v.id])

def make_augmenting_path(distances, previous):
    if distances:
        distance, vertex = distances[0]
        current = vertex
        path = [vertex]
        while previous[current] is not None:
            current = previous[current]
            path.append(current)
        return path[::-1]
    return None


def path_value(path, arcs):
    sum = 0
    # d(P)
    for i in range(len(path)-1):
        src = path[i]
        dst = path[i+1]
        for a in arcs[src]:
            if a.dst.id is dst:
                sum += a.distance
    return sum

# ok
def dijkstra(sources, vertex, arcs):
    distance = [float('inf') for v in range(len(vertex))]
    previous = {}
    heap = []
    for source in sources:
        distance[source.id] = 0
        heapq.heappush(heap, (0, source.id, None))
    while heap:
        dst, vID, prev = heapq.heappop(heap)
        
        if dst > distance[vID]:
            continue
            
        previous[vID] = prev

        for arc in arcs[vID]:
            alt = dst + arc.get_distance()
            if alt < distance[arc.dst.id]:
                distance[arc.dst.id] = alt
                heapq.heappush(heap, (alt, arc.dst.id, vID))
    
    return distance, previous
                

def from_cmd(operation='min'):
    n = int(input())
    num_vertex = 2*n
    V = [Vertex(i) for i in range(num_vertex)]
    S = [v for v in V if v.id < n]
    T = [v for v in V if v.id >= n]
    E = [[] for i in range(num_vertex)]
    for r in range(n):
        line = input()
        splitline = line.split(' ')
        c = 0
        for w in splitline:
            if not w == '':
                # min -> use negative weights from input matrix
                if operation == 'min':
                    e = Edge((r, c+n), V[r], V[c+n], -int(w))
                # max -> use weights from input matrix
                else:
                    e = Edge((r, c+n), V[r], V[c+n], int(w))
                E[r].append(e)
                E[c+n].append(e) 
                c += 1
    expected_value = int(input())
    return Graph(V, S, T, E, expected_value)



g = from_cmd('min')
g.print()
M = hungarian(g)
sum = 0
for i in range(int(g.num_vertex/2)):
    sum += g.E[M[i]][i].weight
print('sum: '+ str(-sum))
print('expected: ' + str(g.expectedvalue))