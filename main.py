from revision import symbol_table, parse_formula

# Gonna fix this later to only import the correct stuff

# List of user beliefs as a believeSet
beliefSet =[]

userInput = ""

print("Please input desired believes.\nEach line is its own belief.\nFinish input by writing \"DONE\"\n")

# Add multiple things to the belief set
while userInput != "DONE":
    # Take input
    userInput = input("Please type input:")

    if userInput == "DONE":
        break
    # Convert to Sympy object and add to the beliefSet
    beliefSet.append(parse_formula(userInput))

print(f'Belief-set: {beliefSet}')

print(f'Symbol Table: {symbol_table}')

# Convert input to CNF

# Convert base to CNF

# Check for contradiction and work towards expansion

# 1. Convert input to CNF 
# 2. Convert belief base to CNF 
# 3. Update belief according to logical 