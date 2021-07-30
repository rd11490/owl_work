import numpy as np



m = np.array([[1,1,0],[1,0,1],[0,1,1]])

y = np.array([3, -6, 9])

res = np.linalg.solve(m, y)
print(res)