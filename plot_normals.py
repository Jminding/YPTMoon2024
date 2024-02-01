import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

normals = np.load("./output/normals_copernicus.npy")
spacing, w, h = 1, normals.shape[0], normals.shape[1]
normals = normals.reshape((w ** 2, 3))
for i in range(len(normals)):
    if np.linalg.norm(normals[i]) != 0:
        normals[i] /= np.linalg.norm(normals[i])
normals = normals.reshape((w, h, 3))
albedos = np.load("./output/albedos_copernicus.npy")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Sample pixels to plot
spacing = 50
x = np.arange(0, 1000, spacing)
y = np.arange(0, 1000, spacing)
X, Y = np.meshgrid(x, y) 

# Extract normal vectors 
U = normals[Y, X, 0] * 500
V = normals[Y, X, 1] * 500
W = normals[Y, X, 2] * 500
test = np.zeros((1000, 1000))

ax.quiver(X, Y, albedos[Y, X, 2], U, V, W, length=0.1, pivot='tail')
# ax.plot_surface(X, Y, albedos[Y, X, 2], cmap='gray', edgecolor='none')

# img = plt.imread('./test_data_libration/moon.11.jpg')

# Image overlay
# ax.imshow(img, extent=(0, 1000, 0, 1000), aspect='auto')  

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
# ax.set_zlim(-900, 900)


plt.title("Surface Normals")
plt.show()