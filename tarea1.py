# Programa para recibir una expresion regular
# convertirlo en un NFA y ese NFA convertirlo
# a un DFA y recibir un string para comprobar si
# existe en el lenguaje definido por el regex
# Luis Fernando Carrasco A01021172
# Daniel Pelagio A01227873
# Jose Luis 
from PySimpleAutomata import automata_IO
from PySimpleAutomata import DFA
from PySimpleAutomata import NFA
import json
import os
from time import sleep

path = os.path.dirname(os.path.abspath(__file__)) + '/'

class Quintuple:
    def __init__(self, alphabet, states, final_states, initial_state, transition_matrix):
        self.alphabet = alphabet
        self.states = states
        self.final_states = final_states
        self.initial_state = initial_state
        self.transition_matrix = transition_matrix


def readExpression(file_name):
    f=open(file_name, "r")

    if(f.mode == 'r'):
        alphabet = f.readline()
        regex = f.readline()

    alphabet_list = alphabet.split(" ")
    alphabet_list[len(alphabet_list)-1] = alphabet_list[len(alphabet_list)-1].rstrip('\n')
    # print(alphabet_list, regex)


def regex2nfa(alphabet, regex):

    return NFA


# function (list, list, list, list, matrix)
# q0: 0: [q0, q1], 1: [q1, q2], ?: [q1, q2, q3]
# q1: 0: [q0], 1: [q1, q2], ?: []
# q2: 0: [q1], 1: [], ?: [q1, q2, q3]
# q3: 0: [q0, q1], 1: [q1], ?: [q1, q2, q3]


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
        if NFA.transition_matrix[i]['?']:  # if there exists epsilon moves for that state
            for j in NFA.transition_matrix[i]['?']:  # for each state in the list of states that the NFA's transition tables has
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
                hand_list = list(set(hand_list) | set(NFA.transition_matrix[state_element][symbol]))

            # Get the lists where you can go with the symbol, but flatten then to have a lists of strings  
            flatten_list = [item for sublist in hand_list for item in sublist]

            # For each string of that new flattened lists 
            for item in flatten_list:
                # Make a new list with the closure of each element
                hand_list = list(set(hand_list) | set(e_closure(NFA, item)))
                
            # Then flatten that new list again
            flatten_list = [item for sublist in hand_list for item in sublist]
            
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


def drawAutomata(DFA_, name_file):
    transitions = []
    for state in DFA_.states:
        for symbol in DFA_.alphabet:
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
    # print(json_dfa)

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

def checkString(DFA, string):
    answer = 'Not valid string'
    current_state = DFA.initial_state

    for element in string:
        # print("Current state: ", current_state)
        # print("Symbol: ", element)
        if DFA.transition_matrix[str(current_state)][element]:
            current_state = DFA.transition_matrix[str(current_state)][element]
        else:
            for final in DFA.final_states:
                if current_state == final:
                    answer = 'Valid string for language'
                    return answer
    
    for final in DFA.final_states:
        if current_state == final:
            answer = 'Valid string for language'
            return answer

    return answer                                    
                                                          
def main():
    while True:
        try:
            file_name = input("Escribe el nombre del archivo que tiene el alfabeto y la expresion regular a analizar.\n")
            readExpression(file_name)
            break
        except:
            print("El archivo introducido no existe!\n")

    alphabet = ['a', 'b', 'c']
    states = ['1', '2', '3', '4', '5', '6', '7', '8']
    final_states = ['4']
    table = {
        '1': {'a': [], 'b': [], 'c': [], '?': ['2', '5']}, 
        '2': {'a': ['3'], 'b': [], 'c': [], '?': []},
        '3': {'a': [], 'b': [], 'c': ['4'], '?': []}, 
        '4': {'a': [], 'b': [], 'c': [], '?': []},
        '5': {'a': [], 'b': [], 'c': [], '?': ['6', '7']},
        '6': {'a': ['8'], 'b': [], 'c': [], '?': []},
        '7': {'a': [], 'b': ['8'], 'c': [], '?': []},
        '8': {'a': [], 'b': [], 'c': [], '?': ['1']}
    }
    option = '0'
    while option != '4':
        option = input("Elija una opcion.\n1. Obtener NFA.\n2. Obtener DFA.\n3. Probar una cadena.\n4. Salir.\n")
        if option == '1':
            NFA = Quintuple(alphabet, states, final_states, '1', table)
        elif option == '2':
            NFA = Quintuple(alphabet, states, final_states, '1', table)
            DFA_US = nfa2dfa(NFA)
            drawAutomata(DFA_US, "dfa.json")
        elif option == '3':
            NFA = Quintuple(alphabet, states, final_states, '1', table)
            DFA_US = nfa2dfa(NFA)
            string_ = input("Escriba la cadena a probar: \n")
            print(checkString(DFA_US, string_))
        elif option != '4':
            print("Por favor, elige una opcion valida!\n")


if __name__=="__main__":
    main()
