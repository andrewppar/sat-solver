from typing import Set
from enum import Enum

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

    def __str__(self):
        pass

    def atomic_formulas(self):
        """The method  for  gathering the atomic formulas in a formula."""
        pass

    def __hash__(self):
        """The method for generating a hash for a formula"""
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

    def __hash__(self):
        return hash(str(self))


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

    def __hash__(self):
        return hash(str(self))

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
        return f"(Or {disjuncts_str})"

    def __eq__(self, form):
        if not isinstance(form, Or):
            return False
        else:
            return self.disjuncts == form.disjuncts

    def __hash__(self):
        return hash(str(self))

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

    def __hash__(self):
        return hash(str(self))

    def atomic_formulas(self) -> Set[Atom]:
        ant_atoms = self.antecedent.atomic_formulas()
        cons_atoms = self.consequent.atomic_formulas()
        return ant_atoms.union(cons_atoms)
