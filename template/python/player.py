#!/bin/python3
import math
from collections import defaultdict
from typing import List
from proboj import (
    Client,
    BuyTurn,
    MoveTurn,
    LoadTurn,
    SiphonTurn,
    ShootTurn,
    RepairTurn,
    ShipType,
    Position,
    Turn,
)

from movement import *
from eval import *
from logistics import *

class MyClient(Client):
    assignedto = defaultdict(lambda : None)
    task = defaultdict(lambda : None)
    job = defaultdict(lambda : None)
    takenby = defaultdict(lambda : None)
    speedup = defaultdict(lambda : False)
    fuelplan = defaultdict(lambda : None)
    mothershipinuse = False
    premothership = Position(0,0)
    def turn(self) -> List[Turn]:

        self.mothershipinuse = False
        player = self.get_my_player()
        my_ships = self.get_my_ships()
        mothership = self.get_my_mothership()
        self.premothership = mothership.position
        ships = self.game_map.ships
        asteroids = self.game_map.asteroids
        cur_ships_types = [my_ships[i].type for i in range(len(my_ships))]
        round = self.game_map.round
        cur_rock = player.rock
        cur_fuel = player.fuel
        turns: List[Turn] = []
        siphoningfuel = defaultdict(lambda:0)
        

        #self.log(f"My ships: {(my_ships)}")
        CheckAssignments(self,ships)

        #if (round<1200): res=BuyShips2(self,cur_rock,cur_fuel,cur_ships_types)
        executeorder66 = 800
        res=BuyShips2(self,cur_rock,cur_fuel,cur_ships_types,executeorder66)

        turns+=res[0]
        cur_rock=res[1]
        cur_fuel=res[2]

        turns+=OperateShips2(self,my_ships,asteroids,ships,mothership,siphoningfuel)



        self.log(turns)
        return turns    

if __name__ == "__main__":
    client = MyClient()
    client.run()
