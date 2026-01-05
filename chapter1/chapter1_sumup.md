# Chapter 1 - The Python Data Model

## Motivation by a short example
Python may not be perfect theoretically but still fun to use Python's agility is grace to its Data Model in python you do `len(some_list_of_yours)` and not `some_list_of_yours`.len

## A Pythonic Card Deck
```
import collections

# namedtuple to represent objects with more than one data types
Card = collections.namedtuple('Card',['rank','suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2,11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank,suit) for suit in self.suits for rank in self.ranks]
    def __len__(self):
        return len(self._cards)
    def __getitem__(self, position):
        return self._cards[position]

wine_card = Card('9','diamonds')
print(f'{wine_card}') # Card(rank='9', suit='diamonds')

deck = FrenchDeck()
print(f'The size of the deck is {len(deck)}') # The size of the deck is 52
```

### Add functionality on FrenchDeck using utilities of the Python Data Model
```
from random import choice
print(f'A random picked card out of the deck is: {choice(deck)}')
# A random picked card out of the deck is: Card(rank='J', suit='clubs')
```

Benefits:
- clarity => users of the class don't memorize arbitrary method names (.size(), .length(), something else?)
- do-not-reinvent-the-wheel => benefit from the already implemented and tested elements of the Python standard library

More functionalities:

- also it gets slicing:
```
print(f'The first 3 cards in the deck: {deck[:3]}')
# The first 3 cards in the deck: [Card(rank='2', suit='spades'), Card(rank='3', suit='spades'), Card(rank='4', suit='spades')]
```

- `FrenchDech._cards` is iterable so also exists methods are already supported:
```
print(f"J diamonds in deck? -> {Card('J','diamonds') in deck}")
# J diamonds in deck? -> True
```

- also sorting is possible, just provide the respective function:
```
suit_values = dict(spades=3,hearts=2,diamonds=1,clubs=0)
def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]

for card in sorted(deck,key=spades_high):
    print(card)

###
# first three printed lines: 
###
# Card(rank='2', suit='clubs')
# Card(rank='2', suit='diamonds')
# Card(rank='2', suit='hearts')
```

### Take-home message - Leverage the data model by Composition
By implementing `__len__` and `__getitem__` on our new class (FrenchDeck), we use the Python's Data model to give the iteration and slicing functionalities on instance of the class, just like any other standard Python sequence (list, tuple, ..).

## Emulating Numeric Types - 2d Vector
Given the draft implementation of a 2d vector at [vector2d.py](chapter1/vector2d.py), the author explains how to integrate special methods on a class:
 - emulating numeric types
 
  -> see `doctest`
 - string representation of objects

  
    `__repr__` vs `__str__`:
    - `__repr__` will display the standard representation of attributes of the instance (helpful for inspection (debugging/logging), e.g `__repr__` will display the attributes with the same type as they are used in constructor)

        `__repr__` is also used in `f-strings` with the `!r`
    - `__str__` will be used by print() to print an user-friendly representation of the instance
    If you have not implemented the __str__ then print() will fall-back to `__repr__`
 - boolean value of object

    Python to evaluate `bool(my_object)`, checks if `__bool__()` or `__len__()` is implemented.

    If `__bool()__` is not implemented then Python will evaluate the `__len__()` if it is implemented and returns zero then the boolean evaluation will return `False`, otherwise it will return `True`.

 - implementing collections

=> this way, we create an API for our newly created `Vector`, which follows the behaviours of built-in functions on standard Python objects.
That is, the `abs(x)` returns the magnitude of a number (real or imaginery), therefore also our implemented `Vector.__abs__()` will return the magnitude of a 2d vector.

## Further reading
Python Data Model: https://docs.python.org/3/reference/datamodel.html
