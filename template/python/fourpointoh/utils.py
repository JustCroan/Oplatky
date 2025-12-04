from proboj import *
from math import sin, cos 

def Dot_Product(vector1: Position, vector2: Position):
    return vector1.x*vector2.x + vector1.y*vector2.y

def Dot_Product_Normalized(vector1: Position, vector2: Position):
    return Dot_Product(vector1, vector2)/(vector1.size()*vector2.size())

def Reflect_Vector(reflector: Position, vector: Position):
    refl = reflector.normalize()
    return vector.scale(-1).add(refl.scale(2*Dot_Product(refl, vector)))

class Matrix:
    def __init__(self, x1: float, x2: float, y1: float, y2: float) -> None:
        self.matrix: list[list[float]] = [[x1, x2], [y1, y2]]
        self.col1 = Position(x1, y1)
        self.col2 = Position(x2, y2)
        self.row1 = Position(x1, x2)
        self.row2 = Position(y1, y2)

    def Matrix_Vector(self, vector: Position) -> Position:
        return Position(Dot_Product(vector, self.row1), Dot_Product(vector, self.row2))
    
    
def Matrix_Scalar(self, num: float) -> Matrix:
    return Matrix(self.matrix[0][0]*num, self.matrix[0][1]*num, self.matrix[1][0]*num, self.matrix[1][1]*num)

def Transpose(matrix: Matrix) -> Matrix:
    return Matrix(matrix.matrix[0][0], matrix.matrix[1][0], matrix.matrix[0][1], matrix.matrix[1][1])
    
def Matrix_Mult(matrix1: Matrix, matrix2: Matrix) -> Matrix:
    return Matrix(Dot_Product(matrix1.row1, matrix2.col1), Dot_Product(matrix1.row1, matrix2.col2), Dot_Product(matrix1.row2, matrix2.col1), Dot_Product(matrix1.row2, matrix2.col2))
