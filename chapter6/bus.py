#!/usr/bin/python3
print("hi")
import copy 

class Bus:
    def __init__(self,passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = list(passengers)

    def pick(self,name):
        self.passengers.append(name)
    def drop(self,name):
        self.passengers.remove(name)

bus1 = Bus(['Alice','Bill','Claire','David'])
bus2 = copy.copy(bus1)
bus3 = copy.deepcopy(bus1)

print(f"{id(bus1), id(bus2), id(bus3)}")