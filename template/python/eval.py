from proboj import *
def ShipToBuy(self,rock,fuel,cur_ships_types):
    player = self.get_my_player()
    if(rock < 250 or fuel < 100):
        return None
    amts = [0,0,0,0,0,0]
    for type in cur_ships_types:
        amts[type.value]+=1
    if(amts[ShipType.DRILL_SHIP.value] == min(amts[1:5])): return ShipType.DRILL_SHIP
    if(amts[ShipType.TRUCK_SHIP.value] == min(amts[1:5])): return ShipType.TRUCK_SHIP
    if(amts[ShipType.SUCKER_SHIP.value] == min(amts[1:5])): return ShipType.SUCKER_SHIP
    if(amts[ShipType.TANKER_SHIP.value] == min(amts[1:5])): return ShipType.TANKER_SHIP
    
def ShipToBuy2(self,rock,fuel,cur_ships_types):
    player = self.get_my_player()
    if(rock < 250 or fuel < 100):
        return None
    amts = [0,0,0,0,0,0]
    for type in cur_ships_types:
        amts[type.value]+=1
    if(amts[ShipType.BATTLE_SHIP.value]<sum(amts)//20): return ShipType.BATTLE_SHIP
    if(amts[ShipType.DRILL_SHIP.value] == min(amts[1:3])): return ShipType.DRILL_SHIP
    if(amts[ShipType.SUCKER_SHIP.value] == min(amts[1:3])): return ShipType.SUCKER_SHIP

def ShipToBuyConquer(self,rock,fuel,cur_ships_types):
    player = self.get_my_player()
    if(rock < 250 or fuel < 100):
        return None
    return ShipType.BATTLE_SHIP