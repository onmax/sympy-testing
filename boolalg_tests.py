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

    """Test case: And
    Desc: Testing with different inputs, giving different canonical and relational inputs yields increased coverage. Exceptions raised.
    """
    def test_and(self):

        # 1 argument
        assert And(1) is true
        # 2 arguments
        assert And(1, 0) is false
        #Raising exceptions
        raises(TypeError, lambda: And(2, D))
        raises(TypeError, lambda: And(D, D < 2))
        assert And(D < 1, D >= 1) is false
        #canonical
        e = D > 1
        assert And(e, e.canonical) is not false
        # to increase covering eval_simplify, inspired from test_boolalg.py
        q, l, qe, le = D > C, C < D, D >= C, C <= D
        assert And(q, l, qe, le) is And(l, le)

    def test_or(self):

        assert Or(1, 0) is true
        assert Or(Not(1), Not(1)) is false
        assert Or(A < 1, A >= 1) is true
        e = A > 1
        assert Or(e, e.canonical) == e
       
    """Test case: Not
    Desc: Test cases test the classmethods eval, to_nnf and inputs of symbols, booleans plus Equality function.
    """
    
    def test_not(self):
        
        assert Not(false) is true
        assert Not(0) is true

        #Multiple booleans
        assert Not(And(And(True, 0), Or(0, False))) is true
        #Equality
        assert Not(Equality(2, 2)) is false
        #eval @classmethod
        assert Not.eval(Equality(1, 1).simplify()) is false
        #to_nnf
        assert Not(Xor(1, 0)).to_nnf(simplify=True) is false

    """Test case: as_Boolean
    Desc: Test cases give statement and path coverage. Desc in comments on each case
    """
    def test_as_Boolean(self):

        #Simple function calls for return statements    
        assert as_Boolean(True) is true
        assert as_Boolean(False) is false
        #Testing Isinstance e, Symbol
        assert as_Boolean(symbols('x')) is symbols('x')
        #Reaching last return statement
        z = symbols('z', zero=True)
        assert all(as_Boolean(i) is S.false for i in (False, S.false, 0, z))
        #Calling with boolean function
        assert as_Boolean(And(1, 0)) is false
        #Raising exception
        self.assertRaises(TypeError, as_Boolean, "String")

    """Test case: Boolean 
    Desc: Testing the overloading of operators, called directly through the use of a Boolean object and as a classmethod.
    """
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

    """Test case: BooleanAtom
    Desc: Simple function call, coverage is indirectly traveled by other cases. 
    """
    def test_BooleanAtom_Class(self):

        #simplify
        assert(BooleanAtom(True)) is not 1

    """Test case: BooleanTrue
    Desc: The tests actually do not contribute to significant coverage. Hard to reach statements. Is indirectly traveled by other tests.
    """
    def test_BooleanTrue_Class(self):

        assert sympify(True) is true

        assert S.true is true
        
        #as_set()
        assert(BooleanTrue(True).as_set()) is not set()


    """Test case: BooleanFunction
    Desc: The apply_patternbased_simplification is very complex and hard to get coverage for. The asserts could not improve coverage significantly, large uncovered area.
    """
    def test_BooleanFunction(self):

        # Raise exception
        self.assertRaises(TypeError, And(0, 1).__lt__, true)

        self.assertRaises(AttributeError, BooleanFunction._to_nnf, Boolean, true, false)

        assert BooleanFunction(Application(), true)._eval_derivative(Equality(1, 2)) is not true
        assert BooleanFunction._apply_patternbased_simplification(true, Equality(1, 0), None, None, None) is not true 
        assert BooleanFunction._apply_patternbased_simplification(true, Equality(1, 0), None, false, true) is not true
        assert BooleanFunction._apply_patternbased_simplification(false, Equality(1, 0), Equality(1,1), true, true, None) is not true

    """Test case: Xor
    Desc: Testing Xor both with relational and canonical objects. Isinstance covered, and BooleanFunction object creation is used to test Xor to_nnf (not covered in to_nnf test case)
    """
    def test_Xor(self):

        assert Xor(BooleanFunction(Application(), true)).to_nnf() is not true

        assert isinstance(Xor(A, B), Xor)
        assert Xor(A, B, Xor(C, D)) == Xor(A, B, C, D)
        assert Xor(A, B, Xor(B, C)) == Xor(A, C)
        assert Xor(A < 1, A >= 1, B) == Xor(0, 1, B) == Xor(1, 0, B)
        e = A > 1
        assert Xor(e, e.canonical) == Xor(0, 0) == Xor(1, 1)


    """Test case: Nand
    Desc: Calling eval for single return statement coverage. 
    """
    def test_Nand(self):

        assert Nand.eval(true) is false

    """Test case: Nor
    Desc: Calling eval for single return statement coverage. 
    """  
    def test_Nor(self):

        assert Nor.eval(true) is false

    """Test case: Xnor
    Desc: Calling eval for single return statement coverage. 
    """
    def test_Xnor(self):

        assert Xnor.eval(true, false) is false

    """Test case: Implies
    Desc: Testing Implies function. More coverage could not be reached through simple function calls.
    """

    def test_Implies(self):

        assert Implies(true, false) is false

    """Test case: Equivalent
    Desc: Testing Equivalent. Hard function to get coverage for. 
    Test cases are testing switching arguments, calling Equivalent within Equivalent and using Equality. Using help from some examples from test_boolalg.py
    """
    def test_Equivalent(self):

        assert Equivalent(true, false) is false
        assert Equivalent(0, D) is Not(D)
        assert Equivalent(Equivalent(A, B), C) is not Equivalent(Equivalent(C, Equivalent(A, B)))
        assert Equivalent(B < 1, B >= 1) is false
        assert Equivalent(C < 1, C >= 1, 0) is false
        assert Equivalent(D < 1, D >= 1, 1) is false
        assert Equivalent(E < 1, S(1) > E) is Equivalent(1, 1)
        assert Equivalent(Equality(C, D), Equality(D, C)) is true

        #to_nnf in Equivalent (could be in Equivalent)
        assert to_nnf(Equivalent(D, B, C)) == (~D | B) & (~B | C) & (~C | D)


    """Test case: to_nnf
    Desc: Testing to_nnf, very complex function, using help from some examples from test_boolalg.py
    """
    def test_to_nnf(self):
       
        #ITE
        assert to_nnf(ITE(A, B, C)) is (~A | B) & (A | C)

        assert to_nnf(Not(A | B)) is ~A & ~B
        assert to_nnf(Not(D & C & A)) is ~D | ~C | ~A
        assert to_nnf(Not(D ^ B ^ C)) is \
        (~D | B | C) & (D | ~B | C) & (D | B | ~C) & (~D | ~B | ~C)
    
        assert to_nnf(Not(ITE(C, B, A))) is (~C | ~B) & (C | ~A)
        assert to_nnf((A >> B) ^ (B >> A)) is (A & ~B) | (~A & B)

    """Test case: as_set
    Desc: Testing as_set, to evaluate expressions as a set. Note that these are classmethods of different classes.
    """
    def test_as_set(self):
        
        #Testing on Boolean for UniversalSet
        assert true.as_set() is S.UniversalSet
        #Testing on Symbol
        assert x.as_set() is S.UniversalSet
        #Testing on Boolean for non UniversalSet
        assert false.as_set() is not S.UniversalSet
        
        assert And(cos(x) < 3, x < 1).as_set() is not (x < 1).as_set()
        #Raising exception
        raises(NotImplementedError, lambda: And(cos(x) < 1, x < 0).as_set())


if __name__ == '__main__':
    unittest.main()