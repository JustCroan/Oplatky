from proboj import *
from movement import *
from eval import *
from logistics import *

def Centralize(ship: Ship, bulharska: float):
    v = ship.vector.size()
    d = ship.position.distance(Position(0,0))
    a = 1+bulharska
    if v/a*(v+1)/2 + 10> d or ( v/a*(v+1)/2 > d and v < 2):
        return MoveTurn(ship.id, ship.vector.normalize().scale(-a))
    else:
        return MoveTurn(ship.id, Position(0, 0).sub(ship.position).normalize().scale(a))



