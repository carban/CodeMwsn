import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np
import math
from main import Mwsn 

# ####################################################

n = 3
F = 5
Di = 15

WIDTH = 100
HEIGHT = 100

MAX_SPEED = 0.8
MIN_SPEED = 0.2

LOW_VALUE = 0.01
DEATH_LIMIT = 5

station = [WIDTH / 2, HEIGHT / 2]

show_annotations = False

sleepInterval = 25

np.random.seed(42)

# ####################################################

fig, ax = plt.subplots()  
ax.grid()  
plt.xlim(0, WIDTH)
plt.ylim(0, HEIGHT)
ax.plot(station[0], station[1], marker="o", c='b', markersize=8, linestyle='dashed')
x, y = np.random.randint(low=LOW_VALUE, high=100, size=(n,)), np.random.randint(low=LOW_VALUE, high=100, size=(n,))
sc, = ax.plot(x, y, marker="o", ls="", c='#72ca00', markersize=5) # set linestyle to none
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

tar_x = np.random.randint(low=LOW_VALUE, high=WIDTH, size=(n,))
tar_y = np.random.randint(low=LOW_VALUE, high=HEIGHT, size=(n,))

speed = np.random.uniform(MIN_SPEED, MAX_SPEED, n)

distances = np.zeros(n)
costs = np.zeros(n)

norm = math.sqrt((WIDTH / 2)**2 + (HEIGHT / 2)**2) * 10

# Initial Annotations -----------------------------------------------------------------
if (show_annotations):
    annotation_list = [plt.annotate(i, (x[i], y[i]), ha='center') for i in range(n)]

# Initial Distances and costs ---------------------------------------------------------
initDist = [math.sqrt((x[i]-station[0])**2 + (y[i]-station[1])**2) for i in range(n)]
initDist = np.array(initDist)

initCost = initDist / norm # max distance in map
cpi = [initCost.tolist() for i in range(F)]
costs_packet = np.zeros((F, n))
# print("cpi", cpi)

# Initial Energies -----------------------------------------------------------------
initEnergies = [100 for i in range(n)]
# initEnergies = [90, 97, 77]

# Initial Residual Energies -----------------------------------------------------------------
initS = np.ones((F+1, n))
initS[0] = initEnergies

# Initial Assigments -----------------------------------------------------------------
initX = np.ones((F, n))

# graphs -----------------------------------------------------------------
graphS = [initEnergies]
graphX = [[0 for i in range(n)]]
graphC = [[0 for i in range(n)]]

# Initial MWSNs model -----------------------------------------------------------------
obj = Mwsn(1, F, n, Di, [], [])

print("###########################################################################################")

XA = initX
S = initS

def animate(f, data):

    time_text.set_text('f = {:d}'.format(f))

    # XA = initX
    # S = initS
    global XA
    global S

    # print("--> XA", XA)
    # print("--> S", S)

    global tar_x
    global tar_y

    getx, gety = sc.get_data()[0], sc.get_data()[1]
    
    dx = tar_x - getx
    dy = tar_y - gety

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
            nx[i] = getx[i] + speed[i] * (dx[i]/abs(dx[i])) # this formula returns 1 if dx[i] >= 0 else -1 
            # calcula y
            ny[i] = (dy[i]/dx[i])*nx[i] - (dy[i]/dx[i])*getx[i] + gety[i]
        else:
            # incrementa y
            ny[i] = gety[i] + speed[i] * (dy[i]/abs(dy[i])) # this formula returns 1 if dy[i] >= 0 else -1 
            # calcula x
            nx[i] = (dx[i]/dy[i])*ny[i] - (dx[i]/dy[i])*gety[i] + getx[i]

        # assign new positions
        x[i] = nx[i]
        y[i] = ny[i]

        # update annotations
        if (show_annotations):
            annotation_list[i].set_position((x[i], y[i]))
        
        # update distances and costs
        distances[i] = math.sqrt((x[i]-station[0])**2 + (y[i]-station[1])**2)
        costs[i] = distances[i] / norm # max distance in map

        # update target
        if ((tar_x[i] - x[i] >= -1 and tar_x[i] - x[i] <= 1) or 
            (tar_y[i] - y[i] >= -1 and tar_y[i] - y[i] <= 1)):
            # update target position
            tar_x[i] = np.random.randint(low=LOW_VALUE, high=WIDTH)
            tar_y[i] = np.random.randint(low=LOW_VALUE, high=HEIGHT)
            # update speed of node i
            speed[i] = np.random.uniform(MIN_SPEED, MAX_SPEED)
            # print("====>", i, "CHANGED")
            # print(a, "TARGETS", tar_x, tar_y)
            # ax.plot(tarx[i], tary[i], marker="o", c='r')
    
    # update data
    sc.set_data(x, y)

    # send costs to solver method *************************************
    # print("COSTS", f, costs)
    S[f+1] = S[f]-(costs*XA[f])
    costs_packet[f] = costs

    if (f == F-1):
        # # SENDING RESIDUAL ENERGIES TO THE MAIN PROGRAM ************
        # print("REAL COSTS PACKET", costs_packet)
        print("S", S)

        obj.setS(S)
        obj.setBi(S[F].tolist())
        XA = obj.compute()
        
        # XA = np.ones((F, n))
        # XA = XA * (Di / n)

        for i in range(F):
            graphX.append(XA[i].tolist())
            graphS.append(S[i+1].tolist())
            graphC.append(costs_packet[i].tolist())
        
        # print("NEW XA", XA)

        S[0] = S[F]
        # S[0] = initEnergies

        # Check Umbral ----------------------
        for i in range(n):
            if (S[F][i] <= DEATH_LIMIT):
                print("*** DEAD ***")
                print("End time:", len(graphX) / F )
                ani.event_source.stop()
                fig, axis = plt.subplots(3)
                  
                axis[0].plot(graphS)
                axis[0].set_title("S")
                  
                axis[1].plot(graphC)
                axis[1].set_title("C")
                  
                axis[2].plot(graphX)
                axis[2].set_title("X")
                plt.show()
                break

# interval 500
ani = matplotlib.animation.FuncAnimation(fig, animate, fargs=([x,y],), frames=F, interval=sleepInterval, repeat=True) 

plt.show()