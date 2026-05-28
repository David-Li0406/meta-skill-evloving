# Kukicha Syntax Examples

## Complete Example: Todo App

```kukicha
petiole main

import "fmt"
import "encoding/json"
import "os"
import "stdlib/files"

type Todo
    id int64
    title string
    completed bool
    tags list of string

func CreateTodo(id int64, title string) Todo
    return Todo
        id: id
        title: title
        completed: false
        tags: list of string{}

func Display on todo Todo string
    status := "[ ]"
    if todo.completed
        status = "[x]"
    return "{status} {todo.id}. {todo.title}"

func MarkComplete on todo reference Todo
    todo.completed = true

func AddTag on todo reference Todo tag string
    todo.tags = append(todo.tags, tag)

func SaveTodos(todos list of Todo, path string) error
    data := json.Marshal(todos) onerr return error
    files.Write(path, string(data)) onerr return error
    return empty

func LoadTodos(path string) list of Todo, error
    content := files.Read(path) onerr return empty list of Todo, error
    todos := list of Todo{}
    json.Unmarshal(list of byte(content), reference of todos) onerr return empty list of Todo, error
    return todos, empty

func main()
    todos := list of Todo{}

    todo1 := CreateTodo(1, "Learn Kukicha")
    todo2 := CreateTodo(2, "Build something cool")

    AddTag(reference of todo1, "learning")
    AddTag(reference of todo1, "programming")
    MarkComplete(reference of todo1)

    todos = append(todos, todo1, todo2)

    for todo in todos
        fmt.Println(Display(todo))

    SaveTodos(todos, "todos.json") onerr panic "failed to save"
    fmt.Println("Saved successfully!")
```

## Error Handling Patterns

### Pattern 1: Panic on Critical Errors
```kukicha
func mustLoadConfig() Config
    data := os.ReadFile("config.json") onerr panic "config missing"
    config := Config{}
    json.Unmarshal(data, reference of config) onerr panic "invalid config"
    return config
```

### Pattern 2: Propagate Errors
```kukicha
func loadUser(id int64) User, error
    data := db.Query("SELECT * FROM users WHERE id = ?", id) onerr return empty User, error
    user := User{}
    parseResult(data, reference of user) onerr return empty User, error
    return user, empty
```

### Pattern 3: Default Values
```kukicha
func getPort() int
    portStr := os.Getenv("PORT") onerr "8080"
    port := strconv.Atoi(portStr) onerr 8080
    return port
```

### Pattern 4: Custom Error Messages
```kukicha
func validateAge(age int) error
    if age < 0
        return error "age cannot be negative"
    if age > 150
        return error "age seems unrealistic"
    return empty
```

## Pipe Operator Chains

### Data Processing Pipeline
```kukicha
import "stdlib/slice"
import "stdlib/parse"
import "stdlib/fetch"

type User
    name string
    age int
    active bool

func getActiveAdultNames(url string) list of string
    return url
        |> fetch.Get()
        |> fetch.Text()
        |> parse.Json() as list of User
        |> slice.Filter(u -> u.active and u.age >= 18)
        |> slice.Map(u -> u.name)
        |> slice.Sort()
```

### File Processing Pipeline
```kukicha
import "stdlib/files"
import "strings"

func processLogFile(path string) list of string
    return path
        |> files.Read()
        |> strings.Split("\n")
        |> slice.Filter(line -> strings.Contains(line, "ERROR"))
        |> slice.Map(line -> strings.TrimSpace(line))
```

## Interface Implementation

```kukicha
interface Formatter
    Format() string

type PlainFormatter
    prefix string

func Format on f PlainFormatter string
    return "{f.prefix}: plain format"

type JSONFormatter
    indent int

func Format on f JSONFormatter string
    return "{\"type\": \"json\", \"indent\": {f.indent}}"

func PrintFormatted(f Formatter)
    fmt.Println(f.Format())

func main()
    plain := PlainFormatter{prefix: "LOG"}
    jsonFmt := JSONFormatter{indent: 2}

    PrintFormatted(plain)
    PrintFormatted(jsonFmt)
```

## Concurrency Patterns

### Worker Pool
```kukicha
func worker(id int, jobs channel of int, results channel of int)
    for job in jobs
        fmt.Println("Worker {id} processing job {job}")
        send results, job * 2

func main()
    jobs := make channel of int, 100
    results := make channel of int, 100

    # Start 3 workers
    for w from 1 through 3
        go worker(w, jobs, results)

    # Send 5 jobs
    for j from 1 through 5
        send jobs, j
    close(jobs)

    # Collect results
    for a from 1 through 5
        result := receive results
        fmt.Println("Result: {result}")
```

### Fan-Out/Fan-In
```kukicha
func producer(out channel of int)
    for i from 0 to 10
        send out, i
    close(out)

func square(in channel of int, out channel of int)
    for n in in
        send out, n * n
    close(out)

func main()
    numbers := make channel of int
    squares := make channel of int

    go producer(numbers)
    go square(numbers, squares)

    for result in squares
        fmt.Println(result)
```

## Generics via stdlib/iter

The `stdlib/iter` package uses special transpilation for generics:

```kukicha
import "stdlib/iter"
import "stdlib/slice"

func main()
    numbers := list of int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    # Filter and transform
    result := numbers
        |> iter.FromSlice()
        |> iter.Filter(n -> n % 2 equals 0)
        |> iter.Map(n -> n * n)
        |> iter.Take(3)
        |> slice.Collect()

    # result is [4, 16, 36]
```

## Testing in Kukicha

```kukicha
petiole mypackage

import "testing"

func TestAddition(t reference testing.T)
    result := Add(2, 3)
    if result != 5
        t.Errorf("expected 5, got {result}")

func TestDivision(t reference testing.T)
    result, err := Divide(10, 2)
    if err != empty
        t.Fatalf("unexpected error: {err}")
    if result != 5
        t.Errorf("expected 5, got {result}")

func TestDivisionByZero(t reference testing.T)
    _, err := Divide(10, 0)
    if err equals empty
        t.Error("expected error for division by zero")
```

## Struct Embedding

```kukicha
type Animal
    name string
    age int

type Dog
    Animal           # Embedded struct
    breed string

func Speak on a Animal string
    return "{a.name} makes a sound"

func Speak on d Dog string
    return "{d.name} barks!"

func main()
    dog := Dog
        Animal: Animal
            name: "Buddy"
            age: 3
        breed: "Golden Retriever"

    fmt.Println(dog.name)      # Access embedded field
    fmt.Println(dog.Speak())   # Calls Dog's Speak method
```

## JSON Handling

```kukicha
import "encoding/json"

type APIResponse
    status string `json:"status"`
    data list of User `json:"data"`
    count int `json:"count"`

func parseResponse(jsonData list of byte) APIResponse, error
    response := APIResponse{}
    json.Unmarshal(jsonData, reference of response) onerr return empty APIResponse, error
    return response, empty

func toJSON(data APIResponse) string
    bytes := json.MarshalIndent(data, "", "  ") onerr return "{}"
    return string(bytes)
```
