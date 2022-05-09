import multiprocessing as mp
import sys

def func(x):
    x = x **2
    return x

def main():
    cpus = mp.cpu_count()
    with mp.Pool(cpus) as pool:
        results = pool.map(func, range(1,50))
    print(results)

if __name__ == '__main__':
    main()
    