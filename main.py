from World import World

def main():
    # n = 15 Di = 35
    n = 15
    F = 5
    Di = 35 

    WIDTH = 100
    HEIGHT = 100

    MAX_SPEED = 0.8
    MIN_SPEED = 0.2

    LOW_VALUE = 0.01
    DEATH_LIMIT = 5
        
    show_annotations = False

    sleepInterval = 25

    initEnergies = [100 for i in range(n)]
    # initEnergies = [83, 91, 100]

    w = World(
        n, F, Di, 
        WIDTH, HEIGHT, MAX_SPEED, MIN_SPEED, LOW_VALUE, DEATH_LIMIT, 
        show_annotations, sleepInterval, initEnergies)

    w.playWorld()

if __name__ == "__main__":
    main()