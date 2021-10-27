import matplotlib.pyplot as plt
import numpy as np

#####################################################


def free_SEAMCAT(d, f, Hb, Hm):

	return 32.4 + 20*np.log10(f) + 10*np.log10(d**2 + ((Hb-Hm)**2)/1e6)


def okumura_SEAMCAT(d, f, Hb, Hm):
	# THIS IS FOR URBAN AND A FREQUENCY BETWEEN 2K AND 3K (OUR CASE)
	# SEAMCAT VERSION FOR 2000 < f < 3000
	alpha = 1
	if(d <= 20):
		alpha = 1
	elif(20 < d and d < 100 ):
		alpha = 1+(0.14+1.87*1e-4*f+1.07*1e-3*Hb)*(np.log10(d/20))**0.8


	if (d < 0.04):
		return free_SEAMCAT(d, f, Hb, Hm)
	elif (0.04 <= d and d < 0.1):
		return free_SEAMCAT(0.04, f, Hb, Hm) + ((np.log10(d)-np.log10(0.04))/(np.log10(0.1)-np.log10(0.04))) * (free_SEAMCAT(0.1, f, Hb, Hm)-free_SEAMCAT(0.04, f, Hb, Hm)) 
	elif (d >= 0.1):
		aHm = (1.1*np.log10(f)-0.7)*min(10,Hm)-(1.56*np.log10(f)-0.8)+max(0,20*np.log10(Hm/10))
		bHb = min(0, 20*np.log10(Hb/30))

		return 46.3 + 33.9*np.log10(2000) + 10*np.log10(f/2000) - 13.82*np.log10(max(30,Hb))+(44.9-6.55*np.log10(max(30,Hb)))*np.log10(d)**alpha - aHm - bHb


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
			CFH = 8.29 * (np.log10(1.54*Hm))**2 - 1.1 #correction
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
			CFH = 8.29 * (np.log10(1.54*Hm))**2 - 1.1
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
	    "Po": 20, #23 #20
	    "Go": 2,
	    "Gi": 2,
	    "Pr": -76 #71 #76
	}

	f = 2400
	large = False
	Hb = 30 #3
	Hm = 1.5 #0.5

	x = np.array([i/1000 for i in range(1, 1200)])
	
	y_pl = [cost231(i, f, large, Hb, Hm) for i in x]
	y_pl_o = [okumura_pl_db(i, f, large, Hb, Hm) for i in x]
	y_pl_f = [free_pl_dbm(i, f) for i in x]

	# y_pl = [okumura_SEAMCAT(i, f, Hb, Hm) for i in x]
	# y_pl = [free_SEAMCAT(i, f, Hb, Hm) for i in x]

	y_pow = [power_cost_w(y_pl[x.tolist().index(i)], router) for i in x]
	y_pow_o = [power_cost_w(y_pl_o[x.tolist().index(i)], router) for i in x]
	y_pow_f = [power_cost_w(y_pl_f[x.tolist().index(i)], router) for i in x]
	# print(y_pow)
	limit_pl = limitPL(router) 
	maxpl, maxdist = max_pl_and_dist(y_pl, x, limit_pl)
	maxpl_o, maxdist_o = max_pl_and_dist(y_pl_o, x, limit_pl)
	maxpl_f, maxdist_f = max_pl_and_dist(y_pl_f, x, limit_pl)
	
	maxpower = power_cost_w(maxpl, router)
	maxpower_o = power_cost_w(maxpl_o, router)
	maxpower_f = power_cost_w(maxpl_f, router)

	print("Path Loss Limit dB  ->", limit_pl)
	print("Max path loss in dB ->", maxpl)
	print("Max Dist in Km      ->", maxdist)
	print("Max power cost in W ->", maxpower)

	fig, (axs1, axs2) = plt.subplots(2)
	axs1.plot(x, y_pl)
	axs1.plot(x, y_pl_o)
	axs1.plot(x, y_pl_f)
	axs1.plot(maxdist, maxpl, color='r', marker='o')
	axs1.plot(maxdist_o, maxpl_o, color='r', marker='o')
	axs1.plot(maxdist_f, maxpl_f, color='r', marker='o')
	axs1.text(maxdist-0.1, maxpl+4, '({}, {})'.format(round(maxdist, 4), round(maxpl, 1)))
	axs1.text(maxdist_o, maxpl_o-6, '({}, {})'.format(round(maxdist_o, 4), round(maxpl_o, 1)))
	axs1.text(maxdist_f, maxpl_f-6, '({}, {})'.format(round(maxdist_f, 4), round(maxpl_f, 1)))	
	axs1.set_title("Distance vs Path Loss")
	axs1.set_xlabel("Distance (Km)")
	axs1.set_ylabel("PL (dB)")
	axs1.legend(['Cost231', 'Okumura-Hata', 'FPL'])      
	axs2.plot(x, y_pow)
	axs2.plot(x, y_pow_o)
	axs2.plot(x, y_pow_f)
	axs2.plot(maxdist, maxpower, color='r', marker='o')
	axs2.plot(maxdist_o, maxpower_o, color='r', marker='o')
	axs2.plot(maxdist_f, maxpower_f, color='r', marker='o')
	axs2.text(maxdist-0.1, maxpower+100, '({},\n {})'.format(round(maxdist, 4), round(maxpower, 1)))
	axs2.text(maxdist_o, maxpower_o+100, '({},\n {})'.format(round(maxdist_o, 4), round(maxpower_o, 1)))
	axs2.text(maxdist_f, maxpower_f+100, '({}, {})'.format(round(maxdist_f, 4), round(maxpower_f, 1)))	
	axs2.set_title("Distance vs Power Cost")
	axs2.set_xlabel("Distance (Km)")
	axs2.set_ylabel("Power (W)")
	axs2.legend(['Cost231', 'Okumura-Hata', 'FPL'])   

	plt.show()

main()
