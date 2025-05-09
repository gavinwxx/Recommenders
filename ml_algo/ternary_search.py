




def ternary_search(f, left, right, eps=1e-9):
    while right - left > eps:
        m1 = left + (right-left) / 3
        m2 = right - (right - left) / 3
        if f(m1) < f(m2):
            right = m2
        else:
            left = m1
    return (left + right) / 2