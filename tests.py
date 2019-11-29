import random

from sympy import (
    Abs, Add, E, Float, I, Integer, Max, Min, N, Poly, Pow, PurePoly, Rational,
    S, Symbol, cos, exp, log, expand_mul, oo, pi, signsimp, simplify, sin,
    sqrt, symbols, sympify, trigsimp, tan, sstr, diff, Function)
from sympy.matrices.matrices import (ShapeError, MatrixError,
                                     NonSquareMatrixError, DeferredVector, _find_reasonable_pivot_naive,
                                     _simplify)
from sympy.matrices import (
    GramSchmidt, ImmutableMatrix, ImmutableSparseMatrix, Matrix,
    SparseMatrix, casoratian, diag, eye, hessian,
    matrix_multiply_elementwise, ones, randMatrix, rot_axis1, rot_axis2,
    rot_axis3, wronskian, zeros, MutableDenseMatrix, ImmutableDenseMatrix, MatrixSymbol)
from sympy.core.compatibility import long, iterable, range, Hashable
from sympy.core import Tuple, Wild
from sympy.functions.special.tensor_functions import KroneckerDelta
from sympy.utilities.iterables import flatten, capture
from sympy.utilities.pytest import raises
from sympy.solvers import solve
from sympy.assumptions import Q
from sympy.tensor.array import Array
from sympy.matrices.expressions import MatPow

from sympy.abc import a, b, c, d, x, y, z, t


def test_creation():
    m1 = Matrix(1, 2, [x, y])
    assert m1[0] == x and m1[1] == y
    m2 = Matrix(2, 2, [x, y, z, t])
    assert m2[0] == x and m2[1] == y and m2[2] == z and m2[3] == t
    raises(IndexError, lambda: Matrix([])[0])
    raises(IndexError, lambda: Matrix(5, 5, list(range(25)))[25])


def test_division():
    v = Matrix(2, 2, [x, y, z, t])
    assert v / z == Matrix(2, 2, [x / z, y / z, z / z, t / z])
    assert sstr(Matrix([0]) / Matrix([0])) == "0"


def test_sum():
    m = Matrix([[4, 4, 4], [x, y, x], [2*y, -1, z*x]])
    assert m + m == Matrix([[8, 8, 8], [2*x, 2*y, 2*x], [4*y, -2, 2*z*x]])
    n = Matrix(1, 2, [x, y])
    raises(ShapeError, lambda: m + n)
    assert n + n == Matrix(1, 2, [x * 2, y * 2])

    m = Matrix(list(range(100, 100 * 100, 100)))
    assert m + m == Matrix(list(range(200, 100 * 100 * 2, 200))) == m.add(m)

    m = Matrix(2, 2, [1, 2, 3, 1])
    n = Matrix(2, 2, [1, 2, 3, 0])
    assert m + n == m.add(n) == n.add(m) == Matrix([[2, 4], [6, 1]])


def test_abs():
    m = Matrix(1, 2, [-3, x])
    n = Matrix(1, 2, [3, Abs(x)])
    assert abs(m) == n
    m = Matrix(3, 2, [-y, -t, -50, -3, x, 10])
    n = Matrix(3, 2, [Abs(y), Abs(t), 50, 3, Abs(x), 10])
    assert abs(m) == n


test_creation()
test_division()
test_sum()
test_abs()
