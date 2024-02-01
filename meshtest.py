from stl import mesh
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np

# Create a new plot
# figure = plt.figure()
# axes = mplot3d.Axes3D(figure)

copernicus = mesh.Mesh.from_file("./3d_model_test/Copernicuscrater3Xv.stl")
# axes.add_collection3d(mplot3d.art3d.Poly3DCollection(copernicus.vectors))

x, y, z = copernicus.x, copernicus.y, copernicus.z
x = x.flatten()
y = y.flatten()
z = z.flatten()
# print(x, y, z)
points = np.stack((x, y, z), axis=-1)
print(np.min(points))
np.savetxt("./output/copernicus_points.txt", points, fmt="%d")
# # Auto scale to the mesh size
# scale = copernicus.points.flatten()
# axes.auto_scale_xyz(scale, scale, scale)

# # Show the plot to the screen
# plt.show()