from random import choices, randrange, random, randint, choice, sample

from colored import bg, fg, attr


# trieda Monk predstavuje mnícha, ktorý hrabe záhradu
class Monk:
    def __init__(self, gene_length, zen_map, new):
        self.gene_length = gene_length  # velkosť génu závisí od obvodu záhrady a počtu kamenov
        self.own_map = [list(x) for x in zen_map]  # vlastná kopia mapky
        self.monk_stuck = False  # ak je mních zaseknutý, tak v danej generácií dalej nehrabe
        self.fitness_score = 0  # fitness score pre mnicha
        self.possible_starting_positions = self.get_all_positions()  # vsetky mozne startovacie pozicie pre mnicha
        self.monk_starting_positions = []  # startovacie pozicie mnicha
        self.moves = []
        if new:  # ak sa vyrobí nový mních tak mu vygenerujem pozicie, ak vytvarame dieta, tak netreba gen. pozicie
            self.generate_starting_positions()  # [ ( X, Y ), Move ]
        self.generate_moves()

    def generate_moves(self):
        self.moves = choices(["UP", "DOWN", "LEFT", "RIGHT"], k=6)
        self.moves.append("LEFT")
        self.moves.append("RIGHT")
        self.moves.append("UP")
        self.moves.append("DOWN")

    def generate_starting_positions(self):

        # ak je pocet genov vacsi ako vsetky mozne pozicie, mnich nemoze zacat hravat
        if self.gene_length > len(self.possible_starting_positions):
            print("Pocet vsetkych dostupnych pozicii je mensi ako pozadovana velkost genomu")
            exit(1)

        # vygeneruj nahodne startovacie pozicie pre mnicha o pocte (pocet kamenov + obvod mapy // 2)
        self.monk_starting_positions = [
            self.possible_starting_positions.pop(randrange(len(self.possible_starting_positions))) for _ in
            range(self.gene_length)]

    # funkcia na vypocet fitness skore pre kazdeho mnicha, ak to nie je kamen, inkrementuj skore
    def fitness(self):
        visited = 0
        for i in range(len(self.own_map)):
            for j in range(len(self.own_map[0])):
                if self.own_map[i][j] > 0:
                    visited += 1
        return visited

    # checkovacia funkcia, ci sa mnich nedostal von z mapy
    def in_bounds(self, position):
        if 0 <= position[0] < (len(self.own_map[0])) and 0 <= position[1] < (len(self.own_map)):
            return True
        return False

    # hlavna funkcia pre pohyb mnicha, ak je startovacia pozicia kamen, return
    def fill_matrice_road(self, position, move_number, init_direction):

        if self.own_map[position[1]][position[0]] != 0:
            return

        self.own_map[position[1]][position[0]] = move_number

        direction = 0
        i = 0

        # zaciatocny smer sa zoberie
        move = init_direction

        # pre kazdy cyklus sa pozri okolo mnicha, posun sa tam, kam je nastaveny smer
        while True:

            down = (position[0], position[1] + 1)
            up = (position[0], position[1] - 1)
            left = (position[0] - 1, position[1])
            right = (position[0] + 1, position[1])
            i += 1

            # pohyb do lava
            if move == "LEFT":
                if not self.in_bounds(left):
                    break
                if self.own_map[left[1]][left[0]] == 0:
                    self.own_map[left[1]][left[0]] = move_number
                    position = left
                    continue

            # pohyb hore
            if move == "UP":
                if not self.in_bounds(up):
                    break
                if self.own_map[up[1]][up[0]] == 0:
                    self.own_map[up[1]][up[0]] = move_number
                    position = up
                    continue

            # pohyb dole
            if move == "DOWN":
                if not self.in_bounds(down):
                    break
                if self.own_map[down[1]][down[0]] == 0:
                    self.own_map[down[1]][down[0]] = move_number
                    position = down
                    continue

            # pohyb doprava
            if move == "RIGHT":
                if not self.in_bounds(right):
                    break
                if self.own_map[right[1]][right[0]] == 0:
                    self.own_map[right[1]][right[0]] = move_number
                    position = right
                    continue

            # ak je mnich zaseknuty, ukonci cestu
            if self.in_bounds(left) and self.in_bounds(down) and self.in_bounds(right) and self.in_bounds(up):
                if self.own_map[left[1]][left[0]] != 0 and self.own_map[down[1]][down[0]] != 0 and \
                        self.own_map[right[1]][right[0]] != 0 and self.own_map[up[1]][up[0]] != 0:
                    self.monk_stuck = True
                    break
            # ak narazil mnich na prekazku, nastav novy smer
            move = self.moves[direction]
            if direction == len(self.moves) - 1:
                direction = 0
            else:
                direction += 1

        return

    # mutacia ktora namiesto generacie novej pozicie iba swapne jednu poziciu mnicha s jednou zo vsetkych moznych
    # startovacich pozici
    def mutate(self, probability, probability_moves):
        for i in range(len(self.monk_starting_positions)):

            index_all = randrange(len(self.possible_starting_positions))

            if random() < probability:
                self.monk_starting_positions[i], self.possible_starting_positions[index_all] = \
                    self.possible_starting_positions[index_all], self.monk_starting_positions[i]

        for j in range(len(self.moves) - 4):
            index = randrange(len(self.moves) - 4)
            if random() < probability_moves:
                self.moves[index] = choice(["LEFT", "DOWN", "RIGHT", "UP"])

    # pre kazdu mnichovu poziciu urob cestu na vlastnej mape
    def translate_genes_to_map(self):
        move_number = 1
        for starting_point in self.monk_starting_positions:
            if self.monk_stuck:
                break
            if self.own_map[starting_point[0][1]][starting_point[0][0]] == 0:
                self.fill_matrice_road(starting_point[0], move_number, starting_point[1])
                move_number += 1

    # styri for cykly ktore obopnu mapu a zistia pozicie hranicnych bodov
    def get_all_positions(self):

        possible_positions = []

        # horne okrajove body
        for x in range(len(self.own_map[0])):
            if self.own_map[0][x] != -1:
                possible_positions.append([(x, 0), "DOWN"])
        possible_positions.append([(0, 0), "RIGHT"])

        # prave okrajove body
        for j in range(len(self.own_map) - 2):
            if self.own_map[j + 1][len(self.own_map[0]) - 1] != -1:
                possible_positions.append([(len(self.own_map[0]) - 1, j + 1), "LEFT"])
        possible_positions.append([(len(self.own_map[0]) - 1, 0), "LEFT"])

        # dolne okrajove body
        for i in range(len(self.own_map[0])):
            if self.own_map[len(self.own_map) - 1][len(self.own_map[0]) - 1 - i] != -1:
                possible_positions.append([(len(self.own_map[0]) - 1 - i, len(self.own_map) - 1), "UP"])
        possible_positions.append([(len(self.own_map[0]) - 1, len(self.own_map) - 1), "LEFT"])

        # lave okrajove body
        for k in range(len(self.own_map) - 2):
            if self.own_map[len(self.own_map) - 2 - k][0] != -1:
                possible_positions.append([(0, len(self.own_map) - 2 - k), "RIGHT"])
        possible_positions.append([(0, len(self.own_map) - 1), "UP"])
        return possible_positions


# trieda ktora predstavuje celu populaciu mnichov
class Population:
    def __init__(self, zen_map, rocks_num):
        self.genes_len = len(zen_map) + len(zen_map[0]) + rocks_num  # pocet genov v kazdom mnichovy
        self.own_map = [list(x) for x in zen_map]  # kopia mapy
        self.genomes = []  # samostatny list mnichov
        self.rocks = rocks_num  # pocet kamenov na mape

    # funkcia, ktora zavola fitness funkciu pre kazdeho mnicha
    def fitness_all(self):
        for monk in self.genomes:
            monk.fitness_score = monk.fitness()

    # funkcia ktora nariadi kazdemu mnichovi aby pohrabal zahradu
    def setup_monks(self):
        for monk in self.genomes:
            monk.translate_genes_to_map()

    # precisti mapy mnichov, nastav im fitness score na nulu
    def clear_monks(self):
        for monk in self.genomes:
            monk.own_map = [list(x) for x in self.own_map]
            monk.fitness_score = 0
            monk.monk_stuck = False

    # vygeneruj N pocet mnichov
    def populate(self, own_map, num):
        self.genomes = [Monk(self.genes_len, own_map, True) for _ in range(num)]

    # selekcia rodicov podla rulety
    def roullete_selection(self):
        return choices(population=self.genomes, weights=[genome.fitness_score for genome in self.genomes], k=2)

    # selekcia rodicov podla turnaja n mnichov
    def tournament_selection(self, number_of_contestants):

        parents = []
        for i in range(2):
            monks = sample(population=self.genomes, k=number_of_contestants)
            monks_sorted = sorted(monks, key=lambda monks: monks.fitness_score, reverse=True)
            parents.append(monks_sorted[0])

        # dole je prvá myšlienka turnaja

        # for j in range(2):
        #     for i in range(number_of_contestants):
        #         index = randrange(0, len(self.genomes))
        #
        #         if self.genomes[index].fitness_score > best_fitness:
        #             best_fitness = self.genomes[index].fitness_score
        #             best_monk = self.genomes[index]
        #     parents.append(best_monk)
        #     best_fitness = 0

        return parents

    # single point crossover pre rodicov, vratia sa startovacie pozicie crossnute medzi rodicmi
    def crossover(self, mother_genome, father_genome):
        length = len(mother_genome)
        index = randint(1, length - 1)
        return mother_genome[0:index] + father_genome[index:], father_genome[0:index] + mother_genome[index:]


# vygeneruj defaultnu mapu, ktora bola uvedena v zadani
def make_default_map():
    rock_pos = [(5, 1), (1, 2), (4, 3), (2, 4), (8, 6), (9, 6)]
    zen_map = [[0 for x in range(12)] for y in range(10)]
    for _ in rock_pos:
        zen_map[_[1]][_[0]] = -1
    return zen_map, 6


# vygeneruj mapu z textoveho suboru
def make_map_file():
    file = open("mapa.txt", "r")
    zen_map = []
    rocks = 0
    for line in file:
        zen_map.append([int(n) for n in line.split()])
    for y in range(len(zen_map)):
        for x in range(len(zen_map[0])):
            if zen_map[y][x] == -1:
                rocks += 1
    return zen_map, rocks


# vypis mapy farebne pomocou kniznice colored
def print_map(zen_map):
    for i in range(len(zen_map)):
        for j in range(len(zen_map[0])):
            if zen_map[i][j] == -1:
                print(f"{bg(222)}{fg(16)}{attr('bold')}K  {attr(0)}", end="")
            elif zen_map[i][j] > 9:
                if zen_map[i][j] == 11:
                    print(f"{bg(222)}{fg('orchid')}{attr('bold')}{zen_map[i][j]} {attr(0)}", end="")
                else:
                    print(f"{bg(222)}{fg(zen_map[i][j])}{attr('bold')}{zen_map[i][j]} {attr(0)}", end="")
            elif zen_map[i][j] < 10:
                if zen_map[i][j] == 3:
                    print(f"{bg(222)}{fg(124)}{attr('bold')}{zen_map[i][j]}  {attr(0)}", end="")
                else:
                    print(f"{bg(222)}{fg(zen_map[i][j])}{attr('bold')}{zen_map[i][j]}  {attr(0)}", end="")
        print("")
    print("")


# vytvorenie dalsej generacie mnichov
def new_population(population_monks, prob_positions, prob_moves, selection_func):
    # elitizmus
    next_generation = [population_monks.genomes[0], population_monks.genomes[1]]

    # pre kazdych dvoch rodicov popar
    for j in range(int(len(population_monks.genomes) / 2) - 1):
        if selection_func == "r":
            parent_1, parent_2 = population_monks.roullete_selection()
        else:
            parent_1, parent_2 = population_monks.tournament_selection(3)

        # vytvorenie novych objektov ako dieta1,dieta2
        Child1 = Monk(population_monks.genes_len, population_monks.own_map, False)
        Child2 = Monk(population_monks.genes_len, population_monks.own_map, False)

        # single point crossover
        Child1.monk_starting_positions, Child2.monk_starting_positions = population_monks.crossover(
            parent_1.monk_starting_positions,
            parent_2.monk_starting_positions)
        Child1.moves, Child2.moves = population_monks.crossover(parent_1.moves, parent_2.moves)

        # mutacia deti
        Child1.mutate(prob_positions, prob_moves)
        Child2.mutate(prob_positions, prob_moves)

        # ulozenie do novej generacie
        next_generation.append(Child1)
        next_generation.append(Child2)

    return next_generation


# hlavna funkcia, evolucia mnichov
def evolution(
        num_monks,
        generation_limit,
        zen_map,
        number_of_rocks,
        prob_positions,
        prob_moves,
        selection_func
):
    # vytvorenie novej prazdnej populacie
    population_monks = Population(zen_map, number_of_rocks)

    # vytvorenie mnichov v populacii
    population_monks.populate(zen_map, num_monks)

    # po maximalnu generaciu
    for i in range(generation_limit):

        # nastav vsetkych mnichov, ich mapy a fitness score
        population_monks.setup_monks()
        population_monks.fitness_all()

        # zorad populaciu mnichvo zostupne
        population_monks.genomes = sorted(population_monks.genomes,
                                          key=lambda genomes: genomes.fitness_score,
                                          reverse=True)

        print(f"Generacia {i}.: {population_monks.genomes[0].fitness_score}")

        # ak je mnich, ktory nasiel cestu zastav a vypis mapu mnicha
        if population_monks.genomes[0].fitness_score == len(zen_map) * len(zen_map[0]) - population_monks.rocks:
            print_map(population_monks.genomes[0].own_map)
            break

        population_monks.genomes = new_population(population_monks, prob_positions, prob_moves, selection_func)

        # precisti mapu
        population_monks.clear_monks()

    population_monks.genomes = sorted(population_monks.genomes,
                                      key=lambda genomes: genomes.fitness_score,
                                      reverse=True)

    print("")


def input_info():
    num_monks = int(input("Zadaj pocet mnichov: "))
    prob_positions = float(input("Zadaj pravdepodobnost mutacie pozicii mnicha (0 - 1): "))
    prob_moves = float(input("Zadaj pravdepodobnost mutacie pohybov mnicha (0 - 1): "))
    selection_func = input("Selektivna funkcia (t - turnaj/ r - ruleta): ")
    return num_monks, prob_positions, prob_moves, selection_func


def main():
    controller = 0
    while controller != 3:
        print("1 - defaultna mapa zo zadania\n2 - mapa zo suboru\n3 - koniec")
        controller = int(input("Zadaj vyber: "))
        if controller == 1:
            zen_map, number_of_rocks = make_default_map()
            num_monks, prob_positions, prob_moves, selection_func = input_info()
            evolution(num_monks, 4000, zen_map, number_of_rocks, prob_positions, prob_moves, selection_func)

        if controller == 2:
            zen_map, number_of_rocks = make_map_file()
            num_monks, prob_positions, prob_moves, selection_func = input_info()
            evolution(num_monks, 4000, zen_map, number_of_rocks, prob_positions, prob_moves, selection_func)

    return


if __name__ == '__main__':
    main()
