import os
import json
import random

krproject2_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(krproject2_path)

#Loading in the argument
def load_argumentation_framework(file_name):
    with open(file_name, 'r') as file:
        argumentation_framework = json.load(file)
        attack_relations = argumentation_framework.get("Attack Relations", [])
    return argumentation_framework

def discussion_game(file_name, claimed_argument):
    argumentation_framework= load_argumentation_framework(file_name)
    P_arguments=[claimed_argument]
    O_arguments=[]

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

        #Proponents turn to choose attack against preceding opponent choice
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
file_name = "example-argumentation-framework.json"
claimed_argument="0"
print(discussion_game(file_name, claimed_argument))

