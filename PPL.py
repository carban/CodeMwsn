import matplotlib.pyplot as plt
import numpy as np

class PPL():
	"""docstring for PPL"""
	def __init__(self, router, f, large=None, Hb=None, Hm=None, PLMODEL="cost231"):
		self.router = router
		self.f = f
		self.large = large
		self.Hb = Hb
		self.Hm = Hm
		self.PLMODEL = PLMODEL
		
	#####################################################

	# FREE PATH LOSS
	def free_pl_dbm(self, d):
	    # return 20.0*math.log(d, 10)+20.0*math.log(f, 10)+20*math.log((4*math.pi)/light, 10)
	    return 20.0*np.log10(d)+20.0*np.log10(self.f)+32.44

	# OKUMURA TYPICAL URBAN PATHLOSS
	# HATA
	def okumura_pl_db(self, d):

		f = self.f
		large = self.large
		Hb = self.Hb
		Hm = self.Hm

		# For large cities 
		if (large):
			if (f >= 150 and f <= 200):
				CFH = 8.29 * (np.log10(1.54*Hm))**2 - 1.1
			elif (f >= 200): # <= 1500
				CFH = 3.2 * (np.log10(11.75*Hm))**2 - 4.97
		# For small and medium-sized cities 
		else:
			CFH = (1.1*np.log10(f)-0.7)*Hm - (1.56*np.log10(f)-0.8)

		return 69.55 + 26.16*np.log10(f) + (44.9-6.55*np.log10(Hb))*np.log10(d) - 13.82*np.log10(Hb) - CFH

	# YOUNG MODEL
	## ------------------------------------------------------


	# COST 231 MODEL | COST HATA MODEL
	def cost231(self, d):

		f = self.f
		large = self.large
		Hb = self.Hb
		Hm = self.Hm

		# For large cities 
		if (large):
			Cm = 3 # Constant Offset in dB
			if (f >= 150 and f <= 200):
				CFH = 8.29 * (np.log10(1.54*Hm))**2 - 1.1 #8.9 and 11
			elif (f >= 200): # <= 1500
				CFH = 3.2 * (np.log10(11.75*Hm))**2 - 4.97
		# For small and medium-sized cities 
		else:
			Cm = 0
			CFH = (1.1*np.log10(f)-0.7)*Hm - (1.56*np.log10(f)-0.8)

		return 46.3 + 33.9*np.log10(f) - 13.82*np.log10(Hb) - CFH + (44.9-6.55*np.log10(Hb))*np.log10(d) + Cm



	##########################################################################################################

	def free_SEAMCAT(self, d):

		f = self.f
		Hb = self.Hb
		Hm = self.Hm

		return 32.4 + 20*np.log10(f) + 10*np.log10(d**2 + ((Hb-Hm)**2)/1e6)

		# *****************

	def cost_SEAMCAT_1500(self, d):

		f = self.f
		Hb = self.Hb
		Hm = self.Hm

		alpha = 1
		if(d <= 20):
			alpha = 1
		elif(20 < d and d < 100 ):
			alpha = 1+(0.14+1.87*1e-4*f+1.07*1e-3*Hb)*(np.log10(d/20))**0.8

		aHm = (1.1*np.log10(f)-0.7)*min(10,Hm)-(1.56*np.log10(f)-0.8)+max(0,20*np.log10(Hm/10))
		bHb = min(0, 20*np.log10(Hb/30))

		return 69.6 + 26.2*np.log10(f) - 13.82*np.log10(max(30,Hb))+(44.9-6.55*np.log10(max(30,Hb)))*np.log10(d)**alpha - aHm - bHb

		# ******************88

	def cost_SEAMCAT_2000(self, d):

		f = self.f
		Hb = self.Hb
		Hm = self.Hm

		alpha = 1
		if(d <= 20):
			alpha = 1
		elif(20 < d and d < 100 ):
			alpha = 1+(0.14+1.87*1e-4*f+1.07*1e-3*Hb)*(np.log10(d/20))**0.8

		aHm = (1.1*np.log10(f)-0.7)*min(10,Hm)-(1.56*np.log10(f)-0.8)+max(0,20*np.log10(Hm/10))
		bHb = min(0, 20*np.log10(Hb/30))

		return 46.3 + 33.9*np.log10(f) - 13.82*np.log10(max(30,Hb))+(44.9-6.55*np.log10(max(30,Hb)))*np.log10(d)**alpha - aHm - bHb

		# ******************88

	def cost_SEAMCAT(self, d):

		f = self.f
		Hb = self.Hb
		Hm = self.Hm

		alpha = 1
		if(d <= 20):
			alpha = 1
		elif(20 < d and d < 100 ):
			alpha = 1+(0.14+1.87*1e-4*f+1.07*1e-3*Hb)*(np.log10(d/20))**0.8

		aHm = (1.1*np.log10(f)-0.7)*min(10,Hm)-(1.56*np.log10(f)-0.8)+max(0,20*np.log10(Hm/10))
		bHb = min(0, 20*np.log10(Hb/30))

		return 46.3 + 33.9*np.log10(2000) + 10*np.log10(f/2000) - 13.82*np.log10(max(30,Hb))+(44.9-6.55*np.log10(max(30,Hb)))*np.log10(d)**alpha - aHm - bHb

		# ******************88

	def extended(self, d):
		# THIS IS FOR URBAN AND A FREQUENCY BETWEEN 1.5K AND 3K (OUR CASE)

		f = self.f

		if (d < 0.04):
			return self.free_SEAMCAT(d)
		elif (0.04 <= d and d < 0.1):
			costL01 = 0
			if (150 < f and f <= 1500):
				costL01 = self.cost_SEAMCAT_1500(0.1)
			elif (1500 < f and f <= 2000):
				costL01 = self.cost_SEAMCAT_2000(0.1)
			elif (2000 < f and f <= 3000):
				costL01 = self.cost_SEAMCAT(0.1)
			return self.free_SEAMCAT(0.04) + ((np.log10(d)-np.log10(0.04))/(np.log10(0.1)-np.log10(0.04))) * (costL01-self.free_SEAMCAT(0.04)) 
		elif (d >= 0.1):
			if (150 < f and f <= 1500):
				return self.cost_SEAMCAT_1500(d)
			elif (1500 < f and f <= 2000):
				return self.cost_SEAMCAT_2000(d)
			elif (2000 < f and f <= 3000):
				return self.cost_SEAMCAT(d)


	##########################################################################################################
	def dbm_to_mw(self, db):
	    return 10.0**(db/10.0)

	def mw_to_w(self, mw):
	    return mw / 1000

	def power_cost_w(self, Pl):

		router = self.router

		Po = router["Pr"] + Pl - router["Go"] - router["Gi"]
		return self.mw_to_w(self.dbm_to_mw(Po))

	def power_cost_w_given_d(self, d):
		name = self.PLMODEL
		if (name == "free"):
			pl = self.free_pl_dbm(d)
		elif (name == "okumura"):
			pl = self.okumura_pl_db(d)
		elif (name == "cost231"):
			pl = self.cost231(d)
		elif (name == "extended"):
			pl = self.extended(d)

		return self.power_cost_w(pl)

	def limitPL(self):
		router = self.router
		return router["Po"] + router["Go"] + router["Gi"] - router["Pr"]	

	def max_pl_and_dist(self, y_pl, x, limit_pl):
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

	def get_max_dist(self):
		x = np.array([i/1000 for i in range(1, 3600)])

		name = self.PLMODEL

		if (name == "free"):
			y_pl = [self.free_pl_dbm(i) for i in x]
		elif (name == "okumura"):
			y_pl = [self.okumura_pl_db(i) for i in x]
		elif (name == "cost231"):
			y_pl = [self.cost231(i) for i in x]
		elif (name == "extended"):
			y_pl = [self.extended(i) for i in x]

		maxpl, maxdist = self.max_pl_and_dist(y_pl, x, self.limitPL())

		return maxdist * 1000 # meters unit