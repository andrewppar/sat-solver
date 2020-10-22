from .formula import Not, And, Or, If, Atom, Formula, Connective
from typing import Set
import random


class RandomFormulaGenerator:
    """A class for  generating a random formula with parameters
    for the number of atomic formulas.
    """

    def __init__(self) -> None:
        self.max_depth = 10
        self.atoms: Set[Atom] = set()
        self.used_atoms: Set[Atom] = set()

    def random_formula_of_depth(self, formula: Formula, depth: int) -> Formula:
        """Generates a random formula with the passed formula at the specified
        depth.

        :param formula: The subformula of a particular depth.
        :param depth: The depth that formula will be in the resulting formula
        :returns: A random formula with the parameter
            formula at the specified depth.
        """
        current_depth = 0
        current_formula: Formula = Atom("p")
        while current_depth <= depth:
            connective = self.random_connective()
            if connective == Connective.negation:
                current_formula = Not(current_formula)
                current_depth += 1
            elif connective == Connective.implication:
                new_formula = self.get_random_atom()
                new_is_antecedent = random.choice([True, False])
                if new_is_antecedent:
                    current_formula = If(new_formula, current_formula)
                else:
                    current_formula = If(current_formula, new_formula)
                current_depth += 1
            elif connective in [Connective.conjunction,
                                Connective.disjunction]:
                new_juncts = self.get_random_atoms()
                new_juncts.add(current_formula)
                if connective == Connective.conjunction:
                    current_formula = And(new_juncts)
                else:
                    current_formula = Or(new_juncts)
                current_depth += 1
        return current_formula

    def random_connective(self) -> Connective:
        """Returns a random connective.

        :returns: A random connective.  """
        connectives = [Connective.negation,
                       Connective.disjunction,
                       Connective.implication,
                       Connective.conjunction]
        return random.choice(connectives)

    def get_random_atom(self) -> Atom:
        if self.atoms == self.used_atoms:
            result = random.choice(list(self.atoms))
        else:
            unused_atoms = self.atoms.difference(self.used_atoms)
            result = random.choice(list(unused_atoms))
            self.used_atoms.add(result)
        return result

    def get_random_atoms(self) -> Set[Formula]:
        atom_count = random.choice(range(len(self.atoms))[1:])
        atom_number = 0
        result: Set[Formula] = set()
        while atom_number <= atom_count:
            result.add(self.get_random_atom())
            atom_number += 1
        return result
