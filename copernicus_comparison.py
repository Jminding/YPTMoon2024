import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

normals = np.load("./output/normals_copernicus.npy")
# plt.hist(1 / normals[:, :, 2].flatten(), bins=100)
# print(normals.shape)
# plt.show()
spacing, w, h = 1, normals.shape[0], normals.shape[1]
# normals = normals.reshape((w ** 2, 3))
# for i in range(len(normals)):
#     if np.linalg.norm(normals[i]) != 0:
#         normals[i] /= np.linalg.norm(normals[i])
# normals = normals.reshape((w, h, 3))
# normals[:, :, 0] *= -1
# normals = np.rot90(normals, 3, (0, 1))

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

x = np.arange(0, w, spacing)
y = np.arange(0, h, spacing)
X, Y = np.meshgrid(x, y)

dz = np.zeros((w, h))
z = np.zeros((w, h))
for i in range(w):
    for j in range(h):
        z[i, j] = z[i, j - 1] + (np.linalg.norm(normals[i, j]) - np.linalg.norm(normals[i, j - 1]))
        # z[i, j] = z[i, j - 1].copy() + normals[i, j, 0].copy()
        # z[i, j] = z[i, j - 1] + math.sqrt(normals[i, j, 0] ** 2 + normals[i, j, 1] ** 2 + normals[i, j, 2] ** 2) - math.sqrt(normals[i, j - 1, 0] ** 2 + normals[i, j - 1, 1] ** 2 + normals[i, j - 1, 2] ** 2)
        # z[i, j] = z[i, j - 1] + math.sqrt(normals[i, j, 0] ** 2 + normals[i, j, 2] ** 2) - math.sqrt(normals[i, j - 1, 0] ** 2 + normals[i, j - 1, 2] ** 2)
        # print(normals[i, j, 0])
for i in range(w):
    for j in range(h):
        dz[i, j] = math.sqrt(normals[i, j, 0] ** 2 + normals[i, j, 2] ** 2) # gradient vector along this axis
        # dz[i, j] = math.sqrt(normals[i, j, 0] ** 2 + normals[i, j, 2] ** 2)
        # dz[i, j] = normals[i, j, 0]
# print(dz)
        
x = x[315:630]
y = y[350:665]
z = z[350:665, 315:630]

heightmap_image = Image.open("./3d_model_test/heightmap_315x315.png")

spacing, w2, h2 = 1, heightmap_image.width, heightmap_image.height
x2 = np.arange(0, w2, spacing)
y2 = np.arange(0, h2, spacing)
X2, Y2 = np.meshgrid(x2, y2)

# Convert the heightmap to a numpy array
heightmap = np.array(heightmap_image) / 3
print(np.where(heightmap == np.max(heightmap)))
print(heightmap[60, 154], heightmap[60, 156])
# exit()
# layout=go.Layout(scene=dict(aspectmode='manual', aspectratio=dict(x=1, y=1, z=0.225)
# fig = go.Figure(data=[go.Surface(z=np.abs(z/17 - heightmap), x=x2, y=y2, colorscale='gray')], layout=go.Layout(scene=dict(aspectmode='manual', aspectratio=dict(x=1, y=1, z=0.225))))
# fig.update_layout(title='Copernicus Crater Height Map Comparison', autosize=False,
#                   margin=dict(l=65, r=50, b=65, t=90))
# fig.show()
# print(np.max(np.abs(z/17 - heightmap)))
# error = np.abs(np.average(z/17) - np.average(heightmap))
# error /= np.max(np.abs(z/17 - heightmap))
# print(error)
# print(w2 * h2)
# RMSE = np.sqrt(np.sum((z - heightmap * 18.05) ** 2) / (w2 * h2))
# print(RMSE)
# RMSE3 = np.sqrt(np.sum((z/18.05 - heightmap) ** 2) / (w2 * h2))
# print(RMSE3)
# print(np.abs(np.max(z) - np.min(z)))
# print(np.max(z) / np.max(heightmap))
# print(f"z: {z}")
# print(f"z/18.05: {z / 18.05}")
# print(f"heightmap: {heightmap}")
# print(f"heightmap * 18.05: {heightmap * 18.05}")
# print(f"z - 18.05 * heightmap: {z - 18.05 * heightmap}")
# print(RMSE / (np.abs(np.max(z) - np.min(z))))
# print(np.max(np.abs(z)))
# RMSE2 = np.sqrt(np.sum((143 * (z - heightmap * 17))) ** 2) / (143 * w2 * 143 * h2)
# print(RMSE2)
# print(np.abs(np.max(z) - np.min(z)))
# print(RMSE2 / (143 * np.abs(np.max(z) - np.min(z))))
# print(np.max(np.abs(z)))

exit()
# fig.write_html("./output/copernicus_heightmap_cropped.html")

# ax.plot_surface(Y, X, z, cmap='gray', edgecolor='none')
# ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([1, 1, 0.225, 1])) # just flatten it a little so it looks better LOL
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.quiver(X, Y, dz, normals[:, :, 0], normals[:, :, 1], normals[:, :, 2], length=0.1, pivot='tail')
# plt.show()

# ax.plot_surface(X, Y, z[Y, X], cmap='viridis', edgecolor='none')
# plt.show()