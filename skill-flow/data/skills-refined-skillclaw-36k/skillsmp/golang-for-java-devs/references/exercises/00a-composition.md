# Exercise 00a: Composition Over Inheritance

**Time:** 15 minutes
**Goal:** Understand Go's composition model vs Java's inheritance

## The Java Pattern

In Java, you use inheritance to share behavior:

```java
public abstract class Animal {
    protected String name;

    public void eat() {
        System.out.println(name + " is eating");
    }

    public abstract void speak();
}

public class Dog extends Animal {
    public Dog(String name) {
        this.name = name;
    }

    @Override
    public void speak() {
        System.out.println(name + " says woof!");
    }
}

// usage
Animal dog = new Dog("Rex");
dog.eat();    // inherited behavior
dog.speak();  // overridden behavior
```

## The Go Way

Go doesn't have inheritance. Instead, it has struct embedding:

```go
type Animal struct {
    Name string
}

func (a Animal) Eat() {
    fmt.Printf("%s is eating\n", a.Name)
}

type Dog struct {
    Animal  // embedded - not inheritance!
}

func (d Dog) Speak() {
    fmt.Printf("%s says woof!\n", d.Name)
}

// usage
dog := Dog{Animal: Animal{Name: "Rex"}}
dog.Eat()    // promoted from Animal
dog.Speak()  // defined on Dog
```

## Key Differences

| Java | Go |
|------|-----|
| `extends` creates IS-A relationship | Embedding creates HAS-A relationship |
| Dog IS-A Animal | Dog HAS an Animal |
| Override methods with `@Override` | Shadow by defining same method |
| `super.method()` calls parent | `d.Animal.Method()` calls embedded |
| Runtime polymorphism | Interfaces for polymorphism |

## Your Task

Create these types using Go's composition:

1. A `Logger` struct with a `Log(message string)` method
2. A `Service` struct that embeds `Logger`
3. A `LoggingService` struct that embeds `Logger` and adds custom logging

## Try First (Optional)

Before looking at the solution, try writing:
- A struct with embedded struct
- Method access through embedding
- Method shadowing (overriding)

---

## Step by Step

### 1. Create the Logger (3 min)

```go
type Logger struct {
    Prefix string
}

func (l Logger) Log(message string) {
    fmt.Printf("[%s] %s\n", l.Prefix, message)
}
```

### 2. Create Service with embedded Logger (5 min)

```go
type Service struct {
    Logger  // embedded
    Name    string
}

func (s Service) DoWork() {
    s.Log("starting work")  // Log is promoted from Logger
    // do work...
    s.Log("finished work")
}

// usage
svc := Service{
    Logger: Logger{Prefix: "SVC"},
    Name:   "my-service",
}
svc.DoWork()
// output:
// [SVC] starting work
// [SVC] finished work
```

### 3. Create LoggingService with method shadowing (5 min)

```go
type LoggingService struct {
    Logger
    Name string
}

// shadows Logger.Log
func (s LoggingService) Log(message string) {
    // add timestamp
    fmt.Printf("[%s] %s: %s - %s\n",
        time.Now().Format("15:04:05"),
        s.Logger.Prefix,
        s.Name,
        message,
    )
}

func (s LoggingService) DoWork() {
    s.Log("starting work")  // calls LoggingService.Log (shadowed)
    s.Logger.Log("direct")  // calls Logger.Log explicitly
}
```

## What Just Happened?

| Concept | Java | Go |
|---------|------|-----|
| Share behavior | Inheritance | Embedding |
| Access parent method | `super.method()` | `s.Embedded.Method()` |
| Override behavior | `@Override` | Define method with same name |
| IS-A relationship | Yes (Dog is Animal) | No (Dog has Animal) |

## The Mental Shift

**Java thinking:** "What is this thing?" (taxonomy)
**Go thinking:** "What can this thing do?" (behavior)

In Go, you don't ask "is Dog an Animal?" You ask "does Dog have the methods I need?"

## Interface Polymorphism

Since Go doesn't have inheritance polymorphism, use interfaces:

```go
type Speaker interface {
    Speak()
}

type Dog struct {
    Name string
}

func (d Dog) Speak() {
    fmt.Printf("%s says woof!\n", d.Name)
}

type Cat struct {
    Name string
}

func (c Cat) Speak() {
    fmt.Printf("%s says meow!\n", c.Name)
}

// both satisfy Speaker interface
func MakeSpeak(s Speaker) {
    s.Speak()
}

MakeSpeak(Dog{Name: "Rex"})   // works
MakeSpeak(Cat{Name: "Whiskers"})  // works
```

## Stretch Goal (if time)

Implement a "decorator" pattern using embedding:

```go
type Writer interface {
    Write(data string) error
}

type FileWriter struct {
    Path string
}

func (f FileWriter) Write(data string) error {
    // write to file
    return nil
}

type LoggingWriter struct {
    Writer  // embed the interface!
}

func (l LoggingWriter) Write(data string) error {
    log.Printf("writing: %s", data)
    return l.Writer.Write(data)  // delegate to embedded
}
```

## Checkpoint

- [ ] I can embed a struct and access its methods
- [ ] I understand shadowing vs overriding
- [ ] I see why Go uses interfaces for polymorphism
- [ ] I accept that Go doesn't have inheritance

**Next:** Exercise 00b - Small Interfaces
