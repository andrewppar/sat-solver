import copy
from .formula import Atom, Not, And, Or, If, Formula
from typing import List, Dict, Tuple
import time

"""A sat-solver implemented in python for experimental purposes.

This implements a sat-solver that can be used for basic purposes.
Currently it's only ~300 lines of code so it is easy to dive into
and manipulate. I plan to use it for experimentation with different
methods of approaching sat-solvers.

  Typical usage example:

    formula = If(Atom("p"), Atom("p"))
    truth_table = TruthTable(formula)
"""


###############
# Truth Table #
###############


class TruthTable:
    """The TruthTable class hold all the possible truth values for a  formula

    This subclass assigns all possible truth values to all of  the atomic
    formulas of a formula and for each possibility evaluates the truth value
    of the formula that it is passed.

    :ivar formula: This is the formula the truth table is being generated for.
    """

    def __init__(self, formula: Formula):
        """The init class for truth tables.

        This class sets the formula. Gets all the atomic formulas. Generates
        the  rows for the truth table. It calculates the value for the
        value of each possibility of assignment to truth tables.
        """
        self.formula = formula
        self.atoms = formula.atomic_formulas()
        start_rows = time.time()
        print("Starting Rows")
        self.atom_rows = self.generate_rows()
        stop_rows = time.time()
        print(f"Done with Rows: {stop_rows - start_rows}")
        self.resolution = self.solve()
        done = time.time()
        print(f"finished {done - stop_rows}")

    def generate_rows(self) -> List[Dict[Atom, bool]]:
        """Generates all the rows for the TruthTable's formula

        This function creates all the possible assignments of T and F
        to the formula for a  truth table.

        :returns: A list of dictionaries whose keys are atomic formulas
                 and whose values are booleans.
        """
        # @todo this is tail recurive -- convert it to a while loop
        # @todo  maybe make List[Dict[Atom, bool]] it's own class?
        atom_list = list(self.atoms)
        return self.generate_rows_internal([], atom_list)

    def generate_rows_internal(self,
                               acc,
                               atom_list) -> List[Dict[Atom, bool]]:
        """An internal method for generating rows of truth tables.

        This function should only be called by generate_rows. It
        is almost explicitly tail recursive and so could be
        optimized with a while loop or some dynamic programming.

        :param acc: An accumulator that is used in the next
            recursive iteration.
        :param atom_list: A list of atomic formulas that is being
            iterated over.

        :returns: A list of dictionaries whose keys are atomic formaulas
                 and whose values are booleans.
        """
        if atom_list == []:
            return [{}]
        else:
            recursive_case = self.generate_rows_internal(acc, atom_list[1:])
            current_atom = atom_list[0]
            result_list: List[Dict[Atom, bool]] = []
            for dictionary in recursive_case:

                # TODO We probably don't need two copies of the dictionary.
                # This could be way more space efficient if we used some other
                # datastructure.
                true_dictionary = copy.copy(dictionary)
                true_dictionary[current_atom] = True
                result_list.append(true_dictionary)
                false_dictionary = copy.copy(dictionary)
                false_dictionary[current_atom] = False
                result_list.append(false_dictionary)
            return result_list

    def solve(self) -> List[Tuple[Dict[Atom, bool], bool]]:
        """Determines the truth value of a formula for each row in
        its truth table.

        :returns: A list of tuples where the first value is a row
            of the truth table and the second value is the value
            of that truth table's formula.
        """
        result = []
        for case in self.atom_rows:
            resolution = self.resolve(case)
            result.append(resolution)
        return result

    def resolve(self,
                case: Dict[Atom, bool]) -> Tuple[Dict[Atom, bool], bool]:
        """Solves a particular row of a truth table.

        :param case: A dictionary of atomic formulas and booleans.

        :returns: A tuple whose first element is the input dictionary
            and whose second element is the value of the truth
            table's formula  for that cases assignment of booleans
            to atomic formulas.
        """
        truth_value = self.resolve_internal(self.formula, case)
        return (case, truth_value)

    def resolve_internal(self,
                         formula: Formula,
                         case: Dict[Atom, bool]) -> bool:
        """A helper to self.resolve()

           :param formula: the formula that is being solved for.e
           :param case: A dictionary of atomic formulas and booleans.

           :returns: A dictionary whose values are atomic formulas and whose
                keys are booleans.
        """
        if isinstance(formula, Atom):
            return case[formula]
        elif isinstance(formula, Not):
            return not self.resolve_internal(formula.negatum, case)
        elif isinstance(formula, And):
            result = True
            for conjunct in formula.conjuncts:
                if not self.resolve_internal(conjunct, case):
                    result = False
            return result
        elif isinstance(formula, Or):
            result = False
            for disjunct in formula.disjuncts:
                if self.resolve_internal(disjunct, case):
                    result = True
            return result
        elif isinstance(formula, If):
            ant_value = self.resolve_internal(formula.antecedent, case)
            cons_value = self.resolve_internal(formula.consequent, case)
            return (not ant_value) or cons_value
        else:
            raise RuntimeError(f"{formula} has not been implemented")

    def show_resolution(self):
        """Prints a representation of a table to stdout."""
        atoms = list(self.atoms)
        atom_string = "|"
        for atom in atoms:
            padding = ""
            if len(str(atom)) < len(str(False)):
                padding = " " * (len(str(False)) - len(str(atom)))
            atom_string += f"{atom}{padding}|"
        header = f"{atom_string}{self.formula}"
        print(header)
        print('-' * len(header))
        for dictionary, value in self.resolution:
            row = "|"
            for atom in atoms:
                atom_case = dictionary[atom]
                padding = ""
                if atom_case:
                    padding = " "
                row += f"{atom_case}{padding}|"
            row += f"{value}"
            print(row)

    def tautology(self) -> bool:
        """Determines whether the formula for a table is a tautology.

        :returns: A boolean that indicates whether or not the formula
            is a tautology.
        """
        result = True
        for case, value in self.resolution:
            if not value:
                result = False
                break
        return result

    def contradiction(self) -> bool:
        result = True
        for case, value in self.resolution:
            if value:
                result = False
                break
        return result
