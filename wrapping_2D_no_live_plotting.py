# Wrapping algorithm in 2D

import time                                     # for computation timing
import numpy as np                              # for random number generation and math calculations
import matplotlib.pyplot as plt                 # for plotting
from matplotlib.animation import FuncAnimation  # for live animation

print("\n------------------------------------------------------------------------------------")
print("                   Wrapping algorithm in 2D, no live plotting                     ")
print("------------------------------------------------------------------------------------\n")

#   Function to sort a list of points lexicographically based on their x and y coordinates, and assign labels
def lexicographic_sort(points):

    # Convert input to numpy array for ease of sorting
    points = np.array(points)
    print("\n-------------------------Initial 2D points-------------------------\n")
    print(points)

    # Sort points lexicographically based on x and y coordinates
    sorted_indices = np.lexsort((points[:, 1], points[:, 0]))
    sorted_points = points[sorted_indices]

    # Find the leftmost point (minimum x and minimum y)
    leftmost_point = min(sorted_points, key=lambda point: (point[0], point[1]))

    # Find the index of the leftmost point
    leftmost_index = np.where((sorted_points[:, 0] == leftmost_point[0]) & (sorted_points[:, 1] == leftmost_point[1]))[0][0]

    # Rearrange the points to start with the leftmost point
    sorted_points = np.roll(sorted_points, -leftmost_index, axis=0)

    # Assign labels to the points
    N = len(sorted_points)
    labels = np.arange(1, N + 1)
    # Update the points with the assigned labels
    #sorted_points = np.hstack((sorted_points, labels.reshape(-1, 1)))
    print("\n-------------------------Sorted 2D points-------------------------\n")
    print(sorted_points)
    return sorted_points


# Disorder function for collinear points -> modifies the coordinates of the 3 points
def apply_disorder(points, epsilon):
        # Generate random displacement in range [-epsilon/2, epsilon/2]
        displacement = (np.random.rand(2) - 0.5) * epsilon
        # Apply displacement to points
        points += displacement


# function to execute if we find 3 collinear points
def collinear_points(points):
        epsilon = 1e-6
        points = apply_disorder(points, epsilon)


# Function to determine the orientation of three points
def orientation(p, q, r):

    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        # 0 if points are collinear, apply a small disorder to make resolve the problem
        collinear_points([p, q, r])
        orientation(p, q, r)
    elif val > 0:
        return 1       # 1 if points are CCW
    else:
        return -1      # -1 if points are CW


#   Function to compute the convex hull of a set of points using Wrapping algorithm
def jarvis_march(points):
    # Find the leftmost point
    leftmost_point = min(points, key=lambda point: point[0])

    # Start at the leftmost point and go counterclockwise
    current_point = leftmost_point
    convex_hull = []
    while True:
        convex_hull.append(current_point)

        # Find the next point in the hull
        next_point = None
        for point in points:
            if (point == current_point).all():
                continue
            if next_point is None:
                next_point = point
            else:
                cross_product = (point[0] - current_point[0]) * (next_point[1] - current_point[1]) - \
                                 (point[1] - current_point[1]) * (next_point[0] - current_point[0])
                if cross_product < 0:
                    next_point = point
                elif cross_product == 0:
                    # If the points are collinear, choose the one farthest from current point
                    dist_next = (next_point[0] - current_point[0])**2 + (next_point[1] - current_point[1])**2
                    dist_point = (point[0] - current_point[0])**2 + (point[1] - current_point[1])**2
                    if dist_point > dist_next:
                        next_point = point
        # We have returned to the start point
        if (next_point == leftmost_point).all():
            break
        current_point = next_point

    return np.array(convex_hull)

# Generate X random points form user input
current_time = int(time.time())
np.random.seed(current_time)
num_of_points = int(input("How many points do you want to examine as per their Convex Hull? -> "))
points = np.random.rand(num_of_points, 2)
start_time = time.time()
points = lexicographic_sort(points)
hull = jarvis_march(points)
finish_time = time.time()
print("\n-------------------------Convex Hull Points-------------------------\n")
print(hull)
print("\nElapsed calculation time: ", finish_time - start_time, "seconds")


# Set up the figure and axis for animation
fig, ax = plt.subplots()
ax.set_title("Wrapping Algorithm for Convex Hull")
ax.set_xlabel("X")
ax.set_ylabel("Y")

# Plot the initial points
scatter = ax.scatter(points[:, 0], points[:, 1], c="b", marker="o")
for i in range(num_of_points):
    ax.text(points[i, 0], points[i, 1], str(i + 1), fontsize=12)

# Initialize an empty line for the convex hull edges
line, = ax.plot([], [], "r-")

# Update function for animation
def update(i):

    if len(hull) > 0:  # Check to ensure hull array is not empty
        # Update the plot with the convex hull
        line.set_data(np.append(hull[:, 0], hull[0, 0]), np.append(hull[:, 1], hull[0, 1]))
    return [scatter, line]

# Create the animation
ani = FuncAnimation(fig, update, frames=len(points), interval=500, blit=True)

plt.show()