import numpy as np
from numpy.linalg import eigvals

## in python3.6, range is xrange of python 2.x
def run_experiment(niter=100):
    K = 100
    results=[]
    for _ in range(niter):
        mat = np.random.randn(K,K)
        max_eigenvalue = np.abs(eigvals(mat)).max()
        results.append(max_eigenvalue)
    return results

if __name__=="__main__":
    some_results = run_experiment()
    print ('Largest one we saw: %s' % np.max(some_results))
