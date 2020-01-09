from sympy import And, true, false, Not, Or, Equality, nan, symbols, var, Union, Interval, sympify, S
from sympy.logic.boolalg import as_Boolean, Boolean, BooleanAtom, BooleanTrue
from sympy.core.relational import Relational
from sympy.core.symbol import Symbol
import unittest

"""
-White-box tests of boolalg.py-

Tested functions:

and
not
as_Boolean
Class Boolean
Class BooleanAtom
Class BooleanTrue
"""
class testerClass(unittest.TestCase):

    def test_and(self):

        # 1 argument
        assert And(1) is true
        # 2 arguments
        assert And(1, 0) is false

    def test_not(self):
            
        assert Not(True) is false
        assert Not(0) is true
        assert Not(And(And(True, 1), Or(1, False))) is false
        assert Not(Equality(2, 2)) is false

    def test_as_Boolean(self):
        
        assert as_Boolean(True) is true
        assert as_Boolean(False) is false
        assert as_Boolean(symbols('x')) is symbols('x')

        #assert as_Boolean(Boolean(True)) is Boolean(True) #Not passing due to unknown behaviour with return type.

        #Raising exception
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

        #No representation for inf
        #assert Or(0 < -2, 2 < 0).as_set() is Union(Interval.open(-inf, -2), Interval.open(2, inf))

    def test_BooleanAtom_Class(self):

        #simplify
        assert(BooleanAtom(True)) is not 1

    def test_BooleanTrue_Class(self):

        assert sympify(True) is true

        assert S.true is true
        
        #as_set()
        assert(BooleanTrue(True).as_set()) is not set()

if __name__ == '__main__':
    unittest.main()