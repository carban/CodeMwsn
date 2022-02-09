import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np
import math
from Mwsn import Mwsn
from PPL import PPL

np.random.seed(42)

class World(object):
    """docstring for world"""
    def __init__(self, n, F, Di, MAX_SPEED, MIN_SPEED, LOW_VALUE, DEATH_LIMIT, TIME_SLOT_VAL, PLMODEL, BATTERY_CAPACITY, router, frequency, large, Hb, Hm, show_annotations, sleepInterval, initEnergies, animation):
        
        super(World, self).__init__()

        # print(initEnergies)

        # ####################################################
        
        # Path Loss and Power cost functions ------------------------------------------
        self.ppl = PPL(router, frequency, large, Hb, Hm, PLMODEL)

        self.n = n
        self.F = F
        self.Di = Di
        
        self.PLMODEL = PLMODEL

        # diameter of the circle | CHECK THE OTHER PLACES WHERE WITH AND NORM APPEARS
        # self.WIDTH = self.ppl.get_max_dist() * 2
        self.WIDTH = 55 * 2
        self.HEIGHT = self.WIDTH

        self.MAX_SPEED = MAX_SPEED
        self.MIN_SPEED = MIN_SPEED

        self.LOW_VALUE = LOW_VALUE
        self.DEATH_LIMIT = DEATH_LIMIT

        self.TIME_SLOT_VAL = TIME_SLOT_VAL

        self.BATTERY_CAPACITY = BATTERY_CAPACITY  

        self.initEnergies = initEnergies

        self.show_annotations = show_annotations
        self.annotation_list = []

        self.sleepInterval = sleepInterval

        self.isDeath = False

        self.counter = 0

        self.animation = animation

        # ####################################################

        self.station = [self.WIDTH / 2, self.HEIGHT / 2]

        # self.norm = math.sqrt((WIDTH / 2)**2 + (HEIGHT / 2)**2) # 50 using the circle area because radius
        self.norm = self.WIDTH / 2
        # self.conv = 0.025 / self.norm

        self.annotation_list = []
        self.x = np.random.uniform(low=LOW_VALUE, high=self.WIDTH, size=(n,)) 
        # self.y = np.random.randint(low=LOW_VALUE, high=100, size=(n,))
        self.y = np.array([self.get_posy_givenx(x) for x in self.x])

        self.time_text = ""

        self.tar_x = np.random.uniform(low=LOW_VALUE, high=self.WIDTH, size=(n,))
        # self.tar_y = np.random.randint(low=LOW_VALUE, high=HEIGHT, size=(n,))
        self.tar_y = np.array([self.get_posy_givenx(x) for x in self.tar_x])

        self.speed = np.random.uniform(MIN_SPEED, MAX_SPEED, n)

        self.distances = np.zeros(n)
        self.costs = np.zeros(n)
        self.costs_packet = np.zeros((F, n))

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
        self.factor = 100; 
        maxcost = self.ppl.power_cost_w_given_d(self.norm/1000) * self.factor
        self.obj = Mwsn(1, F, n, Di, [], [], maxcost, self.TIME_SLOT_VAL, self.BATTERY_CAPACITY)
        self.ani = {}
        self.sc = {} # just for animation

    def showResults(self):

        print(" |||||||||| Results ||||||||||")

        length = len(self.graphS)
        print("  N:                      ", self.n)
        print("  F:                      ", self.F)
        print("  Di:                     ", self.Di)
        print("  Initial Energies:       ", self.initEnergies)
        print("  Death Limit:            ", self.DEATH_LIMIT, "%")
        print("  Final Energies:         ", self.S[self.F])
        print("  Total number of frames: ", length)
        print("  Optimization events:    ", length / self.F )
        print("  TS per frame:           ", round(np.mean([np.sum(f) for f in self.graphX]), 3))
        print("  Path loss model:        ", self.PLMODEL)


        # PLOTING GRAPHS ##############################################
        self.graphS.pop(0)
        fig, ax = plt.subplots(3)
        ax[0].plot(self.graphS)
        ax[0].plot([self.DEATH_LIMIT for i in range(length)], c='r')
        ax[0].set_title("S")

                      
        ax[1].plot(self.graphC)
        ax[1].set_title("C")
                      
        ax[2].plot(self.graphX)
        ax[2].set_title("X")
        plt.show()

        #############################################################333

    def get_posy_givenx(self, x):
        rootvalue = math.sqrt(self.norm**2 - (x-self.norm)**2)
        limit_up = rootvalue+self.norm
        limit_down = -rootvalue+self.norm
        limit_down = limit_down - 2 if limit_down == self.norm else limit_down
        # print("Limits", limit_up, limit_down)  
        return np.random.uniform(low=limit_down, high=limit_up)

    def playWorldAnimated(self):

        fig, ax = plt.subplots()
        # self.ax = ax 
        ax.grid()  
        plt.xlim(0, self.WIDTH)
        plt.ylim(0, self.HEIGHT)
        #plot circle area
        ax.add_patch(plt.Circle((self.station[0], self.station[1]), self.WIDTH / 2, color='#f7c1dc'))
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

    # def pl_dbm(self, d, f):
    #     return 20.0*math.log(d, 10)+20.0*math.log(f, 10)+32.44

    # def dbm_to_mw(self, db):
    #     return 10.0**(db/10.0)

    # def mw_to_w(self, mw):
    #     return mw / 1000

    # def power_cost(self, d):
    #     # d in Km
    #     f = 5e3 #MHz
    #     Po = 23
    #     Go = 2
    #     Gi = 2
    #     Pr = -71
    #     Pl = self.pl_dbm(d, f)
    #     Po = Pr + Pl - Go - Gi

    #     return self.mw_to_w(self.dbm_to_mw(Po))

    def animate(self, f=None, data=None):

        f = self.counter
        # self.time_text.set_text('f = {:d}'.format(f))

        n = self.n
        F = self.F

        # getx, gety = self.sc.get_data()[0], self.sc.get_data()[1]
        getx, gety = self.x, self.y

        dx = self.tar_x - getx
        dy = self.tar_y - gety

        m = dy / dx
        nx = np.zeros(n)
        ny = np.zeros(n)

        x = np.zeros(n)
        y = np.zeros(n)

        # updating positions and targets RWP approach 
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
            self.distances[i] = ((math.sqrt((x[i]-self.station[0])**2 + (y[i]-self.station[1])**2))) / 1000 # * self.conv
            # CHANGE IT TO JUST ONE FUNCTION...IT'S BETTER YOU KNOW
            self.costs[i] = self.ppl.power_cost_w_given_d(self.distances[i]) * self.factor
            # self.costs[i] = self.ppl.power_cost_w(self.ppl.okumura_pl_db(self.distances[i]))
            # print("dist ==>", i, self.distances[i])
            print("cost ==>", self.costs[i])
            # self.costs[i] = self.power_cost((self.distances[i]*3) / 1000)
            # print("dist ==>", (self.distances[i]*3) / 1000)
            # self.costs[i] = self.distances[i] / self.norm # max distance in map
            # self.costs[i] = self.costFunction(self.distances[i] / self.norm) / 10
            # print("i->", i, self.distances[i], self.distances[i]*3, (self.distances[i]*3)/1000, self.costs[i]) 

            # update target
            if ((self.tar_x[i] - x[i] >= -1 and self.tar_x[i] - x[i] <= 1) or 
                (self.tar_y[i] - y[i] >= -1 and self.tar_y[i] - y[i] <= 1)):
                # update target position
                self.tar_x[i] = np.random.uniform(low=self.LOW_VALUE, high=self.WIDTH)
                # self.tar_y[i] = np.random.randint(low=self.LOW_VALUE, high=self.WIDTH)
                self.tar_y[i] = self.get_posy_givenx(self.tar_x[i])
                # update speed of node i
                self.speed[i] = np.random.uniform(self.MIN_SPEED, self.MAX_SPEED)
                # print("====>", i, "CHANGED")
                # print("TARGETS", self.tar_x[i], self.tar_y[i])
                # self.ax.plot(self.tar_x[i], self.tar_y[i], marker="o", c='r')
        
        # update data
        if (self.animation):
            self.sc.set_data(x, y)
        self.x = x
        self.y = y

        # send costs to solver method *************************************
        # fullcost = (self.costs*self.MX[f]*self.TIME_SLOT_VAL)
        self.S[f+1] = self.S[f]-(self.costs*self.MX[f]*self.TIME_SLOT_VAL)  # self.S[f]-(self.costs*self.MX[f]) / Di
        # print(self.S[f+1])
        self.costs_packet[f] = self.costs
        # ccc = (fullcost/3.8)*1000
        # print("*******")
        # for i in range(len(ccc)):
        #     print("Node ", i, 5000/ccc[i])
        # print("==>", self.costs*self.MX[f]*self.TIME_SLOT_VAL)

        # Check Umbral ----------------------
        for i in range(n):

            percent = (self.S[self.F][i]*100)/self.BATTERY_CAPACITY
            # print("====>", percent)
            if (self.S[self.F][i] != 1 and percent < self.DEATH_LIMIT):
                if (self.animation):
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

                percent = (self.S[i+1]*100)/self.BATTERY_CAPACITY

                self.graphS.append(percent.tolist())
                self.graphX.append(self.MX[i].tolist())
                self.graphC.append(self.costs_packet[i].tolist())
            
            self.S[0] = self.S[F]
            # S[0] = initEnergies

            self.counter = 0
        else:
            self.counter += 1