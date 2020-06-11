import scipy.stats as sp
import numpy as np
import pandas as pd

def calOR(ct: np.array) -> float:
    res = (ct[0,0]*ct[1,1])/(ct[0,1]*ct[1,0])
    if np.isinf(res):
        res = np.inf
    return res

def chi_test(ct: np.array) -> float:
    res = sp.chi2_contingency(ct)
    return res[1]

def fisher_test(ct: np.array) -> float:
    res = sp.fisher_exact(ct)
    return res[1]


if __name__ == "__main__":
    """
    contingency table
         | 3bil  | gnomad |
    alt  |   a   |    c   |
    ref  |  b    |    d   |

    """    
    # obs = np.array([[5, 15], [10, 20]])
    container = []
    for C, D in zip((10000,1), (1, 10000)):
        B = 0
        for a in range(1,11):
            ct = np.array([[a, C],[B, D]])
            o_ratio = calOR(ct)
            chi_p = chi_test(ct)
            fis_p = fisher_test(ct)
            print(f"Cont. Table:")
            print(f"A: {a}, C: {C}", end=" ")
            print(f"{o_ratio: .2f}, {chi_p: .2e}, {fis_p: .2e}")
            container.append([ct[0,0], ct[1,0], ct[0, 1], ct[1, 1], o_ratio, chi_p, fis_p])
    for C, D in zip((10000,1), (1, 10000)):
        B = 0
        for a in range(30, 1000, 50):
            ct = np.array([[a, C],[B, D]])
            o_ratio = calOR(ct)
            chi_p = chi_test(ct)
            fis_p = fisher_test(ct)
            print(f"Cont. Table:")
            print(f"A: {a}, C: {C}", end=" ")
            print(f"{o_ratio: .2f}, {chi_p: .2e}, {fis_p: .2e}")
            container.append([ct[0,0], ct[1,0], ct[0, 1], ct[1, 1], o_ratio, chi_p, fis_p])

    df = pd.DataFrame(container, columns = ["a", "b", "c", "d", "OR", "chi_p", "fisher_p"])
    print(f"{df}")
    

