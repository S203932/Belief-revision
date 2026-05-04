from sympy.logic.boolalg import Not, And
from beliefBase import BeliefBase,Belief
from revision import parse_formula
from inferenceEngine import InferenceEngine

# Need to instantiate the inferenceEngine to use its methods
engine = InferenceEngine()

def test_closure():
    '''
    If something logical follows from the beliefs it should already be in the belief set
    '''
    B = BeliefBase()
    B.add(parse_formula("A->B"))
    B.add(parse_formula("A"))

    phi = parse_formula("B")

    B_star = B.copy()
    B_star.revise(Belief(phi, 1))

    # if B*phi entails something, it should be consistent
    for f in B_star.formulas():
        assert engine.entails(B_star.formulas(), f)

def test_success():
    '''
    Revised belief base must accept new information
    '''
    B = BeliefBase()
    B.add(parse_formula("A"))

    phi = parse_formula("B")

    B.revise(Belief(phi, 1))

    assert B.entails(phi)

def test_inclusion():
    '''
    Revised beliefs should be no larger than current belief base in addition to new belief
    '''
    B = BeliefBase()
    B.add(parse_formula("A->B"))

    phi = parse_formula("A")

    B_star = B.copy()
    B_star.revise(Belief(phi, 1))

    B_plus = B.copy()
    B_plus.expand(Belief(phi, 1))

    for f in B_star.formulas():
        assert engine.entails(B_plus.formulas(), f)

def test_vacuity():
    '''
    If the beliefbase does not imply that the new belief is false, any attempt at adding the new belief
    to the beliefbase should do nothing, but simply add the belief to the beliefbase'''
    B = BeliefBase()
    B.add(parse_formula("A"))

    phi = parse_formula("B")

    assert not B.entails(Not(phi))

    B_star = B.copy()
    B_star.revise(Belief(phi, 1))

    B_plus = B.copy()
    B_plus.expand(Belief(phi, 1))

    assert set(B_star.formulas()) == set(B_plus.formulas())

def test_consistency():
    '''
    Revising the belief base with a non-contradictory belief should not result in the belief base becoming
    inconsistent'''
    B = BeliefBase()
    B.add(parse_formula("A"))

    phi = parse_formula("B")

    B.revise(Belief(phi, 1))

    assert B.is_consistent()

def test_extensionality():
    '''
    If two beliefs means the same, then revising the beliefbase with either should produce the same result'''

    B = BeliefBase()

    phi = parse_formula("A->B")
    psi = parse_formula("~A | B")  # equivalent

    B1 = B.copy()
    B2 = B.copy()

    B1.revise(Belief(phi, 1))
    B2.revise(Belief(psi, 1))

    for f in B1.formulas():
        assert engine.entails(B2.formulas(), f)

    for f in B2.formulas():
        assert engine.entails(B1.formulas(), f)


def test_superexpansion():
    '''
    If you revise your beliefbase with a combined statement (phi AND psi), then everything you end up beliving
    should be obtainable by:\n
    1. revising with phi\n
    2. then expanding with psi'''
    B = BeliefBase()

    phi = parse_formula("A")
    psi = parse_formula("B")

    B1 = B.copy()
    B1.revise(Belief(And(phi, psi), 1))

    B2 = B.copy()
    B2.revise(Belief(phi, 1))
    B2.expand(Belief(psi, 1))

    for f in B1.formulas():
        assert engine.entails(B2.formulas(), f)


def test_subexpansion():
    '''
    If after revising with phi, the beliefbase does not contradict phi, then adding phi explicitly should not
    give anything new beyond revising with phi AND psi '''
    B = BeliefBase()

    phi = parse_formula("A")
    psi = parse_formula("B")

    B_phi = B.copy()
    B_phi.revise(Belief(phi, 1))

    if not B_phi.entails(Not(psi)):
        B1 = B_phi.copy()
        B1.expand(Belief(psi, 1))

        B2 = B.copy()
        B2.revise(Belief(And(phi, psi), 1))

        for f in B1.formulas():
            assert engine.entails(B2.formulas(), f)