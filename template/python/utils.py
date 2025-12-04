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
        self.matrix: list[Position] = [Position(x1, x2), Position(y1, y2)]

    def Matrix_Vector(self, vector: Position) -> Position:
        return Position(Dot_Product(vector, self.matrix[0]), Dot_Product(vector, self.matrix[1]))
    
    def Matrix_Scalar(self, num: float):
        return Matrix(self.matrix[0].x*num, self.matrix[0].y*num, self.matrix[1].x*num, self.matrix[1].y*num)


