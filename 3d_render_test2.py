import numpy as np

def calculate_normals_with_gradient(surface_function, x, y):
    """
    Calculate normal vectors to a surface using gradients with np.gradient.

    Parameters:
    - surface_function: Function that represents the surface. Should take three NumPy arrays (x, y, z) of the same shape as input.
    - x, y, z: 1D NumPy arrays representing the coordinates of the surface grid.

    Returns:
    - normals: Tuple of three NumPy arrays representing the normal vectors along x, y, and z axes.
    """

    # Calculate the gradient using np.gradient
    gradient_x, gradient_y= np.gradient(surface_function(x, y), axis=(0, 1))

    # Combine the gradients to get the normal vectors
    normals = np.stack([gradient_x, gradient_y], axis=-1)
    
    # Normalize the normals
    norm_magnitude = np.linalg.norm(normals, axis=-1, keepdims=True)
    normals /= norm_magnitude

    return normals

# Example usage:
def example_surface_function(x, y):
    # Replace this with your actual surface function
    return x ** 2 * y

# Define the grid
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
# z = np.linspace(-5, 5, 100)

# Create a meshgrid
X, Y = np.meshgrid(x, y, indexing='ij')

# Calculate normal vectors
normals = calculate_normals_with_gradient(example_surface_function, X, Y)

# Print the result
# print("Points on surface:\n", points_on_surface)
# print("Normal vectors:\n", normals)

# # Plot the surface and normal vectors
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = example_surface_function([X, Y])
ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)

# Plot the normal vectors
scale_factor = 1  # Adjust the scale of the vectors for better visualization
ax.quiver(points_on_surface[:, 0], points_on_surface[:, 1], example_surface_function(points_on_surface),
          normals[:, 0] * scale_factor, normals[:, 1] * scale_factor, np.zeros_like(normals[:, 0]),
          length=0.1, normalize=True)

# Set labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Show the plot
plt.show()
