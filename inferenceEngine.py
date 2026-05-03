from sympy.logic.boolalg import And, Or, Not, to_cnf

class InferenceEngine:
    
    def entails(self, beliefs, belief):
        # Negate the formula
        negated = Not(belief)

        clauses = []

        # Add all beliefs + negated formula
        for b in beliefs + [negated]:
            cnf = to_cnf(b)
            clauses.extend(self.extract_clauses(cnf))

        # If contradiction that means it entails
        return self.resolution_unsat(clauses)

    def extract_clauses(self,expr):
        clauses = []

        if isinstance(expr, And):
            for arg in expr.args:
                clauses.extend(self.extract_clauses(arg))

        elif isinstance(expr, Or):
            clause = set()

            for arg in expr.args:
                if isinstance(arg, Or):
                    clause.update(arg.args)
                else:
                    clause.add(arg)

            clauses.append(clause)

        else:
            clauses.append({expr})

        return clauses
    
    def resolution_unsat(self,clauses):
        '''
        returns True if unsatisfiable (contradiction found)
        '''

        # Use frozenset so clauses can be stored in a set
        clauses = set(frozenset(c) for c in clauses)

        while True:
            new = set()

            clause_list = list(clauses)

            for i in range(len(clause_list)):
                for j in range(i + 1, len(clause_list)):
                    c1 = clause_list[i]
                    c2 = clause_list[j]

                    resolvents = self.resolve(set(c1), set(c2))

                    if frozenset() in resolvents:
                        return True  # UNSAT

                    new.update(resolvents)

            # No clauses means no contradiction
            if new.issubset(clauses):
                return False  # satisfiable

            clauses.update(new)


    def resolve(self,c1, c2):
        """
        Generate all resolvents between two clauses.
        Each clause is a set of literals.
        """
        resolvents = []

        for lit in c1:
            neg = self.negate_literal(lit)

            if neg in c2:
                new_clause = (c1 - {lit}) | (c2 - {neg})

                if any(self.negate_literal(l) in new_clause for l in new_clause):
                    continue
                resolvents.append(frozenset(new_clause))

        return resolvents
    

    def negate_literal(self,lit):
        '''
        Return the negation of the literal'''
        if lit.func == Not:
            return lit.args[0]
        return Not(lit)