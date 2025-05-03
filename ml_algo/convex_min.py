import math
def gradient_descent_list(f, grad_f, x_init, learning_rate=0.01, tolerance=1e-6, max_iter=1000):
    x = x_init[:]
    lr = learning_rate
    for _ in range(max_iter):
        grad = grad_f(x)
        x_new = [x[i] - lr * grad[i] for i in range(len(x))]
        diff = [x_new[i] - x[i] for i in range(len(x))]
        if math.sqrt(sum(d*d for d in diff)) < tolerance:
            break
        x = x_new
    return x


def gradient_descent_single(f, grad_f, x_init, learning_rate=0.01, tolerance=1e-6, max_iter=1000):
    x = x_init
    lr = learning_rate
    for _ in range(max_iter):
        grad = grad_f(x)
        x_new = x - lr * grad
        if abs(f(x_new) - f(x)) < tolerance:
            break
        x = x_new
    return x