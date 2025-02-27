import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

normals = np.load("./output/normals_copernicus.npy")
spacing, w, h = 1, normals.shape[0], normals.shape[1]
# normals = normals.reshape((w ** 2, 3))
# for i in range(len(normals)):
#     if np.linalg.norm(normals[i]) != 0:
#         normals[i] /= np.linalg.norm(normals[i])
# normals = normals.reshape((w, h, 3))
normals[:, :, 0] *= -1
normals = np.rot90(normals, 3, (0, 1))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = np.arange(0, w, spacing)
y = np.arange(0, h, spacing)
X, Y = np.meshgrid(x, y)

dz = np.zeros((w, h))
z = np.zeros((w, h))
for i in range(w):
    for j in range(1, h):
        z[i, j] = z[i, j - 1] + normals[i, j, 0]
        # print(normals[i, j, 0])
for i in range(w):
    for j in range(h):
        dz[i, j] = math.sqrt(normals[i, j, 0] ** 2 + normals[i, j, 1] ** 2 + normals[i, j, 2] ** 2) # Magnitude??
        # dz[i, j] = math.sqrt(normals[i, j, 1] ** 2 + normals[i, j, 2] ** 2)
        # dz[i, j] = normals[i, j, 0]
# print(dz)

ax.plot_surface(Y, X, dz, cmap='gray', edgecolor='none')
ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([1, 1, 0.225, 1])) # just flatten it a little so it looks better LOL
# ax.quiver(X, Y, dz, normals[:, :, 0], normals[:, :, 1], normals[:, :, 2], length=0.1, pivot='tail')
plt.show()

# ax.plot_surface(X, Y, z[Y, X], cmap='viridis', edgecolor='none')
# plt.show()