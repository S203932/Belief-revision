from revision import symbol_table, parse_formula
from beliefBase import BeliefBase

# BeliefBase 
beliefBase:BeliefBase = BeliefBase()

# At the moment you can only add, later also add contraction

userInput = ""

print("Please input desired believes.\nEach line is its own belief.\nFinish input by writing \"DONE\"\n")

# User input to contiously add new beliefs
while userInput != "DONE":
    # Take input
    userInput = input("Please type input:")

    if userInput == "DONE":
        break

    beliefBase.add(parse_formula(userInput))

    print(beliefBase)

    print(f'Symbol Table: {symbol_table}')


#Final state

print(beliefBase)

print(f'Symbol Table: {symbol_table}')