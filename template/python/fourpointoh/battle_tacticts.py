from proboj import *
from movement import *
from eval import *
from logistics import *

def Centralize(self,ship: Ship, bulharska: float, asteroids , myships):

    v = ship.vector.size()
    d = ship.position.distance(Position(0,0))
    a = 1+bulharska
    if v/a*(v+1)/2 + 10> d or ( v/a*(v+1)/2 > d and v < 2):
        return MoveTurn(ship.id, ship.vector.normalize().scale(-a))
    else:
        return MoveTurn(ship.id, Position(0,0).sub(ship.position).normalize().scale(a))

def Constant_Centralize(ship: Ship, bulharska: float):
    d = ship.position.size()
    if 2*bulharska < d and ship.vector.size() > bulharska - 0.01:
        return None
    elif ship.vector.size() == 0: return MoveTurn(ship.id, Position(0,0).sub(ship.position).normalize().scale(bulharska))
    else:
        return MoveTurn(ship.id, ship.vector.scale(-1))

