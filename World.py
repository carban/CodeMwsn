import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np
import math
from Mwsn import Mwsn 

np.random.seed(42)

class World(object):
    """docstring for world"""
    def __init__(self, n, F, Di, WIDTH, HEIGHT, MAX_SPEED, MIN_SPEED, LOW_VALUE, DEATH_LIMIT, show_annotations, sleepInterval, initEnergies, animation):
        
        super(World, self).__init__()

        # ####################################################

        self.n = n
        self.F = F
        self.Di = Di

        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.MAX_SPEED = MAX_SPEED
        self.MIN_SPEED = MIN_SPEED

        self.LOW_VALUE = LOW_VALUE
        self.DEATH_LIMIT = DEATH_LIMIT

        self.initEnergies = initEnergies

        self.show_annotations = show_annotations
        self.annotation_list = []

        self.sleepInterval = sleepInterval

        self.isDeath = False

        self.counter = 0

        self.time_slot_val = 3.6111e-5    

        self.animation = animation

        # ####################################################

        self.station = [WIDTH / 2, HEIGHT / 2]

        self.annotation_list = []

        self.x = np.random.randint(low=LOW_VALUE, high=100, size=(n,)) 
        self.y = np.random.randint(low=LOW_VALUE, high=100, size=(n,))

        self.time_text = ""

        self.tar_x = np.random.randint(low=LOW_VALUE, high=WIDTH, size=(n,))
        self.tar_y = np.random.randint(low=LOW_VALUE, high=HEIGHT, size=(n,))
        self.speed = np.random.uniform(MIN_SPEED, MAX_SPEED, n)

        self.distances = np.zeros(n)
        self.costs = np.zeros(n)
        self.costs_packet = np.zeros((F, n))

        self.norm = math.sqrt((WIDTH / 2)**2 + (HEIGHT / 2)**2) * 10
        # print("====>", self.norm)

        # Initial Residual Energies -----------------------------------------------------------------
        initS = np.ones((F+1, n))
        initS[0] = initEnergies

        # Initial Assigments -----------------------------------------------------------------
        initX = np.ones((F, n))

        # graphs -----------------------------------------------------------------
        self.graphS = [initEnergies]
        self.graphX = [[0 for i in range(n)]]
        self.graphC = [[0 for i in range(n)]]

        self.MX = initX
        self.S = initS

        # Initial MWSNs model -----------------------------------------------------------------
        self.obj = Mwsn(1, F, n, Di, [], [], self.time_slot_val)
        self.ani = {}
        self.sc = {} # just for animation

    def showResults(self):

        print(" |||||||||| Results ||||||||||")

        length = len(self.graphS)
        print("  N:                      ", self.n)
        print("  F:                      ", self.F)
        print("  Di:                     ", self.Di)
        print("  Initial Energies:       ", self.initEnergies)
        print("  Death Limit:            ", self.DEATH_LIMIT)
        print("  Final Energies:         ", self.S[self.F])
        print("  Total number of frames: ", length)
        print("  Optimization events:    ", length / self.F )

        fig, ax = plt.subplots(3)
        ax[0].plot(self.graphS)
        ax[0].plot([self.DEATH_LIMIT for i in range(length)], c='r')
        ax[0].set_title("S")
                      
        ax[1].plot(self.graphC)
        ax[1].set_title("C")
                      
        ax[2].plot(self.graphX)
        ax[2].set_title("X")
        plt.show() 

    def playWorldAnimated(self):

        fig, ax = plt.subplots() 
        ax.grid()  
        plt.xlim(0, self.WIDTH)
        plt.ylim(0, self.HEIGHT)
        ax.plot(self.station[0], self.station[1], marker="o", c='b', markersize=8, linestyle='dashed')
        self.sc, = ax.plot(self.x, self.y, marker="o", ls="", c='#72ca00', markersize=5) # set linestyle to none
        # self.time_text = ax.text(0.02, 0.95, 'f = {:d}'.format(4), transform=ax.transAxes)

        # Initial Annotations -----------------------------------------------------------------
        if (self.show_annotations):
            self.annotation_list = [plt.annotate(i, (self.x[i], self.y[i]), ha='center') for i in range(self.n)]

        self.ani = matplotlib.animation.FuncAnimation(fig, self.animate, fargs=([self.x, self.y],), frames=self.F, interval=self.sleepInterval, repeat=True)

        plt.show()

    def playWorld(self):
        if(self.animation):
            self.playWorldAnimated()
        else:
            while (not self.isDeath):
                self.animate()

    def pl_dbm(self, d, f):
        return 20.0*math.log(d, 10)+20.0*math.log(f, 10)+32.44

    def dbm_to_mw(self, db):
        return 10.0**(db/10.0)

    def mw_to_w(self, mw):
        return mw / 1000

    def power_cost(self, d):
        # d in Km
        f = 5e3 #MHz
        Po = 23
        Go = 2
        Gi = 2
        Pr = -71
        Pl = self.pl_dbm(d, f)
        Po = Pr + Pl - Go - Gi

        return self.mw_to_w(self.dbm_to_mw(Po))

    def animate(self, f=None, data=None):

        f = self.counter
        # self.time_text.set_text('f = {:d}'.format(f))

        n = self.n
        F = self.F

        # getx, gety = self.sc.get_data()[0], self.sc.get_data()[1]
        getx, gety = self.x, self.y
        # print("getx", getx)

        dx = self.tar_x - getx
        dy = self.tar_y - gety

        m = dy / dx
        nx = np.zeros(n)
        ny = np.zeros(n)

        x = np.zeros(n)
        y = np.zeros(n)

        for i in range(n):

            # update positions
            # si la pendiente no esta muy inclinada
            if (m[i] >= -5 and m[i] <= 5):
                # incrementa x
                nx[i] = getx[i] + self.speed[i] * (dx[i]/abs(dx[i])) # this formula returns 1 if dx[i] >= 0 else -1 
                # calcula y
                ny[i] = (dy[i]/dx[i])*nx[i] - (dy[i]/dx[i])*getx[i] + gety[i]
            else:
                # incrementa y
                ny[i] = gety[i] + self.speed[i] * (dy[i]/abs(dy[i])) # this formula returns 1 if dy[i] >= 0 else -1 
                # calcula x
                nx[i] = (dx[i]/dy[i])*ny[i] - (dx[i]/dy[i])*gety[i] + getx[i]

            # assign new positions
            x[i] = nx[i]
            y[i] = ny[i]

            # update annotations
            if (self.show_annotations):
                self.annotation_list[i].set_position((x[i], y[i]))
            
            # update distances and costs
            self.distances[i] = math.sqrt((x[i]-self.station[0])**2 + (y[i]-self.station[1])**2)
            self.costs[i] = self.power_cost((self.distances[i]*3) / 1000)
            # self.costs[i] = self.distances[i] / self.norm # max distance in map
            # self.costs[i] = self.costFunction(self.distances[i] / self.norm) / 10
            # print("i->", i, self.distances[i], self.distances[i]*3, (self.distances[i]*3)/1000, self.costs[i]) 

            # update target
            if ((self.tar_x[i] - x[i] >= -1 and self.tar_x[i] - x[i] <= 1) or 
                (self.tar_y[i] - y[i] >= -1 and self.tar_y[i] - y[i] <= 1)):
                # update target position
                self.tar_x[i] = np.random.randint(low=self.LOW_VALUE, high=self.WIDTH)
                self.tar_y[i] = np.random.randint(low=self.LOW_VALUE, high=self.HEIGHT)
                # update speed of node i
                self.speed[i] = np.random.uniform(self.MIN_SPEED, self.MAX_SPEED)
                # print("====>", i, "CHANGED")
                # print(a, "TARGETS", tar_x, tar_y)
                # ax.plot(tarx[i], tary[i], marker="o", c='r')
        
        # update data
        if (self.animation):
            self.sc.set_data(x, y)
        self.x = x
        self.y = y

        # send costs to solver method *************************************
        # fullcost = (self.costs*self.MX[f]*self.time_slot_val)
        self.S[f+1] = self.S[f]-(self.costs*self.MX[f]*self.time_slot_val)  # self.S[f]-(self.costs*self.MX[f]) / Di
        self.costs_packet[f] = self.costs

        # ccc = (fullcost/3.8)*1000
        # print("*******")
        # for i in range(len(ccc)):
        #     print("Node ", i, 5000/ccc[i])
        # print("==>", self.costs*self.MX[f]*self.time_slot_val)

        # Check Umbral ----------------------
        for i in range(n):

            percent = (self.S[self.F][i]*100)/19
            # print("====>", percent)

            if (percent > 6 and percent < self.DEATH_LIMIT):
                self.ani.event_source.stop()
                self.isDeath = True
                self.showResults()
                break

        if (f == F-1 and not self.isDeath):

            # # SENDING RESIDUAL ENERGIES TO THE MAIN PROGRAM ************
            # print("REAL COSTS PACKET", costs_packet)
            # print("S", self.S)

            self.obj.setS(self.S)
            self.obj.setBi(self.S[F].tolist())
            self.MX = self.obj.compute()
            
            # MX = np.ones((self.F, self.n))
            # self.MX = MX * (self.Di / self.n)

            # print("X", self.MX)

            # Save values for results ----------------------
            for i in range(F):

                percent = (self.S[i+1]*100)/19

                self.graphS.append(percent.tolist())
                self.graphX.append(self.MX[i].tolist())
                self.graphC.append(self.costs_packet[i].tolist())
            
            self.S[0] = self.S[F]
            # S[0] = initEnergies

            self.counter = 0
        else:
            self.counter += 1