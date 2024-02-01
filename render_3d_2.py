import os
try:
    import numpy as np
    import matplotlib.pyplot as plt, mpld3
    from mpl_toolkits.mplot3d import Axes3D
    import plotly.graph_objects as go
except ImportError:
    os.system("pip install numpy matplotlib mpld3 plotly")
    import numpy as np
    import matplotlib.pyplot as plt, mpld3
    from mpl_toolkits.mplot3d import Axes3D
    import plotly.graph_objects as go
from cmap_options import CMAP

normals = np.load("./output/normals.npy")
albedos = np.load("./output/albedos.npy")

heights = albedos[:, :, 2]
heights = np.rot90(heights, k=-1)
# heights /= np.linalg.norm(heights)

y, x = np.meshgrid(np.linspace(0, 1, 730), np.linspace(0, 1, 730))
u = normals[:, :, 0]
v = normals[:, :, 1]
w = normals[:, :, 2]

# fig = go.Figure(data=go.Cone(
#     x=x,
#     y=y,
#     z=heights,
#     u=u,
#     v=v,
#     w=w,
#     sizemode="absolute",
#     sizeref=2,
#     anchor="tip"))
# fig.update_layout(
#       scene=dict(domain_x=[0, 1],
#                  camera_eye=dict(x=-1.57, y=1.36, z=0.58)))
# fig.show()
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.quiver(x, y, heights, u, v, w, length=0.1, normalize=True)
surface = ax.plot_surface(x, y, heights, cmap=CMAP().jet)
fig.colorbar(surface, ax=ax, shrink=0.5, aspect=10)
ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([1, 1, 0.225, 1])) # just flatten it a little so it looks better LOL
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Height')
plt.title("Height Map of the Moon")
plt.show()
