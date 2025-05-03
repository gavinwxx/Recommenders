import random

def biased_coin(p):
    return 1 if random.random() < p else 0

def von_neumann_extractor(p):
    """
    This function uses the von Neumann extractor to generate a fair coin flip
    from a biased coin with probability p of landing heads.
    """
    while True:
        flip1 = biased_coin(p)
        flip2 = biased_coin(p)
        if flip1 != flip2:
            return flip1
        # If both flips are the same (00 or 11), discard and repeat
    
bias = 0.8

unbiased_bits = [von_neumann_extractor(bias) for _ in range(20)]
print("Unbiased bits generated from biased coin flips:", unbiased_bits)
