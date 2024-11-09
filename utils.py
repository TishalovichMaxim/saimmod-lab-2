from scipy import stats

def calc_t_crit(alpha: float, n: int):
    return stats.t.ppf(1 - alpha/2, n)

def calc_f_crit(alpha, dfn, dfd):
    return stats.f.ppf(q=1-alpha, dfn=dfn, dfd=dfd)

