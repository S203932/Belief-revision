from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr
import re


# This class is for all the methods needed for the revision
# Using Sympy objects to express the beliefs -> the expressions

# All known symbols will be stored in here
symbol_table = {}

def extract_symbols(expression:str):
    '''
    Find all words or single letters and put them in a list
    '''
    return set(re.findall(r"[A-Za-z]+", expression))


def get_symbol(name:str):
    '''
    Check if the name is a known symbol and otherwise add it to known symbols.
    '''
    if name not in symbol_table:
        symbol_table[name] = symbols(name)
    return symbol_table[name]


def preprocess(expression:str):
    '''
    Make sure implies and biconditional is properly understood. 
    Can be "->" or ">>".
    Can be "<->" or "=="
    '''
    expression = expression.replace("<->", "==")
    expression = expression.replace("->", ">>")

    return expression



def parse_formula(expr_str:str):
    '''
    Parsing the user input into a 
    '''
    expr_str = preprocess(expr_str)
    
    # Local dictionary based on input
    local_dict = {name: get_symbol(name) for name in extract_symbols(expr_str)}
    
    # Using sympy to parse the string into an expression to use for computation
    expr = parse_expr(expr_str, local_dict=local_dict, evaluate=False)
    
    return expr