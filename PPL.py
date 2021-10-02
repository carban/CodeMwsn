import matplotlib.pyplot as plt
import numpy as np

class PPL():
	"""docstring for PPL"""
	def __init__(self, router, f, large=None, Hb=None, Hm=None):
		self.router = router
		self.f = f
		self.large = large
		self.Hb = Hb
		self.Hm = Hm
		
	#####################################################

	# FREE PATH LOSS
	def free_pl_dbm(self, d):
	    # return 20.0*math.log(d, 10)+20.0*math.log(f, 10)+20*math.log((4*math.pi)/light, 10)
	    return 20.0*np.log10(d)+20.0*np.log10(self.f)+32.44

	# OKUMURA TYPICAL URBAN PATHLOSS
	# HATA
	# Low level = 1500 OKUMURA
	# I use 2400 because YOLO
	# Low level = 1920 HATA
	# I use 2400 because YOLO
	def okumura_pl_db(self, d):

		f = self.f
		large = self.large
		Hb = self.Hb
		Hm = self.Hm

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
	def cost231(self, d):

		f = self.f
		large = self.large
		Hb = self.Hb
		Hm = self.Hm

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
	def dbm_to_mw(self, db):
	    return 10.0**(db/10.0)

	def mw_to_w(self, mw):
	    return mw / 1000

	def power_cost_w(self, Pl):

		router = self.router

		Po = router["Pr"] + Pl - router["Go"] - router["Gi"]
		return self.mw_to_w(self.dbm_to_mw(Po))

	def power_cost_w_given_d(self, d, path_loss_model_name):
		name = path_loss_model_name
		if (name == "free"):
			pl = self.free_pl_dbm(d)
		elif (name == "okumura"):
			pl = self.okumura_pl_db(d)
		elif (name == "cost231"):
			pl = self.cost231(d)

		return self.power_cost_w(pl)

	def limitPL(self, router):
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
