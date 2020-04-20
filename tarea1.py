# Programa para recibir una expresion regular
# convertirlo en un NFA y ese NFA convertirlo
# a un DFA y recibir un string para comprobar si
# existe en el lenguaje definido por el regex

# Luis Fernando Carrasco A01021172
# Daniel Pelagio A01227873
# José Luis García Reymundo A01063645


from PySimpleAutomata import automata_IO
from PySimpleAutomata import DFA
from PySimpleAutomata import NFA
import json
import os
from time import sleep
import nfa as rgx

path = os.path.dirname(os.path.abspath(__file__)) + '/'

class Quintuple:
    def __init__(self, alphabet, states, final_states, initial_state, transition_matrix):
        self.alphabet = alphabet
        self.states = states
        self.final_states = final_states
        self.initial_state = initial_state
        self.transition_matrix = transition_matrix


# This functions reads a file with the regex, and will return a list with lists of 3 elements (regex, alphabet and tokens)
def readExpression(file_name):
    pth = path + file_name
    f=open(pth, "r")
    rules = []

    if(f.mode == 'r'):
        listLines = f.readlines()
        print(listLines)
        cont = 0
        for line in listLines:
            if cont == 0:
                alphabet = line.strip()
                alphabet_list = alphabet.split(" ")
                alphabet_list[len(alphabet_list)-1] = alphabet_list[len(alphabet_list)-1].rstrip('\n')
                cont += 1
            elif cont == 1:
                regex = line.strip()
                regex = regex.rstrip('\n')
                cont += 1
            elif cont == 2:
                token = line.strip()
                token = token.rstrip('\n')
                cont = 0
                rules.append([alphabet_list, regex, token])

    return rules


# function (list, list, list, list, matrix)
# q0: 0: [q0, q1], 1: [q1, q2], eps: [q1, q2, q3]
# q1: 0: [q0], 1: [q1, q2], eps: []
# q2: 0: [q1], 1: [], eps: [q1, q2, q3]
# q3: 0: [q0, q1], 1: [q1], eps: [q1, q2, q3]


def nfa2dfa(NFA):    
    # First we neeed initial state prime, obtained by doing e-closure on the initial state
    initial_state_prime = e_closure(NFA, NFA.initial_state)

    # The alphabet remains the same
    alphabet = NFA.alphabet 

    # We obtain the DFA states from the function move, and also pass the transition table as an argument (the function modifies it as a pointer)
    transition_prime = {}
    states_prime = move(NFA, initial_state_prime, alphabet, transition_prime)

    # We obtain the final states from the DFA
    final_states_prime = get_final_states(NFA, states_prime)

    # Finally we set up the complete DFA and return it after
    DFA = Quintuple(alphabet, states_prime, final_states_prime, initial_state_prime, transition_prime)

    return DFA # this is a new quituple without epsilon moves


def get_final_states(NFA, states_prime):  # function that resolves the final states of the DFA according to NFA's final states
    final_states = []
    for i in states_prime:  # for each state of the DFA
        for x in NFA.final_states:  # and each state from the final list of states in NFA
            if x in i:  # if the DFA state has final state from NFA
                final_states.append(i)  # added to final list of states DFA

    return final_states


def e_closure(NFA, state):  # function that gets the e closure method from the state given
    new_set_states = []
    new_set_states.append(state)  # always adds the given state as a first state

    for i in new_set_states:  # for that does eclosure for every state in the list, included new added elements
        if i in NFA.transition_matrix: # Check if the state has epsion moves
            if NFA.transition_matrix[i]['eps']:  # if there exists epsilon moves for that state
                for j in NFA.transition_matrix[i]['eps']:  # for each state in the list of states that the NFA's transition tables has
                    if j not in new_set_states:  # if it does not exist already in the list, it's added
                        new_set_states.append(j)

    return new_set_states


# Returns the DFA states and modifies the given attribute of transition prime 
def move(NFA, initial_state_prime, alphabet, transition_prime):
    DFA_states = []
    DFA_states.append(initial_state_prime)
    hand_list = []
    # transition_prime = {}
    
    for current_state in DFA_states:
        transition_prime[str(current_state)] = {}

        for symbol in alphabet:
            # print('all states', DFA_states)
            hand_list = []
            for state_element in current_state:
                
                if state_element in NFA.transition_matrix:
                    # Check if the symbol of the alphabet exists in the transition matrix
                    if symbol in NFA.transition_matrix[state_element]:
                        hand_list = list(set(hand_list) | set(NFA.transition_matrix[state_element][symbol]))

            if all(isinstance(elem, list) for elem in hand_list):
                # Get the lists where you can go with the symbol, but flatten then to have a lists of strings  
                flatten_list = [item for sublist in hand_list for item in sublist]

            else:
                flatten_list = hand_list

            # For each string of that new flattened lists 
            for item in flatten_list:
                # Make a new list with the closure of each element
                hand_list = list(set(hand_list) | set(e_closure(NFA, item)))
            
            if all(isinstance(elem, list) for elem in hand_list):        
                # Then flatten that new list again
                flatten_list = [item for sublist in hand_list for item in sublist]
            else:
                flatten_list = hand_list
            
            # Remove duplicate lists on the states list
            if checkList(DFA_states, flatten_list) == False:
                if flatten_list != []:  #  checks if the list to add as a state is empty, so it is not added
                    DFA_states.append(flatten_list)
            
            if checkList(DFA_states, flatten_list) == False:  # if it is a new state, added to the transition table
                transition_prime[str(current_state)][symbol] = flatten_list
            else:  # else if it already exists
                for i in DFA_states:  # check which state it is and add the state in the right order, so  there are no duplicates in different order 
                    if set(i) == set(flatten_list):
                        transition_prime[str(current_state)][symbol] = i

    # print(DFA_states)
    return DFA_states


def checkList(DFA_states, list2):  # function that checks if a list of list has a given list
    same = False  # returns false in case there is none
    for i in DFA_states:
        if set(i) == set(list2):
            same = True  # returns true in case there is one that is the same (same elements, no order matters)
            break
    return same


def drawAutomataNFA(NFA_, name_file):
    transitions = []
    alphabet_ = []
    alphabet_ = NFA_.alphabet.copy()
    alphabet_.append('eps')
    for state in NFA_.states:
        for symbol in alphabet_:

            # Check first if the key exists (symbol in the alphabet)
            if symbol in NFA_.transition_matrix[str(state)]:

                # Then check if there is anything in the list 
                if NFA_.transition_matrix[str(state)][symbol]:
                    print(NFA_.transition_matrix[str(state)][symbol])
                    cont = 0
                    for trans in NFA_.transition_matrix[str(state)][symbol]:
                        str_ = ''
                        # print(NFA_.transition_matrix[str(state)][symbol][cont])
                        str_ = NFA_.transition_matrix[str(state)][symbol][cont]
                        transitions.append([str(state), symbol, str_])
                        cont+=1

    json_ = {
        "alphabet": alphabet_,
        "states": NFA_.states,
        "initial_states": [NFA_.initial_state],
        "accepting_states": NFA_.final_states,
        "transitions": transitions
    }

    json_nfa = json.dumps(json_)

    try:
        f=open(name_file, "w")
        f.write(json_nfa)
        f.close()

    except:
        f.close()

    finally:
        nfa_example = automata_IO.nfa_json_importer(name_file)
        automata_IO.nfa_to_dot(nfa_example, 'nfa-output', path)
        print(json_nfa)
    print("Checa el NFA como una cincotupla en el archivo con el nombre nfa.json\n")
    print("Checa la imagen del grafo, con el nombre nfa-output.dot.svg.\n")

    return json_nfa 


def drawAutomata(DFA_, name_file):
    transitions = []
    for state in DFA_.states:
        for symbol in DFA_.alphabet:
            if str(DFA_.transition_matrix[str(state)][symbol]) != '[]':
                transitions.append([str(state), symbol, str(DFA_.transition_matrix[str(state)][symbol])])

    states_strings = []
    for i in DFA_.states:
        states_strings.append(str(i))

    final_states_strings = []
    for i in DFA_.final_states:
        final_states_strings.append(str(i))

    json_ = {
        "alphabet": DFA_.alphabet,
        "states": states_strings,
        "initial_state": str(DFA_.initial_state),
        "accepting_states": final_states_strings,
        "transitions": transitions
    }

    json_dfa = json.dumps(json_)

    try:
        f=open(name_file, "w")
        f.write(json_dfa)
        f.close()

    except:
        f.close()

    finally:
        dfa_example = automata_IO.dfa_json_importer(name_file)
        automata_IO.dfa_to_dot(dfa_example, 'dfa-output', path)
    print("Checa el DFA como una cincotupla en el archivo con el nombre dfa.json\n")
    print("Checa la imagen del grafo, con el nombre dfa-output.dot.svg.\n")

    return json_dfa 


def checkString(DFA, string, NFA_list):
    answer = 'invalid'
    current_state = DFA.initial_state

    for element in string:
        print("current: ", current_state)
        print("element: ", element)
        # Check if the symbol exists, so dict doesnt break 
        if element in DFA.transition_matrix[str(current_state)]:
            if DFA.transition_matrix[str(current_state)][element]:
                current_state = DFA.transition_matrix[str(current_state)][element]
            else:
                current_state = 'invalid'
                answer = 'invalid_syntax'
                break

        else:
            current_state = 'invalid'
            answer = 'symbol_not_recognized: "' + element + '"'
            break
    
    for final in DFA.final_states:
        if current_state == final:
            answer =checkTokenType(NFA_list, current_state)
            return answer

    return answer                                    


def checkTokenType(NFA_list, state_list):
    for state in state_list:
        tkn = []
        tkn = str(state).split('_')
        if state in NFA_list[tkn[1]].final_states:
            return tkn[1]
    
    return 'invalid'


def checkInput(entrada, DFA, NFA_list):
    f=open(path+'programa.o.txt', "w")
    
    for elem in entrada:
        if(f.mode == 'w'):
            if elem == '':
                f.write('\n')
            else:
                token = checkString(DFA, elem, NFA_list)
                f.write(token + ' ')

    f.close()
                                            
def main():
    alphabet = []
    regex = ''
    table = {}
    while True:
        try:
            file_name = input("Escribe el nombre del archivo que tiene el alfabeto y la expresion regular a analizar.\n")
            rules = readExpression(file_name)
            # alphabet = readExpression(file_name)[0]
            # regex = readExpression(file_name)[1]
            break

        except:
            print("El archivo introducido no existe!\n")

    NFA_list = {} # A dict where each key is the token type, and the value is the Quintuple

    # For each rule in the rules list, create a Quintuple object and append it to the list
    for rule in rules:
        regex = rule[1]
        alphabet = rule[0]
        token = rule[2]
        nfa_temp = []
        nfa_temp = rgx.regexToNFA(regex, alphabet, token)
        temp = None
        print("CACA: ", nfa_temp[3])
        temp = Quintuple(alphabet[:-1], nfa_temp[1], nfa_temp[2], nfa_temp[3], nfa_temp[4])
        NFA_list[token] = temp

    # print(NFA_list[0][0].transition_matrix)
    # print(NFA_list[1][0].transition_matrix)

    merged_alphabets = set()
    merged_states = []
    merged_dict = {}
    merged_final_states = []
    merged_initial = []

    for token in NFA_list:
        merged_dict.update(NFA_list[token].transition_matrix)
        for symbol in NFA_list[token].alphabet:
            merged_alphabets.add(symbol)
        
        for state in NFA_list[token].states:
            merged_states.append(state)

        for final in NFA_list[token].final_states:
            merged_final_states.append(final)

        print("SDFSDF: ", NFA_list[token].initial_state)
        merged_initial.append(NFA_list[token].initial_state)

    merged_states.append('INIT')
    merged_dict['INIT'] = {}
    merged_dict['INIT']['eps'] = merged_initial

    merged_nfa = Quintuple(list(merged_alphabets), merged_states, merged_final_states, 'INIT', merged_dict)
    merged_dfa = nfa2dfa(merged_nfa)

    # drawAutomata(merged_dfa, "dfa.json")
    print(checkString(merged_dfa, "1001", NFA_list))
    # drawAutomataNFA(merged_nfa, "nfa.json")

    f=open(path+'programa.txt', "r")

    if(f.mode == 'r'):
        data = f.readlines()
    
    f.close()

    str_data = []
    temp = []
    for i in data:
        for x in i.split(' '):
            temp = []
            if '\n' in x:
                temp = x.split('\n')
                str_data.append(temp[0])
                str_data.append(temp[1])
            else:
                str_data.append(x)

    checkInput(str_data, merged_dfa, NFA_list)
    print(str_data)


if __name__=="__main__":
    main()
