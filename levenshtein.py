###Yes there is a library. I didn't use it because there was an install error and I'm too lazy to fix it

import numpy as np

def similarity(data, target):
    data = data.lower()
    target = target.lower()
    threshold = 2
    matrix = np.zeros((len(data)+1,len(target)+1))
    for i in range(1,len(target)+1):
        matrix[0][i] = i
    for i in range(1,len(data)+1):
        matrix[i][0] = i
    for x in range(1,len(data)+1):
        for y in range(1,len(target)+1):
            if data[x-1] == target[y-1]:
                matrix[x,y] = min(
                    matrix[x-1,y] +1,
                    matrix[x-1,y-1],
                    matrix[x,y-1]+1 )
            else:
                matrix[x,y] = min(
                    matrix[x-1,y] +1,
                    matrix[x-1,y-1]+1,
                    matrix[x,y-1]+1 )
    return matrix[len(data),len(target)]
