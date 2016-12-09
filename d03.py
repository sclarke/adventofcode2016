import pandas as pd

df = pd.read_table('d03.txt', sep='\s+', header=None)


def is_triangle(row):
    a, b, c = sorted(row)
    return a + b > c


triangles = df.apply(is_triangle, axis=1)
print(triangles.sum())

import numpy as np

a = np.array(df)
a = a.reshape((3, -1), order='F').T

a_tri = np.array([is_triangle(row) for row in a])
print(a_tri.sum())
