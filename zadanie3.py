from copy import copy, deepcopy

from random import choices, randrange, random, randint, choice, sample


class Genome:
    def __init__(self, gene_length, zen_map, new):
        self.gene_length = gene_length
        self.own_map = [list(x) for x in zen_map]
        self.monk_stuck = False
        self.fitness_score = 0
        self.possible_starting_positions = self.get_all_positions()  # all possible starting points on the map
        self.monk_starting_positions = []  # a subset of all possible starting points
        self.moves = []  # on the map, my representation of genes
        if new:
            self.generate_starting_positions()  # [ ( X, Y ), Move ]
        self.generate_moves()



    def generate_moves(self):
        self.moves = choices(["UP", "DOWN", "LEFT", "RIGHT"], k=16)
        self.moves.append("LEFT")
        self.moves.append("RIGHT")
        self.moves.append("UP")
        self.moves.append("DOWN")

    def generate_starting_positions(self):
        self.monk_starting_positions = [
            self.possible_starting_positions.pop(randrange(len(self.possible_starting_positions))) for _ in
            range(self.gene_length)]



    def fitness(self):
        visited = 0
        for i in range(len(self.own_map)):
            for j in range(len(self.own_map[0])):
                if self.own_map[i][j] != 0 and self.own_map[i][j] != -1:
                    visited += 1
        return visited

    def in_bounds(self, position):
        if 0 <= position[0] < (len(self.own_map[0])) and 0 <= position[1] < (len(self.own_map)):
            return True
        return False

    def fill_matrice_road(self, position, move_number, init_direction):

        if self.own_map[position[1]][position[0]] != 0:
            return

        self.own_map[position[1]][position[0]] = move_number

        direction = 0
        i = 0


        move = init_direction
        while True:
            if i == 10000:
                print("")
            down = (position[0], position[1] + 1)
            up = (position[0], position[1] - 1)
            left = (position[0] - 1, position[1])
            right = (position[0] + 1, position[1])
            i += 1

            if self.in_bounds(left) and self.in_bounds(down) and self.in_bounds(right) and self.in_bounds(up):
                if self.own_map[left[1]][left[0]] != 0 and self.own_map[down[1]][down[0]] != 0 and \
                        self.own_map[right[1]][right[0]] != 0 and self.own_map[up[1]][up[0]] != 0:
                    self.monk_stuck = True
                    break

            if move == "LEFT":
                if not self.in_bounds(left):
                    break
                if self.own_map[left[1]][left[0]] == 0:
                    self.own_map[left[1]][left[0]] = move_number
                    position = left
                    continue

            if move == "UP":
                if not self.in_bounds(up):
                    break
                if self.own_map[up[1]][up[0]] == 0:
                    self.own_map[up[1]][up[0]] = move_number
                    position = up
                    continue

            if move == "DOWN":
                if not self.in_bounds(down):
                    break
                if self.own_map[down[1]][down[0]] == 0:
                    self.own_map[down[1]][down[0]] = move_number
                    position = down
                    continue

            if move == "RIGHT":
                if not self.in_bounds(right):
                    break
                if self.own_map[right[1]][right[0]] == 0:
                    self.own_map[right[1]][right[0]] = move_number
                    position = right
                    continue

            move = self.moves[direction]
            if direction == len(self.moves) - 1:
                direction = 0
            else:
                direction += 1

        return




    # mutate function does not generate new starting positions but only swaps a position in monk_starting_positions with
    # one from possible_starting_positions -> optimized
    def mutate(self, probability, mutations_num, probability_moves, moves_mutations_num):
        for i in range(mutations_num):
            index_monk = randrange(len(self.monk_starting_positions))
            index_all = randrange(len(self.possible_starting_positions))

            if random() < probability:

                self.monk_starting_positions[index_monk], self.possible_starting_positions[index_all] = deepcopy(self.possible_starting_positions[index_all]), deepcopy(self.monk_starting_positions[index_monk])


        for j in range(moves_mutations_num):
            index = randrange(len(self.moves)-4)
            if random() < probability_moves:
                self.moves[index] = choice(["LEFT", "DOWN", "RIGHT", "UP"])

    # for every monk's position start raking the garden, if the monk is stuck -> end
    def translate_genes_to_map(self):
        move_number = 1
        for starting_point in self.monk_starting_positions:
            if self.monk_stuck:
                break
            if self.own_map[starting_point[0][1]][starting_point[0][0]] == 0:
                self.fill_matrice_road(starting_point[0], move_number, starting_point[1])
                move_number += 1


    # vyplnit cisla tahov do mapy pre dany gen
    def get_all_positions(self):

        possible_positions = []
        for x in range(len(self.own_map[0])):
            if self.own_map[0][x] != -1:
                # self.fill_matrice_road((x, 0), move_num, "DOWN")
                possible_positions.append([(x, 0), "DOWN"])

        for j in range(len(self.own_map) - 2):
            if self.own_map[j + 1][len(self.own_map[0]) - 1] != -1:
                # self.fill_matrice_road((len(self.own_map[0]) - 1, j + 1), move_num, "LEFT")
                possible_positions.append([(len(self.own_map[0]) - 1, j + 1), "LEFT"])

        for i in range(len(self.own_map[0])):
            if self.own_map[len(self.own_map) - 1][len(self.own_map[0]) - 1 - i] != -1:
                #    self.fill_matrice_road((len(self.own_map[0]) - 1 - i, len(self.own_map) - 1), move_num, "UP")
                possible_positions.append([(len(self.own_map[0]) - 1 - i, len(self.own_map) - 1), "UP"])

        for k in range(len(self.own_map) - 2):
            if self.own_map[len(self.own_map) - 2 - k][0] != -1:
                #  self.fill_matrice_road((0, len(self.own_map) - 2 - k), move_num, "RIGHT")
                possible_positions.append([(0, len(self.own_map) - 2 - k), "RIGHT"])

        return possible_positions


class Population:
    def __init__(self, zen_map, rocks_num):
        self.genes_len = len(zen_map) + len(zen_map[0]) + rocks_num
        self.genome_len = 2 * len(zen_map) + 2 * len(zen_map[0]) - 4
        self.own_map = [list(x) for x in zen_map]
        self.genomes = []

    def fitness_all(self):
        for monk in self.genomes:
            monk.fitness_score = monk.fitness()

    def setup_monks(self):
        for monk in self.genomes:
            monk.translate_genes_to_map()

    def clear_monks(self):
        for monk in self.genomes:
            monk.own_map = [list(x) for x in self.own_map]
            monk.fitness_score = 0
            monk.monk_stuck = False

    def populate(self, own_map, num):
        self.genomes = [Genome(self.genes_len, own_map, True) for _ in range(num)]


    def roullete_selection(self):
        weights = [genome.fitness_score for genome in self.genomes]
        return choices(population=self.genomes, weights=weights, k=2)

    def crossover(self, mother_genome, father_genome):
        length = len(mother_genome)
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


def new_population(population_monks):

    next_generation = [population_monks.genomes[0], population_monks.genomes[1]]

    for j in range(int(len(population_monks.genomes) / 2) - 1 ):
        parent_1, parent_2 = population_monks.roullete_selection()

        Child1 = Genome(population_monks.genes_len, population_monks.own_map, False)
        Child2 = Genome(population_monks.genes_len, population_monks.own_map, False)

        Child1.monk_starting_positions, Child2.monk_starting_positions = population_monks.crossover(
            parent_1.monk_starting_positions,
            parent_2.monk_starting_positions)
        Child1.mutate(0.5, 8, 0.5, 8)
        Child2.mutate(0.5, 8, 0.5, 8)

        next_generation.append(Child1)
        next_generation.append(Child2)

    return next_generation

def evolution(
        fitness_limit,
        generation_limit,
        zen_map,
        number_of_rocks,
):
    population_monks = Population(zen_map, number_of_rocks)

    population_monks.populate(zen_map, 28)

    for i in range(generation_limit):
        next_gen=[]
        if i == 200:
            print("")
        population_monks.setup_monks()
        population_monks.fitness_all()

        population_monks.genomes = sorted(population_monks.genomes,
                                          key=lambda genomes: genomes.fitness_score,
                                          reverse=True)



        if population_monks.genomes[0].fitness_score == 114:
            print_map(population_monks.genomes[0].own_map)
            break
        print(f"Generacia {i}: {population_monks.genomes[0].fitness_score}")




        population_monks.genomes = new_population(population_monks)

        population_monks.clear_monks()

    population_monks.genomes = sorted(population_monks.genomes,
                                      key=lambda genomes: genomes.fitness_score,
                                      reverse=True)

    print("")


def main():
    zen_map, number_of_rocks = make_default_map()
    evolution(100,4000, zen_map, number_of_rocks)
    population = 0

    return


if __name__ == '__main__':
    main()
    make_default_map()
