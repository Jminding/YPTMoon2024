# # import matplotlib.pyplot as plt
# # from mpl_toolkits.mplot3d import Axes3D
# # import numpy as np
# # import math

# # # generate a random surface h(x, y)  = x^2 * y
# # x = np.arange(0, 5, 1)
# # y = np.arange(0, 5, 1)
# # X, Y = np.meshgrid(x, y)
# # Z = X ** 2 * Y

# # # calculate the gradient vector field
# # # dz = np.gradient(Z)
# # # M = np.hypot(*dz)
# # # # plot dx
# # # fig, axe = plt.subplots(figsize=(12, 12))
# # # # axe.contour(X, Y, Z, 30, cmap="jet", linewidths=0.75)
# # # # axe.quiver(X, Y, dz[1], dz[0], M, cmap="jet", units='xy', pivot='tail', width=0.03, scale=5)
# # # axe.set_aspect("equal")  # Don't stretch the scale
# # # axe.grid()
# # # plt.show()

# # # plot the surface
# # fig = plt.figure()
# # ax = fig.add_subplot(projection='3d')
# # ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
# # ax.set_xlabel('x')
# # ax.set_ylabel('y')
# # plt.show()

# import numpy as np
# import sympy as sp
# import matplotlib.pyplot as plt

# def find_normal_gradient_on_grid(function, X, Y):
#     # Define the symbolic variables
#     x, y = sp.symbols('x y')

#     # Define the function symbolically
#     f = sp.sympify(function)

#     # Compute the partial derivatives
#     df_dx = sp.diff(f, x)
#     df_dy = sp.diff(f, y)

#     # Convert the partial derivatives to NumPy functions
#     df_dx_func = sp.lambdify((x, y), df_dx, 'numpy')
#     df_dy_func = sp.lambdify((x, y), df_dy, 'numpy')

#     # Evaluate the derivatives on the grid
#     df_dx_values = df_dx_func(X, Y)
#     df_dy_values = df_dy_func(X, Y)

#     # Create the normal gradient vectors
#     normal_gradient_x = -df_dy_values
#     normal_gradient_y = df_dx_values

#     return normal_gradient_x, normal_gradient_y

# # Example usage with your provided grid
# x = np.arange(0, 5, 1)
# y = np.arange(0, 5, 1)
# X, Y = np.meshgrid(x, y)

# # Define your function (replace this with your actual function)
# function_to_evaluate = 'x ** 2 * y'

# # Compute normal gradient vectors on the grid
# normal_gradient_x, normal_gradient_y = find_normal_gradient_on_grid(function_to_evaluate, X, Y)

# gradients = np.stack((normal_gradient_x, normal_gradient_y), axis=-1)

# # Create the surface
# Z = X ** 2 * Y # Evaluate the function to get Z values

# # Create a 3D plot
# # fig = plt.figure()
# # ax = fig.add_subplot(111, projection='3d')

# # # Plot the surface
# # # ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)

# # # Plot the normal vectors
# # scale_factor = 10  # Adjust the scale of the vectors for better visualization
# # ax.quiver(X, Y, Z, normal_gradient_x * scale_factor, normal_gradient_y * scale_factor, np.ones_like(Z),
# #           cmap='viridis', length=0.1, normalize=True)

# # # Set labels
# # ax.set_xlabel('X')
# # ax.set_ylabel('Y')
# # ax.set_zlabel('Z')

# # # Show the plot
# # plt.show()

# # gradients[:, :, 0] *= -1
# # gradients[:, :, 1] *= -1
# # gradients *= -1
# gradients = np.rot90(gradients, 3, (0, 1))

# z = np.zeros((5, 5))
# for i in range(5):
#     for j in range(5):
#         z[i, j] = z[i, j - 1] + (np.linalg.norm(gradients[i, j]) - np.linalg.norm(gradients[i, j - 1]))

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# # ax.plot_surface(Y, X, Z, cmap='gray', edgecolor='none')
# ax.plot_surface(Y, X, z * 60 / 17.5, cmap='gray', edgecolor='none')
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z')
# # ax.set_title('Reconstructed with Proportionality')
# plt.show()

# # Print or use the results as needed
# # print("Normal Gradient Vector in the x-direction:")
# # print(normal_gradient_x)
# # print("\nNormal Gradient Vector in the y-direction:")
# # print(normal_gradient_y)


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def z(x,y):
    return x ** 2 * y

x = np.linspace(0, 5, 10)
y = np.linspace(0, 5, 10)
X, Y = np.meshgrid(x, y)
Z = z(X, Y)

dx = dy = 0.1  

dz_dx, dz_dy = np.gradient(Z, dx, dy)
dz_dx = dz_dx / np.linalg.norm(dz_dx)
dz_dy = dz_dy / np.linalg.norm(dz_dy)
dZ = 1 - np.sqrt(dz_dx**2 + dz_dy**2)

gradients = np.stack((-dz_dy, dz_dx, dZ), axis=-1)
print(gradients.shape)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.quiver(X, Y, Z, dz_dx, dz_dy, dZ, length=10)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.zaxis.set_rotate_label(False) 
ax.set_zlabel('z');
ax.set_title('Gradient vectors of z=x^2+y^2')

heights = np.zeros((len(x), len(y)))
for i in range(len(y)):
    for j in range(len(x)):
        heights[i, j] = heights[i, j - 1] + (np.linalg.norm(gradients[i, j]) - np.linalg.norm(gradients[i, j - 1]))
    
print(heights)
heights = np.rot90(heights, 5, (0, 1))

ax.plot_surface(Y, X, heights * 500, cmap='viridis', edgecolor='none')

plt.show()