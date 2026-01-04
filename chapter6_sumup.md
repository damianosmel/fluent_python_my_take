# Chapter 6 - Object References, Mutability & Recycling

## Difference between `==` and `is``

`==`  --> `__eq__`


`is` --> checks object ID (reference/object's address in memory)

Common use of `is` - check with singleton:
- `x is None`
- `x is not None`


## Shallow copy
```
l1 = [1,2,3]
l2 = list(l1) # or l2 = l1[:]
l2 == l1 # True
l2 is l1 # False
# l2 is a new list (memory reference) but its contents are of the same references as the contents of the initial list
```

## Deep copy
```
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

print(f'{id(bus1.passengers), id(bus2.passengers), id(bus3.passengers)}')
# will print: (129826490908624, 129826490908000, 129826490907376)
```

## Parameter passing in Python - Call by sharing

Each formal parameter of the function gets a copy of each reference in the arguments

=> the parameters inside the function become aliases of the actual arguments

=>> so a function may change any mutable object passed as its parameters

That is:
```
class HauntedBus:
    """A bus model haunted by ghost passengers"""
    def __init__(self,passengers=[]):
        self.passengers = passengers

    def pick(self,name):
        self.passengers.append(name)

    def drop(self,name):
        self.passengers.remove(name)

bus1 = HauntedBus(['Alice','Bill'])
bus1.passengers
bus1.pick('Charlie')
bus1.drop('Alice')
bus1.passengers # ['Bill','Charlie']
bus2 = HauntedBus()
bus2.pick('Carrie')
bus2.passengers # ['Carrie]
bus3 = HauntedBus()
bus3.passengers # ['Carrie']
bus3.pick('Dave')
bus2.passengers # ['Carrie','Dave']
```

Please note:

`bus2` and `bus3` refer to the same list (`HauntedBus.__init__.__defaults__[0]`)

**Solution:** assign to a new empty list each time the argument is `None`,
as in the following snippet:

```
class TwilightBus:
    """A bus model that makes passengers vanish"""
    def __init__(self,passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = passengers
    def pick(self,name):
        ...
    def drop(self,name):
        ...
```

But you still get an alias to an external data from the else of `__init__`:

```
badminton_team = ['Maraki','Thaleia','Alkyone']
bus = TwilightBus(badminton_team)
bus.drop('Maraki')
bus.drop('Alkyone')
print(f'{badminton_team}') # contains only the 'Thaleia' element
# because Python's call by sharing, the self.passengers and the passengers are labeling the same variable "box"
```

## Garbage collector -> when an object is not referenced by any variable