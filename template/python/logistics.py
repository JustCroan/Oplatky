from proboj import *
from movement import *
from eval import *
from collections import defaultdict
from battle_tacticts import *

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

def BuyShips2(self,cur_rock,cur_fuel,cur_ships_types):
    turns = []
    while(True):
        ship_to_buy = ShipToBuy2(self,cur_rock,cur_fuel,cur_ships_types)
        if(ship_to_buy is None): break 
        turns.append(BuyTurn(ship_to_buy))
        self.log(f"Buying {ship_to_buy}")
        cur_ships_types.append(ship_to_buy)
        cur_rock-=250
        cur_fuel-=100
    return [turns,cur_rock,cur_fuel]

def BuyShipsConquer(self,cur_rock,cur_fuel,cur_ships_types):
    turns = []
    while(True):
        ship_to_buy = ShipToBuyConquer(self,cur_rock,cur_fuel,cur_ships_types)
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
                return mothership.id
            else:
                bestrock = 0
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
            return mothership.id
        else:
            bestfuel = 0
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

def Assign2(self,ship,asteroids,siphoningfuel):
    fuelcap = float('inf')
    sfswitch = 0
    if(ship.type == ShipType.DRILL_SHIP):
        bestdist = float('inf')
        best = None
        for asteroid in asteroids:
            if(asteroid is None): continue
            try: 
                if 0.02 >= Dot_Product(asteroid.position.sub(self.game_map.get_my_mothership().position), self.game_map.get_my_mothership().sub(self.premothership)): continue
            except: pass
            if(asteroid.type==AsteroidType.ROCK_ASTEROID and self.takenby[asteroid.id] is None and asteroid.owner_id != self.my_player_id):
                if ship.position.distance(asteroid.position)<bestdist:
                    bestdist = ship.position.distance(asteroid.position)
                    best=asteroid
        if(best is not None):
            self.job[ship.id]=best.id
            self.takenby[best.id]=ship.id
            self.fuelplan[ship.id]=min(min((ship.fuel+sfswitch*siphoningfuel[ship.id])/5,bestdist/5),fuelcap)
            self.speedup[ship.id]=True
            return best.id
    elif(ship.type == ShipType.SUCKER_SHIP):
        bestdist = float('inf')
        best = None
        for asteroid in asteroids:
            if(asteroid is None): continue
            if(asteroid.type==AsteroidType.FUEL_ASTEROID and self.takenby[asteroid.id] is None and asteroid.owner_id != self.my_player_id):
                if ship.position.distance(asteroid.position)<bestdist:
                    bestdist = ship.position.distance(asteroid.position)
                    best=asteroid
        if(best is not None):
            self.job[ship.id]=best.id
            self.takenby[best.id]=ship.id
            self.fuelplan[ship.id]=min(min((ship.fuel+sfswitch*siphoningfuel[ship.id])/5,bestdist/5),fuelcap)
            self.speedup[ship.id]=True
            return best.id
    elif(ship.type == ShipType.BATTLE_SHIP):
        bestdist = float('inf')
        best = None
        for asteroid in asteroids:
            if(asteroid is None): continue
            if(self.takenby[asteroid.id] is None and asteroid.owner_id != self.my_player_id):
                if ship.position.distance(asteroid.position)<bestdist:
                    bestdist = ship.position.distance(asteroid.position)
                    best=asteroid
        if(best is not None):
            self.job[ship.id]=best.id
            self.takenby[best.id]=ship.id
            self.fuelplan[ship.id]=min(min((ship.fuel+sfswitch*siphoningfuel[ship.id])/20,bestdist/5),fuelcap)
            self.speedup[ship.id]=True
            return best.id
    return None

def AssignMothership(self,mothership,asteroids,my_ships):
    global index
    index += 1
    best = None
    bestdist = float('inf')
    for asteroid in asteroids:
        if asteroid is None or asteroid.owner_id == self.my_player_id or self.takenby[asteroid.id] is not None or mothership.position.distance(asteroid.position)>100000:continue
        curdist = 0
        for my_ship in my_ships:
            curdist += asteroid.position.distance(my_ship.position)
        asteroiddists = []
        for asteroid2 in asteroids:
            if(asteroid2 is None): continue
            asteroiddists.append(asteroid.position.distance(asteroid2.position))
        asteroiddists.sort()
        asteroiddist = sum(asteroiddists[0:len(asteroiddists)])
        if(curdist*50+asteroiddist<bestdist):
            bestdist=curdist*50+asteroiddist
            best=asteroid.position
    self.job[mothership.id]=best
    self.premothership=self.job[mothership.id]
    self.fuelplan[mothership.id] = mothership.fuel/6
    self.speedup[mothership.id] = True
    return best

Mothership_Movement = [500,750,1000,1200,1500,1800]
Mothership_Movement_Precal = [i-150 for i in Mothership_Movement]
index = -1

def OperateShips2(self,my_ships,asteroids,ships,mothership,siphoningfuel):
    turns = []
    fuelintake = 100
    fuelintake = int(max(mothership.fuel//(1.5*(len(my_ships))),fuelintake))
    for ship in my_ships:

        
        if(ship.type == ShipType.DRILL_SHIP):
            if(self.job[ship.id] is None):
                Assign2(self,ship,asteroids,siphoningfuel)
                turns.append(LoadTurn(ship.id,mothership.id,ship.rock))
            else:
                if(self.job[ship.id]==mothership.id or asteroids[self.job[ship.id]] is None):
                    if (self.job[ship.id]!=mothership.id): self.speedup[ship.id]=True
                    self.job[ship.id]=mothership.id
                    dist = ship.position.distance(mothership.position)
                    if(dist < 15 and mothership.position.distance(self.premothership)<1):
                        if(ship.vector.size()>0.1 and ship.fuel>ship.vector.size()):
                            turns.append(MoveTurn(ship.id,Brake(ship)))
                        else:
                            if(not self.mothershipinuse):
                                self.log(f"siphonujem {ship.id}")
                                turns.append(SiphonTurn(mothership.id,ship.id,min(int(mothership.fuel),int(fuelintake))))
                                siphoningfuel[ship.id]+=min(mothership.fuel,fuelintake)
                                Assign2(self,ship,asteroids,siphoningfuel)
                                self.mothershipinuse=True
                                self.job[ship.id]=None
                    else:
                        turns.append(DecideMove(self,ship,self.premothership))
                else:
                    if(ship.position.distance(asteroids[self.job[ship.id]].position)<50): 
                        turns.append(MoveTurn(ship.id,Brake(ship)))
                    else:
                        goal = asteroids[self.job[ship.id]]
                        if(ship.position.distance(goal.position)<50): 
                            turns.append(MoveTurn(ship.id,Brake(ship)))
                        else:
                            turns.append(DecideMove(self,ship,goal))



        elif(ship.type == ShipType.SUCKER_SHIP):
            if(self.job[ship.id] is None):
                Assign2(self,ship,asteroids,siphoningfuel)
            else:
                if(self.job[ship.id]==mothership.id or asteroids[self.job[ship.id]] is None):
                    if (self.job[ship.id]!=mothership.id): self.speedup[ship.id]=True
                    self.job[ship.id]=mothership.id
                    dist = ship.position.distance(mothership.position)
                    if(dist < 15 and mothership.position.distance(self.premothership)<1):
                        if(ship.vector.size()>0.1 and ship.fuel>ship.vector.size()):
                            turns.append(MoveTurn(ship.id,Brake(ship)))
                        else:
                            turns.append(SiphonTurn(ship.id,mothership.id,max(int(ship.fuel)-int(fuelintake),0)))
                            self.job[ship.id]=None
                    else:
                        turns.append(DecideMove(self,ship,self.premothership))
                else:
                    if(ship.position.distance(asteroids[self.job[ship.id]].position)<50): 
                        turns.append(MoveTurn(ship.id,Brake(ship)))
                    else:
                        goal = asteroids[self.job[ship.id]]
                        if(ship.position.distance(goal.position)<50): 
                            turns.append(MoveTurn(ship.id,Brake(ship)))
                        else:
                            turns.append(DecideMove(self,ship,goal))




        elif(ship.type == ShipType.BATTLE_SHIP):
            if(self.job[ship.id] is None or asteroids[self.job[ship.id]] is None or asteroids[self.job[ship.id]].owner_id == self.my_player_id):
                Assign2(self,ship,asteroids,siphoningfuel)
            if(self.job[ship.id] is not None and asteroids[self.job[ship.id]] is not None):
                goal = asteroids[self.job[ship.id]]
                dist = ship.position.distance(goal.position)
                if(dist < 50):
                    ch = 0
                    for othership in ships:
                        if(othership.player_id != self.my_player_id and ship.position.distance(othership.position)<500):
                            turns.append(ShootTurn(ship.id,othership.id))
                            ch = 1
                            break
                    if(not ch):
                        turns.append(MoveTurn(ship.id,Brake(ship)))
                else:
                    ch = 0
                    for othership in ships:
                        if(othership.player_id != self.my_player_id and ship.position.distance(othership.position)<500 and othership.type == ShipType.BATTLE_SHIP):
                            turns.append(ShootTurn(ship.id,othership.id))
                            ch = 1
                            break
                    if(not ch):
                        turns.append(MoveTurn(ship.id,Adjust2(ship,goal)))
        elif(ship.type == ShipType.MOTHER_SHIP):
            self.log(f"rounder {self.game_map.round}")
            if(self.game_map.round in [500,1000,1500]):
                self.log(f"assignujem mothershipke {AssignMothership(self,mothership,asteroids,my_ships)}")
            if self.job[ship.id] is not None:
                if(not self.mothershipinuse) and self.game_map.round >= Mothership_Movement[index]:
                    if(ship.position.distance(self.job[ship.id])<max(50,mothership.vector.size()+10)):
                        turns.append(MoveTurn(ship.id,Brake(ship)))
                        self.job[ship.id]=None
                    else:
                        turns.append(DecideMove(self,mothership,self.job[ship.id]))
                    self.mothershipinuse=True
    return turns
def OperateShips(self,my_ships,asteroids,ships,mothership):
    presun = defaultdict(lambda:0)
    turns = []

    for ship in my_ships:
        if(ship.type == ShipType.TRUCK_SHIP):
            if(self.task[ship.id] is None):
                self.log(Assign(self,ship,mothership,my_ships))
            if(self.task[ship.id] is not None):
                goal = ships[self.task[ship.id]]
                dist = ship.position.distance(goal.position)
                self.log(f"som {ship.id} potom {goal.id} potom {ship.rock} potom {dist}")
                if(dist < 20):
                    if(goal.type == ShipType.MOTHER_SHIP):
                        self.log(f"Loadujem {ship.id} potom {goal.id} potom {ship.rock} ")
                        turns.append(LoadTurn(ship.id,goal.id,ship.rock))
                        self.task[ship.id]=None
                        presun[goal.id]=1
                    elif goal.rock>0:
                        self.log(f"loadujem {goal.id} potom {ship.id} potom {goal.rock} potom {ship.position.distance(goal.position)}")
                        turns.append(LoadTurn(goal.id,ship.id,goal.rock))
                        self.assignedto[self.task[ship.id]]=None
                        self.task[ship.id]=None
                        presun[goal.id]=1
                # elif dist<60 and ship.vector.size() > 3:
                #     turns.append(MoveTurn(ship.id,ship.vector.scale(-1)))
                else:
                    turns.append(MoveTurn(ship.id,Ultra_Adjust(ship,goal)))



        elif(ship.type == ShipType.TANKER_SHIP):
            if(self.task[ship.id] is None):
                Assign(self,ship,mothership,my_ships)
            else:
                goal = ships[self.task[ship.id]]
                dist = ship.position.distance(goal.position)
                if(dist < 20):
                    if(goal.type == ShipType.MOTHER_SHIP): 
                        turns.append(SiphonTurn(ship.id,goal.id,ship.fuel))
                        self.task[ship.id]=None
                        presun[goal.id]=1
                    elif(goal.fuel>0):
                        turns.append(SiphonTurn(goal.id,ship.id,goal.fuel))
                        self.assignedto[self.task[ship.id]]=None
                        self.task[ship.id]=None
                        presun[goal.id]=1
                # elif dist<60 and ship.vector.size() > 3:
                #     turns.append(MoveTurn(ship.id,ship.vector.scale(-1)))
                else:
                    turns.append(MoveTurn(ship.id,Ultra_Adjust(ship,goal)))



        elif(ship.type == ShipType.BATTLE_SHIP):
            pass



    for ship in my_ships:
        if(presun[ship.id]): continue
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
                else: turns.append(MoveTurn(ship.id,Ultra_Adjust(ship,best)))




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
                if(bestdist<50): self.log('brakae') ; turns.append(MoveTurn(ship.id,Brake(ship)))
                turns.append(MoveTurn(ship.id,Ultra_Adjust(ship,best)))
                pass
        elif(ship.type == ShipType.MOTHER_SHIP):
            pass
    return turns
def CheckAssignments(self,ships):
    for key in self.task:
        if(ships[key].is_destroyed):
            self.assigned[self.task[key]] = None
            self.task[key] = None

