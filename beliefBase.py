from sympy.logic.boolalg import Not, to_cnf
from itertools import combinations
from inferenceEngine import InferenceEngine

# Need to instantiate the inferenceEngine to use its methods
engine = InferenceEngine()


class Belief:
    '''
    Consists of a belief/formula and a priority (higher = more important)
    '''
    def __init__(self, formula, priority:int):
        self.formula = formula
        self.priority = priority

    def __str__(self):
        return f"{self.formula} (p={self.priority})"
    
    def __eq__(self, other):
        return isinstance(other, Belief) and self.formula == other.formula and self.priority == other.priority

    def __hash__(self):
        return hash((self.formula, self.priority))


class BeliefBase:
    '''
    Has a list of belief objects as its memory.\n
    Uses weak partial meet contraction to update'''
    def __init__(self):
        self.beliefs = []


    def add(self, belief, priority=1):
        '''
        Add a new belief to the belief base
        '''
        
        # Handle duplicates first by updating to the highest priority value 
        # among contenders to that given belief
        for b in self.beliefs:
            if b.formula == belief:
                old_priority = b.priority
                b.priority = max(b.priority, priority)
                print(f"Updated priority: {belief} ({old_priority} → {b.priority})")
                return

        belief = Belief(belief, priority)

        # If the belief is already implied by current beliefs, skip
        if engine.entails([b.formula for b in self.beliefs], belief.formula):
            print("Belief already entailed. Skipping")
            return

        # If the negated belief is implied by current beliefs then revise
        elif engine.entails([b.formula for b in self.beliefs],Not(belief.formula)):
            self.revise(belief)

        # Append belief is no conflict and not implied
        else:
            self.beliefs.append(belief)
            return

    def is_consistent(self):
        '''
        Check if the beliefs in the beliefBase is consistent'''
        clauses = []
        for b in self.beliefs:
            cnf = to_cnf(b.formula)
            clauses.extend(engine.extract_clauses(cnf))

        return not engine.resolution_unsat(clauses)


    def revise(self, belief):
        # Contract
        self.contract(Not(belief.formula))

        # EXPAND
        self.beliefs.append(belief)

    # weak partial meet contraction
    def contract(self, belief_formula):
        """
        Remove beliefs until belief_formula is no longer entailed.
        Uses priority (low priority removed first).
        """
        remainders = self.generate_remainders(belief_formula)

        if not remainders:
            self.beliefs = []
            return
            
        # choose best remainder
        best = self.select_best_remainder(remainders)

        removed = set(self.beliefs) - set(best)
        for r in removed:
            print(f"Contract removed: {r}")

        self.beliefs = best


    def generate_remainders(self, belief_formula):
        '''
        Creating remainders prioritizing maximum size'''
        remainders = []
        n = len(self.beliefs)

        # Try all subset sizes (largest first = maximal subsets)
        for size in range(n, -1, -1):
            # This will grow exponentially 2^n
            for subset in combinations(self.beliefs, size):
                formulas = [b.formula for b in subset]

                if not engine.entails(formulas, belief_formula):
                    remainders.append(list(subset))

            # Stop early to keep only maximal ones
            if remainders:
                break

        return remainders
    
    def select_best_remainder(self, remainders):
        """
        Choose the remainder that preserves the highest total priority.
        """

        def score(remainder):
            return sum(b.priority for b in remainder)

        # pick remainder with highest score, ties will go to largest amount of beliefs in set 
        best = max(
            remainders,
            key=lambda r: (sum(b.priority for b in r), len(r))
        )

        return best

    # To show the current beliefBase
    def __str__(self):
        string:str = "BeliefBase content:\n"
        for belief in self.beliefs:
            string += str(belief) + "\n"
        return string
    


