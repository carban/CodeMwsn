import matplotlib.pyplot as plt
import numpy as np

#####################################################

# FREE PATH LOSS
def free_pl_dbm(d, f):
    # return 20.0*math.log(d, 10)+20.0*math.log(f, 10)+20*math.log((4*math.pi)/light, 10)
    return 20.0*np.log10(d)+20.0*np.log10(f)+32.44

# OKUMURA TYPICAL URBAN PATHLOSS
# HATA
# Low level = 1500 OKUMURA
# I use 2400 because YOLO
# Low level = 1920 HATA
# I use 2400 because YOLO
def okumura_pl_db(d, f, large, Hb, Hm):

	# For large cities 
	if (large):
		if (f >= 150 and f <= 200):
			CFH = 8.9 * (np.log10(1.54*Hm))**2 - 11
		elif (f >= 200): # <= 1500
			CFH = 3.2 * (np.log10(11.75*Hm))**2 - 4.97
	# For small and medium-sized cities 
	else:
		CFH = (1.1*np.log10(f)-0.7)*Hm - (1.56*np.log10(f)-0.8)

	return 69.55 + 26.16*np.log10(f) + (44.9-6.55*np.log10(Hb))*np.log10(d) - 13.82*np.log10(Hb) - CFH

# YOUNG MODEL
## ------------------------------------------------------


# COST 231 MODEL | COST HATA MODEL
def cost231(d, f, large, Hb, Hm):

	# For large cities 
	if (large):
		Cm = 0 # Constant Offset in dB
		if (f >= 150 and f <= 200):
			CFH = 8.9 * (np.log10(1.54*Hm))**2 - 11
		elif (f >= 200): # <= 1500
			CFH = 3.2 * (np.log10(11.75*Hm))**2 - 4.97
	# For small and medium-sized cities 
	else:
		Cm = 3
		CFH = (1.1*np.log10(f)-0.7)*Hm - (1.56*np.log10(f)-0.8)

	return 46.3 + 33.9*np.log10(f) - 13.82*np.log10(Hb) - CFH + (44.9-6.55*np.log10(Hb))*np.log10(d) + Cm



#####################################################
def dbm_to_mw(db):
    return 10.0**(db/10.0)

def mw_to_w(mw):
    return mw / 1000

def power_cost_w(Pl, router):
	Po = router["Pr"] + Pl - router["Go"] - router["Gi"]
	return mw_to_w(dbm_to_mw(Po))

def limitPL(router):
    return router["Po"] + router["Go"] + router["Gi"] - router["Pr"]	

def max_pl_and_dist(y_pl, x, limit_pl):
	maxdist = 0
	maxpl = 0
	for pls in y_pl:
		# print(pls)
		if (pls >= limit_pl):
			maxpos = y_pl.index(pls)
			maxpl = pls
			maxdist = x[maxpos]
			break
	return maxpl, maxdist

# 2200 -> 101 max pl -> d = 0.09
# 5000 -> 98 max pl

def main():

	router = {
	    "Po": 23,
	    "Go": 2,
	    "Gi": 2,
	    "Pr": -71
	}

	f = 5000
	large = True
	Hb = 3
	Hm = 0.5

	x = np.array([i/1000 for i in range(1, 1000)])
	
	y_pl = [cost231(i, f, large, Hb, Hm) for i in x]
	# y_pl = [okumura_pl_db(i, f, large, Hb, Hm) for i in x]
	# y_pl = [free_pl_dbm(i, f) for i in x]

	y_pow = [power_cost_w(y_pl[x.tolist().index(i)], router) for i in x]
	# print(y_pow)
	limit_pl = limitPL(router) 
	maxpl, maxdist = max_pl_and_dist(y_pl, x, limit_pl)
	maxpower = power_cost_w(maxpl, router)

	print("Path Loss Limit dB  ->", limit_pl)
	print("Max path loss in dB ->", maxpl)
	print("Max Dist in Km      ->", maxdist)
	print("Max power cost in W ->", maxpower)

	fig, (axs1, axs2) = plt.subplots(2)
	axs1.plot(x, y_pl)
	axs1.plot(maxdist, maxpl, color='r', marker='o')
	axs1.set_title("Distance vs Path Loss")
	axs1.set_xlabel("Distance (Km)")
	axs1.set_ylabel("PL (dBm)")      
	axs2.plot(x, y_pow)
	axs2.plot(maxdist, maxpower, color='r', marker='o')
	axs2.set_title("Distance vs Power Cost")
	axs2.set_xlabel("Distance (Km)")
	axs2.set_ylabel("Power (W)")   

	plt.show()

main()
