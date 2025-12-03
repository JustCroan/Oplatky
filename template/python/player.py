#!/bin/python3
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

class MyClient(Client):
    def turn(self) -> List[Turn]:

        player = self.get_my_player()
        my_ships = self.get_my_ships()
        self.log(f"My ships: {my_ships}")
        turns: List[Turn] = []
        round = self.game_map.round
        cur_rock = player.rock
        cur_fuel = player.fuel
        while(True):
            ship_to_buy = ShipToBuy(self,cur_rock,cur_fuel)
            if(ship_to_buy is None): break 
            turns.append(BuyTurn(ship_to_buy))
            self.log(f"Buying {ship_to_buy}")
            my_ships.append(ship_to_buy)
            cur_rock-=250
            cur_fuel-=100
        return turns

if __name__ == "__main__":
    client = MyClient()
    client.run()
