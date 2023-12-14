import os
import json
import random
import sys

#Loading in the argument
def load_argumentation_framework(file_name):
    with open(file_name, 'r') as file:
        argumentation_framework = json.load(file)
        attack_relations = argumentation_framework.get("Attack Relations", [])
    return argumentation_framework


def conflict_free(arguments, attacks):
    cf = []
    cf.append('')

    for i in range(len(arguments)):
        if [arguments[i], arguments[i]] not in attacks:
            cf.append(arguments[i])
            # print(f'Added {arguments[i]} to the conflict-free set')

        for j in range(i + 1, len(arguments)):
            if [arguments[i], arguments[j]] not in attacks and [arguments[j], arguments[i]] not in attacks and [
                arguments[i], arguments[i]] not in attacks and [arguments[j], arguments[j]] not in attacks:
                cf.append([arguments[i], arguments[j]])
                # print(f'Added {arguments[i]} and {arguments[j]} to the conflict-free set')

    return cf


def defended(arguments, attacks):
    defended = []

    # if argument is not attacked
    defend_counter = 0
    for i in range(len(arguments)):
        for attacker, attacked in attacks:
            if arguments[i] != attacked:
                defend_counter += 1
        if defend_counter == len(attacks):
            defended.append(arguments[i])
            # print(f'{arguments[i]} is not attacked')
        defend_counter = 0

    # if argument is attacked but also defended
    for i in range(len(arguments)):
        attr = []
        for attacker, attacked in attacks:
            if arguments[i] == attacked:
                attr.append(attacker)
        # print(f'{arguments[i]} is attacked by {attr}')

        attr_copy = attr[:]
        for x in range(len(attr_copy)):
            for attacker, attacked in attacks:
                if attr_copy[x] == attacked and attr_copy[x] in attr and arguments[i] != attr_copy[x]:
                    attr.remove(attr_copy[x])
                    # print(f'deleted {attr_copy[x]}')
                    # print(attr)
        if len(attr) == 0 and arguments[i] not in defended:
            defended.append(arguments[i])
            # print(f'{arguments[i]} is defended')

    return defended


def preferred(arguments, attacks):
    cf = conflict_free(arguments, attacks)
    deff = defended(arguments, attacks)
    attacked = []

    for i in arguments:
        if i not in deff:
            attacked.append(i)

    # preferred extensions
    admissable = cf[:]

    for i in attacked:
        for j in cf:
            if i in j:
                if j in admissable:
                    admissable.remove(j)

    length = []
    for i in admissable:
        length.append(len(i))

    maxlength = max(length)
    preferred = []

    for i in admissable:
        if len(i) == maxlength:
            preferred.append(i)

    return (preferred)

#example input
#file_name = "example-argumentation-framework.json"
#argumentation_data = load_argumentation_framework(file_name) # native python forn
# Encodeing the loaded argumentation data as a JSON-formatted string, IDK which is better
#encoded_argumentation = json.dumps(argumentation_data, indent=2)
#print(argumentation_data["Arguments"]["3"])

def discussion_game(file_name, claimed_argument):
    argumentation_framework= load_argumentation_framework(file_name)
    arguments1 = argumentation_framework.get("Arguments", [])
    arguments = list(arguments1.keys())
    attacks = argumentation_framework.get("Attack Relations", [])
    pe=preferred(arguments, attacks)
    print(pe)
    P_arguments=[claimed_argument]
    O_arguments=[]

    #checking if claimed argument is in preferred extension
    second_elements = []
    for sublist in pe:
        second_elements.append(sublist[1])

    if claimed_argument not in second_elements:
        return print("Please enter a claimed arument in the proponents preferred extension")


    print("Welcome to the Discussion Game where you will be playing as the Opponent attacking the Proponents arguments")

    while True:
        p_argument = P_arguments[-1]
        print(f"\nProponent:{p_argument}= {argumentation_framework['Arguments'][p_argument]}")


        #Opponents turn
        #for all past proponents argument you check which attacks are possible
        for a in P_arguments:
            all_attack_options = [attack for attack in argumentation_framework['Attack Relations'] if a == attack[1]]
            attack_options = [attack for attack in all_attack_options if attack[0] not in O_arguments]

        if not attack_options:
            print("Proponent Wins!! Opponent is unable to make a move.")
            break
        print(attack_options)


        #opponent choosing an attack
        opponent_attack= int(input("Select one of the attack options given:"))
        chosen_attack= attack_options[opponent_attack]
        O_arguments.append(chosen_attack[0])
        print(chosen_attack)
        print(f"Opponent attacks with{chosen_attack} against {p_argument}") # could be nicer to have better text given for the players

        # CONDITION: if opponent uses argument previously from proponent
        if chosen_attack[0] in P_arguments:
            print("Opponent Wins!! because he has shown that the proponent contradicts itself")
            break

        #Proponent turn to choose attack against preceding opponent choice
        P_attack_options=[attack for attack in argumentation_framework['Attack Relations'] if chosen_attack[0] == attack[1]]

        if not P_attack_options:
            print("Opponent Wins!! Proponent has no choices left.")
            break

        P_chosen_attack=random.choice(P_attack_options)
        print(f"Proponent has chosen the following attack: {P_chosen_attack}")

        #CONDITION: If the proponent uses an argument previously used by the opponent, then the opponent wins
        if P_chosen_attack[0] in O_arguments:
            print("Opponent Wins!! because the proponent contradicts itself")
            break

        P_arguments.append( P_chosen_attack[0])



#testing
#file_name = "example-argumentation-framework.json"
#file_name = "af1.json"
#file_name = "af2.json"
#file_name = "af3.json"
#claimed_argument="d"
#discussion_game(file_name, claimed_argument)


if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 4:
        print("Usage: python script.py <function_name> <file_name> <claimed_argument>")
        sys.exit(1)

    # Extract command-line arguments
    function_name = sys.argv[1]
    file_name = sys.argv[2]
    claimed_argument = sys.argv[3]

    # Call the appropriate function based on the provided function name
    if function_name == "discussion_game":
        discussion_game(file_name, claimed_argument)
    else:
        print("Invalid function name. Supported functions: discussion_game")

