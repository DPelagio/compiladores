class AbstractAutomata(object):

    def __init__(self, initial_state: int, final_states: list, state_table: list):
        self.initial_state = 0
        self.final_states = final_states
        self.state_table = state_table
    
    def getState(self, actual_state: int, symbol: str) -> int:
        pass
    
    def recognizeToken(self, inputStr: str) -> bool:
        pass
    
    def _recognizeBase(self, inputStr: str) -> bool:
        n = 0
        c = inputStr[n]
        n += 1
        while n <= len(inputStr):
            self.initial_state = self.getState(self.initial_state, c)

            if self.initial_state != -1 and n < len(inputStr):
                c = inputStr[n]
                n += 1
            else:
                break
        
        for i in range(0, len(self.final_states)):
            if self.final_states[i] == self.initial_state:
                self.initial_state = 0
                return True
        self.initial_state = 0
        return False

class Digit(AbstractAutomata):

    def __init__(self, final_states: list, state_table: list):
        AbstractAutomata.__init__(self, 0, final_states, state_table)
    
    def recognizeToken(self, inputStr):
        return self._recognizeBase(inputStr)
    
    def getState(self, actual_state, symbol):
        switcher = {
            '0': 0,
            '1': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9
        }
        result = switcher.get(symbol, -1)
        return self.state_table[actual_state][result] if result != -1 else result
        

class DecimalNumber(AbstractAutomata):
    
    def __init__(self, final_states: list, state_table: list):
        AbstractAutomata.__init__(self, 0, final_states, state_table)
    
    def recognizeToken(self, inputStr):
        return self._recognizeBase(inputStr)
    
    def getState(self, actual_state, symbol):
        switcher = {
            '0': 0,
            '1': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '.': 10
        }
        result = switcher.get(symbol, -1)
        return self.state_table[actual_state][result] if result != -1 else result

if __name__ == '__main__':
    # Digito
    F_Digit = [1]
    Table_Digit = [[1,1,1,1,1,1,1,1,1,1],
                    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
    ]
    digit = Digit(F_Digit, Table_Digit)
    digit_value = '1'
    validate = digit.recognizeToken(digit_value)
    print(f"{digit_value} es {validate}")
    
    # Decimal
    F_Decimal = [3]
    Table_Decimal = [[1,1,1,1,1,1,1,1,1,1,-1], 
                    [1,1,1,1,1,1,1,1,1,1,2],
                    [3,3,3,3,3,3,3,3,3,3,-1],
                    [3,3,3,3,3,3,3,3,3,3,-1]
    ]
    decimal = DecimalNumber(F_Decimal, Table_Decimal)
    decimal_value = '3.12'
    validate_decimal = decimal.recognizeToken(decimal_value)
    print(f"{decimal_value} es {validate_decimal}")