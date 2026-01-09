# Chapter 11 - A Pythonic Object

> For a library or framework to be Pythonic is to make it as easy and natural as possible for a Python programmer to pick up how to perform a task.
 - Martijn Faassen, creator of Python and JavaScript frameworks.


`Iterator` -> make unpacking work:
```
def __iter__(self):
    return (i for i in (self.x,self.y))
```

## An alternative Constructor

Include a functionality to import Vector2d from a binary sequence. Looking at the standard library for inspiration, we see `.frombytes` from the `array.array`. Using this inspiration you can create `frombytes`. Please note that this method takes the `@classmethod` decorator.

### Classmethod vs. staticmethod
The main difference of these two decorators:
 - `@classmethod`: alternative constructors
 - `@staticmethod`: functions that happen to be inside a class, but they could also naturally be out of its definition

### Formatted displays
 The f-strings, the format() built-in function, and the str.format() delegate the actual formatting to <ins>each type</ins> by calling the `.__format__(format_spec)` method

 Further reading for [Format Specification Mini-Language](https://docs.python.org/3/library/string.html#formatspec)
  - [Formatted string literals](https://docs.python.org/3/reference/lexical_analysis.html#f-strings)
  - [Format string syntax](https://docs.python.org/3/library/string.html#format-string-syntax)

## A hashable Vector2d

With the current implementation of Vector2d we can add it into a set as it's *still unhashable*.

therefore, we need to implement the `__hash__` and `__eq__`.
*!Please note:* But you do need to make the instance immutable.

Resulted changes into implementation:
 - `self.__x = float(x)` make attribute private
 - `@property` decorator marks the getter method of a property

    the getter method is named after the public property it exposes: `x`
 
 ```
  @property
  def x(self):
    return self.__x
 ```

## Supporting positional pattern matching
Vector2d is currently supporting keyword patterns:

```
 def keyword_pattern_demo(v:Vector2d) -> None:
    match v:
        case Vector2d(x=0,y=0):
            print(f'{v!r} is null')
        case Vector2d(x=0):
            print(f'{v!r} is vertical')
        case _:
            print(f'{v!r} is awesome')
        ...
```

But it does not support positional patterns:
you need to add:
```
 class Vector2d:
    __match_args__ = ('x','y')
    # etc
    ...
```

By the changes up to now, extended Vector2d looks like: [vector2d_v0.py](chapter11/vector2d_v0.py)

*!Please note:* You shall implement the methods that you need, the user of your application does not care if the underlying objects are full Pythonic. 
But if you build a library for other, then the end-users of your code may expect more of the "Pythonic" behaviours.

## Saving memory with `__slots__`

Python uses an alternative storage mode lfor the instance attributes, if you define a class attribute named `__slots__` including a sequence of attribute names.

=> attributes included in `__slots__` are stored in hidden array or references that use <ins>less memory</ins> than the default `dict` of the class.

You can see the updated vector2d with `__slots__` at [vector2d_v0_slots.py](chapter11/vector2d_v0_slots.py).

## Overriding class attributes
You can override a class attribute for a specific instance:
```
from vector2d_v0_slots import Vector2d

v1 = Vector2d(1.1,2.2)
dumpd = bytes(v1)

# only for v1 instance change the Vector2d.typecode attribute
v1.typecode = 'f'
dumpf = bytes(v1)
```

A more *idiomatic Python* way of achieving the permanent change of a class attribute -> `sub-classing`

```
from vector2d_v0_slots import Vector2d
 class ShortVector2d(Vector2d):
    typecode = 'f'
```