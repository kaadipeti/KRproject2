import json
import random

def load_arguments(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
        arguments = data['Arguments']
        attack_relations = data['Attack Relations']
    #print("a")
    return arguments, attack_relations

def get_possible_attacks(argument, attack_relations, used_arguments):
    possible_attacks = []
    for attack in attack_relations:
        if attack[1] == argument and attack[0] not in used_arguments:
            possible_attacks.append(attack[0])
    #print("b")
    return possible_attacks

def display_preferred_extensions(preferred_exts):
    print("Preferred Extensions:")
    for i, extension in enumerate(preferred_exts, start=1):
        print(f"Extension {i}: {extension}")

def main(file_name, claimed_argument):
    arguments, attack_relations = load_arguments(file_name)
    proponent_turn = True
    used_arguments = [claimed_argument]
    opponent_used_arguments = []

    # Find preferred extensions
    preferred_exts = find_preferred_extensions(arguments, attack_relations)

    # Display preferred extensions
    display_preferred_extensions(preferred_exts)

    # Check if the claimed argument is in any preferred extension
    if claimed_argument not in [arg for ext in preferred_exts for arg in ext]:
        print("Invalid claimed argument! Please choose an argument from a preferred extension.")
        return

    current_argument = claimed_argument

    while True:
        if proponent_turn:
            print(f"Proponent's turn - Current argument: {current_argument}")
            possible_defenses = []

            # Find possible defenses against the current argument
            for ext in preferred_exts:
                if current_argument in ext:
                    possible_defenses.extend([arg for arg in ext if (arg, current_argument) in attack_relations])

            if not possible_defenses:
                print("Opponent wins! Proponent unable to make a move.")
                break

            print("Possible defenses by opponent:", possible_defenses)
            selected_defense = input("Select an argument to defend the current argument: ")

            if selected_defense in possible_defenses and selected_defense not in opponent_used_arguments:
                used_arguments.append(selected_defense)
                current_argument = selected_defense
                proponent_turn = False
                opponent_used_arguments.append(selected_defense)
            else:
                print("Invalid defense! Please choose a valid argument to defend.")
        else:
            # Opponent's turn (Computer's turn)
            print(f"Opponent's turn - Current argument: {current_argument}")
            possible_attacks = []

            # Find possible attacks against the current argument
            for ext in preferred_exts:
                if current_argument in ext:
                    possible_attacks.extend([arg for arg in ext if (current_argument, arg) in attack_relations])

            if not possible_attacks:
                print("Proponent wins! Opponent unable to make a move.")
                break

            print("Possible attacks by opponent:", possible_attacks)
            selected_attack = random.choice(possible_attacks)  # Randomly select an argument

            used_arguments.append(selected_attack)
            current_argument = selected_attack
            proponent_turn = True

    print("Game Over!")


def find_preferred_extensions(arguments, attack_relations):
    # Initialize an empty list to store preferred extensions
    preferred_extensions = []

    # Create a function to check if an argument is attacked by another argument
    def is_attacked(arg, attacks):
        return any(attack[1] == arg for attack in attacks)

    # Function to find arguments that are not attacked
    def find_undefended_arguments(arg_list, attacks):
        return [arg for arg in arg_list if not is_attacked(arg, attacks)]

    # Find all arguments that are not attacked
    undefended_arguments = find_undefended_arguments(arguments, attack_relations)

    # Keep iterating until no new arguments are added to preferred extensions
    while undefended_arguments:
        preferred_extensions.append(undefended_arguments)
        new_attacks = [attack for attack in attack_relations if attack[0] in undefended_arguments]
        undefended_arguments = find_undefended_arguments(
            [attack[1] for attack in new_attacks],
            [attack for attack in attack_relations if attack not in new_attacks]
        )

    return preferred_extensions

# Usage
file_name = "example-argumentation-framework.json"
claimed_argument = "2"
main(file_name, claimed_argument)
