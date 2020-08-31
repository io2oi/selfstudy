from multiprocessing import Pool
import time

def run_withpool(worker, data: list, num_threads: int) -> list:
    res = list()
    with Pool(num_threads) as pool_handle:
        res = pool_handle.map(worker, data)
    return res

def worker(arg1):
    time.sleep(5)
    res = arg1 + 1
    return res

def main():
    n_thr = 3
    input = list(range(6))
    output = run_withpool(worker, input, n_thr)
    print(output)
    
if __name__=="__main__":
    main()
