# Chapter 8 - Type Hints in Functions

## PEP484 - Gradual typing
A gradual type system:
 - is optional
 - does not catch type errors at runtime
 - does not enhance peformance

### mypy - Python type checker

`messages.py`:
```
def show_count(count: int, word: str) -> str:
    if count == 1:
        return f'1 {word}'
    count_str = str(count) if count else 'no'
    return f'{count_str} {word}s'
```

Run `mypy` on `messages.py`:
```
> pip install mypy
> mypy messages.py
```

`messages_test.py`:
```
from pytest import mark
from messages import show_count

@mark.parametrize('qty, expected',[
    (1,'1 part'),
    (2,'2 parts')
])

def test_show_count(qty,expected):
    got = show_count(qty,'part')
    assert got == expected

def test_show_count_zero():
    got = show_count(0,'part')
    assert got == 'no parts'
```

Run `mypy` (with more strict option) on test: 
`> mypy --disallow-incomplete-defs messages_test.py`

### Formatting code
Code Style: Use flake8 and blue:
- flake8 -> reports on code styling
- blue   -> formats code 

## Using None as default

`show_count()` for nouns with plural => `Optional[type]` makes an argument optional with a variable of type `type` otherwise the variable will be `None`. However you shall explicitly provide the `None` as default.


```
# plural may be str or None
from typing import Optional
def show_count(count: int, singular: str, plural: Optional[str]=None) -> str:
    ...
```

## Types are defined by supported operations
```
from collections import abc
def double(x: abc.Sequence):
    return x * 2
```

At <ins>static</ins> time this declaration is only for object that their class implements the __mul__ method.

## Duck typing

Two common typing ways:

- Duck typing

    Have a look at [birds.py](chapter8/birds.py), if you can invoke `birdie.quack()`, then `birdie` is a `Duck` <ins>in this context</ins>.

    => In Python as in (Smalltalk, JavaScript and Ruby),
objects have types but variables (and parameters) are <ins>untyped</ins>.

    It does not matter what the declared type of the object is, <ins>only what operations it actually supports</ins>.

    Duck typing is enforced at runtime.

- Nominal typing

    In other languages (C++, Java, C#) objects and variables have types. But objects only exist at runtime.
    
    If `Duck` is a subclass of `Bird`, you can assign a Duck instance to a parameter annotated as `birdie: Bird`.

    <ins>But</ins> in the body of a function, the type checker considers the the call `birdie.quack()` as illegal, because `birdie` is nominally is a `Bird` and this class does provide the `.quack()` method.

Now run mypy on the [birds.py](chapter8/birds.py) gives you:

```
birds.py:15 error: "Bird" has no attribute "quack"
Found 1 error in 1 file (checked 1 source file)
```

But, now let's run the `birds` module to the see the run-time behaviour:

```
from birds import *

daffy = Duck()
alert(daffy)
alert_duck(daffy)
alert_bird(daffy)
```

All calls are valid, the `alert_bird(daffy)` is valid, as it accepts a `Bird` instance as parameter and daffy is also a `Bird` - the superclass of `Duck`.

```
> python3 daffy.py
Quack!
Quack!
Quack!
```

And what if after time, we extend the functionality of `birds`?

Let's investigate for example the [wood.py](chapter8/woody.py):

mypy on the file `> mypy woody.py`:

```
wood.py:5 error: Argument 1 to "alert_duck" has incompatible type "Bird"; expected "Duck" 
```

And in run-time:

```
>>> from birds import *
>>> woody = Bird()
>>> alert(woody)
Traceback (most recent call last):
  ...
AttributeError: 'Bird' object has no attribute 'quack'
>>>
>>> alert_duck(woody)
Traceback (most recent call last):
  ...
AttributeError: 'Bird' object has no attribute 'quack'
>>>
>>> alert_bird(woody)
Traceback (most recent call last):
  ...
AttributeError: 'Bird' object has no attribute 'quack'
```

Running `mypy` already gave us warning for the last two method calls. For the first one it could not as the method is untyped.

## Types usable in annotations

 All major types that you can use with annotations:
  - `typing.Any`
  - simple types and classes
  - `typing.Optional` and `typing.Union`
  - generic collections, including tuples and mappings
  - abstract base classes
  - generic iterables
  - parametrized generics and TypeVar
  - typing.Protocols - the key to *static duck typing*
  - typing.Callable
  - typing.NoReturn

### `Any` type
 The keystone for gradual type system is the `Any` type a.k.a *dynamic type*.

when a type checker sees an untyped function like this:
 ```
 def double(x):
     return x * 2
 ```

it assumes this:
 ```
 def double(x: Any) -> Any:
     return x * 2
 ```

### Behavioural subtyping
 To discuss about the *subtype-of* relation, consider the following code snippet:


 ```
 class T1:
     ...
 class T2:
     ...
 def f1(p:T1) -> None:
     ...
 o2 = T2()

 f1(o2) # OK
 ```

 Barbara Liskov defined `is-subtype-of` in <ins>terms of supported operations</ins>:

 > if an object `T2` substitutes an object of type `T1` and the program still behaves correctly, then `T2` is *subtype-of* `T1`.

 The call f1(o2) is an application of the Liskov Substitution Principle - LSP.


 But:

 ```
 def f2(p: T2) -> None:
    ...
 o1 = T1()

 f2(o1) # type error
 ```

! every `T2` is a `T1` but the reverse is not true:
`T2` may implement additional methods, so an instance of `T1` may not be an instance of `T2`.

In gradual type systems, there is another relationship: *consistent-with*, which applies whenever *subtype-of* applies, with special provisions for type `Any`:

The rules for `consistent-with` are:
 1. Given `T1` and a subtype `T2`, then `T2` is consistent-with `T1` (Liskov subsitution).
 2. Every type is *consistent-with* `Any`: you can pass objects of every type Any where an argument declared of type `Any`.
 3. `Any` is *consistent-with* every type: you can always pass an object of type `Any` where an argument of another type is expected.

### Simple types and classes

 Simple types like `int`, `float`, `float`, `str`, and `bytes` may be used directly in type hints. But also `FrenchDeck`, `Vector2d`, and `Duck` can also be type hints.

 *!Please note:* `int` is *consistent-with* `float` and `float` is *consistent-with* `complex` => `int` is *consistent-with* `complex`. (PEP 484)

### Optional and Union Types

 We have seen the use of `Optional` in the `show_count` definition.

 `Optional[str]` is actually a shortcut for `Union[str, None]`.

 We can write:
 `str | bytes` instead of `Union[str,bytes]` since Python 3.10.

 so the show_count parameter can be updated to:
 
 ```
 plural: Optional[str] = None # before
 plurall: str | None = None
 ```

 *!Please note:* it's not recommended to return an union of types from a method call, as you force the caller to check the type of the return object.

### Generic collections

 - stuff: list[str]
 - stuff: list[Any] equivalently stuff: list

 PEP 585 - *Type Hinting Generics In Standard Collections*: lists the collections from the standard library accepting generic type hints.

**Tuple types**

 Three ways to annotate tuple types:

  - tuples as records

     See [coordinates.py](chapter8/coordinates.py)
 
  - tuples as records with named fields

     See [coordinates_named.py](chapter8/coordinates_named.py)

     using `typing.NamedTuple` is a factory for subclasses, so `Coordinate` is a consistent with `tuple[float,float]`, <ins>but the reverse is not true</ins>.

  - tuples as immutable sequences
     To annotate tuples of unspecified length, used as immutable lists, you do:
    
     tuple[int, ...]

     also `stuff: tuple[Any, ...]` is equivalent to `stuff: tuple`

** Mappings **

 You can use the following syntax: `stuff: dict[str,set[str]]`

### Abstract Base Classes
> Be conservative in what you send, be liberal in what you accept. - Postel's law, a.k.a. the Robustness Principle

The quote with an example:
```
from collections.abc import Mapping

def name2hex(name: str, color_map: Mapping[str,int]) -> str:
    ...
```
 Making the type of the second parameter `Mapping`, you give the freedom to the caller to use `dict`, `defaultdict`, or any other *subtype-of* Mapping. 

But, on the following example you restrict the argument to be only `dict`
```
def name2hex(name:str, color_map: dict[str,int]) -> str:
    ...
```

### Iterables

 Under the entry of typing.List, the Python documentation says:
    Generic version of list. Useful for annotating <ins>return types</ins>. To <ins>annotate arguments</ins> it is preferred to use an abstract collection type such as `Sequence` or `Iterable`
 Similar comment appears for `typing.Dict` and `typing.Set`.

 for example:
  `def fsum(__seq: Iterable[float]) -> float`

### Parametrized generics and TypeVar

Looking at [sample.py](chapter8/sample.py) we see the usage of `TypeVar`. It is used in type signatures, so you can refer to the same unspecified type more than once.

You can also bound the types that TypeVar can be by:
`HashableT = TypeVar('HashableT', bound=Hashable)`

### Static protocols

The `protocol` type, as presented in PEP 544, is defined by specifying one or more methods, and the type checker verifies that those methods are implemented where that protocol type is required.

`protocol` comes in handy to force that a `TypeVar` implements some needed method:

For example to implement the `top` we need the `TypeVar` class of the elements to have implemented the *less than* method.

Please see the protocol in [comparable.py](chapter8/comparable.py) and an implementation of `top` in [top.py](chapter8/top.py). We provide some tests for `top`, in [top_test.py](chapter8/top_test.py).

### Callable

To annotate callback parameters or callable objects returned by high-order functions, the `collections.abc` module provides the `Callable` type, parametrized like this:

`Callable[[ParamType1,ParamType2], ReturnType]`

To see more details on using `callable` as type, see [update.py](chapter8/update.py),

`update(probe_ok,display_wrong)` does not work because a function accepting `int` may or may not be able to handle `float`.

`update(probe_ok,display_ok)` does work because a function accepting `complex` will be able to handle `float` (Remember: `float` is *consistent-with* `complex`)

### NoReturn
 This is a special type used to annotate the return type of functions tha never return.

 For example: `sys.exit()`:
 `def exit(__status: object = ...) -> NoReturn: ...`