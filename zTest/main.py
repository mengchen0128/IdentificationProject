import numpy as np

dydt=np.array([[1,2],[3,4]])
print(dydt)
dydt=[i for j in dydt for i in j]
print(dydt)

arr = np.array([[1,2,3],
                [4,5,6],
                [7,8,9]])
# 取出第一行
print(arr[0,:])
# 取出第一列
print(arr[:, 1:2])

P = np.array([[0],[0]])