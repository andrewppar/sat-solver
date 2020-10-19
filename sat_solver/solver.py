import copy
from enum import Enum
from typing import Set, List, Dict, Tuple

"""A sat-solver implemented in python for experimental purposes.

This implements a sat-solver that can be used for basic purposes.
Currently it's only ~300 lines of code so it is easy to dive into
and manipulate. I plan to use it for experimentation with different
methods of approaching sat-solvers.

  Typical usage example:

    formula = If(Atom("p"), Atom("p"))
    truth_table = TruthTable(formula)
"""


############
# Language #
############

class Connective(Enum):
    """
    This Enum is for capturing
    the connectives in a way that
    is more robust than just using strings.
    """

    negation = "Not"
    conjunction = "And"
    disjunction = "Or"
    implication = "Implies"
    atomic = "Atom"


class Formula:
    """This is the top of the Formula  Ontology.

        In Java this would be an abstract class.

            :ivar main_connective: The main connective of a formula
    """

    def __init__(self, main_connective: Connective):
        """Inits Fromula  with main_connective"""
        self.main_connective = main_connective

    def atomic_formulas(self):
        """The method  for  gathering the atomic formulas in a formula."""
        pass


class Atom(Formula):
    """The atomic formlua class.

    This is the class of all atomic formulas.

    :ivar root: This is a string that represents the value of the
        atomic formula.
    """
    def __init__(self, root: str):
        """Inits Atom with a root string

        This is the class that has atomic formulas as
        instances.
        """
        self.main_connective = Connective.atomic
        super().__init__(self.main_connective)
        self.root = root

    def __str__(self):
        return self.root

    def __eq__(self, form) -> bool:
        if not isinstance(form, Atom):
            return False
        else:
            return self.root == form.root

    def __hash__(self):
        return hash(self.root)

    def atomic_formulas(self):
        return set([self])


class Not(Formula):
    """The negation class

    This is the subclass of Formula for negations.

    :attribute negatum: The immedate subformula of a negation
    """

    def __init__(self, negatum: Formula):
        """Inits the Negation class with a negated subformula"""
        self.main_connective = Connective.negation
        super().__init__(self.main_connective)
        self.negatum = negatum

    def __str__(self):
        return f"(Not {str(self.negatum)})"

    def __eq__(self, form):
        if not isinstance(form, Not):
            return False
        else:
            return self.negatum == form.negatum

    def atomic_formulas(self) -> Set[Atom]:
        return self.negatum.atomic_formulas()


class And(Formula):
    """The conjunction class

    This is the subclass of Formula for conjunctions

    :attribute conjuncts: A list of the immediate subformulas
        of a conjunction.
    """

    def __init__(self, conjuncts: Set[Formula]):
        """Inits the Conjunction class with a list of subformulas."""
        self.main_connective = Connective.conjunction
        super().__init__(self.main_connective)
        self.conjuncts = conjuncts

    def __str__(self):
        conjuncts_str = ""
        for conjunct in self.conjuncts:
            conjuncts_str += f" {str(conjunct)}"
        return f"(And {conjuncts_str})"

    def __eq__(self, form):
        if not isinstance(form, And):
            return False
        else:
            return self.conjuncts == form.conjuncts

    def atomic_formulas(self) -> Set[Atom]:
        result: Set[Atom] = set()
        for conjunct in self.conjuncts:
            result = result.union(conjunct.atomic_formulas())
        return result


class Or(Formula):
    """The disjunction class

    This is the subclass of Formula for disjunctions

     :attribute disjuncts: A list of the immediate subformulas
        of a disjunction.
    """

    def __init__(self, disjuncts: Set[Formula]):
        self.main_connective = Connective.disjunction
        super().__init__(self.main_connective)
        self.disjuncts = disjuncts

    def __str__(self):
        disjuncts_str = ""
        for disjunct in self.disjuncts:
            disjuncts_str += f" {str(disjunct)}"
        return f"(And {disjuncts_str})"

    def __eq__(self, form):
        if not isinstance(form, Or):
            return False
        else:
            return self.disjuncts == form.disjuncts

    def atomic_formulas(self) -> Set[Atom]:
        result: Set[Atom] = set()
        for disjunct in self.disjuncts:
            result = result.union(disjunct.atomic_formulas())
        return result


class If(Formula):
    """The Conditional Class

    This is the subclass of Formula for implications

   :ivar antecedent: The antecedent of the conditional
   :ivar consequent: The consequent of the conditional
   """

    def __init__(self, antecedent: Formula, consequent: Formula):
        self.main_connective = Connective.implication
        super().__init__(self.main_connective)
        self.antecedent = antecedent
        self.consequent = consequent

    def __str__(self):
        ant = str(self.antecedent)
        cons = str(self.consequent)
        return f"(If {ant} {cons})"

    def __eq__(self, form):
        if not isinstance(form, If):
            return False
        else:
            ants_eq = self.antecedent == form.antecedent
            cons_eq = self.consequent == form.consequent
            return ants_eq and cons_eq

    def atomic_formulas(self) -> Set[Atom]:
        ant_atoms = self.antecedent.atomic_formulas()
        cons_atoms = self.consequent.atomic_formulas()
        return ant_atoms.union(cons_atoms)

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
        self.atom_rows = self.generate_rows()
        self.resolution = self.solve()

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
