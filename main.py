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

    MAX_SPEED = data["MAX_SPEED"]
    MIN_SPEED = data["MIN_SPEED"]

    LOW_VALUE = 0.001
    DEATH_LIMIT = data["DEATH_LIMIT"]

    TIME_SLOT_VAL = data["TIME_SLOT_VAL"] 

    ANIMATION = data["SHOW_ANIMATION"]

    STATIC_NODES = data["STATIC_NODES"]
        
    SHOW_ANNOTATIONS = data["SHOW_ANNOTATIONS"]

    SLEEP_INTERVAL = data["SLEEP_INTERVAL"]
    
    BATTERY_CAPACITY = data["BATTERY_CAPACITY"]

    # 3.8 Wh -> 20% where battery capacity is 19 Wh
    INIT_ENERGIES = data["INIT_ENERGIES"]# [18.94, 18.95, 19, 19, 18.94, 18.95],  [19, 18.94]  [18.998, 18.99, 18.997]
    if (len(INIT_ENERGIES) == 0):
        INIT_ENERGIES = [BATTERY_CAPACITY for i in range(N)]
        
    # INIT_ENERGIES = [18.992, 19, 18.998, 19, 18.992] # different levels
    # INIT_ENERGIES = [3.84, 3.84, 3.84, 3.84, 3.83, 3.83, 3.83, 3.82, 3.81, 3.81]

    ROUTER = data["ROUTER"]

    FREQUENCY = data["FREQUENCY"]
    LARGE = data["LARGE"]
    Hb = data["Hb"]
    Hm = data["Hm"]

    EC_VALUE = data["EC_VALUE"]

    MAX_DIST = data["MAX_DIST"]

    SCALED_COST = data["SCALED_COST"]

    PLMODEL = data["PLMODEL"]

    SOLVER = data["SOLVER"]

    w = World(
        SEED,
        N, F, Di, 
        MAX_SPEED, MIN_SPEED, LOW_VALUE, DEATH_LIMIT, TIME_SLOT_VAL, EC_VALUE, MAX_DIST,
        SCALED_COST, PLMODEL, SOLVER, BATTERY_CAPACITY, ROUTER, FREQUENCY, LARGE, Hb, Hm,
        STATIC_NODES, SHOW_ANNOTATIONS, SLEEP_INTERVAL, INIT_ENERGIES, ANIMATION)

    print(" ||||||||||||||||||||| START |||||||||||||||||||||")

    w.playWorld()

if __name__ == "__main__":
    main()