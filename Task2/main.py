import json
import animals
import csv

MAX_NUMBER_OF_ROUNDS = 50
NUMBER_OF_SHEEPS = 15
MAX_LIMIT_OF_COORDINATES = 10.0
SHEEP_MOVEMENT_DISTANCE = 0.5
WOLF_MOVEMENT_DISTANCE = 1.0


def save_to_json(data):
    with open(file="pos.json", mode="w") as file:
        json.dump(data, file, indent=4)

def alive_status_save(list_of_alive):
    with open(file="alive_status.csv", mode="w") as file:
        writer = csv.DictWriter(file, fieldnames=["round_no", "sheeps_alive"])
        for item in list_of_alive:
            writer.writerow({'round_no' :item['round_no'], 'sheeps_alive' : item['sheeps_alive']})

def init_animals():
    sheeps = []
    for i in range(NUMBER_OF_SHEEPS):
        sheeps.append(animals.sheep(i+1, SHEEP_MOVEMENT_DISTANCE, MAX_LIMIT_OF_COORDINATES))
    wolf = animals.wolf(WOLF_MOVEMENT_DISTANCE)
    return sheeps, wolf

def symulation_algorithm():
    sheeps, wolf = init_animals()
    sheeps_alive = NUMBER_OF_SHEEPS
    round_number = 0
    list_to_save = []
    list_of_alive = []
    sheeps_pos = [None] * NUMBER_OF_SHEEPS


    for round_number in range(MAX_NUMBER_OF_ROUNDS):
        print(f"Round_no {round_number + 1}")
        for sheep in sheeps:
            sheep.move()
        wolf.nearest_sheep(sheeps)
        print(f"Wolf chasing a sheep with index {wolf.nearest_sheep_index}")
        attacked, sheep_index = wolf.attack()
        if attacked:
            print(f"Wolf attacked sheep {sheep_index}")
            sheeps = [sheep for sheep in sheeps if sheep.index != sheep_index]
            sheeps_pos[sheep_index-1] = None
            sheeps_alive -= 1
        else:
            wolf.move()
        list_of_alive.append({'round_no' : round_number + 1, 'sheeps_alive' : sheeps_alive})
        print(f"wolf_pos: {wolf.position[0]:.3f}, {wolf.position[1]:.3f}")
        print("sheeps alive:", sheeps_alive)
        for s in sheeps:
            sheeps_pos[s.index - 1] = [s.position[0], s.position[1]]
        list_to_save.append({'round_no' : round_number + 1, 'wolf_pos' : [wolf.position[0], wolf.position[1]],
                              'sheep_pos' : sheeps_pos.copy()})
        if sheeps_alive == 0:
            print("All sheeps have been eaten. Simulation ends.")
            break
    else:
        print("Maximum number of rounds reached. Simulation ends.")
    save_to_json(list_to_save)
    alive_status_save(list_of_alive)

symulation_algorithm()