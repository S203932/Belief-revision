from sympy import symbols,Basic, true, false
from sympy.logic.boolalg import And, Or, Not, Implies, Equivalent, to_cnf
from sympy.parsing.sympy_parser import parse_expr
import re
from revision import symbol_table, parse_formula

from inferenceEngine import InferenceEngine

engine = InferenceEngine()


class BeliefBase:
    def __init__(self):
        self.beliefs = []

    def add(self, belief):
        '''
        Add a new belief to the belief base
        '''

        # If the belief is already implied by current beliefs, skip
        if engine.entails(self.beliefs,belief):
            print("Belief already entailed. Skipping")
            return

        # If the negated belief is implied by current beliefs then revise
        elif engine.entails(self.beliefs,Not(belief)):
            self.revise(belief)

        # Append belief is no conflict and not implied
        else:
            self.beliefs.append(belief)
            return

    def is_consistent(self):
        clauses = []
        for b in self.beliefs:
            cnf = to_cnf(b)
            clauses.extend(engine.extract_clauses(cnf))

        return not engine.resolution_unsat(clauses)

    # The AGM just uses FIFO at the moment, needs to be improved
    def revise(self, belief):
        
        self.beliefs.append(belief)

        while not self.is_consistent() and self.beliefs:
            self.beliefs.pop(0)

    # To show the current beliefBase
    def __str__(self):
        string:str = "BeliefBase content:\n"
        for belief in self.beliefs:
            string += str(belief) + "\n"
        return string