import matplotlib.pyplot as plt
import numpy as np
import math
import scipy.constants as const

light = const.speed_of_light

def pl_seamcat(d, f):
    return 32.44 + 10*math.log(d, 10)+20*math.log(f, 10)

def pl_mw(d, f):
    return ((math.pi*4.0*d*f)/light)**2

def pl_dbm(d, f):
    # return 20.0*math.log(d, 10)+20.0*math.log(f, 10)+20*math.log((4*math.pi)/light, 10)
    return 20.0*math.log(d, 10)+20.0*math.log(f, 10)+32.44

def dbm_to_mw(db):
    return 10.0**(db/10.0)

def mw_to_db(mw):
    return 10.0*math.log(mw, 10.0)

################################

def mw_to_w(mw):
    return mw / 1000

def power_cost_dbm(d, f):
    Po = 23
    Go = 2
    Gi = 2
    Pr = -71
    Pl = pl_dbm(f, d)
    Po = Pr + Pl - Go - Gi
    # Pr = Po + Go - Pl + Gi 
    return Po

def power_cost_w(d, f):
    Po = 23
    Go = 2
    Gi = 2
    Pr = -71
    Pl = pl_dbm(f, d)
    Po = Pr + Pl - Go - Gi
    return mw_to_w(dbm_to_mw(Po))

def main():
    f = 5e3 #Mhz
    d = 0.379 #Km
    print("mw:       ", pl_mw(d*1e3, f*1e6))
    print("dbm:      ", pl_dbm(d, f))
    print("mw->dbm:  ", mw_to_db(pl_mw(d*1e3, f*1e6)))
    print("dbm->mw:  ", dbm_to_mw(pl_dbm(d, f)))
    # print("Constant: ", 20*math.log((4*math.pi)/light, 10))

    # print(pl_db(0.377, f))

    x = np.array([i/100 for i in range(1, 100)])
    y = [power_cost_w(i, f) for i in x]
    plt.plot(x,y)   
    plt.plot(d, power_cost_w(d, f), color='red', marker='o')
    plt.show()
    print("--->", power_cost_w(d, f))


main()
