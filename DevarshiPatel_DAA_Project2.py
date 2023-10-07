from functools import cmp_to_key
from collections import namedtuple
import time
import random

# A Point class using namedtuple.
# It automatically provides with attributes x and y, and create Point objects just like regular class instances.
start = time.time_ns()
Point = namedtuple("Point", ["x", "y"])

# defining p0 as a referance Point instance with coordinates (0, 0).
p0 = Point(0, 0)

# Function to find next to top in a stack
# checks whether the stack has at least two elements before trying to access the second-to-last element. This helps prevent potential IndexError exceptions when the stack is empty or contains only one element.
def nextPoint(S):
    if len(S) >= 2:
        return S[-2]
    else:
        return None 

# Function to find the square of the distance between p1 and p2 using the power operator.
def distSq(p1, p2):
    return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2
# the compare function determines the order of points based on their orientation with respect to a reference point p0.
def compare(p1, p2):
    o = orientation(p0, p1, p2)
    
    if o == 0:
        distance1 = distSq(p0, p2)
        distance2 = distSq(p0, p1)
        return -1 if distance1 >= distance2 else 1
    elif o == 2:
        return -1
    else:
        return 1
# finds the bottommost point among a list of points based on their y coordinates, breaking ties with the x coordinate.
def find_bottommost_point(points):
    bottommost = points[0]
    for point in points[1:]:
        if point.y < bottommost.y or (point.y == bottommost.y and point.x < bottommost.x):
            bottommost = point
    return bottommost

# orientation of 3 ordered points in the plane by calculating the slopes of the line segments formed by the points. If the slopes are equal, then the points are collinear.
# If the slope of the line segment formed by the first two points is less than the slope of the line segment formed by the last two points, then the orientation is counter-clockwise, 
# otherwise it is clockwise.
def orientation(p, q, r):
    slope_value = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if slope_value == 0:
        return 0  # Collinear
    elif slope_value > 0:
        return 1  # Clockwise
    else:
        return 2  # Counterclockwise
def convexHull(points):
    n = len(points)
    # Locate the lowest point
    min_point = find_bottommost_point(points)

    # Place the bottom-most point at first position
    points[0], points[points.index(min_point)] = points[points.index(min_point)], points[0]

    #Sort the first point first among the n-1 points. 
    #If point p2 has a larger polar angle (in an anticlockwise orientation) than point p1, then p2 comes before p1 in the result after sorting.
    p0 = points[0]
    points = sorted(points, key=cmp_to_key(compare))

    # If two or more points make the same angle with p0,
    # Remove all but the one that is farthest from p0
    # Remember that, in the above sorting, our criteria was
    # to keep the farthest point at the end when more than
    # one point has the same angle.
    m = 1  # Initialize size of the modified array
    for i in range(1, n):
        # Keep removing i while the angle of i and i+1 is the same
        # with respect to p0
        while (i < n - 1) and (orientation(p0, points[i], points[i + 1]) == 0):
            i += 1
        points[m] = points[i]
        m += 1  # Update the size of the modified array

    # If the modified array of points has less than 3 points,
    # convex hull is not possible
    if m < 3:
        return

    # Create an empty stack and push the first three points to it
    S = []
    S.append(points[0])
    S.append(points[1])
    S.append(points[2])

    # Process remaining n-3 points
    for i in range(3, m):
        # Keep removing the top while the angle formed by
        # points next-to-top, top, and points[i] makes
        # a non-left turn
        while (len(S) > 1) and (orientation(nextPoint(S), S[-1], points[i]) != 2):
            S.pop()
        S.append(points[i])
    while S:
        p = S[-1]
        print(f"({p.x}, {p.y})")
        S.pop()

def random_points(m):
    points = []
    for _ in range(m):
        x = random.randint(1,100)
        y = random.randint(1,100)
        points.append(Point(x,y))
    return points

#Main
m = 100000
points = random_points(m)
convexHull(points)
#To measure the elapsed time or execution time of a block of code in nanoseconds, we can use the time.time_ns() function.
end = time.time_ns()
print("Time taken", end-start, "ns")




