# Belief-revision

Belief Revision Assignment made for 02180 Intro to AI, SP25 at DTU. 

# Concept

A beliefbase has been implemented that uses weak partial meet contraction operator. 

When adding beliefs to the belief base:
- Remainders are generated (highest amount of remainders first)
- The remainders are selected through priority
- Beliefs are removed based on maximal consistent subsets

Beliefs are stored in the given form they're presented in, but during evaluation they're converted CNF. 
Each belief is represented via a Belief object that holds the belief in a Sympy object along with a priority as an int. The higher the priority the more important the belief. 

It should be mention, that at the moment, the main identified bottleneck is when generating remainders. 
All subsets for the belief base are generated, meaning that for n beliefs the number of subsets are $2^n$, given that a belief is either included or excluded. At larger belief sets this can become computationally heavy.

# How to run the beliefBase

The belief base can be run by running the file `main.py`. 

Each line in the input consists of a `belief, priority`.
I.e. if you want to add the belief $A\rightarrow B$ with a priority equal to `5`, then you'd add the following:

'''
A->B,5
'''

The following operators can be used:

1. Implies, `->`
2. Not, `~`
3. And, `&`
4. Biconditional, `<->`
5. XOR, `^`

Also, parenthesis are allowed to group. 

Beliefs can be words as well and are defined using regex with all natural letters (upper and lower case).
This means that one can say: 

'''latex
Alice\rightarrow Bob,4
'''

And this would result in the belief $Alice\rightarrow Bob$ with a priority value of 4. 


# How to run the test for the AGM Revision postulates

The project contains automated tests to show that all 8 AGM Revision postulates has been met. 
To run those, input into the terminal at root `python -m pytest `. 
All the tests can be found in `tests/test_agmRevisionPostulates.py`.

