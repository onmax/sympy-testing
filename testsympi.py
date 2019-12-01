import sympy as sym 
from sympy.matrices import *

x = Matrix(4,4,[2,-1,1,8,11,4,2,0,9,8,5,9,12,-7,-1,6])
y = Matrix(3,2, [-1,2,3,5,1,2])
z = Matrix(3,3, [1,-1,3,3,4,2,0,2,5])




print x
print('\n')
print y
print('\n')
print z
print('\n')


print "Row swap function"

print "Test1"
x.row_swap(1,3)     # Ok
print x
print('\n')

print "Test2"
#y.row_swap(1,3)     # error   IndexError: Index out of range: a[3]
#print y  
print('\n')

print "Test3"
z.row_swap(0,-2)     # access row with negative index
print z
print('\n')

#----------------------------------------------------------------------#

x = Matrix(4,4,[2,-1,1,8,11,4,2,0,9,8,5,9,12,-7,-1,6])
y = Matrix(3,2, [-1,2,3,5,1,2])
z = Matrix(3,3, [1,-1,3,3,4,2,0,2,5])

print "Col swap function"

print "Test1"
x.col_swap(0,3)
print x
print('\n')

print "Test2"
#y.col_swap(1,3)      # error   IndexError: Index out of range: a[3]
#print x
print('\n')

print "Test3"
z.col_swap(0,-2)     # access column with negative index
print z
print('\n')

#-------------------------------------------------------------------#

#  determinent #
print "Determinent function"

A = Matrix(3,3,[-1,-6,3,5,6,-7,-2,0,1])

print "Test1"
a = det(A)       # -24 page:526
print a
print('\n')


B = Matrix(3,2,[2,3,6,7,9,6])
print "Test2"
#b = det(B)      #   sympy.matrices.common.ShapeError: Det of a non-square matrix
#print b 
#print('\n')

print "Test3"
#c = det()      # calling function without argument       TypeError: det() takes exactly 1 argument (0 given)


#-----------------------------------------------------------------------------#

#  eigenvals #
print "eigenvals function"

K = Matrix(2,2,[2, 0, 1, 3])       
A = Matrix(2,2,[-20,10,10,-10])    # complex eigenvalues 
y = Matrix(3,2, [-1,2,3,5,1,2])    # non-sequre matrix

print K
print('\n')
print A
print('\n')
print y
print('\n')

print "Test1"
EigenValues = K.eigenvals()
print EigenValues
print('\n')

print "Test2"
EigenValues = A.eigenvals()
print EigenValues
print('\n')

print "Test3"
#EigenValues = y.eigenvals()
#print EigenValues
print('\n')

#-----------------------------------------------------------------------------#

#  eigen vector #
print "eigenvects function"

B = Matrix([[3, -2,  4, -2], [5,  3, -3, -2], [5, -2,  2, -2], [5, -2, -3,  3]])
y = Matrix(3,2, [-1,2,3,5,1,2])    # non-sequre matrix

print B
print('\n')


print "Test1"
EigenVectors = B.eigenvects()
print EigenVectors
print('\n')

print "Test2"
#EigenVectors = y.eigenvects()
#print EigenVectors
print('\n')

#-----------------------------------------------------------------------------#

#  eye function #
print "eye function"

print "Test1"
print eye(3)
print('\n')

print "Test2"
print eye(20)
print('\n')

print "Test3"
#print eye(-3)
print('\n')

print "Test4"
#print eye(3.5)
print('\n')

print "Test5"
#print eye()
print('\n')

#-----------------------------------------------------------------------------#

#  Cholesky function #
print "Cholesky function"


A = Matrix(3,3,[4,12,-16,12,37,-43,-16,-43,98])
B = Matrix(3,3,[25,15,-5,15,18,0,-5,0,11])
y = Matrix(3,2, [-1,2,3,5,1,2])


print A
print('\n')
print B
#print y.cols
print('\n')
print y
print('\n')


print "Test1"
Z = A.cholesky()
print Z
print('\n')


print "Test2"
C = B.cholesky()
print C
print('\n')

D = B.cholesky() * B.cholesky().T
print D
print('\n')


print "Test3"
E = y.cholesky()
print E
print('\n')