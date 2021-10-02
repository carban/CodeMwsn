import subprocess
import json
import numpy as np
import math
import os

class Mwsn:
    def __init__(self, K, F, N, Di, bi, ci, time_slot_val):

        self.path_minizinc = "/home/carban/PortableApps/MiniZincIDE-2.4.3-bundle-linux-x86_64/bin/minizinc"
        self.path_model = "/home/carban/Documents/TG/Model6.mzn"
        
        self.K = K
        self.F = F
        self.N = N
        self.Di = Di
        self.bi = bi
        self.ci = ci
        self.time_slot_val = time_slot_val
        self.cf = []

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

        # Actual costs ----------------------------------------------------------------
        C = np.ones((self.F, self.N))
        
        # for j in range(self.F):
        #     for k in range(self.N):
        #         if (self.X_bef[j][k] != 0):
        #             C[j][k] = (self.S[j][k]-self.S[j+1][k])/self.X_bef[j][k] # (Di * (S[j]-S[j+1]))/X[j]
        #         else:
        #             # print("dsfsdfsfsd", self.X_bef[j])
        #             C[j][k] = (self.S[j][k]-self.S[j+1][k])

        for i in range(self.F):
            C[i] = (self.S[i]-self.S[i+1])/(self.X_bef[i]*self.time_slot_val)

        self.ci = C.reshape(self.F, self.N)
        self.ci = [self.ci[i].tolist() for i in range(self.F)]
        # print("Costs calculated", self.ci)

        for i in range(self.K):   
            for j in range(self.F):
                # ||||||||||||||||||||||||||||| MINIZINC MODEL |||||||||||||||||||||||||||||||||
                command = [
                        self.path_minizinc, 
                        self.path_model, "--solver", "Gecode", 
                        "-D", "N="+str(self.N), 
                        "-D", "Di="+str(self.Di), 
                        "-D", "b="+str(self.bi), 
                        "-D", "c="+str(self.ci[j]),
                        "-D", "time_slot_val="+str(self.time_slot_val)
                    ]
                
                # print("ci[j]", self.ci[j])
                # print(command)

                process = subprocess.Popen(command, stdout=subprocess.PIPE)
                output, error = process.communicate()
                outs = output.decode("utf-8").split("\n")
                # print(outs, error)

                s = json.loads(outs[0])
                self.X = np.append(self.X, s[0])
                self.bi = s[1]
                print(s)

                # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

            # Amount of time slots computed -----------------------------------------------   
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
