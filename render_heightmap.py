import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go

heightmap_image = Image.open("./3d_model_test/heightmap_resized.png")

spacing, w, h = 1, heightmap_image.width, heightmap_image.height
x = np.arange(0, w, spacing)
y = np.arange(0, h, spacing)
X, Y = np.meshgrid(x, y)

# Convert the heightmap to a numpy array
heightmap = np.array(heightmap_image)

# heightmap = (heightmap * -1)

# Display the heightmap
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_surface(X, Y, heightmap[X, Y], cmap='gray', edgecolor='none')
# ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([1, 1, 0.225, 1])) # just flatten it a little so it looks better LOL
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Height')
# plt.show()
fig = go.Figure(data=[go.Surface(z=heightmap, x=x, y=y, colorscale='gray')], layout=go.Layout(scene=dict(aspectmode='manual', aspectratio=dict(x=1, y=1, z=0.225))))
fig.update_layout(title='Copernicus Crater Height Map Rendered from 3D Model', autosize=False,
                  margin=dict(l=65, r=50, b=65, t=90))
fig.show()

fig.write_html("./output/copernicus_heightmap_3d.html")