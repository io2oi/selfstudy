import scipy.stats as sp
import numpy as np

def calOR(ct: np.array) -> float:
    res = (ct[0,0]*ct[1,1])/(ct[0,1]*ct[1,0])
    if np.isinf(res):
        res = np.inf
    return res

def chi_test(ct: np.array) -> float:
    res = sp.chi2_contingency(ct)
    return res[1]


if __name__ == "__main__":
    obs = np.array([[5, 15], [10, 20]])
    obs2 = np.array([[1000,99990],[0,10]])
    for ct in [obs, obs2]:
        o_ratio = calOR(ct)
        chi_p = chi_test(ct)
        print(f"table: {ct}, OR: {o_ratio: .2f}, p-val: {chi_p: .2f}")
