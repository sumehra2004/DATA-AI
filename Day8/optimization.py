from multiprocessing import Pool
import time
def work(n):
    return n+n
if __name__ == "__main__":
    start = time.time()

    with Pool() as pool:              # uses number of CPU cores by default
        results = pool.map(work, range(10**6))
    end = time.time()