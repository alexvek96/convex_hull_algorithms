# Incremental (Graham's Scan) algorithm in 2D with live plotting

import time                                     # for computation timing
import numpy as np                              # for random number generation and math calculations
import matplotlib.pyplot as plt                 # for plotting
from matplotlib.animation import FuncAnimation  # for live animation
from matplotlib.widgets import Button           # for Pause/Resume Button to interact with the user in a better way

print("\n------------------------------------------------------------------------------------")
print("           Incremental (Graham's Scan) algorithm in 2D, with live plotting            ")
print("------------------------------------------------------------------------------------\n")

# Define a global variable to store the previous hull
prev_hull = np.empty((0, 2))

# variable that stores the total time that we pause the plot animation (=the calculation fo the algorithm)
# this pausing time must be ignored from the overall calculation time, because it is "false additional" time
overall_stop_time = 0

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


#   Function to compute the convex hull of a set of points using Graham's Scan (Incremental) algorithm
def graham_scan(points):
    """
    Returns:
        List of points in the convex hull in CCW order
    """
    if len(points) < 3:
        return []

    # Compute the upper hull
    upper_hull = []
    for p in points:
        while len(upper_hull) >= 2 and orientation(upper_hull[-2], upper_hull[-1], p) == -1:
            upper_hull.pop()  # Pop points that do not make a CCW turn
        upper_hull.append(p)  # Push the current point onto the upper hull


    # Compute the lower hull
    lower_hull = []
    for p in reversed(points):
        while len(lower_hull) >= 2 and orientation(lower_hull[-2], lower_hull[-1], p) == -1:
            lower_hull.pop()  # Pop points that do not make a CCW turn
        lower_hull.append(p)  # Push the current point onto the lower hull

    # Merge the upper and lower hulls to obtain the final convex hull
    convex_hull = upper_hull[:-1] + lower_hull[:-1]
    return convex_hull


# Generate X random points form user input
current_time = int(time.time())
np.random.seed(current_time)
num_of_points = int(input("How many points do you want to examine as per their Convex Hull? -> "))
points = np.random.rand(num_of_points, 2)
start_time = time.time()
points = lexicographic_sort(points)


# Set up the figure and axis for animation
fig, ax = plt.subplots()
ax.set_title("Graham\'s Scan Algorithm for Convex Hull")
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
    global overall_stop_time
    global prev_hull
    plot_time_start = time.time()
    hull = np.array(graham_scan(points[:i + 2]))  # Convert the hull list to a numpy array
    if len(hull) > 0:  # Check to ensure hull array is not empty
        # Update the plot with the convex hull
        line.set_data(np.append(hull[:, 0], hull[0, 0]), np.append(hull[:, 1], hull[0, 1]))
        # Check if the hull is the same as the previous hull
        if np.array_equal(hull, prev_hull):
            ani.event_source.stop()  # Stop the animation
        else:
            prev_hull = hull.copy()  # Update the previous hull
    if i == num_of_points - 1:
        finish_time = time.time()
        print('\n-------------------------Convex Hull Points-------------------------\n', hull)
        print("\nElapsed calculation time: ", finish_time - start_time - overall_stop_time, "seconds")
    plot_time_end = time.time()
    return [scatter, line]


# Create the animation
ani = FuncAnimation(fig, update, frames=len(points), interval=500, blit=True)

# Pause/Resume Button
axpause = plt.axes([0.7, 0.05, 0.1, 0.075])
btn_pause = Button(axpause, 'Pause', color='lightgrey', hovercolor='lightblue')

# Boolean variable to keep track of animation status
is_animation_running = True

# Function to pause/unpause the animation
def pause_animation(event):
    global stop_time_begin
    global is_animation_running
    if is_animation_running:
        ani.event_source.stop()
        stop_time_begin = time.time()
        btn_pause.color = 'lightblue'
    else:
        global stop_time_end
        global overall_stop_time
        ani.event_source.start()
        stop_time_end = time.time()
        overall_stop_time = overall_stop_time + stop_time_end - stop_time_begin
        btn_pause.color = 'lightgrey'
    is_animation_running = not is_animation_running

btn_pause.on_clicked(pause_animation)

plt.show()