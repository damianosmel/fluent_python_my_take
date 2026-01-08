# Chapter 10 - Design Patterns with First-Class Functions

Design pattern is a general recipe for solving a common design problem.

A famous book on design patterns is *Design Patterns: Elements of Resuable Object-Oriented Software* by Erich Gamma, Richard Helm, Ralph Johnson and John Vlissides - a.k.a "the Gang of Four". The book catalogs 23 patterns consisting of arrangements of classes examplified with code in C++.

## Case Study: Refactoring Strategy

Consider an online store with these discount rules:
• Customers with 1,000 or more fidelity points get a global 5% discount per order.
• A 10% discount is applied to each line item with 20 or more units in the same
order.
• Orders with at least 10 distinct items get a 7% global discount.

## Classic strategy

A classical way to implement the strategy pattern is with an abstract class which is extended to each special sub-strategy (a bullet from above).
Such implementation is found at [order.py](chapter10/order.py)

## Function-oriented strategy

You can observe that the specialized strategies have no state (no instance attributes). You could say they look a lot like plain functions. Therefore, we can refactor our code in a function-oriented way: [strategy.py](chapter10/strategy.py)

## Finding strategies in a module

We can also choose the best strategy from the available ones, as shown in the example: [best_promo.py](chapter10/best_promo.py)

## Decorator-enhanced strategy pattern
Automatically add new strategies in the pool of strategies tried out to find the best one. In [strategy_registration_decorator.py](chapter10/strategy_registration_decorator.py)

## The command pattern

The command design pattern describes the scenario that an invoker (say a `Menu`) asks for a command and then the concrete command is executed and the corresponding receiver is used (for `OpenCommand.execute()` the receiver is the `Application` and for PasteCommand.execute() the receiver is the `Document`).

See a snippet of the implementation of the command pattern using functions at [macro_command.py](chapter10/macro_command.py)
