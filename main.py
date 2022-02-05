import json
from World import World

# Main method
def main():

    # Opening JSON file
    file = open("data.json")
     
    # Returns JSON object as dictionary
    data = json.load(file)
    
    N = data["N"]
    F = data["F"]
    Di = data["Di"]

    MAX_SPEED = data["MAX_SPEED"]
    MIN_SPEED = data["MIN_SPEED"]

    LOW_VALUE = data["LOW_VALUE"]
    DEATH_LIMIT = data["DEATH_LIMIT"]

    TIME_SLOT_VAL = data["TIME_SLOT_VAL"] 

    ANIMATION = data["ANIMATION"]
        
    SHOW_ANNOTATIONS = data["SHOW_ANNOTATIONS"]

    SLEEP_INTERVAL = data["SLEEP_INTERVAL"]

    BATTERY_CAPACITY = data["BATTERY_CAPACITY"]

    # 3.8 Wh -> 20% where battery capacity is 19 Wh
    INIT_ENERGIES = data["INIT_ENERGIES"]
    # INIT_ENERGIES = [18.992, 19, 18.998, 19, 18.992] # different levels
    # INIT_ENERGIES = [3.84, 3.84, 3.84, 3.84, 3.83, 3.83, 3.83, 3.82, 3.81, 3.81]

    ROUTER = data["ROUTER"]

    FREQUENCY = data["FREQUENCY"]
    LARGE = data["LARGE"]
    Hb = data["Hb"]
    Hm = data["Hm"]

    PLMODEL = data["PLMODEL"]

    w = World(
        N, F, Di, 
        MAX_SPEED, MIN_SPEED, LOW_VALUE, DEATH_LIMIT, TIME_SLOT_VAL,
        PLMODEL, BATTERY_CAPACITY, ROUTER, FREQUENCY, LARGE, Hb, Hm,
        SHOW_ANNOTATIONS, SLEEP_INTERVAL, INIT_ENERGIES, ANIMATION)

    w.playWorld()

if __name__ == "__main__":
    main()