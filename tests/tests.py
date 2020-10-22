from sat_solver import * 
import unittest

P = Atom("P")
Q = Atom("Q")
R = Atom("R")
S = Atom("S")
T = Atom("T")

class TestSatSolver(unittest.TestCase): 

    def test_one(self): 
        formula = If(And([P, 
                          If(P, Q),
                          If(Q, R), 
                          If(R, S)]), S)
        table = TruthTable(formula)
        self.assertEqual(table.tautology(), True)

    def test_two(self): 
        formula = If(And([Not(S), 
                          If(P, Q),
                          If(Q, R), 
                          If(R, S)]), Not(P))
        table = TruthTable(formula)
        self.assertEqual(table.tautology(), True)
    
    def test_three(self):
        formula = If(And([Or([Not(P), Q]), 
                          Not(Q), 
                          Or([P, Q])]),
                          Q)
        table = TruthTable(formula)
        self.assertEqual(table.tautology(), True)

    def test_four(self): 
        formula = If(And([Or([P,Q]), 
                          Not(P), 
                          If(Q,R)]),
                          R)
        table = TruthTable(formula)
        self.assertEqual(table.tautology(), True) 

    def test_five(self): 
        formula = If(And([P,
                          If(P, Not(Q)),
                          If(R, Q), 
                          If(Not(R), S)]), 
                          S)
        table = TruthTable(formula)
        self.assertEqual(table.tautology(), True) 

    def test_six(self): 
        formula = If(And([If(If(P,Q),If(R,S)), 
                          Or([If(R,T),If(P,Q)]), 
                          Not(If(R,T))]), 
                    If(R, S)) 
        table = TruthTable(formula)
        self.assertEqual(table.tautology(), True) 


    def test_seven(self): 
        formula = If(And([If(P,Q),
                          If(Q,R)]),
                     And([P,R]))
        table =  TruthTable(formula)
        self.assertEqual(table.tautology(), False)

class TestBenchmark(unittest.TestCase): 
    
    def test_20_atoms(self):
        rf = RandomFormulaGenerator()
        atoms = set(map(lambda x: Atom(str(x)), range(19)))
        rf.atoms = atoms
        f = rf.random_formula_of_depth(Atom("p"), 3)
        print(f)
        tt = TruthTable(f)


