# Common Code Smells

## Bloaters

**Long Method** - Method has too many lines
- Solution: Extract methods

**Large Class** - Class has too many responsibilities
- Solution: Split into smaller classes

**Long Parameter List** - More than 5 parameters
- Solution: Use parameter object or builder pattern

**Data Clumps** - Same variables appear together
- Solution: Extract to class

## Object-Orientation Abusers

**Switch Statements** - Complex switch/case logic
- Solution: Polymorphism

**Refused Bequest** - Subclass doesn't use parent functionality
- Solution: Replace inheritance with delegation

## Change Preventers

**Divergent Change** - One class changed for many reasons
- Solution: Extract class

**Shotgun Surgery** - Single change requires many small changes
- Solution: Move method/field

## Dispensables

**Duplicate Code** - Same code in multiple places
- Solution: Extract method

**Dead Code** - Unused code
- Solution: Delete it

**Speculative Generality** - "Just in case" code
- Solution: Remove until needed

## Couplers

**Feature Envy** - Method uses another class more than its own
- Solution: Move method

**Inappropriate Intimacy** - Classes too dependent on each other
- Solution: Move method/field or extract class

**Message Chains** - a.getB().getC().getD()
- Solution: Hide delegate
