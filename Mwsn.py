import subprocess
import json
import numpy as np
import math
import os
from scipy.interpolate import InterpolatedUnivariateSpline


class Mwsn:
    def __init__(self, K, F, N, Di, bi, ci, maxcost, time_slot_val, battery, solver):

        self.path_minizinc = "/home/carban/PortableApps/MiniZincIDE-2.4.3-bundle-linux-x86_64/bin/minizinc"
        self.path_model = "/home/carban/Documents/TG/CodeMwsn/CPM/Model6.mzn"
        
        self.K = K
        self.F = F
        self.N = N
        self.Di = Di
        self.bi = bi
        self.ci = ci
        self.maxcost = maxcost
        self.time_slot_val = time_slot_val
        self.battery = battery
        self.cf = []
        self.solver = solver

        self.S = np.ones((F+1, N))
        # self.S[0] = bi

        self.X = np.array([])
        self.X_bef = np.ones((F, N))

    def setBi(self, bi):
        self.bi = bi 

    def setCf(self, cf):
        self.cf = cf

    def setS(self, S):
        self.S = S

    def getLastS(self):
        return self.S[self.F]
    
    def formatAssignment(self, X):
        out = []
        for i in range(self.F):
            a = np.array([])
            for j in range(self.N):
                a = np.append(a, np.ones(int(X[i][j])) * j)
            
            a = [int(a[k]) for k in range(self.Di)]
            out.append(a)
        return out

    def compute(self):

        self.X = np.array([])

        # print(self.S)

        # Actual costs ----------------------------------------------------------------
        C = np.ones((self.F, self.N))
        
        for j in range(self.F):
            for k in range(self.N):
                if (self.X_bef[j][k] != 0):
                    C[j][k] = (self.S[j][k]-self.S[j+1][k])/(self.X_bef[j][k]*self.time_slot_val) # (Di * (S[j]-S[j+1]))/X[j]
                else:
                    # print"(dsfsdfsfsd", self.X_bef[j])
                    # print("***********", self.S[j][k], self.S[j+1][k])
                    # C[j][k] = (self.S[j][k]-self.S[j+1][k])
                    C[j][k] = self.maxcost

        # for i in range(self.F):
        #     C[i] = (self.S[i]-self.S[i+1])/(self.X_bef[i]*self.time_slot_val)

        self.ci = C.reshape(self.F, self.N)
        # print("Costs calculated", self.ci)
        self.ci = [self.ci[i].tolist() for i in range(self.F)]
        # ----------------------------------------------------------------------------------

        # Extrapolation ||||||||||||||||||||||

        if(False):
            Fext = self.F * 2
            xi = np.array([i/10 for i in range(1, self.F+1)])
            exc = np.array(self.ci)

            order = 2
            # continous_x = np.linspace(0, Fext/10, 30)

            for i in range(self.N):

                column = exc[:,i]

                # count how many real cost are there
                vali = column != self.maxcost
                print("valiii", vali)
                hmc = sum(vali)
                print("++++++>>>", hmc)

                if(hmc == 0 or hmc == 1):
                    exc[:,i] = column
                else:
                    if(hmc == 2):
                        order = 1
                    elif(hmc > 2):
                        order = 2

                    # vector sol with the max values
                    sol = [self.maxcost if not vali[j] else -1 for j in range(self.F)]
                    print("sol", sol)

                    # vector for extrapolation
                    extra = np.array([])
                    for j in range(self.F):
                        if (vali[j]):
                            extra = np.append(extra, column[j])
                    print("extra", extra)

                    xi = [i/10 for i in range(1, len(extra)+1)]
                    print("xi", xi)
                    s = InterpolatedUnivariateSpline(xi, extra, k=order)
                    y = abs(s([i/10 for i in range(hmc+1, (hmc*2)+1)]))

                    ww = 0
                    for j in range(self.F):
                        if (vali[j]):
                            sol[j] = y[ww]
                            ww += 1

                    exc[:,i] = sol
                print("column", i, "extrapolated", exc[:, i])

            print("exc ======>", exc)
            
            self.ci = exc.reshape(self.F, self.N)
            self.ci = [self.ci[i].tolist() for i in range(self.F)]
            print("Costs EXTRAPOLATE", self.ci)     

        # End Extrapolation ||||||||||||||||||||||

        for i in range(self.K):   
            for j in range(self.F):
                # ||||||||||||||||||||||||||||| MINIZINC MODEL |||||||||||||||||||||||||||||||||
                command = [
                        self.path_minizinc, 
                        self.path_model, "--solver", self.solver, 
                        "-D", "N="+str(self.N), 
                        "-D", "Di="+str(self.Di), 
                        "-D", "b="+str(self.bi), 
                        "-D", "c="+str(self.ci[j]),
                        "-D", "time_slot_val="+str(self.time_slot_val),
                        "-D", "battery="+str(self.battery)
                    ]
                
                # print("ci[j]", self.ci[j])
                # print(command)

                try:
                    process = subprocess.Popen(command, stdout=subprocess.PIPE)
                    output, error = process.communicate()
                    outs = output.decode("utf-8").split("\n")
                    # print(outs, error)

                    s = json.loads(outs[0])
                    self.X = np.append(self.X, s[0])
                    self.bi = s[1]
            
                    states = s[1]
                    states = [round((s*100)/self.battery, 4) for s in states]

                    print(s[0], "\n", states)
                    print("________________________________________________________________________________")


                except Exception as e:
                    print(e)
                    print(outs, error)
                    print("---unsat---")
                    m = self.N if self.Di >= self.N else self.Di 

                    if (m == self.N):
                        arr = np.ones(self.N)
                    else:
                        idx = np.argpartition(self.ci[j], m)
                        print(idx)
                        arr = np.array([0 for i in range(self.N)])
                        for ele in idx[:m]:
                            arr[ele] = 1
                    
                    self.X = np.append(self.X, arr)
                    self.bi = self.bi-self.ci[j]*arr
                    self.bi = self.bi.tolist()
                    states = self.bi
                    states = [round((s*100)/self.battery, 4) for s in states]

                    print(arr, "\n", states)
                    print("________________________________________________________________________________")


                # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

            # Amount of time slots computed -----------------------------------------------   
            # print("X", self.X.reshape(self.F, self.N))

            self.X = self.X.reshape(self.F, self.N)
            self.X_bef = self.X
            # os.system('clear')
            # print("X", self.X)
            # print("bi", self.bi)
            # print("ci", self.ci)
            # print("cf", self.cf)

            # print("------------------------------------------------------------------------------------------")
            # formatedX = self.formatAssignment(self.X)
            # for j in range(self.F):
            #     print(j, formatedX[j])

            #     *** SEND SCHEDULE ***          SendTimeFrequencyToAllNodes()           *** SEND SCHEDULE ***
            return self.X
