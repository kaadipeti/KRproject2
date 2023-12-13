
def conflict_free(arguments, attacks):
    cf = []
    
    cf.append('')
    for i in range(len(arguments)):
        if [arguments[i], arguments[i]] not in attacks:
            cf.append(arguments[i])
            # print(f'Added {arguments[i]} to the conflict-free set')

        for j in range(i + 1, len(arguments)):
            if [arguments[i], arguments[j]] not in attacks and [arguments[j], arguments[i]] not in attacks and [arguments[i], arguments[i]] not in attacks and [arguments[j], arguments[j]] not in attacks:
                cf.append([arguments[i], arguments[j]])
                #print(f'Added {arguments[i]} and {arguments[j]} to the conflict-free set')
    
    return cf




def defended(arguments,attacks):
    defended = []
    
    # if argument is not attacked
    defend_counter = 0
    for i in range(len(arguments)):
        for attacker,attacked in attacks:
            if arguments[i] != attacked:
                defend_counter += 1
        if defend_counter == len(attacks):
            defended.append(arguments[i])
            #print(f'{arguments[i]} is not attacked')
        defend_counter = 0
    
    # if argument is attacked but also defended
    for i in range(len(arguments)):
        attr = []
        for attacker,attacked in attacks:
            if arguments[i] == attacked:
                attr.append(attacker)
       # print(f'{arguments[i]} is attacked by {attr}')
        
        
        
        attr_copy = attr[:]
        for x in range(len(attr_copy)):
            for attacker, attacked in attacks:
                if attr_copy[x] == attacked and attr_copy[x] in attr and arguments[i] != attr_copy[x]:
                    attr.remove(attr_copy[x])
                    #print(f'deleted {attr_copy[x]}')
                    #print(attr)
        if len(attr) == 0 and arguments[i] not in defended:
            defended.append(arguments[i])
            #print(f'{arguments[i]} is defended')

    return defended



def preferred(arguments,attacks):
    cf = conflict_free(arguments, attacks)
    deff = defended(arguments,attacks)
    attacked = []
    
    for i in arguments:
        if i not in deff:
            attacked.append(i)
    
    # preferred extensions
    admissable = cf[:]
    
    for i in attacked:
        for j in cf:
            if i in j:
                admissable.remove(j)
    
    length = []
    for i in admissable:
        length.append(len(i))
    
    maxlength = max(length)
    preferred = []
    
    for i in admissable:
        if len(i) == maxlength:
            preferred.append(i)
    
    return(preferred)

### EXAMPLE ###

{
    "Arguments" : {
        "0": "We should go to the cinema.",
        "1": "We should go to the gym.",
        "2": "The gym is better for the health than the cinema.",
        "3": "We have no time for evening activities, since there is an exam coming up.",
        "4": "The exam is in a few weeks.",
        "5": "We have no money for cinema or gym.",
        "6": "We just got our sallaries."
    },
    
    "Attack Relations" : [
        ["0","1"], ["1","0"], ["2","0"], 
        ["3","0"], ["3","1"], ["4","3"],
        ["5","0"], ["5","1"], ["6","5"]
    ]
}



arguments = ['a', 'b', 'c', 'd', 'e']
attacks = [['a', 'b'], ['c', 'b'], ['c', 'd'], ['d', 'c'], ['d', 'e'], ['e', 'e']]
#attacks = [('a', 'b'), ('c', 'b'), ('c', 'd'), ('d', 'c'), ('d', 'e'), ('e', 'e')]

preferred(arguments, attacks)
