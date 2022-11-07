"""Throw out an encounter based on some variables"""
import csv
import random

from fractions import Fraction as fr

# How many monsters per encounter
NUM_MONSTERS = 5
OWNED_BOOKS = ['Monster Manual', "Player's Handbook"]
MAX_SINGLE_CR = 15
MAX_SUM_CR = 200
MIN_SUM_CR = 70

def _filter_on_books(entry:list) -> bool:
    """Filter for owner books."""
    for elem in OWNED_BOOKS:
        if elem in entry[13]:
            return True
    return False

def _convert_cr_to_float(cr_string:str) -> float:
    try:
        return float(cr_string)
    except ValueError:
        return float(fr(cr_string))

def calculate_encounter(monster_list) -> tuple():
    """Create an encounter giving attention to MAX_SUM_CR"""
    cr_sum = 0
    enc_list = []
    for _ in range(0, NUM_MONSTERS):
        rand = random.randint(0, len(monster_list)-1)
        monster_cr = _convert_cr_to_float(monster_list[rand][11])

        # Loop over monsters until a monster with a CR < MAX_SINGLE_CR is reached
        while monster_cr > MAX_SINGLE_CR or (cr_sum + monster_cr) > MAX_SUM_CR:
            rand = random.randint(0, len(monster_list)-1)
            monster_cr = _convert_cr_to_float(monster_list[rand][11])

        enc_list.append(monster_list[rand])
        cr_sum += monster_cr
    return (enc_list, cr_sum)


if __name__ == "__main__":
    # Open the monster list
    monster_list = []
    with open('monsters.csv', newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            monster_list.append(row)

    # Filter the list
    filtered_monster_list = filter(_filter_on_books, monster_list)
    monster_list = list(filtered_monster_list)

    encounter_list = calculate_encounter(monster_list)
    while encounter_list[1] < MIN_SUM_CR:
        encounter_list = calculate_encounter(monster_list)

    for monster in encounter_list[0]:
        print(f'{monster[0]} | {monster[11]} | {monster[13]}')
    print(f"CR-Sum: {encounter_list[1]}")
