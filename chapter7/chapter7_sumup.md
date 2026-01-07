# Chapter 7 - Functions as First-Class Objects

Functions are first-order objects in Python

```
def factorial(n):
    """return n!"""
    return 1 if n < 2 else n * factorial(n-1)
```

### Functions as argument
```
fact = factorial
for number,number_factorial in enumerate(map(fact,range(5))):
    print(f'factorial({number})={number_factorial}')
```

### High-order function
A fucntion that takes a function as argument or returns a function as the result is a *high-order function*.

For example: `map`, `filter`, `reduce`.

### Dynamic set of arguments

Use the pattern: `fn(*args,**kwargs)`

## Modern replacements for map, filter and reduce
```
odds_factorial = [(n,factorial(n)) for n in range(6) if n % 2]

for (num,num_fact) in odds_factorial:
    print(f'{num}! = {num_fact}')
```

### Lambdas - Use with care
```
fruits = ['strawberry','fig','apple','cherry']
sorted(fruits, key = lambda word: word[::-1])
```

## What is callable in Python?
 - user-defined functions (example: created with `def`)
 - built-in functions (example: `len`)
 - built-in methods (example: `dic.get`)
 - methods (example: functions defined on the body of a class)
 - classes (when new instance of class is invoked, the class runs `__new__` to create the instance and then `__init__` to initialize it)
 - class instances (when a class defines `__call__` method, then its instances may be invoked as functions)
 - generator functions (functions using the `yield`)
 - native coroutine functions (functions or methods defined with `async def`)
 - asynchronous generator functions (functions or methods `async def` that have `yield` in their body)

### User-defined callable types

Adding `__call__` on bingo box will make the class to be callable:

```
import random

class BingoCage:
    def __init__(self,items):
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    def __call__(self):
        return self.pick()
```

will do:
```
bingo = BingoCage(range(3))
print(f"pick an element: {bingo.pick()}")
# 1
print(f"pick using the __call__ function: {bingo()}")
# 0
print(f"is the function callable? {callable(bingo)}")
# True
```

## From positional to keyword-only parameters
```
def tag(name, *content, class_=None, **attrs):
    """Generate one ore more HTML tags"""
    if class_ is not None:
        attrs['class'] = class_
    attr_pairs = (f' {attr}="{value}"' for attr,value in sorted(attrs.items()))
    attr_str = ''.join(attr_pairs)
    if content:
        elements = (f'<{name}{attr_str}>{c}</{name}>' for c in content)
        return '\n'.join(elements)
    else:
        return f'<{name}{attr_str} />'
```

will do:
```
tag('p','hello','world')

# <p>hello</p>
# <p>world</p>
```

The first positional argument *can be given as* keyword *as well*:

`tag(content="testing", name="img")`

### Keyword-only after *
```
def f(a, *, b):
    ...
```

### Positional-only before *
```
def divmod(a, b, /):
    ...
```

## Packages for functional programming

! Operators instead of lambda.

### operator module

Get item from tuple:
```
metro_data = [
    ('Tokyo', 'JP', 36.933, (35.689722,139.691667)),
    ('Delhi NCR', 'IN', 21.935, (28.613889,77208889))
]

for city in sorted(metro_data,key=itemgetter(1)):
    print(city)

# ('Delhi NCR', ...)
# ('Tokyo', ...)
```

Get item by name:

For Metropolitan cities:
```
from collections import namedtuple
from operator import attrgetter

LatLon = namedtuple('LatLon', 'lat lon')
Metropolis = namedtuple('Metropolis', 'name cc pop coord')
metro_areas = [Metropolis(name,cc,pop,LatLon(lat, lon)) for name, cc, pop, (lat, lon) in metro_data]
```

you can access the `coord.lat` nested-attribute using `attrgetter`:
```
name_lat = attrgetter('name','coord.lat')
for city in sorted(metro_areas, key=attrgetter('coord.lat')):
    print(name_lat(city))

# ('Delhi NCR',28.613889)
# ('Tokyo', 35.689722)
```

### Call method

`operator.methodcaller` method it creates a function on the fly; the function it creates calls a method by name on the object given as argument:

```
from operator import methodcaller
s = 'The time has come'
hyphenate = methodcaller('replace',' ', '-')

hyphenate(s)
# 'The time-has-come'

from unicode, functions
nfc = functools.partial(unicodedata.normalize,'NFC')
s1 ='café'
s2 = 'cafe\u0301'
s1 == s2 # False
nfc(s1) == nfc(s2) # True
```