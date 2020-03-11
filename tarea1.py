# Programa para recibir una expresion regular
# convertirlo en un NFA y ese NFA convertirlo
# a un DFA y recibir un string para comprobar si
# existe en el lenguaje definido por el regex
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
    print(alphabet_list, regex)

def regex2nfa(alphabet, regex):

    return quintuple

# function (list, list, list, list, matrix)
def nfa2dfa(quintuple):
    return new_quintuple

def main():
    readExpression('test.txt')

if __name__=="__main__":
    main()