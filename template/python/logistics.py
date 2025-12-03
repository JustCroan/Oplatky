from proboj import *
from movement import *
from eval import *
def BuyShips(self,cur_rock,cur_fuel,cur_ships_types):
    turns = []
    while(True):
        ship_to_buy = ShipToBuy(self,cur_rock,cur_fuel,cur_ships_types)
        if(ship_to_buy is None): break 
        turns.append(BuyTurn(ship_to_buy))
        self.log(f"Buying {ship_to_buy}")
        cur_ships_types.append(ship_to_buy)
        cur_rock-=250
        cur_fuel-=100
    return [turns,cur_rock,cur_fuel]

def Assign(self,ship,mothership,my_ships):
    if(ship.type == ShipType.TRUCK_SHIP):
            if(ship.rock>0):
                self.task[ship.id]=mothership.id
            else:
                bestrock = -1
                best = None
                for drill in my_ships:
                    if(drill.type==ShipType.DRILL_SHIP and self.assignedto[drill.id] is None):
                        if drill.rock>bestrock:
                            bestrock=drill.rock
                            best=drill
                if(best is not None):
                    self.task[ship.id]=best.id
                    self.assignedto[best.id]=ship.id
                    return best.id
    elif(ship.type == ShipType.TANKER_SHIP):
        if(ship.fuel>0):
            self.task[ship.id]=mothership.id
        else:
            bestfuel = -1
            best = None
            for sucker in my_ships:
                if(sucker.type==ShipType.SUCKER_SHIP and self.assignedto[sucker.id] is None):
                    if sucker.fuel>bestfuel:
                        bestfuel=sucker.fuel
                        best=sucker
            if(best is not None):
                self.task[ship.id]=best.id
                self.assignedto[best.id]=ship.id
                return best.id
    return None


def OperateShips(self,my_ships,asteroids,ships,mothership):
    turns = []
    for ship in my_ships:
        if(ship.type == ShipType.DRILL_SHIP):
            best = None
            bestdist = float('inf')
            for asteroid in asteroids:
                if(asteroid is None): continue
                dist = ship.position.distance(asteroid.position)
                if(asteroid.type == AsteroidType.ROCK_ASTEROID and dist<bestdist):
                    bestdist = dist
                    best = asteroid
            if(best is not None):
                if(bestdist<50): turns.append(MoveTurn(ship.id,Brake(ship)))
                else: turns.append(MoveTurn(ship.id,Adjust(ship,best)))
        elif(ship.type == ShipType.TRUCK_SHIP):
            if(self.task[ship.id] is None):
                self.log(Assign(self,ship,mothership,my_ships))
            if(self.task[ship.id] is not None):
                goal = ships[self.task[ship.id]]
                dist = ship.position.distance(goal.position)
                if(dist < 20):
                    if(goal.type == ShipType.MOTHER_SHIP):
                        turns.append(SiphonTurn(ship.id,self.task[ship.id],ship.rock))
                        self.task[ship.id]=None
                    else:
                        turns.append(SiphonTurn(self.task[ship.id],ship.id,ship.rock))
                        self.assignedto[self.task[ship.id]]=None
                        self.task[ship.id]=None
                else:
                    self.log("hybem")
                    turns.append(MoveTurn(ship.id,Adjust(ship,goal)))
        elif(ship.type == ShipType.SUCKER_SHIP):
            best = None
            bestdist = float('inf')
            for asteroid in asteroids:
                if(asteroid is None): continue
                dist = ship.position.distance(asteroid.position)
                if(asteroid.type == AsteroidType.FUEL_ASTEROID and dist<bestdist):
                    bestdist = dist
                    best = asteroid
            if(best is not None):
                if(bestdist<50): turns.append(MoveTurn(ship.id,Brake(ship)))
                turns.append(MoveTurn(ship.id,Adjust(ship,best)))
        elif(ship.type == ShipType.TANKER_SHIP):
            if(self.task[ship.id] is None):
                Assign(self,ship,mothership,my_ships)
            else:
                goal = ships[self.task[ship.id]]
                dist = ship.position.distance(goal.position)
                if(dist < 20):
                    if(goal.type == ShipType.MOTHER_SHIP): 
                        turns.append(SiphonTurn(ship.id,self.task[ship.id],ship.fuel))
                        self.task[ship.id]=None
                    else: 
                        turns.append(SiphonTurn(self.task[ship.id],ship.id,ship.fuel))
                        self.assignedto[self.task[ship.id]]=None
                        self.task[ship.id]=None
                else:

                    turns.append(MoveTurn(ship.id,Adjust(ship,goal)))
        elif(ship.type == ShipType.BATTLE_SHIP):
            pass
        elif(ship.type == ShipType.MOTHER_SHIP):
            pass
    return turns
def CheckAssignments(self,ships):
    for key in self.task:
        if(ships[key].is_destroyed):
            self.assigned[self.task[key]] = None
            self.task[key] = None