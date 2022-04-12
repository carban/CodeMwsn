import json
from World import World

# Main method
def main():

    # Opening JSON file
    file = open("data.json")
     
    # Returns JSON object as dictionary
    data = json.load(file)
    
    SEED = data['SEED']

    N = data["N"]
    F = data["F"]
    Di = data["Di"]

    if(N == 0 or F == 0 or Di == 0):
        print("\n =====> The values for N, F and Di must be bigger than 0\n")
        assert(False)

    CONSTRAINT_V1 = data["CONSTRAINT_V1"]

    if(CONSTRAINT_V1 and N > Di):
        print("\n =====> If you're using the version 1 of the constraint 1, Di must be bigger than N\n")
        assert(False)

    MAX_SPEED = data["MAX_SPEED"]
    MIN_SPEED = data["MIN_SPEED"]

    if (MAX_SPEED < MIN_SPEED):
        print("\n =====> Max speed must be bigger than Min speed\n")
        assert(False)
    elif (MAX_SPEED <= 0 or MAX_SPEED > 0.6):
        print("\n =====> Max speed must be bigger than 0 and less than 0.6\n")
        assert(False)
    elif(MIN_SPEED <= 0 and MIN_SPEED > 0.4):             
        print("\n =====> Min speed must be bigger than 0 and less than 0.4\n")
        assert(False)

    LOW_VALUE = 0.001
    DEATH_LIMIT = data["DEATH_LIMIT"]

    TIME_SLOT_VAL = data["TIME_SLOT_VAL"] 

    ANIMATION = data["SHOW_ANIMATION"]

    STATIC_NODES = data["STATIC_NODES"]
        
    SHOW_ANNOTATIONS = data["SHOW_ANNOTATIONS"]

    SLEEP_INTERVAL = data["SLEEP_INTERVAL"]
    
    BATTERY_CAPACITY = data["BATTERY_CAPACITY"]

    INIT_ENERGIES = data["INIT_ENERGIES"]
    if (len(INIT_ENERGIES) == 0):
        INIT_ENERGIES = [BATTERY_CAPACITY for i in range(N)]

    ROUTER = data["ROUTER"]

    FREQUENCY = data["FREQUENCY"]
    LARGE = data["LARGE"]
    Hb = data["Hb"]
    Hm = data["Hm"]

    EXTRA = data["EXTRAPOLATION"]

    EC_VALUE = data["EC_VALUE"]

    MAX_DIST = data["MAX_DIST"]

    if (MAX_DIST < 10):
        print("\n =====> The distance must be bigger than 10 meters\n")
        assert(False)     

    SCALED_COST = data["SCALED_COST"]

    PLMODEL = data["PLMODEL"]

    if (PLMODEL not in ["extended", "cost231", "okumura", "free"]):
        print("\n =====> Only select between 'extended', 'cost231', 'okumura', 'free'\n")
        assert(False)

    SOLVER = data["SOLVER"]
    if (SOLVER not in ["Gecode", "COIN-BC"]):
        print("\n =====> Only select between 'Gecode', 'COIN-BC'\n")
        assert(False)

    w = World(
        SEED,
        N, F, Di, CONSTRAINT_V1,
        MAX_SPEED, MIN_SPEED, LOW_VALUE, DEATH_LIMIT, TIME_SLOT_VAL, EC_VALUE, MAX_DIST,
        SCALED_COST, PLMODEL, SOLVER, BATTERY_CAPACITY, ROUTER, FREQUENCY, LARGE, Hb, Hm,
        STATIC_NODES, SHOW_ANNOTATIONS, SLEEP_INTERVAL, INIT_ENERGIES, ANIMATION, EXTRA)

    print(" ||||||||||||||||||||| START |||||||||||||||||||||")

    w.playWorld()

if __name__ == "__main__":
    main()