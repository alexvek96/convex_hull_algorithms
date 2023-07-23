# Quick Hull algorithm in 2D, no live plotting

import matplotlib.pyplot as plt     # for plotting
import numpy as np                  # for random number generation and math calculations
import random                       # for random number generation and math calculations
import time                         # for computation timing

print("\n------------------------------------------------------------------------------------")
print("                   Quick Hull algorithm in 2D, no live plotting                     ")
print("------------------------------------------------------------------------------------\n")


# Function to calculate distance between 2 points
def Point_Distance(point1, point2):
    difference = ((point1[0]-point2[0])**2) + ((point1[1]-point2[1])**2)
    distance = difference**(1/2)
    return distance


# Function to find the line equation if we know 2 points of it
def Line(point1, point2):
    equal = []
    x = point1[1] - point2[1]
    equal.append(x)
    y = point2[0] - point1[0]
    equal.append(y)
    c = (point2[1]*point1[0]) - (point1[1]*point2[0])
    equal.append(c)
    return equal


# Function to calculate distance of a point to a line
def Distance_Point_to_Line (point, line):
    counter = abs((line[0]*point[0]) + (line[1]*point[1]) + (line[2]))
    denominator = (line[0]**2 + line[1]**2)**(1/2)
    distance = counter/denominator
    return distance


# Function to find the farthest point from a reference point
def Farthest_Point(point1, point2, points):
    p = Line(point1, point2)
    max_distance = Distance_Point_to_Line(points[0], p)
    max_point = points[0]
    i = 1
    count = len(points)

    # check for every point if it has a greater distance from the reference point
    while (i < count):
        if (Distance_Point_to_Line(points[i], p) > max_distance):
            max_distance = Distance_Point_to_Line(points[i], p)
            max_point = points[i]
        i = i + 1
    return max_point


# Function to find whether the point is above or below the reference line
def Determinant(point1, point2, point3):
    det = (point1[0]*point2[1]) + (point3[0]*point1[1]) + (point2[0]*point3[1]) - (point3[0]*point2[1]) - (point2[0]*point1[1]) - (point1[0]*point3[1])
    return det


# function to delete any points from the list of 'points' that are inside the left_point, right_point and PointFar
# because if a point is inside the triangle of 3 other points, then it does not belong to the convex hull
def Delete_Point(left_point, right_point, PointFar, points):

    # Create two empty lists to store the points to the left and right of PointFar, respectively
    list_left = []
    list_right = []

    # Iterate over each point in the input 'points' list
    for point in points:

        # Determine if the point is to the left of the line formed by left_point and PointFar
        if (Determinant(left_point, PointFar, point) > 0):
            list_left.append(point)

    # Iterate over each point in the input 'points' list (again)
    for point in points:

        # Determine if the point is to the right of the line formed by PointFar and right_point
        if (Determinant(PointFar, right_point, point) > 0):
            list_right.append(point)

    i = 0   # counter

    while (len(points) != 0 and (i < len(points))):
        if (len(list_left) != 0 and len(list_right)!=0):

            # If both 'list_left' and 'list_right' are non-empty, remove points that are not in either list
            if (not (points[i] in list_right)  and not (points[i] in list_left)):

                points.pop(i)   # If the point is not in either list, remove it from 'points'
            else:
                i = i+1 # If the point is in either list, move on to the next point

        elif (len(list_left) == 0 and len(list_right) != 0):

            # If 'list_left' is empty but 'list_right' is not, remove points that are not in 'list_right'
            if (not (points[i] in list_right)) :
                points.pop(i)   # If the point is not in 'list_right', remove it from 'points'
            else:
                i = i+1 # If the point is in 'list_right', move on to the next point

        elif (len(list_right) == 0 and len(list_left) != 0):

            # If 'list_right' is empty but 'list_left' is not, remove points that are not in 'list_left'
            if (not points[i] in list_left):
                points.pop(i)   # If the point is not in 'list_left', remove it from 'points'
            else:
                i = i + 1   # If the point is in 'list_left', move on to the next point
        else:
            points.pop(i)   # If both 'list_left' and 'list_right' are empty, remove all points in 'points'


# Quick Hull function
def QuickHull(left_point, max_point, right_point, points):

    hull = []
    points.sort()
    if (len(points) == 0):
        hull.append(max_point)
        return hull
    elif (len(points) == 1):
        hull.append(max_point)
        hull.append(points[0])
        points.pop(0)
        return hull
    elif (len(points) > 1):
        hull.append(max_point)
        # Separate the points into two lists, one for the outer points and one for the inner points
        inner_point = []
        outer_point = []
        for point in (points) :
            if (Determinant(left_point, max_point, point) > 0):
                outer_point.append(point)
            elif (Determinant(left_point, max_point, point) < 0):
                inner_point.append(point)

        LeftHull = []
        RightHull = []

        # If there are outer points, find the farthest point from the left edge and recursively find the left hull
        if (len(outer_point) > 0 ):
            Far_Left_Point = Farthest_Point(left_point, max_point, outer_point)
            Delete_Point(left_point, max_point, Far_Left_Point, outer_point)
            LeftHull = QuickHull(left_point, Far_Left_Point,max_point, outer_point)

        # If there are inner points, find the farthest point from the right edge and recursively find the right hull
        if (len(inner_point) > 0 ):
            Far_Right_Point = Farthest_Point(max_point, right_point, inner_point)
            Delete_Point(max_point, right_point, Far_Right_Point, inner_point)
            RightHull = QuickHull(max_point, Far_Right_Point, right_point, inner_point)

        # Add the left and right hulls to the main hull list
        hull = hull + LeftHull + RightHull
        return hull


def SortHull(list_hull):

    hull = []
    # Assigning first two points as left and right points
    left_point = list_hull[0]
    right_point = list_hull[1]
    list_hull.remove(left_point)
    # Appending right point to hull and setting up for lower hull
    hull.append(right_point)
    lower_hull = []

    # Iterating over remaining points in list_hull
    for point in list_hull:
        # If point is to the right of the line formed by left and right point, append to hull
        if (Determinant(left_point, right_point, point) > 0):
            hull = [point] + hull
        # If point is to the left of the line formed by left and right point, append to lower_hull
        elif (Determinant(left_point, right_point, point) < 0):
            lower_hull.append(point)

    # Sorting both hull and lower_hull based on x-coordinate
    lower_hull.sort()
    hull.sort()

    # Reversing the order of points in lower_hull
    lower_hull = list(reversed(lower_hull))

    # Combining all points to form a complete hull and returning it
    hull = [left_point] + hull + lower_hull + [left_point]

    return (hull)


# initialize points list
points = []

# Generate X random points form user input
current_time = int(time.time())
np.random.seed(current_time)
num_of_points = int(input("How many points do you want to examine as per their Convex Hull? -> "))
x_values = []

for i in range(num_of_points):
    x = random.randint(-100,100)        # random coordinates for the points
    if i == 1:
        x_values.append(x)
    else:
        if x in x_values:               # if the new point has x-coordinate that already exists, repeat the number generation
            continue
    y = random.randint(-100,100)
    point = x,y
    points.append(point)

print("\n-------------------------Initial 2D points-------------------------\n")
print(np.array(points))

points.sort()
print("\n-------------------------Sorted 2D points-------------------------\n")
print(np.array(points))

start_time = time.time()
left_point = points[0]
# create a helper list of the points, to plot later
points_for_plot = points[:]
# popping out 1st and last (n-th) points because they must be included in the convex hull from scratch
points.pop(0)
right_point = points[len(points)-1]
points.pop(len(points)-1)

hull = []
if (len(points) == 0):
    # If there are no points, add the left and right points to the hull
    hull.append(left_point)
    hull.append(right_point)
elif (len(points) == 1):
    # If there is only one point, add the left, right and the point to the hull
    hull.append(left_point)
    hull.append(right_point)
    hull.append(points[0])
elif (len(points) > 1):
    # If there are more than one points, add the left and right points to the hull
    hull.append(left_point)
    hull.append(right_point)

    # Divide points into 2 areas, namely the upper area (left_point) and the lower area (right_point)
    lefts = []
    rights = []
    for point in points:
        if (Determinant(left_point, right_point, point) > 0):
            lefts.append(point)
        elif (Determinant(left_point, right_point, point) < 0):
            rights.append(point)

    LeftHull = []
    RightHull = []

    # Search for the upper Convex Hull
    if (len(lefts) > 0):
        Far_Left_Point = Farthest_Point(left_point, right_point, lefts)
        Delete_Point(left_point, right_point, Far_Left_Point, lefts)
        LeftHull = QuickHull(left_point, Far_Left_Point, right_point, lefts)

    # Search for the lower Convex Hull
    if (len(rights) > 0):
        Far_Right_Point = Farthest_Point(left_point, right_point, rights)
        Delete_Point(right_point, left_point, Far_Right_Point, rights)
        RightHull = QuickHull(right_point, Far_Right_Point, left_point, rights)

    hull = hull + LeftHull + RightHull

final_hull = []
final_hull = SortHull(hull)
finish_time = time.time()

print("\n-------------------------Convex Hull Points-------------------------\n")
print(np.array(final_hull)[:-1])

# elapsed time
print("\nElapsed calculation time: ", "{:.8f}".format(finish_time - start_time), "seconds")

# points that are on the convex hull
x_hull = []
y_hull = []
for i in range(len(final_hull)) :
    x_hull.append(final_hull[i][0])
    y_hull.append(final_hull[i][1])

# all points in general
x_point = []
y_point = []
for i in range(len(points_for_plot)):
    x_point.append(points_for_plot[i][0])
    y_point.append(points_for_plot[i][1])

# print all points and the convex hull
plt.scatter(x_point, y_point, color="blue")
for i in range(len(points_for_plot)):
    plt.text(x_point[i], y_point[i], str(i+1), fontsize=12)
plt.plot(x_hull, y_hull, color="red")
plt.scatter(x_hull, y_hull, color="blue")
plt.title("Quick Hull Algorithm for Convex Hull")
plt.ylabel("Y")
plt.xlabel("X")
plt.show()