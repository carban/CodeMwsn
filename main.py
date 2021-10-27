from World import World

def main():
    # n = 15 Di = 35
    n = 3
    F = 5
    Di = 15

    MAX_SPEED = 0.6
    MIN_SPEED = 0.2

    LOW_VALUE = 0.001
    DEATH_LIMIT = 99.9

    TIME_SLOT_VAL = 3.6111e-5  

    animation = False
        
    show_annotations = False

    sleepInterval = 25

    BATTERY_CAPACITY = 19

    # 3.8 Wh -> 20% where battery capacity is 19 Wh
    initEnergies = [BATTERY_CAPACITY for i in range(n)]
    # initEnergies = [3.84, 3.84, 3.84, 3.84, 3.83, 3.83, 3.83, 3.82, 3.81, 3.81]

    router = {
        "Po": 20,
        "Go": 2,
        "Gi": 2,
        "Pr": -76
    }

    frequency = 2400
    large = False
    Hb = 30
    Hm = 1.5

    PLMODEL = "cost231"

    w = World(
        n, F, Di, 
        MAX_SPEED, MIN_SPEED, LOW_VALUE, DEATH_LIMIT, TIME_SLOT_VAL,
        PLMODEL, BATTERY_CAPACITY, router, frequency, large, Hb, Hm,
        show_annotations, sleepInterval, initEnergies, animation)

    w.playWorld()

if __name__ == "__main__":
    main()