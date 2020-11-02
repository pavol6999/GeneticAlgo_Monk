from copy import copy, deepcopy
from random import choices, randrange, random, randint, choice


class Genome:
    def __init__(self, length, zen_map):
        self.length = length
        self.genome = []
        self.own_map = deepcopy(zen_map)

        self.generate_genome()
        self.translate_genome_to_map()

        self.fitness_score = self.fitness()

    def generate_genome(self):
        self.genome = choices([1, 0], k=self.length)
        self.moves = choices(["UP", "DOWN", "LEFT", "RIGHT"], k=16)


    def fitness(self):
        visited = 0
        for i in range(len(self.own_map)):
            for j in range(len(self.own_map[0])):
                if self.own_map[i][j] != 0:
                    visited += 1
        return visited

    def in_bounds(self, position):
        if 0 <= position[0] < (len(self.own_map[0])) and 0 <= position[1] < (len(self.own_map)):
            return True
        return False

    # TODO
    def fill_matrice_road(self, position, move_number, init_direction):

        direction = 0
        i = 0
        self.moves.append("LEFT")
        self.moves.append("RIGHT")
        self.moves.append("UP")
        self.moves.append("DOWN")

        move = init_direction
        while True:
            down = (position[0], position[1] + 1)
            up = (position[0], position[1] - 1)
            left = (position[0] - 1, position[1])
            right = (position[0] + 1, position[1])
            i += 1

            if i ==9000:
                self.fitness_score = -1
                break

            if self.moves[direction] == "LEFT":
                if not self.in_bounds(left):
                    break
                if self.own_map[left[1]][left[0]] == 0:
                    self.own_map[left[1]][left[0]] = move_number
                    position = left
                    continue

            if self.moves[direction] == "UP":
                if not self.in_bounds(up):
                    break
                if self.own_map[up[1]][up[0]] == 0:
                    self.own_map[up[1]][up[0]] = move_number
                    position = up
                    continue

            if self.moves[direction] == "DOWN":
                if not self.in_bounds(down):
                    break
                if self.own_map[down[1]][down[0]] == 0:
                    self.own_map[down[1]][down[0]] = move_number
                    position = down
                    continue

            if self.moves[direction] == "RIGHT":
                if not self.in_bounds(right):
                    break
                if self.own_map[right[1]][right[0]] == 0:
                    self.own_map[right[1]][right[0]] = move_number
                    position = right
                    continue

            if direction == len(self.moves) - 1:
                direction = 0
            else:
                direction += 1
        return

    def mutate(self, probability, mutations_num, probability_moves, moves_mutations_num):
        for i in range(mutations_num):
            index = randrange(len(self.genome))
            if random() < probability:
                self.genome[index] = abs(self.genome[index] - 1)

        for j in range(moves_mutations_num):
            index = randrange(len(self.moves))
            if random() < probability_moves:
                self.moves[index] = choice(["LEFT", "DOWN", "RIGHT", "UP"])


    def start_raking(self,positions):
        for i in range(len(positions)):
            self.fill_matrice_road(positions[i],i+1)

    # vyplnit cisla tahov do mapy pre dany gen
    def translate_genome_to_map(self):
        move_num = 1
        genome_positions = []
        for x in range(len(self.own_map[0])):
            if self.genome[x]:
                if self.own_map[0][x] == 0:
                    self.own_map[0][x] = move_num
                    genome_positions.append((x, 0))
                    self.fill_matrice_road((x, 0),move_num, "DOWN")
                    move_num += 1

        for j in range(len(self.own_map) - 2):
            if self.genome[j + len(self.own_map[0])]:
                if self.own_map[j+1][len(self.own_map[0]) - 1] == 0:
                    self.own_map[j + 1][len(self.own_map[0]) - 1] = move_num
                    genome_positions.append((len(self.own_map[0]) - 1, j+1))
                    self.fill_matrice_road((len(self.own_map[0]) - 1, j + 1), move_num, "LEFT")
                    move_num += 1


        for i in range(len(self.own_map[0])):
            if self.genome[i + len(self.own_map[0]) - 1 + len(self.own_map) - 1]:
                if self.own_map[len(self.own_map) - 1][len(self.own_map[0]) - 1 - i] == 0:
                    self.own_map[len(self.own_map) - 1][len(self.own_map[0]) - 1 - i] = move_num
                    genome_positions.append((len(self.own_map[0]) - 1 - i, len(self.own_map) - 1))
                    self.fill_matrice_road((len(self.own_map[0]) - 1 - i, len(self.own_map) - 1), move_num, "UP")
                    move_num += 1

        for k in range(len(self.own_map) - 2):
            if self.genome[2 * (len(self.own_map[0]) - 1) + len(self.own_map) + k]:
                if self.own_map[len(self.own_map) - 2 - k][0] == 0:
                    self.own_map[len(self.own_map) - 2 - k][0] = move_num
                    genome_positions.append((0,len(self.own_map) - 2 - k))
                    self.fill_matrice_road((0, len(self.own_map) - 2 - k), move_num, "RIGHT")
                    move_num += 1
        print_map(self.own_map)
        self.start_raking(genome_positions)

        print("")

class Population:
    def __init__(self, zen_map, rocks_num):
        self.genomes_num = len(zen_map) + len(zen_map[0]) + rocks_num
        self.genome_len = 2 * len(zen_map) + 2 * len(zen_map[0]) - 4
        self.own_map = deepcopy(zen_map)
        self.genomes = self.populate(deepcopy(self.own_map))

    def populate(self, own_map):
        return [Genome(self.genome_len, own_map) for _ in range(self.genomes_num)]

    # TODO
    def roullete_selection(self):
        return

    def crossover(self, mother_genome, father_genome):
        length = len(mother_genome.genome)
        index = randint(1, length - 1)
        return mother_genome[0:index] + father_genome[index:], father_genome[0:index] + mother_genome[index:]


def make_default_map():
    rock_pos = [(5, 1), (1, 2), (4, 3), (2, 4), (8, 6), (9, 6)]
    zen_map = [[0 for x in range(12)] for y in range(10)]
    for _ in rock_pos:
        zen_map[_[1]][_[0]] = -1
    return zen_map, 6


# TODO make random map
def make_random_map(size_x, size_y, small_rocks, big_rocks):
    return


def print_map(zen_map):
    for i in range(len(zen_map)):
        for j in range(len(zen_map[0])):
            if zen_map[i][j] == -1:
                print('K', end="  ")
            elif zen_map[i][j] > 9:
                print(zen_map[i][j], end=" ")
            elif zen_map[i][j] < 10:
                print(zen_map[i][j], end="  ")
        print("")
    print("")


# TODO
def selection_func():
    return


#


def main():
    zen_map, number_of_rocks = make_default_map()

    population = Population(zen_map, number_of_rocks)
    print_map(zen_map)
    return


if __name__ == '__main__':
    main()
    make_default_map()
