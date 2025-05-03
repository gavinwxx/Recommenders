
def welford(data_stream):
    """
    Welford's method for calculating the mean and variance in a single pass.
    
    Parameters:
    data_stream (iterable): An iterable stream of numerical data.
    
    Returns:
    tuple: A tuple containing the mean and variance of the data stream.
    """
    n = 0
    mean = 0.0
    M2 = 0.0 # accumulator that keeps track of the running total of square differences between each data point and the mean

    for x in data_stream:
        n += 1
        delta = x - mean
        mean += delta / n
        delta2 = x - mean
        M2 += delta * delta2

    if n < 2:
        return mean, float('nan')  # Variance is undefined for n < 2
    else:
        variance = M2 / n # Population variance
        sample_variance = M2 / (n - 1)  # Sample variance
        return mean, variance,sample_variance