from z3 import *

Object = DeclareSort('Object')
Human = Function('Human', Object, BoolSort())
Mortal = Function('Mortal', Object, BoolSort())

# A well known philosopher 
socrates = Const('socrates', Object)

# Free variables used in forall must be declared Const in python
x = Const('x', Object)

axioms = [ForAll([x], Implies(Human(x), Mortal(x))), 
          Human(socrates)]

s = Solver()
s.add(axioms)

# prints sat so axioms are coherent
print(s.check())

# classical refutation
s.add(Not(Mortal(socrates)))

# prints unsat so socrates is Mortal
print(s.check()) 
