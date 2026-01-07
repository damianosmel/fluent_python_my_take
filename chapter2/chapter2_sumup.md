# Chapter 2 - An Array of Sequences

## Overview of Built-in Sequences

Two types of sequences based on containing elements:
 - container sequences - items of different types

  (they) keep *references* to the objects which they contain

  Examples: `list`, `tuple` & `collections.deque`

 - flat sequences - primitive type items

  (they) store the *value of its contents* in its own memory space

  Examples: `str`, `bytes` & `array.array`

*!Please note:* every Python object in memory has a header with metadata.

A float, the simplest Python object has a value field and two metadata fields:
 - `ob_refcnt` -> object's reference count
 - `ob_type` -> pointer to object's type
 - `ob_fval` -> C double holding the value of a float


Two types of sequences based on mutability:
 - mutable sequences: `list`,`bytearray.array.array`,`collections.deque`
 - immutable sequences: `tuple`,`str`,`bytes`

## List Comprehensions & Generator Expressions

### List Comprehensions & Readability
Example: build a list of Unicode code points from a string
```
symbols = '$¢£¥€¤'
codes = []
for symbol in symbols:
    codes.append(ord(symbol))
codes
# [36, 162, 163, 165, 8364, 164]
````

But more readable using list-comprehensions:
```
symbols = '$¢£¥€¤'
codes = [ord(symbol) for symbol in symbols]
```

### Walrus operator
Access the variable used in list-comprehensions (and generators)
```
x = 'ABC'
codes = [last := ord(c) for c in x]
# last = 67, but c is gone
```

### Funtional methods vs. listcomps
List comprehensions can provide a more readable code compared to `lambda` and `map/filter`

```
# with listcomps
beyond_ascii = [ord(s) for s in symbols if ord(s) > 127]
# with map/filter
beond_ascii_map_filter = list(filter(lambda c: c > 127, map(ord,symbols)))
```

### Generator Expressions
To initialize sequences (such tuples or arrays), you can use generator expression (genexp) instead of listcomp in order to save memory. This is because genexp yield items one by one.

```
symbols = '$¢£¥€¤'
tuple(ord(symbol) for symbol in symbols)
```

*!Please note:* genexps use the same syntax as listcomps, but are enclosed in parentheses rather brackets

```
for tshirt in (f'{color} {size} for color in colors for size in sizes'):
    print(tshirt)
```

## Tuples are not just immutable lists
Tuples =
 - records (with no field names)
 - immutable lists

*Why* tuples?
by using them as records (immutable lists), you gain:
 - clarity -> length will never change
 - performance -> tuple uses less memory than a list of the same length

*!Please note:* when using tuples as immutable lists, take care of the two main differences:
 - length of the record is not fixed
 - order of elements is important (as it signifies the what is the element about)
 
 > Order of elements is important:

`city,year,pop,chg,area = ('Tokyo',2003,32_450,0.66,8014)`

*!Please note:* tuples are with mutable elements => not anymore hashable

## Unpacking Sequences & Iterables

```
# unpacking
lax_coordinates = (33.9,-118.4)
latitude, longitude = lax_coordinates
```

### Using * to Grab Excess Items
```
# unpacking with *
t = (1,12)
divmod(*t)

# * to grab excess items
a,b,c, *rest = range(5)
rest
# 3,4
```

### Nested unpacking
```
metro_areas = [
('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
('São Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]

def unpack_nested_tuples():
    print(f'{"City":15} | {"latitude":>9} | {"longtitude":>9}')
    for name,_,_,(lat,lon) in metro_areas:
        if lon <= 0:
            print(f'{name:15} | {lat:9.4f} | {lon:9.4f}')

unpack_nested_tuples()
# will print:
City            |  latitude | longtitude
Mexico City     |   19.4333 |  -99.1333
New York-Newark |   40.8086 |  -74.0204
São Paulo       |  -23.5478 |  -46.6358
```

## Pattern matching with sequences

### Structural pattern matching

Used for list, tuple, memoryview, range, array.array, collections.deque

Example. Imagine you have a robot to which you communicate with messages like `('BEEPER', 400, 3)`

```
def handle_command(self, message):
    match message:
        case ['BEEPER', frequency, times]:
            self.beep(times, frequency)
        case ['NECK', angle]:
            self.rotate_neck(angle)
        case ['LED', ident, intensity]:
            self.leds[ident].set_brightness(ident, intensity)
        case ['LED', ident, red, green, blue]:
            self.leds[ident].set_color(ident, red, green, blue)
        case _:
            #raise InvalidCommand(message)
            pass
```

## Slicing
*!!Please note:* Slicing in Python exclude the last item in slices and ranges
How to use: `some_iterable[start:stop:step]`

for multidimensional objects: `vector2d[start:stop:step,start_:stop_:step_]`

## Using + & * with sequences

**Wrong way** to initialize a list
```
weird_board = [['_']*3] * 3
weird_board[0][0] = '*'
weird_board
# [['*','_','_'],['*','_','_'],['*','_','_']]
```

*=>* the inner list is created once and its reference used in all three elements

*=>>* changing one element-list, you change all.

**Correct way:** Create different list-elements (different objects/references)

`board = [['_']*3 for i range(3)]`

### Augmented assigments with sequences

Python implements the assignment with the respective implementation of the `__iadd__` of the class of the object.

=> if the `__iadd__` is not implemented then `a += b` =>
1. evaluate `a+b`, producing a new object
2. save the resulted object `(a+b)` to `a`

=> the identity of `a` changes if the `__iadd__` is not implemented.

!! Python puzzle !!

What will happen when you run the following code:
```
t = (1,2,[30,40])
t[2] += [50,60]
```