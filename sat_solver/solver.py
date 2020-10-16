import copy
from enum import Enum
from typing import Set, List, Dict, Tuple


############
# Language #
############

class Connective(Enum):

    negation = "Not"
    conjunction = "And"
    disjunction = "Or"
    implication = "Implies"
    atomic = "Atom"


class Formula:

    def __init__(self, main_connective: Connective):
        self.main_connective = main_connective

    def atomic_formulas(self):
        pass


class Atom(Formula):

    def __init__(self, root: str):
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

    def __init__(self, negatum: Formula):
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

    def __init__(self, conjuncts: Set[Formula]):
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

    def __init__(self, formula: Formula):
        self.formula = formula
        self.atoms = formula.atomic_formulas()
        self.atom_rows = self.generate_rows()
        self.resolution = self.solve()

    def generate_rows(self) -> List[Dict[Atom, bool]]:
        # @todo this is tail recurive -- convert it to a while loop
        # @todo  maybe make List[Dict[Atom, bool]] it's own class?
        atom_list = list(self.atoms)
        return self.generate_rows_internal([], atom_list)

    def generate_rows_internal(self,
                               acc,
                               atom_list) -> List[Dict[Atom, bool]]:
        if atom_list == []:
            return [{}]
        else:
            recursive_case = self.generate_rows_internal(acc, atom_list[1:])
            current_atom = atom_list[0]
            result_list: List[Dict[Atom, bool]] = []
            for dictionary in recursive_case:
                true_dictionary = copy.copy(dictionary)
                true_dictionary[current_atom] = True
                result_list.append(true_dictionary)
                false_dictionary = copy.copy(dictionary)
                false_dictionary[current_atom] = False
                result_list.append(false_dictionary)
            return result_list

    def solve(self) -> List[Tuple[Dict[Atom, bool], bool]]:
        result = []
        for case in self.atom_rows:
            resolution = self.resolve(case)
            result.append(resolution)
        return result

    def resolve(self,
                case: Dict[Atom, bool]) -> Tuple[Dict[Atom, bool], bool]:
        truth_value = self.resolve_internal(self.formula, case)
        return (case, truth_value)

    def resolve_internal(self,
                         formula: Formula,
                         case: Dict[Atom, bool]) -> bool:
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
        result = True
        for case, value in self.resolution:
            if not value:
                result = False
                break
        return result
