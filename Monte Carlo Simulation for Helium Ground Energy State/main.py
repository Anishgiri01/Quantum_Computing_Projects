import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load your data; assuming the delimiter in your file is whitespace

x_vals = []
y_vals = []
z_vals = []

# Read the output.txt file
with open('output.txt', 'r') as file:
    for line in file:
        columns = line.split()
        if len(columns) >= 3:
            try:
                x = float(columns[0])
                y = float(columns[1])
                z = float(columns[2])

                # Filter out outcast values
                if -5 <= z <= 0:
                    x_vals.append(x)
                    y_vals.append(y)
                    z_vals.append(z)

            except ValueError:
                continue

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# To create a continuous 3D plot, you can use the trisurf function
ax.plot_trisurf(x_vals, y_vals, z_vals)

ax.set_xlabel('b')
ax.set_ylabel('Z')
ax.set_zlabel('Energy')

plt.show()