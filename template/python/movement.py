from proboj import *
from utils import *
from math import sqrt

#Use to stay in range of target
def Hover(ship: Ship, target: Asteroid | Ship):
    return MoveTurn(ship.id,target.position.sub(ship.position).normalize())

def Is_overshooting(ship: Ship, target: Asteroid | Ship | Position):
    goalpos: Position
    if(not isinstance(target, Position)): goalpos=target.position
    else: goalpos = target
    return goalpos.distance(ship.position) < ship.vector.size()

#Whether we can use faster movement
def Fast(ship: Ship):
    return 1 + 2*(int(ship.type == ShipType.TANKER_SHIP or ship.type == ShipType.TRUCK_SHIP))

def Normalize_Fuel(ship: Ship, vector: Position):
    if ship.fuel >= vector.size() - Fast(ship):
        return vector
    else:
        return vector.normalize().scale(max(1, ship.fuel + Fast(ship) - 0,1))

#Flight adjuster for asteroid
'''
def Adjust(ship: Ship, target: Asteroid):
    v = ship.vector.size()
    dif = target.position.sub(ship.position)
    d = ship.position.distance(target.position)
    project = dif.normalize().scale((ship.position.x*dif.x + ship.position.y*dif.y)/d)
    if v*(v+1)/2 - 15 > d:
        return project.sub(ship.vector).normalize()
'''
def Adjust(ship: Ship, target: Asteroid | Ship):
    v = ship.vector.size()
    d = ship.position.distance(target.position)
    a = Fast(ship)
    if v/a*(v+1)/2 + 10> d or ( v/a*(v+1)/2 > d and v < 2):
        return ship.vector.normalize().scale(-1)
    else:
        return target.position.sub(ship.position).normalize().scale(a)
    
def Adjust2(ship: Ship, target: Asteroid | Ship | Position, fuelplan=1):
    goalpos = target
    if(not isinstance(target, Position)): goalpos=target.position
    v = ship.vector.size()
    d = ship.position.distance(goalpos)
    a = Fast(ship)
    if not Is_overshooting(ship, target):
        if (v-fuelplan)/a*(v+fuelplan)/2 > d:
            return Normalize_Fuel(ship, ship.vector.scale(-1).add(goalpos.sub(ship.position).normalize().scale(v-a)))
        else:
            return Normalize_Fuel(ship, ship.vector.scale(-1).add(goalpos.sub(ship.position).normalize().scale(v+a)))
    else:
        return Normalize_Fuel(ship, goalpos.sub(ship.position).sub(ship.vector))

    
def Ultra_Adjust(ship: Ship, target: Asteroid | Ship):
    ve = ship.vector
    dif = target.position.sub(ship.position)
    do = Dot_Product(ve, dif)
    sds = Dot_Product(ve, ve) - Fast(ship)**2
    sdt = Dot_Product(dif, dif)
    try: 
        koef1 = ( do*2 + sqrt( 4*(do**2) - 4*sds*sdt ) )/sdt
        koef2 = ( do*2 - sqrt( 4*(do**2) - 4*sds*sdt ) )/sdt

        vects = sorted([dif.scale(koef1), dif.scale(koef2)], key= lambda x: Dot_Product(x, dif))

        v = ship.vector.size()
        d = ship.position.distance(target.position)
        if v*(v+1)/2 > d:
            return vects[0].sub(ve)
        else:
            return vects[1].sub(ve)
    except:
        v_dot = dif.normalize().scale(Dot_Product_Normalized(ve, dif)*ve.size())
        return v_dot.sub(ve).normalize().scale(Fast(ship))

#Begin Movement to target with some target time    
def Begin_Route(ship: Ship, target: Asteroid | Ship | Position, time_target: int):
    goalpos = target
    if(not isinstance(target, Position)): goalpos=target.position
    dist = ship.position.distance(goalpos)
    dir = goalpos.sub(ship.position).normalize()
    k = max(1, (4*dist - time_target**2)/(2*time_target)-5)
    return dir.scale(k)

def Begin_Fuel_Route(ship: Ship, target: Asteroid | Ship | Position, fuel_target: float):
    goalpos = target
    if(not isinstance(target, Position)): goalpos=target.position
    v = ship.vector.size()
    d = ship.position.distance(goalpos)
    a = Fast(ship)
    return Normalize_Fuel(ship, ship.vector.scale(-1).add(goalpos.sub(ship.position).normalize().scale(v + fuel_target)))

def Brake(ship: Ship):
    return ship.vector.scale(-1)

def DecideMove(self,ship,goal):
    if(self.speedup[ship.id]): 
        self.speedup[ship.id]=False
        return (MoveTurn(ship.id,Begin_Fuel_Route(ship,goal,self.fuelplan[ship.id])))
    else: 
        return (MoveTurn(ship.id,Adjust2(ship,goal,self.fuelplan[ship.id])))

def Path_Offset(ship: Ship, target: Asteroid | Ship | Position):
    goalpos: Position
    if(not isinstance(target, Position)): goalpos=target.position
    else: goalpos = target
    return Dot_Product(goalpos.sub(ship.position), ship.vector)

def Is_shoot_capable(ship: Ship, targer: Asteroid | Ship | Position):
    pass

