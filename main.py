from revision import symbol_table, parse_formula
from beliefBase import BeliefBase

# BeliefBase object 
beliefBase:BeliefBase = BeliefBase()

userInput = ""

print("Please input desired believes.\nEach line is its own belief followed by priority(comma seperation).\nFinish input by writing \"DONE\"\n")

# User input to contiously add new beliefs
while userInput != "DONE":
    # Take input
    userInput = input("Please type input:")

    if userInput == "DONE":
        break
    
    # Belief is composed of formula and priority, they're comma separated
    formula_str, priority_str = userInput.split(",")

    #Parsing is done by revision class
    beliefBase.add(parse_formula(formula_str.strip()), int(priority_str.strip()))

    # Showing the outcome
    print(beliefBase)

    #Showing symbols being used
    print(f'Symbol Table: {symbol_table}')


#Final state when ending the program

print(beliefBase)

print(f'Symbol Table: {symbol_table}')