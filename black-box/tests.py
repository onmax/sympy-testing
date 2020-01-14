import random

from sympy import *
from sympy.matrices import *

from sympy.core.compatibility import long, iterable, range, Hashable
from sympy.core import Tuple, Wild
from sympy.functions.special.tensor_functions import KroneckerDelta
from sympy.utilities.iterables import flatten, capture
from sympy.utilities.pytest import raises
from sympy.solvers import solve
from sympy.assumptions import Q
from sympy.tensor.array import Array
from sympy.matrices.common import *
from sympy.matrices.matrices import *
from sympy.matrices.expressions import MatPow

from sympy.abc import a, b, c, d, x, y, z, t

from parse import *

m22 = Matrix(2, 2, [1, 2, 3, 4])
m12 = Matrix(1, 2, [1, 2])
m16 = Matrix(1, 6, [2, 4, 6, 4, 8, 10])
m44 = Matrix([[2,  -1, 1, 8], [11, 4, 2, 0], [9, 8, 5, 9], [12,  -7,  -1, 6]])
m32 = Matrix([[1, 2], [3, 5], [1, 2]])
m33 = Matrix([[1, -1, 3], [3, 4, 2], [0, 2, 5]])

sm33 = Matrix([[4, 4, 4], [x, y, x], [2 * y, -1, z * x]])
v1 = [11, 4, 2, 0]
v2 = [-145, 54, 9135]


def test_creation():
    m1 = Matrix(1, 2, [x, y])
    assert m1[0] == x and m1[1] == y
    assert m1 == Matrix([[x, y]])
    assert m1[:] == [x, y]
    assert m1.cols == 1 and m1.rows == 2

    m2 = Matrix(2, 2, [x, y, z, t])
    assert m2[0] == x and m2[1] == y and m2[2] == z and m2[3] == t
    assert m2 == Matrix([[x, y], [z, t]])
    assert m2[:] == [x, y, z, t]
    assert m2.cols == 2 == m2.rows

    raises(ValueError, lambda: Matrix(2, 2, []))
    raises(ValueError, lambda: Matrix(-2, 2, []))
    raises(ValueError, lambda: Matrix(3, 3, range(15)))
    raises(IndexError, lambda: Matrix((1))[2])
    raises(IndexError, lambda: Matrix((1, 2))[2])
    raises(IndexError, lambda: Matrix([])[0])

    with raises(IndexError):
        Matrix((1, 2))[1:2] = 5
    with raises(IndexError):
        Matrix((1, 2))[3] = 5

    m1 = Matrix([[x, 0], [0, 0]])
    assert m1.cols == m1.rows == 2
    assert m1[:] == [x, 0, 0, 0]

    m2 = Matrix(2, 2, [x, 0, 0, 0])
    assert m2.cols == m2.rows == 2
    assert m2[:] == [x, 0, 0, 0]

    assert m1 == m2

    m32 = Matrix(3, 2, range(1, 7))
    m42 = Matrix(4, 2, range(7, 15))
    m = Matrix([m32, m42])
    assert m.cols == 2
    assert m.rows == 7
    assert m[:] == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    # TODO Check that using negative indexes works


def test_sum():
    assert m22 + m22 == Matrix(2, 2, [2, 4, 6, 8])

    raises(ShapeError, lambda: m22 + n12)

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


def test_division():
    m = Matrix(2, 2, [2, 4, 6, 8])
    assert m / m == Matrix(2, 2, [1, 0, 0, 1])
    assert m / 2 == Matrix(2, 2, [1, 2, 3, 4])

    raises(ShapeError, lambda: m / m)

    m = Matrix(2, 2, [x, y, z, t])
    assert m / z == Matrix(2, 2, [x / z, y / z, z / z, t / z])
    assert sstr(Matrix([0]) / Matrix([0])) == "0"


def test_abs():
    m = Matrix(1, 2, [-3, x])
    n = Matrix(1, 2, [3, Abs(x)])
    assert abs(m) == n

    m = Matrix(3, 2, [-y, -t, -50, -3, x, 10])
    n = Matrix(3, 2, [Abs(y), Abs(t), 50, 3, Abs(x), 10])
    assert abs(m) == n


def test_transpose():
    def own_transpose(m):
        mv = []
        for i in range(m.shape[0]):
            mv.append([])
            for j in range(m.shape[1]):
                mv[-1].append(m[i, j])
        mt_ = [[mv[j][i] for j in range(len(mv))] for i in range(len(mv[0]))]
        return Matrix(mt_)

    assert m22.transpose() == own_transpose(m22)
    assert m33.transpose() == own_transpose(m33)
    assert m16.transpose() == own_transpose(m16)
    assert m32.transpose() == own_transpose(m32)
    assert sm33.transpose() == own_transpose(sm33)


def test_shape():
    assert m22.shape == (2, 2)
    assert m12.shape == (1, 2)
    assert m16.shape == (1, 6)
    assert m44.shape == (4, 4)
    assert m32.shape == (3, 2)
    assert m33.shape == (3, 3)
    assert Matrix().shape == (0, 0)


def test_minor_submatrix():
    successful_cases = parse_removecolrow()
    for (m, i, j, ms) in successful_cases:
        m = Matrix(m).minor_submatrix(i, j)
        assert m == Matrix(ms)

    raises(ValueError, lambda: m33.minor_submatrix(-4, 1))
    raises(ValueError, lambda: m33.minor_submatrix(4, 1))


def test_swaps():
    m44_ = m44
    assert m44_.row_swap(1, 3) == Matrix(
        [[2, -1, 1, 8], [12, -7, -1, 6], [9, 8, 5, 9], [11, 4, 2, 0][12, -7, -1, 6]])
    assert m44_.col_swap(1, 3) == Matrix(
        [[2, 8,  1, -1], [11, 0,  2,  4], [9, 9,  5,  8], [12, 6, -1, -7]])

    m = Matrix([[4, 4, 4], [x, y, x], [2 * y, -1, z * x]])
    assert m.row_swap(1, 1) == m.col_swap(1, 1)
    assert m.row_swap(0, 1) == Matrix(
        [[x, y, x], [4, 4, 4], [2 * y, -1, z * x]])
    assert m.row_swap(1, 2) == Matrix([[x, x, y], [4, 4, 4], [2*y, x*z, -1]])

    m = Matrix(2, 2, [x, y, z, t])
    raises(IndexError, lambda: m.row_swap(0, 4))
    raises(IndexError, lambda: m.col_swap(0, 4))

    m32_ = m32
    assert m32_.row_swap(-1, 2) == Matrix([[1, 2], [3, 5], [1, 2]])
    assert m32_.row_swap(-1, 2) == Matrix([[2, 1], [5, 3], [2, 1]])

    m33_ = m33
    assert m33_.row_swap(0, 2) == Matrix([[0, 2, 5], [3, 4, 2], [1, -1, 3]])
    assert m33_.col_swap(0, 2) == Matrix([[5, 2, 9], [3, -1, 1], [2, 4, 3]])


def test_zeros():
    successful_cases = parse_zeros_n_eye('./zeros/zeros.txt')
    for case in successful_cases:
        dim = case[0]
        m = Matrix(case[1])
        if dim[0] == dim[1]:
            assert zeros(dim[0]) == m
        else:
            assert zeros(dim[0], dim[1]) == m

    assert Matrix() == zeros(0)

    raises(ValueError, lambda: zeros(-1))
    raises(ValueError, lambda: zeros(-42, 1))
    raises(ValueError, lambda: zeros(10, -1))
    raises(ValueError, lambda: zeros(3.2))
    raises(ValueError, lambda: zeros(51.78))


def test_ones():
    successful_cases = parse_zeros_ones_n_eye('./ones/ones.txt')
    for case in successful_cases:
        dim = case[0]
        m = Matrix(case[1])
        if dim[0] == dim[1]:
            assert ones(dim[0]) == m
        else:
            assert ones(dim[0], dim[1]) == m

    assert Matrix() == ones(0)

    raises(ValueError, lambda: ones(-1))
    raises(ValueError, lambda: ones(-42, 1))
    raises(ValueError, lambda: ones(10, -1))
    raises(ValueError, lambda: ones(3.2))
    raises(ValueError, lambda: ones(51.78))


def test_eye():
    successful_cases = parse_zeros_n_eye('./eye/eyes.txt')
    for case in successful_cases:
        dim = case[0]
        m = Matrix(case[1])
        if dim[0] == dim[1]:
            assert eye(dim[0]) == m
        else:
            assert eye(dim[0], dim[1]) == m

    assert Matrix() == eye(0)

    raises(ValueError, lambda: eye(-1))
    raises(ValueError, lambda: eye(-42))
    raises(ValueError, lambda: eye(3.2))
    raises(ValueError, lambda: eye(51.78))


def test_det():
    assert det(m22) == -2
    assert det(Matrix()) == 1
    assert det(Matrix([1])) == 1
    assert det(m44) == -198
    assert det(sm33) == -4 * x ** 2 * z + 4 * \
        x * y * z + 8 * x * y - 8 * y ** 2

    raises(ShapeError, lambda: det(m12))
    raises(ShapeError, lambda: det(m32))

    successful_cases = parse_determinants()
    for case in successful_cases:
        m = Matrix(case[0])
        assert case[1] == m.det(method="bareis") == m.det(
            method="det_lu") == m.det("Bareis")

    # https://github.com/sympy/sympy/blob/master/sympy/matrices/tests/test_matrices.py#L4104


def test_eigenvals():
    '''
    It takes the solutions given by the script written in Matlab which ut can be seen in eigenvals.m. The results of
    the scripts are written in eigenvals.txt which Python will read to check if the results of the library are the 
    same.

    If you want to add more tests, you can add them in the script in Matlab. Python will do everything automatically.
    '''

    def item_in_list(lst, it):
        for item in lst:
            if item.startswith(it):
                return True
        return False

    successful_cases = parse_eigenvalues()
    for case in successful_cases:
        m = Matrix(case[0])
        eigenvals = [str(x.evalf()) for x in m.eigenvals(multiple=True)]
        assert len(eigenvals) == len(case[1]) and set(map(lambda x: item_in_list(
            eigenvals, x), case[1])) == {True}

    raises(NonSquareMatrixError, lambda: m12.eigenvals())
    raises(NonSquareMatrixError, lambda: m32.eigenvals())


def test_eigenvectors():
    def test_eigenvector(m, lb, v):
        identity = eye(v.shape[0])
        # (A - eigenvalue[i] * I) * v = 0
        s = Mul(Add(m, Mul(-1, Mul(lb, identity))), v).evalf(0)

        # remove imaginary part
        if (str(type(s)) == "<class 'sympy.matrices.expressions.matexpr.ZeroMatrix'>"):
            assert sstr(s) == "0"
        else:
            assert Integer(s.norm()) == 0

    def test_matrix(m):
        vectors = m.eigenvects(chop=True)
        for sol in vectors:
            test_eigenvector(m, sol[0], sol[2][0])

    test_matrix(m22)
    test_matrix(m33)

    # Comment this one, it takes too much time!
    # test_matrix(m44)

    raises(NonSquareMatrixError, lambda: m12.eigenvects())
    raises(NonSquareMatrixError, lambda: m32.eigenvects())


def test_inv():
    def test_for_matrix(m):
        # A * A^-1 == A^-1 * A == I
        minv = m.inv()
        mI = eye((m.shape)[0])
        assert Mul(m, minv) == Mul(minv, m) == mI

    test_for_matrix(m22)
    test_for_matrix(m33)
    test_for_matrix(m44)

    raises(NonSquareMatrixError, lambda: m12.eigenvects())
    raises(NonSquareMatrixError, lambda: m32.eigenvects())


def test_qr():
    def test_for_matrix(m, matlabq, matlabr):
        Q, R = m.QRdecomposition()
        a = Abs(Q.evalf()) - Abs(matlabq)
        b = Abs(R.evalf()) - Abs(matlabr)
        assert a.norm() < 0.000000000001 and b.norm() < 0.000000000001

    successful_cases = parse_qr()
    for case in successful_cases:
        m = Matrix(case[0])
        matlabq = Matrix(case[1])
        matlabr = Matrix(case[2])
        test_for_matrix(m, matlabq, matlabr)


test_qr()


def test_diag():

    def own_diag(v):
        nv = list(map(lambda x: [x], v))
        return Matrix(nv)

    assert diag(v1) == own_diag(v1)
    assert diag(v2) == own_diag(v2)
    assert diag(list(range(100, 1.5, 10000))) == own_diag(list(range(100, 1.5, 10000)))


def test_cholesky():
    successful_cases = parse_cholesky()
    for (m, s) in successful_cases:
        m = Matrix(m).cholesky().evalf()
        assert Integer((m - Matrix(s)).norm()) == min(m.shape) - 2

    m = Matrix([[1, 1, 3], [1, 3, 2], [3, 2, 5]])
    raises(NonPositiveDefiniteMatrixError,
           lambda: m32.cholesky())

    raises(ValueError, lambda: m22.cholesky())
    raises(ValueError, lambda: m33.cholesky())

    raises(NonSquareMatrixError, lambda: m12.cholesky())
    raises(NonSquareMatrixError, lambda: m32.cholesky())


def test_charpoly():
    def get_components(e):
        l = [x.split(' + ') for x in e.split(' - ')]
        flat = [item for sublist in l for item in sublist]
        flat.sort()
        return flat

    def compare_charpolies(a, b):
        e1 = a[a.index('(') + 1:a.index(',')]
        e2 = b[b.index('(') + 1:b.index(',')]
        assert get_components(e1) == get_components(e2)

    successful_cases = parse_charpoly()
    for (m, s) in successful_cases:
        m = Matrix(m).charpoly()
        compare_charpolies(sstr(m), s)

    raises(NonSquareMatrixError, lambda: m12.cholesky())
    raises(NonSquareMatrixError, lambda: m32.cholesky())

'''
test_creation()
test_division()
test_sum()
test_abs()
test_eigenvals()
test_det()
test_eigenvectors()
test_eye()
test_diag()
test_cholesky()
'''
