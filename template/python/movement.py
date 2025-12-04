from proboj import *
from utils import *

#Use to stay in range of target
def Hover(ship: Ship, target: Asteroid | Ship):
    return MoveTurn(ship.id,target.position.sub(ship.position).normalize())
    

#Whether we can use faster movement
def Fast(ship: Ship):
    return 1 + 2*(int(ship.type == ShipType.TANKER_SHIP or ship.type == ShipType.TRUCK_SHIP))

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
    
def Adjust2(ship: Ship, target: Asteroid | Ship):
    v = ship.vector.size()
    d = ship.position.distance(target.position)
    a = Fast(ship)
    if v/a*(v+1)/2 + 5> d:
        return ship.vector.scale(-1).add(target.position.sub(ship.position).normalize().scale(v-1))
    else:
        return ship.vector.scale(-1).add(target.position.sub(ship.position).normalize().scale(v+1))
    

    
def Ultra_Adjust(ship: Ship, target: Asteroid | Ship):
    ve = ship.vector
    dif = target.position.sub(ship.position)
    do = Dot_Product(ve, dif)
    sds = Dot_Product(ve, ve) - Fast(ship)**2
    sdt = Dot_Product(dif, dif)
    try: 
        koef1 = ( do*2 + ( do**2 - 4*sds*sdt )**0.5 )/sdt
        koef2 = ( do*2 - ( do**2 - 4*sds*sdt )**0.5 )/sdt

        vects = sorted([dif.scale(koef1), dif.scale(koef2)], key= lambda x: x.size())

        v = ship.vector.size()
        d = ship.position.distance(target.position)
        a = Fast(ship)
        if v/a*(v+1)/2 > d:
            return vects[0].sub(ve)
        else:
            return vects[1].sub(ve)
    except:
        v_dot = dif.normalize().scale(Dot_Product_Normalized(ve, dif)*ve.size())
        return v_dot.sub(ve).normalize()

#Begin Movement to target with some target time    
def Begin_Route(ship: Ship, target: Asteroid | Ship, time_target: int):
    dist = ship.position.distance(target.position)
    dir = target.position.sub(ship.position).normalize()
    k = max(1, (4*dist - time_target**2)/(2*time_target)-5)
    return dir.scale(k)

def Brake(ship: Ship):
    return ship.vector.scale(-1)
