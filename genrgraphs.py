
import random
rgraphspath = '/home/macsilva/Desktop/ufrgs/cadeiras/2022/02/alg_avancados/matching/rgraphs/'

for n in range(100, 401):
    with open(rgraphspath + '{}.dat'.format(n), 'w') as f:
        f.write('{}\n'.format(n))
        for row in range(n):
            r = str(random.randint(-256, 256))
            for column in range(n-1):
                r = r + ' ' + str(random.randint(-256, 256))
            f.write(r + '\n')

            