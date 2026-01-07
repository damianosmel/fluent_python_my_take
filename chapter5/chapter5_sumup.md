# Chapter 5 - Data Class Builders

A Data class is an object of Python's Data Model, that is just a collections of fields
with little or no extra functionality.

Three flavours of data classes

 - `collections.namedtuple` -> available since Python 2.6
 - `typing.NamedTuple` -> supporting type hints since Python 3.5
 - `@dataclasses.dataclass` -> class decorator allows more customization than previous alternatives

*Why* not just a normal class?
```
class Coordinate:
    def __init__(self,lat,lon):
        self.lat = lat
        self.lon = lon

moscow = Coordinate(55.76,37.62)
print(f"{moscow}") # not helpful __repr__
# <coordinates.Coordinate object at 0x107142f10>
location = Coordinate(55.76,37.62)
location == moscow #meaningless __eq__
# False
```

Two cons using the usual `__init__`:
 - not helpful `__repr__`
 - meaningless `__eq__`

*But*, data-classes provide helpful `__init__`, `__repr__` and `__eq__`:

 - namedtuple:
    ```
    from collections import namedtuple
    Coordinate = namedtuple('Coordinate', 'lat lon')
    issubclass(Coordinate, tuple)
    # True
    moscow = Coordinate(55.756,37.617)
    print(f"{moscow}")
    # Coordinate(55.756,37.617)
    moscow == Coordinate(lat=55.756,lon=37.617)
    # True
    ```
 - typehints with NamedTuple:
    ```
    import typing
    Coordinate = typing.NamedTuple('Coordinate',[('lat',float),('lon',float)])
    # or Coordinate = typing.NamedTuple('Coordinate',lat=float,lon=float)
    issubclass(Coordinate, tuple)
    # True
    typing.get_type_hints(Coordinate)
    # {'lat': <class 'float'>, 'lon': <class 'float'>}
    ```
 - dataclass:
    ```
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class Coordinate:
        lat:float
        lon:float

        def __str__(self):
            ns = 'N' if self.lat >= 0 else 'S'
            we = 'E' if self.lon >= 0 else 'W'
            return f'{abs(self.lat):.1f} {ns}, {abs(self.lot):.1f} {we}'
    ```
*!Please note:* dataclasses create mutable objects however adding `frozen=True` will make the instances immutable.

*!! A hack * - Add additional functionality on a named tuple!!
```
from chapter1 import FrenchDeck

Card = collections.namedtuple('Card',['rank','suit'])
# add attribute needed for ranking
Card.suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)
# create the ranking logic as a function
def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    suit_value = card.suit_values[card.suit]
    return rank_value * len(card.suit_values) + suit_value

# and now the hack -- make this logic as an attribute of the namedtuple
Card.overall_rank = spades_high
lowest_card = Card('2','clubs')
lowest_card.overall_rank() # returns 0
```

## Variable annotation syntax

`var_name : some_type = 'some_default_value'`

PEP 484 - Acceptable type hints - https://peps.python.org/pep-0484/#acceptable-type-hints
Acceptable types:
 1. concrete class str or FrenchDeck
 2. parametrized collection type list[int]
 3. typing.Optional -> Optional[str] => str or None

## More on dataclasses
dataclasses -> https://docs.python.org/3/library/dataclasses.html
`@dataclass(eq=True,frozen=True)` -> `__hash__` is generated for this `dataclass`

## Dataclass as code-smell
But, use with care, data class can also be a *code smell* as they separate object abstractions with functionality (contrary to the main idea of OOP to place behaviour and data together).

Some scenarios that a data class shall have little or no behaviour:

 - data class as scaffolding:
   it can be an initial, simplistic implementation of a class to jump-start a new objector module. *By the time*, the class should get its own methods instead of relying on methods of other classes to operate on its instances.
   
   => Scaffolding is temporary.

  - data class as intermediate representation:
    useful to:
    - build records about to be exported to JSON or some other interchange format
    - hold data that was just imported, crossing some system boundary (read data from db query) => data class object shall immutable

## Pattern matching class instances - Extending structural pattern matching

the general matching pattern:
```
match x:
    case float():
        do_something_with(x)
```

This pattern works for nine blessed built-in types:

`bytes`, `dict`, `float`, `frozenset`, `int`, `list`, `set`, `str`, `tuple`

### Keyword class patterns
```
import typing

class City(typing.NamedTuple):
    continent: str
    name: str
    country: str

cities = [
    City('Asia', 'Tokyo', 'JP'),
    City('Asia', 'Delhi', 'IN'),
    City('North America', 'Mexico City', 'MX'),
    City('North America', 'New York', 'US'),
    City('South America', 'São Paulo', 'BR'),
]
```

Match the Asian cities and collect the country attribute:
```
def match_asian_countries():
    results = []
    for city in cities:
        match city:
            case City(continent='Asia', country=cc):
                results.append(cc)
    return results
```

### Positional class patterns
```
def match_asian_countries():
    results = []
    for city in cities:
        match city:
            case City('Asia',_,country):
            results.append(country)
    return results
```