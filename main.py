from World import World

def main():
    # n = 15 Di = 35
    n = 10
    F = 5
    Di = 30 

    WIDTH = 100
    HEIGHT = 100

    MAX_SPEED = 0.6
    MIN_SPEED = 0.2

    LOW_VALUE = 0.01
    DEATH_LIMIT = 99.8

    TIME_SLOT_VAL = 3.6111e-5  
        
    show_annotations = False

    sleepInterval = 25

    initEnergies = [19 for i in range(n)]
    # initEnergies = [83, 91, 100]

    router = {
        "Po": 23,
        "Go": 2,
        "Gi": 2,
        "Pr": -71
    }

    frequency = 5000
    large = True
    Hb = 3
    Hm = 0.5

    animation = False

    w = World(
        n, F, Di, 
        WIDTH, HEIGHT, MAX_SPEED, MIN_SPEED, LOW_VALUE, DEATH_LIMIT, TIME_SLOT_VAL,
        router, frequency, large, Hb, Hm,
        show_annotations, sleepInterval, initEnergies, animation)

    w.playWorld()

if __name__ == "__main__":
    main()