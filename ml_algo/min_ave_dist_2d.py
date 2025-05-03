from convex_min import gradient_descent_list
import math
import termchart
def ave_dist(pt, data):
    x, y = pt
    total = 0.0
    for xi, yi in data:
        dx,dy = x - xi, y - yi
        dist = math.sqrt(dx*dx +dy*dy)
        total += dist
    return total/len(data)

def gradient(pt, data, epsilon=1e-8):
    x,y = pt
    grad_x, grad_y = 0.0, 0.0
    for xi, yi in data:
        dx, dy = x - xi, y - yi
        dist = math.sqrt(dx * dx + dy * dy) + epsilon
        grad_x += dx / dist
        grad_y += dy / dist
    n = len(data)
    return [grad_x/n, grad_y/n]


# Sample data points
data_points = [
    [1.0, 2.0],
    [3.0, 4.0],
    [5.0, 0.0],
    [2.0, 1.0]
]

# Initial guess (e.g., centroid)
initial_point = [
    sum(p[0] for p in data_points) / len(data_points),
    sum(p[1] for p in data_points) / len(data_points)
]

# Find the point minimizing average distance
optimal_point = gradient_descent_list(
    f=lambda p: ave_dist(p, data_points),
    grad_f=lambda p: gradient(p, data_points),
    x_init=initial_point,
    learning_rate=0.1,
    tolerance=1e-6,
    max_iter=1000
)

print("Optimal Point:", optimal_point)
# Create a graph object
graph = termchart.Graph(data_points)

# Draw the graph
graph.draw()