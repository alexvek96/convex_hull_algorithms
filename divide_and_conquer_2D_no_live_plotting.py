# Divide and Conquer algorithm in 2D, no live plotting

import matplotlib.pyplot as plt                 # for plotting
import numpy as np                              # for random number generation and math calculations
import random                                   # for random number generation and math calculations
import time                                     # for computation timing


print("\n------------------------------------------------------------------------------------")
print("              Divide and Conquer algorithm in 2D, no live plotting                     ")
print("------------------------------------------------------------------------------------\n")

# Function to find whether the point is above or below the reference line
def determinant(a, b, c):

    # a: point, the point on the left end of line segment ab
    # b: point, the point on the right end of line segment ab
    # c: point, the point for which the direction and location is computed

    det = (a[0] * b[1] + b[0] * c[1] + c[0] * a[1]) - (a[1] * b[0] + b[1] * c[0] + c[1] * a[0])
    return det

# Function to implement the Divide and Conquer algorithm recursively
def devide_and_conquer(points):

    # Sort the points in increasing order of x-coordinates
    points = sorted(points)
    n = len(points)

    # Choose the leftmost and rightmost points as the endpoints of the convex hull
    left_most_point = points[0]
    right_most_point = points[n - 1]

    # Initialize the convex hull with the leftmost and rightmost points
    convex_set = {left_most_point, right_most_point}
    # Split the remaining points into two sets, one for the upper hull and one for the lower hull
    upper_hull = []
    lower_hull = []

    for i in range(1, n - 1):
        # Find the determinant of the three points to determine whether they are on the upper or lower hull
        det = determinant(left_most_point, right_most_point, points[i])

        if det > 0:
            upper_hull.append(points[i])
        elif det < 0:
            lower_hull.append(points[i])

    # Recursively construct the upper and lower hulls
    construct_hull(upper_hull, left_most_point, right_most_point, convex_set)
    construct_hull(lower_hull, right_most_point, left_most_point, convex_set)

    return sorted(convex_set)

# function to update the state of the current convex hull
def construct_hull(points, left, right, convex_set):

    # points: the hull of points from which to choose the next convex-hull point
    # left: the point to the left  of line segment joining left and right
    # right: τhe point to the right of the line segment joining left and right

    # If there are any initial points left
    if points:
        extreme_point = None
        extreme_point_distance = float("-inf")
        candidate_points = []

        # Find the point with the largest determinant
        for p in points:
            det = determinant(left, right, p)

            # p is on the left of the line joining left and right
            if det > 0:
                candidate_points.append(p)

                if det > extreme_point_distance:
                    extreme_point_distance = det
                    extreme_point = p

        # If an extreme point is found
        if extreme_point:

            # Recursively construct the hull on the left and right of the extreme point
            construct_hull(candidate_points, left, extreme_point, convex_set)
            # Add the extreme point to the convex hull
            convex_set.add(extreme_point)
            construct_hull(candidate_points, extreme_point, right, convex_set)


# Function to compute the angle between two points and the x-axis
def angle(p1, p2):
    return np.arctan2(p2[1]-p1[1], p2[0]-p1[0])


# initialize points list
points = []

# Generate X random points form user input
current_time = int(time.time())
np.random.seed(current_time)
num_of_points = int(input("How many points do you want to examine as per their Convex Hull? -> "))
x_values = []
for i in range(num_of_points):
    x = random.randint(-100,100)            # random coordinates for the points
    if i == 1:
        x_values.append(x)
    else:
        if x in x_values:                   # if the new point has x-coordinate that already exists, repeat the number generation
            while x in x_values:
                x = random.randint(-100, 100)   # regenerate x-coordinate
    y = random.randint(-100,100)
    point = x,y
    points.append(point)

print("\n-------------------------Initial 2D points-------------------------\n")
print(np.array(points))

start_time = time.time()
convex_hull_points = devide_and_conquer(points)
finish_time = time.time()

print("\n-------------------------Convex Hull Points-------------------------\n")
print(np.array(convex_hull_points))


# elapsed time
print("\nElapsed calculation time: ", "{:.8f}".format(finish_time - start_time), "seconds")


# Set up the figure and axis for animation
fig, ax = plt.subplots()
ax.set_title("Divide and Conquer Algorithm for Convex Hull")
ax.set_xlabel("X")
ax.set_ylabel("Y")

# conversions for better data manipulation
points = np.array(points)
convex_hull_points = np.array(convex_hull_points)

# Plot the initial points
scatter = ax.scatter(points[:, 0], points[:, 1], c="b", marker="o")
for i in range(num_of_points):
    ax.text(points[i, 0], points[i, 1], str(i + 1), fontsize=12)

# Plot the convex hull points
scatter = ax.scatter(convex_hull_points[:, 0], convex_hull_points[:, 1], c="b", marker="o")

# Find the center of mass of the points to use it for CW sorting
center = np.mean(convex_hull_points, axis=0)

# Sort the points in clockwise order
# We need the sorting in order to plot the line of the convex hull. It doesn't matter
# if the sorting is CW or CCW for the line to be plotted.
cw_sorted_points = sorted(convex_hull_points, key=lambda p: angle(center, p))

for i in range(len(cw_sorted_points)):
    p1 = cw_sorted_points[i]
    if i == len(cw_sorted_points) - 1:
        p2 = cw_sorted_points[0]
    else:
        p2 = cw_sorted_points[i+1]
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], c="r")


plt.show()