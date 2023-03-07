from copy import deepcopy
import heapq
import time

def augment(matched_vertex, M, augmenting_path):
    matched_vertex += 2
    for i in range(len(augmenting_path)-1):
        if i%2 == 0:
            M[augmenting_path[i]]   = augmenting_path[i+1]
            M[augmenting_path[i+1]] = augmenting_path[i]
    return matched_vertex

def dijkstra(W, M, P, n):
    distances = [float('inf') for v in range(2*n)]
    previous = {}
    heap = []
    for s in range(n):
        if M[s] == None:
            distances[s] = 0
            # heap += (
            # source distance to source = 0,
            # source,
            # source previous node = None)
            heapq.heappush(heap, (0, s, None))
    while heap:
        dist, vertex, prev = heapq.heappop(heap)

        if dist > distances[vertex]:
            continue

        previous[vertex] = prev

        # vertex belongs to S
        # that could happen if:
        # . vertex is matched
        # . vertex is free
        if vertex < n:
            for i in range(n, 2*n):
                if not M[vertex] == i:
                    alt = dist + dijkstra_dist(vertex, i, W, M, P, n)
                    if alt < distances[i]:
                        distances[i] = alt
                        heapq.heappush(heap, (alt, i, vertex))
        # vertex belongs to T,
        # that only happens when vertex is matched
        # therefore, only neighbor is Mvertex
        elif n <= vertex < 2*n:
            if M[vertex] is not None:
                alt = dist + dijkstra_dist(vertex, M[vertex], W, M, P, n)
                if alt < distances[M[vertex]]:
                    distances[M[vertex]] = alt
                    heapq.heappush(heap, (alt, M[vertex], vertex))
    return distances, previous

def make_augmenting_path(vertex, previous):
    path = [vertex]
    current = vertex
    while previous[current] is not None:
        current = previous[current]
        path.append(current)
    return path[::-1]

def dijkstra_dist(src, dst, W, M, P, n):
    # dist'(src, dst) = dist(src, dst) - (p(dst) - p(src))
    # s -> t arc
    if src < n and n <= dst < 2*n:
        return -W[src][dst-n] - (P[dst] - P[src])
    # t -> s arc only if Mt = s and Ms = t
    elif (n <= src < 2*n and dst < n) and \
        (M[src] == dst and M[dst] == src):
        return W[dst][src-n] - (P[dst] - P[src])
    else:
        quit('Error -- dijsktra dist')



def update_potentials(P, distances):
    for v in range(len(P)): 
        P[v] = P[v] + distances[v]


######################
##  get input data  ##
######################
start = time.time()
n = int(input())
V = [i for i in range(2*n)]
M = [None for i in range(2*n)]
matched_vertex = 0
W = [[] for i in range(n)]
maxwe = float('-inf')
for r in range(n):
    line = input()
    splitline = line.split(' ')
    for w in splitline:
        if not w == '':
            if maxwe <= -int(w):
                maxwe = -int(w)
            W[r].append(-int(w)) 
value = int(input())
P = []
for i in range(2*n):
    if i < n:
        P.append(0)
    else:
        P.append(-maxwe)


#########################
##  run matching algo  ##
#########################
count = 0
while matched_vertex < 2*n:
    prevnum = deepcopy(matched_vertex)

    distances, previous = dijkstra(W, M, P, n)
    tuples_list = [(distances[i], i) for i in range(n, 2*n) if M[i] == None]
    ######################################
    ##  select minimun augmenting path  ##
    mindist = float('inf')
    minvertex = None
    for dist, vertex in tuples_list:
        if mindist > dist:
            mindist = deepcopy(dist)
            minvertex = deepcopy(vertex)
    ######################################
    augmenting_path = make_augmenting_path(minvertex, previous)
    matched_vertex = augment(matched_vertex, M, augmenting_path)
    update_potentials(P, distances)
    count += 1
    # print('{}: dist {}'.format(count, distances))
    # print('{}: M {}'.format(count, M))


###########################################
##  get value and assert it is correct   ##
###########################################
sum = 0
for i in range(n):
    sum += W[i][M[i]-n]
assert -sum == value
end = time.time() - start
print('{},{},{},{}'.format(end, value, -sum, M))