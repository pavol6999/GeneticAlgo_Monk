import csv
import genetic_algo


#funkcia mi zapise data do csv formatu
def write_csv(data, test_name, col_names):
    with open(f'testy/{test_name}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(col_names)
        for i in range(len(data)):
            writer.writerow([data[i][j] for j in range(len(col_names))])

        print(f"vysledky su zapisane v testy/{test_name}.csv")


# test ktory mi vrati priemernu genraciu najdenia vysledku za n počet opakovani
def test_n_times(n, num_monks, prob_positions, prob_moves, selection_func):
    if n == 1:
        print("Max fitness, median a najhorsie fitness sa zapise do test/test_1.csv")
    solutions =0

    for i in range(n):
        solution_num, data = genetic_algo.evolution(num_monks, 4000, zen_map, number_of_rocks, prob_positions, prob_moves,
                               selection_func, True)
        solutions+=solution_num


    # ak je pocet testov raz, teda iba raz spustime algoritmus tak nech mi ulozi data do csv
    if n == 1:
        write_csv(data,"test_1", ["Gen Number", "Max fitness", "Median", "Worst Fitness"])



    return solutions/n

# test na zistenie ci je lepsi turnaj alebo ruleta
def test_select_func():
    data = []
    for i in range(10,200,10):
        t_avg = test_n_times(50, i, 0.10, 0.10, 't')
        print(f"{i} - TURNAJ select, priemer najdenia riesenia: {t_avg} generacia")
        r_avg = test_n_times(50, i, 0.10, 0.10, 'r')
        print(f"{i} - RULETA select, priemer najdenia riesenia: {r_avg} generacia")
        data.append([i,t_avg,r_avg])
    write_csv(data, "test_2", ["Monk count", "Tournament AVG", "Roulette AVG"])

# test 100 jedincov, turnaj, neznamy parameter su sance mutacie
def test_mutations():

    # rozne pravdepodobnosti mutacie, od ziadnej mutacie po zmutovanie kazdeho genu
    prob_chance = [0.05, 0.1, 0.15, 0.2, 0.5]
    print("Tabulka bude zapisana do test_3.csv")
    data = []
    data_temp = []

    # pravdepodobnost mutacie pozicie mnicha
    for i in prob_chance:
        # pravdepodobnost mutacie rozhodnutia pohybu
        temp = [i]
        for j in prob_chance:

            t_avg = test_n_times(50, 100, i, j, 't')

            temp.append(t_avg)
            print(f"Priemerne najdene riesenie pre P_moves {j} a P_positions {i} je {t_avg} generacia")
        data.append(temp)
    write_csv(data,"test_3",["P_positions.P_moves", "0.05", "0.1", "0.15", "0.2", "0.5"])
    print("Tabulka bola zapisana do test_3.csv")

if __name__ == '__main__':
        print("1 - test N x riešenie\n2 - test selektivnych funkcii pri tvorbe jedinca\n3 - test pravdepodobnosti mutacii\n4 - koniec")
        controller = 0
        zen_map, number_of_rocks = genetic_algo.make_default_map()

        while controller != 4:
            controller = int(input("Zadajte volbu: "))

            if controller == 1:

                n = int(input("Kolko krat chcete test zopakovat: "))
                num_monks, prob_positions, prob_moves, selection_func = genetic_algo.input_info()
                test_n_times(n, num_monks, prob_positions, prob_moves, selection_func)
                if n > 1:
                    print(f"Riesenie sa v priemere naslo v {n}. generacii")


            if controller == 2:
                print("Spustam porovnanie rulety a turnaja pre mutaciu 10%")
                test_select_func()

            if controller == 3:
                print("Spustam porovnanie pravdepodobnosti mutacii")
                test_mutations()