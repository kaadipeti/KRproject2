import json

def load_arguments(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
        arguments = data['Arguments']
        attack_relations = data['Attack Relations']
    return arguments, attack_relations

def get_possible_attacks(argument, attack_relations, used_arguments):
    possible_attacks = []
    for attack in attack_relations:
        if attack[1] == argument and attack[0] not in used_arguments:
            possible_attacks.append(attack[0])
    return possible_attacks

def main(file_name, claimed_argument):
    arguments, attack_relations = load_arguments(file_name)
    proponent_turn = True
    used_arguments = [claimed_argument]

    current_argument = claimed_argument

    while True:
        if proponent_turn:
            print(f"Proponent's turn - Current argument: {current_argument}")
            possible_attacks = get_possible_attacks(current_argument, attack_relations, used_arguments)

            if not possible_attacks:
                print("Opponent wins! Proponent unable to make a move.")
                break

            print("Possible attacks by opponent:", possible_attacks)
            selected_attack = input("Select an argument to attack: ")

            if selected_attack in possible_attacks:
                used_arguments.append(selected_attack)
                current_argument = selected_attack
                proponent_turn = False
            else:
                print("Invalid attack! Please choose a valid argument.")
        else:
            print(f"Opponent's turn - Current argument: {current_argument}")
            selected_attack = input("Select an argument to defend the current argument: ")

            if selected_attack in used_arguments:
                print("Opponent wins! Proponent contradicts itself.")
                break

            current_argument = selected_attack
            used_arguments.append(selected_attack)
            proponent_turn = True

    print("Game Over!")

# Usage
file_name = "af1.json"
claimed_argument = "k"
main(file_name, claimed_argument)
