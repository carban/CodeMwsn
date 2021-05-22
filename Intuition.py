N = n
f = 1
RE = np.ones((F+1, N))
RE[0] = actualEnergies
costs = np.ones((N))
vDistances = np.ones((N))

while(not death):
	vDistances
	vCosts = funCost(vDistances)
	RE[f+1] = RE[f]-(vCosts*MX[f])
	# Validar si hay un nodo por debajo del umbral
	if (f == F):
		solution.S = S
		solution.B = S[F]
		MX = solution.solve()

		S[0] = S[F]
		f = 0
	else:
		f += 1

##################solve########################33333

C = np.ones((F, N))
MX = np.ones((F, N))

for f in range(F):
    C[f] = (S[f]-S[f+1])/X_bef[f]

for f in range(F):
	solution = model(N, Di, Bi, Ci[f])
	MX.add(solution.x)
	Bi = solution.Bi

return MX 