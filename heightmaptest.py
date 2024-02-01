import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

normals = np.load("./output/normals.npy").reshape((730 ** 2, 3))
for i in range(len(normals)):
    if np.linalg.norm(normals[i]) != 0:
        normals[i] /= np.linalg.norm(normals[i])
normals = normals.reshape((730, 730, 3))

dot = np.dot(normals, [0, 0, 1])
angle = np.arccos(dot)
# print(angle.min(), angle.max()) 

# length = np.linalg.norm(normals, axis=-1)

# dz = length * 100 * np.sin(angle)

# # print((dz > 0).all())

# z = dz.cumsum(axis=0).cumsum(axis=1)

# print(z.shape)
# # exit()

# spacing = 15

# x = np.arange(0, 730, spacing)  
# y = np.arange(0, 730, spacing)
# X, Y = np.meshgrid(x, y)

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# ax.plot_surface(X, Y, z[Y, X], cmap='terrain')
# plt.show()

# Setup histogram plot
fig, ax = plt.subplots()
counts, bins, patches = ax.hist(angle, bins=36, range=(0, np.pi))

# Plot formatting
ax.set_title("Theta Angle Distribution")  
ax.set_xlabel("Theta")
ax.set_ylabel("Frequency")

ax.set_xticks([0, np.pi])
ax.set_xticklabels(['$0$', '$\pi$'])

# fig.tight_layout()
plt.show()