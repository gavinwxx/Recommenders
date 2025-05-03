
class StreamingStats:
    def __init__(self):
        self.count = 0
        self.mean = 0.0
        self.M2 = 0.0  # Sum of squares of differences from the current mean
    
    def update(self, x):
        self.count += 1
        delta = x - self.mean
        self.mean += delta / self.count
        delta2 = x - self.mean
        self.M2 += delta * delta2
    
    def get_mean(self):
        return self.mean if self.count else float('nan')

    def get_variance(self):
        return self.M2 / self.count if self.count else float('nan')

    def get_sample_variance(self):
        return self.M2 / (self.count - 1) if self.count > 1 else float('nan')
    
stats = StreamingStats()

# Simulate streaming data
import random
for _ in range(1000000):  # For example, 1 billion data points
    x = random.random()  # Replace with actual streaming data
    stats.update(x)

print("Mean:", stats.get_mean())
print("Population Variance:", stats.get_variance())
print("Sample Variance:", stats.get_sample_variance())