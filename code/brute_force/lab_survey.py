"""Reproducible survey behind Section 6.2 ("Observations in other sieves").
Random sieves: the prime 2 followed by k in {5,...,8} distinct primes from 3..37 in random
order, with modulus <= 3*10^7. For each sieve and stage: birth law (set version),
missing differences, shadows, persistent holes, missing differences caused by blocked births.
Fixed seed 77 and a fixed number of sieves (3689) make the run deterministic.
Usage: python lab_survey.py [number_of_sieves]"""
import random, sys
from math import prod
from lab import badaj

def main(n_sieves=3689, seed=77):
    random.seed(seed)
    POOL = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    done = law = missing = shadows = 0
    persistent = []; blocked = []
    while done < n_sieves:
        k = random.randint(5, 8); S = random.sample(POOL, k)
        if prod(S) * 2 > 3 * 10**7:
            continue
        w = badaj('', [2] + S); done += 1
        law += w['prawo_ok']; missing += len(w['brak']); shadows += len(w['cienie'])
        persistent += w['trwale']; blocked += w['zabojstwa']
    print("sieves: %d, birth law exact in: %d" % (done, law))
    print("missing differences: %d, of which shadows: %d" % (missing, shadows))
    print("persistent holes: %d, missing because of blocked births: %d" % (len(persistent), len(blocked)))

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3689)
