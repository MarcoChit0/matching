from copy import deepcopy
import time

start = time.time()
n = int(input())
matrix = []
for r in range(n):
    line = input()
    splitline = line.split(' ')
    row = []
    for c in splitline:
        if not c == '':
            row.append(int(c))
    matrix.append(row)
# value = int(input())

costs = deepcopy(matrix)

# Subtract the smallest entry in each row from all the other entries in the row. 
# This will make the smallest entry in the row now equal to 0. 
for row in range(n):
    rmin = float('inf')
    for column in range(n):
        if rmin > matrix[row][column]:
            rmin = deepcopy(matrix[row][column]) 
    for column in range(n):
        matrix[row][column] = matrix[row][column] - rmin

# Subtract the smallest entry in each column from all the other entries in the column. 
# This will make the smallest entry in the column now equal to 0. 
for column in range(n):
    cmin = float('inf')
    for row in range(n):
        if cmin > matrix[row][column]:
            cmin = deepcopy(matrix[row][column]) 
    for row in range(n):
        matrix[row][column] = matrix[row][column] - cmin

dostep3 = True
# Draw lines through the row and columns that have the 0 entries such that the fewest lines possible are drawn. 
while dostep3:
    zeros = []
    rmax = 0
    rmax_positions = [i for i in range(n)]
    rcount = [0 for i in range(n)]
    cmax = 0
    cmax_positions = [i for i in range(n)]
    ccount = [0 for i in range(n)]
    for row in range(n):
        for column in range(n):
            if matrix[row][column] == 0:
                # add zero position
                zeros.append((row, column))
                # update row counter
                rcount[row] = rcount[row] + 1
                if rmax < rcount[row]:
                    rmax = deepcopy(rcount[row])
                    rmax_positions = [deepcopy(row)]
                elif rmax == rcount[row]:
                    rmax_positions.append(deepcopy(row))
                # update column counter
                ccount[column] = ccount[column] + 1
                if cmax < ccount[column]:
                    cmax = deepcopy(ccount[column])
                    cmax_positions = [deepcopy(column)]
                elif cmax == ccount[column]:
                    cmax_positions.append(deepcopy(column))
    covered = []
    uncovered = []
    uncrows = [0 for i in range(n)]
    unccolumns = [0 for i in range(n)]
    rlines = []
    clines = []
    for row, column in zeros:
        if row in rlines or column in clines:
            covered.append((row,column))
        elif row in rmax_positions:
            rlines.append(row)
            covered.append((row, column))
        elif column in cmax_positions:
            clines.append(column)
            covered.append((row, column))
        else:
            uncovered.append((row, column))
            uncrows[row] = uncrows[row] + 1
            unccolumns[column] = unccolumns[column] + 1

    while len(uncovered) > 0:
        rmax = max([r for r in uncrows])
        cmax = max([c for c in unccolumns])
        if rmax >= cmax: 
            index = uncrows.index(rmax)
            uncrows[index] = 0
            rlines.append(index)
            cov = [(r,c) for r, c in uncovered if r == index]
            uncovered = [(r,c) for r, c in uncovered if not r == index]
        else:
            index = unccolumns.index(cmax)
            unccolumns[index] = 0
            clines.append(index)
            cov = [(r,c) for r, c in uncovered if c == index]
            uncovered = [(r,c) for r, c in uncovered if not c == index]
        covered.extend(cov)

    if len(rlines) + len(clines) == n:
        dostep3 = False
    else:
        minunc = float('inf')
        for row in [r for r in range(n) if r not in rlines]:
            for column in [c for c in range(n) if c not in clines]:
                if minunc > matrix[row][column]:
                    minunc = deepcopy(matrix[row][column])
        for row in [r for r in range(n) if r not in rlines]:
            if row not in rlines:
                for column in range(n):
                    matrix[row][column] = matrix[row][column] - minunc
        for column in clines:
            for row in range(n):
                matrix[row][column] = matrix[row][column] + minunc

selections = []
for row in range(n):
    candidates = []
    for column in range(n):
        if matrix[row][column] == 0:
            candidates.append(column)
    selections.append(candidates)

selected = [0 for i in range(n)]
while sum(selected) < n:
    colisions = []
    count = 0
    for s in selections:
        if len(s) == 1:
            selected[s[0]] = 1
        else:
            colisions.append(deepcopy(count))
        count += 1
    for col in colisions:
        for s in selections[col]:
            if selected[s] == 1:
                del selections[col][selections[col].index(s)]

sol = 0
count = 0
pairs = []
for s in selections:
    sol += costs[count][s[0]]
    count += 1
    pairs.append((count, s[0]))
print('pairs:')
print('time: {}'.format(time.time() - start))
print(pairs)
print('value:')
print(sol)