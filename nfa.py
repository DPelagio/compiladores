import collections

transitions=[]
initialStack=[]
finalStack=[]

class Node:
    def __init__(self, out, value):
        self.out = out
        self.value = value

    def __repr__(self):
        return repr((self.value, self.out))

class CharNode(Node):
    """sub clase nodo caracter"""

class OperatorNode(Node):
    """sub clase nodo operador"""

class EOLNode(Node):
    """sub clase nodo fin"""

class OrderedSet:
    def __init__(self, seq=()):
        self._list = list(seq)
        self._set = set(seq)

    def __iter__(self):
        return iter(self._list)

    def __contains__(self, item):
        return item in self._set

    def put(self, item):
        if item in self._set:
            return
        self._list.append(item)
        self._set.add(item)

    def clear(self):
        self._list = []
        self._set = set()

CONCATENATE = '.'
ZERO_OR_MORE = '*'
ZERO_OR_ONE = '?'
ONE_OR_MORE = '+'
ALTERNATE = '|'
PAR_OPEN = '('
PAR_CLOSE = ')'
RIGHT = 0
LEFT = 1
EOL = EOLNode(out=[], value='EOL')

Operator = collections.namedtuple(
    'Operator',
    [
        'precedence',
        'associativity'
    ]
)

Operators = {
    ZERO_OR_MORE: Operator(precedence=5, associativity=RIGHT),
    CONCATENATE: Operator(precedence=4, associativity=LEFT),
    ALTERNATE: Operator(precedence=3, associativity=LEFT)
}

def hasPrecedence(a: str, b: str) -> bool:
    return ((Operators[b].associativity == RIGHT and
             Operators[b].precedence < Operators[a].precedence) or
            (Operators[b].associativity == LEFT and
             Operators[b].precedence <= Operators[a].precedence))

def popGreaterThan(ops: list, op: str) -> list:
    out = []
    while (ops and ops[-1] in Operators and hasPrecedence(ops[-1], op)):
        out.append(ops.pop())
    return out

def popUntilGroupStart(ops: list) -> list:
    out = []
    while True:
        op = ops.pop()
        if op == PAR_OPEN:
            break
        out.append(op)
    return out

def reversePolish(expression: str) -> str:
    output = []
    operators = []
    for char in expression:
        if char == PAR_OPEN:
            operators.append(char)
            continue
        elif char == PAR_CLOSE:
            output.extend(popUntilGroupStart(operators))
            continue
        elif char in Operators:
            output.extend(popGreaterThan(operators, char))
            operators.append(char)
            continue
        output.append(char)
    output.extend(reversed(operators))
    return ''.join(output)

def concatenate(expression: str, join=CONCATENATE) -> str:
    output = []
    atoms_count = 0
    for char in expression:
        if char == PAR_OPEN:
            if atoms_count:
                output.append(join)
            output.append(char)
            atoms_count = 0
            continue
        elif char in (PAR_CLOSE, ALTERNATE):
            output.append(char)
            atoms_count = 0
            continue
        elif char in (ZERO_OR_MORE, ONE_OR_MORE, ZERO_OR_ONE):
            output.append(char)
            atoms_count += 1
            continue
        atoms_count += 1
        if atoms_count > 1:
            output.append(join)
            atoms_count = 1
        output.append(char)
    return ''.join(output)

def combine(origin_state: Node, target_state, visited=None):
    visited = visited or set()
    if origin_state in visited:
        return
    
    visited.add(origin_state)
    for i, state in enumerate(origin_state.out):
        if state is EOL:
            origin_state.out[i] = target_state
        else:
            combine(state, target_state, visited)

def NFA(expression):
    states = []
    for char in expression:
        if char not in Operators: # * . |
            states.append(CharNode(out=[EOL], value=char))
            continue
        elif char == CONCATENATE:
            state_b = states.pop()
            state_a = states.pop()
            combine(state_a, state_b)
            states.append(state_a)
            continue
        elif char == ALTERNATE:
            state_b = states.pop()
            state_a = states.pop()
            states.append(OperatorNode(out=[state_a, state_b], value=char))
            continue
        elif char == ZERO_OR_MORE:
            state = states.pop()
            new_state = OperatorNode(out=[state, EOL], value=char)
            combine(state, new_state)
            states.append(new_state)
            continue
    return states[0]

def union(initial, final):
    initial1 = initialStack.pop()
    initial2 = initialStack.pop()
    final1 = finalStack.pop()
    final2 = finalStack.pop()
    transitions.append([str(initial),'?',str(initial1)])
    transitions.append([str(initial),'?',str(initial2)])
    transitions.append([str(final1),'?',str(final)])
    transitions.append([str(final2),'?',str(final)])
    initialStack.append(initial)
    finalStack.append(final)

def kleene(initial, final):
    initial1 = initialStack.pop()
    final1 = finalStack.pop()
    transitions.append([str(initial),'?',str(final)])
    transitions.append([str(initial),'?',str(initial1)])
    transitions.append([str(final1),'?',str(initial1)])
    transitions.append([str(final1),'?',str(final)])
    initialStack.append(initial)
    finalStack.append(final)

def posit(initial, final):
	initial1 = initialStack.pop()
	final1 = finalStack.pop()
	transitions.append([str(initial),'?',str(initial1)])
	transitions.append([str(final1),'?',str(initial1)])
	transitions.append([str(final1),'?',str(final)])
	initialStack.append(initial)
	finalStack.append(final)

def concatenation():
    initial1 = initialStack.pop()
    initial2 = initialStack.pop()
    final1 = finalStack.pop()
    final2 = finalStack.pop()
    for i in transitions:
        if i[0] == str(initial1):
            i[0] = str(final2)
    
    initialStack.append(initial2)
    finalStack.append(final1)

def Thompson(expression):
    count = 0
    count2 = 1
    for char in expression:
        if char not in Operators:
            transitions.append([str(count), char,str(count2)])
            initialStack.append(count)
            finalStack.append(count2)
            count = count + 2
            count2 = count2 + 2
        elif char == ZERO_OR_MORE:
            kleene(count, count2)
            count = count + 2
            count2 = count2 + 2
        elif char == ALTERNATE:
            union(count, count2)
            count = count + 2
            count2 = count2 + 2
        elif char == ONE_OR_MORE:
            posit(count, count2)
            count = count + 2
            count2 = count2 + 2
        elif char == CONCATENATE:
            concatenation()
    return transitions

def isMatch(states: OrderedSet) -> bool:
    return EOL in states

def putState(state, states):
    if state in states:
        return
    elif state is EOL:
        states.put(EOL)
        return
    elif isinstance(state, CharNode):
        states.put(state)
        return
    for s in state.out:
        putState(s, states)

def validator(state, value) -> bool:
    curr_list = OrderedSet()
    next_list = OrderedSet()
    putState(state, curr_list)
    
    for char in value:
        if not curr_list:
            break
        for curr_state in curr_list:
            if char != curr_state.value:
                continue
            for next_state in curr_state.out:
                putState(next_state, next_list)
        curr_list, next_list = next_list, curr_list
        next_list.clear()
    return isMatch(curr_list)

def compileRegex(expression: str):
    return NFA(reversePolish(concatenate(expression)))

def regexToNFA(expression: str, alphabet: list):
    matrix = Thompson(reversePolish(concatenate(expression)))
    bluePill = {}
    for item in matrix:
        bluePill.setdefault(item[0], {}).setdefault(item[1], []).append(item[2])
    
    for item in bluePill:
        for char in alphabet:
            if not char in bluePill[item]:
                bluePill[item][char] = []
    
    return [alphabet, list(bluePill), list(map(str, finalStack)), str(initialStack.pop()), bluePill]