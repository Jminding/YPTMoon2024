import os
try:
    import numpy as np
    import matplotlib.pyplot as plt, mpld3
    from mpl_toolkits.mplot3d import Axes3D
except ImportError:
    os.system("pip install numpy matplotlib mpld3")
    import numpy as np
    import matplotlib.pyplot as plt, mpld3
    from mpl_toolkits.mplot3d import Axes3D
from cmap_options import CMAP

# TODO: make it work with normal surfaces???

# Assuming your 730x730 matrix is stored in the variable 'matrix'
# Each element of the matrix is a 3D vector [x, y, z]

# Generate some example data (replace this with your actual matrix)
matrix = np.load("./output/normals.npy")

# Extract the z-values (heights) from the matrix
heights = matrix[:, :, 2]
heights = np.where(heights != 0, heights, np.nan)
heights[heights > -20] -= 50
heights *= 60

heights = np.rot90(heights, k=-1)

# Create a meshgrid for x and y coordinates
y, x = np.meshgrid(np.arange(730), np.arange(730))

# Create a 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot the surface

surface = ax.plot_surface(x, y, heights, cmap=CMAP().jet)
fig.colorbar(surface, ax=ax, shrink=0.5, aspect=10)

# Set labels
ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([1, 1, 0.225, 1])) # just flatten it a little so it looks better LOL
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Height')

plt.title("Height Map of the Moon")
# Show the plot
plt.show()

mpld3.save_html(fig, "./output/height_map.html")

# Makes sense that albedo gives a good height map because it tells you about light and dark spots I guess?
