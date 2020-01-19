from sympy import *
from sympy.logic.boolalg import (
    And, Boolean, Equivalent, ITE, Implies, Nand, Nor, Not, Or,
    POSform, SOPform, Xor, Xnor, conjuncts, disjuncts,
    distribute_or_over_and, distribute_and_over_or,
    eliminate_implications, is_nnf, is_cnf, is_dnf, simplify_logic,
    to_nnf, to_cnf, to_dnf, to_int_repr, bool_map, true, false,
    BooleanAtom, is_literal, term_to_integer, integer_to_term,
    truth_table, as_Boolean, BooleanFunction, Application, BooleanTrue)
from sympy.utilities.pytest import raises, XFAIL, slow
from sympy.utilities import cartes

from itertools import combinations
from sympy.core.relational import Relational
from sympy.core.symbol import Symbol
import unittest

"""
-White-box tests of boolalg.py-

Tested functions:

and
not
or
xor
nand
xnor 
implies
equivalent
to_nnf
as_set
as_Boolean
Class Boolean
Class BooleanAtom
Class BooleanTrue
Class BooleanFunction

"""

A, B, C, D = symbols('A:D')
a, b, c, d, e, w, x, y, z = symbols('a:e w:z')

class testerClass(unittest.TestCase):

    def test_and(self):

        # 1 argument
        assert And(1) is true
        # 2 arguments
        assert And(1, 0) is false

        raises(TypeError, lambda: And(2, A))
        raises(TypeError, lambda: And(A < 2, A))
        assert And(A < 1, A >= 1) is false
        e = A > 1
        assert And(e, e.canonical) == e.canonical
        g, l, ge, le = A > B, B < A, A >= B, B <= A
        assert And(g, l, ge, le) == And(l, le)

    def test_or(self):

        assert Or(1, 0) is true
        assert Or(Not(1), Not(1)) is false
        assert Or(A < 1, A >= 1) is true
        e = A > 1
        assert Or(e, e.canonical) == e
       

    def test_not(self):
            
        assert Not(True) is false
        assert Not(0) is true
        assert Not(A) is ~A
        assert Not(And(And(True, 1), Or(1, False))) is false
        assert Not(Equality(2, 2)) is false
        assert Not.eval(Equality(1, 1).simplify()) is false
        assert Not(Xor(1, 0)).to_nnf(simplify=True) is false
        raises(ValueError, lambda: Not(type(2)))

    def test_as_Boolean(self):
        
        assert as_Boolean(True) is true
        assert as_Boolean(False) is false
        assert as_Boolean(symbols('x')) is symbols('x')
        z = symbols('z', zero=True)
        assert all(as_Boolean(i) is S.false for i in (False, S.false, 0, z))
        assert as_Boolean(And(1, 0)) is false
        self.assertRaises(TypeError, as_Boolean, "String")

    def test_Boolean_Class(self):

        #__and__(self, other)
        assert true.__and__(true) is not false

        #__or__(self, other)
        assert true.__or__(false) is not false

        #__invert__(self)
        assert true.__invert__() is false

        #__lshift__(self, other)
        assert true.__lshift__(false) is true

        #__rshift__(self)
        assert true.__rshift__(true) is true

        #rrshift = lshift
        assert true.__rrshift__(false) is true.__lshift__(false)

        #rlshift = rshift
        assert true.__rlshift__(false) is true.__rshift__(false)

        #__xor__(self, other)
        assert true.__xor__(true) is false

        #rxor = xor
        assert true.__rxor__(true) is true.__xor__(true)

        # equals(self, other)
        assert Not(And(True, False, False)).equals(And(Not(True), Not(False), Not(False))) is False

        # to_nnf(self, simplify=True)
        assert Not(True).to_nnf() is false

        # as_set()
        assert Equality(1, 0).as_set() is Equality(1, 0).as_set() 
        assert And(-2 < 1, 1 < 2).as_set() is And(-2 < 1, 1 < 2).as_set()

    def test_Overloading(self):
 
        assert A & B == And(A, B)
        assert A | B == Or(A, B)
        assert (A & B) | C == Or(And(A, B), C)
        assert A >> B == Implies(A, B)
        assert A << B == Implies(B, A)
        assert ~A == Not(A)
        assert A ^ B == Xor(A, B)

    def test_BooleanAtom_Class(self):

        #simplify
        assert(BooleanAtom(True)) is not 1

    def test_BooleanTrue_Class(self):

        assert sympify(True) is true

        assert S.true is true
        
        #as_set()
        assert(BooleanTrue(True).as_set()) is not set()

    def test_BooleanFunction(self):

        # Raise exception
        self.assertRaises(TypeError, And(0, 1).__lt__, true)

        self.assertRaises(AttributeError, BooleanFunction._to_nnf, Boolean, true, false)

        assert BooleanFunction(Application(), true)._eval_derivative(Equality(1, 2)) is not true
        assert BooleanFunction._apply_patternbased_simplification(true, Equality(1, 0), None, None, None) is not true 
        assert BooleanFunction._apply_patternbased_simplification(true, Equality(1, 0), None, false, true) is not true
        assert BooleanFunction._apply_patternbased_simplification(false, Equality(1, 0), Equality(1,1), true, true, None) is not true

    def test_Xor(self):

        assert Xor(BooleanFunction(Application(), true)).to_nnf() is not true

        assert isinstance(Xor(A, B), Xor)
        assert Xor(A, B, Xor(C, D)) == Xor(A, B, C, D)
        assert Xor(A, B, Xor(B, C)) == Xor(A, C)
        assert Xor(A < 1, A >= 1, B) == Xor(0, 1, B) == Xor(1, 0, B)
        e = A > 1
        assert Xor(e, e.canonical) == Xor(0, 0) == Xor(1, 1)

    def test_Nand(self):

        assert Nand.eval(true) is false
       
    def test_Nor(self):

        assert Nor.eval(true) is false

    def test_Xnor(self):

        assert Xnor.eval(true, false) is false

    def test_Implies(self):

        assert Implies(true, false) is false

    def test_Equivalent(self):

        assert Equivalent(1, A) == A
        assert Equivalent(0, A) == Not(A)
        assert Equivalent(A, Equivalent(B, C)) != Equivalent(Equivalent(A, B), C)
        assert Equivalent(A < 1, A >= 1) is false
        assert Equivalent(A < 1, A >= 1, 0) is false
        assert Equivalent(A < 1, A >= 1, 1) is false
        assert Equivalent(A < 1, S(1) > A) == Equivalent(1, 1) == Equivalent(0, 0)
        assert Equivalent(Equality(A, B), Equality(B, A)) is true

        #to_nnf in Equivalent
        assert to_nnf(Equivalent(A, B, C)) == (~A | B) & (~B | C) & (~C | A)

    def test_to_nnf(self):

        (A | B | C) & (~A | ~B | C) & (A | ~B | ~C) & (~A | B | ~C)
        assert to_nnf(ITE(A, B, C)) == (~A | B) & (A | C)
        assert to_nnf(Not(A | B | C)) == ~A & ~B & ~C
        assert to_nnf(Not(A & B & C)) == ~A | ~B | ~C
        assert to_nnf(Not(A ^ B ^ C)) == \
        (~A | B | C) & (A | ~B | C) & (A | B | ~C) & (~A | ~B | ~C)

        assert to_nnf(Not(ITE(A, B, C))) == (~A | ~B) & (A | ~C)
        assert to_nnf((A >> B) ^ (B >> A)) == (A & ~B) | (~A & B)

    def test_as_set(self):
    
        assert true.as_set() == S.UniversalSet
        assert false.as_set() == S.EmptySet
        assert x.as_set() == S.UniversalSet
        assert And(x < 1, sin(x) < 3).as_set() == (x < 1).as_set()
        raises(NotImplementedError, lambda: (sin(x) < 1).as_set())


if __name__ == '__main__':
    unittest.main()
