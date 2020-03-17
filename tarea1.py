# Programa para recibir una expresion regular
# convertirlo en un NFA y ese NFA convertirlo
# a un DFA y recibir un string para comprobar si
# existe en el lenguaje definido por el regex
# Luis Fernando Carrasco A01021172
# Daniel Pelagio A01227873
# Jose Luis 

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
                DFA_states.append(flatten_list)
            #print("DFA states: ", DFA_states)
            
            transition_prime[str(current_state)][symbol] = flatten_list
    print(DFA_states)
    return DFA_states


def checkList(DFA_states, list2):  # function that checks if a list of list has a given list
    same = False  # returns false in case there is none
    for i in DFA_states:
        if set(i) == set(list2):
            same = True  # returns true in case there is one that is the same (same elements, no order matters)
            break
    return same


def main():
    readExpression('test.txt')
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

    NFA = Quintuple(alphabet, states, final_states, '1', table)
    DFA = nfa2dfa(NFA)
    print('Initial state prime = ', DFA.initial_state)
    print('Alphabet = ', DFA.alphabet)
    print('DFA states = ', DFA.states)
    print('DFA transition table = ', DFA.transition_matrix)
    print('DFA final states = ', DFA.final_states)


if __name__=="__main__":
    main()