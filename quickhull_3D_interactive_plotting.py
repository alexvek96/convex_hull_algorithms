# Quick Hull algorithm in 3D, no live plotting, using 'scipy' package

import numpy as np
import time
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

print("\n------------------------------------------------------------------------------------")
print("        Quick Hull algorithm through ConvexHull lib in 3D, no live plotting           ")
print("------------------------------------------------------------------------------------\n")

# Generate X random 3D points from user input
current_time = int(time.time())
np.random.seed(current_time)
num_of_points = int(input("How many points do you want to examine as per their Convex Hull? -> "))
x = np.random.uniform(-10, 10, size=num_of_points)
y = np.random.uniform(-10, 10, size=num_of_points)
z = np.random.uniform(-10, 10, size=num_of_points)
points = np.vstack((x, y, z)).T

print("\n-------------------------Initial 3D points-------------------------\n")
print(points)

start_time = time.time()
# Compute the convex hull of the points
hull = ConvexHull(points)
finish_time = time.time()

# Plot the convex hull
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Set initial view angles for rotation interaction with mouse
ax.view_init(elev=30, azim=45)

# Enable mouse interaction
ax.mouse_init()

ax.set_title("Quick Hull Algorithm for Convex Hull in 3D")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

# Plot the inner points of the hull with a black border around the body
inner_points = np.setdiff1d(np.arange(num_of_points), hull.vertices)
ax.scatter(points[inner_points, 0], points[inner_points, 1], points[inner_points, 2], c='red', edgecolor='black', linewidths=3, marker='s', s=10)

# Plot the Convex Hull points with the same color but with no border
ax.scatter(hull.points[:,0], hull.points[:,1], hull.points[:,2], c='red', marker='X', s=10)
ax.plot_trisurf(hull.points[:,0], hull.points[:,1], hull.points[:,2], triangles=hull.simplices, color='grey', alpha=0.35)

hull_points = np.delete(points, inner_points, axis=0)
print("\n------------------------- Convex Hull Points (", len(hull_points), "points) -------------------------\n")
print(hull_points)

# elapsed computation time
print("\nElapsed calculation time: ", finish_time - start_time, "seconds")

plt.show()