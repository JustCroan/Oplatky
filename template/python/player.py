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

class MyClient(Client):
    def turn(self) -> List[Turn]:
        my_ships = self.get_my_ships()
        turns: List[Turn] = []
        round = self.game_map.round
        
        return turns


if __name__ == "__main__":
    client = MyClient()
    client.run()
