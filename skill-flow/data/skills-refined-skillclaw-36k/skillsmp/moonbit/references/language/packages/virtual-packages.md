### Managing Projects with Packages

#### Virtual Packages

###### WARNING
Virtual package is an experimental feature. There may be bugs and undefined behaviors.

You can define virtual packages, which serves as an interface. They can be replaced by specific implementations at build time. Currently virtual packages can only contain plain functions.

Virtual packages can be useful when swapping different implementations while keeping the code untouched.

##### Defining a virtual package

You need to declare it to be a virtual package and define its interface in a MoonBit interface file.

Within `moon.pkg.json`, you will need to add field [`virtual`](../toolchain/moon/package.md#declarations) :

```json
{
  "virtual": {
    "has-default": true
  }
}
```

The `has-default` indicates whether the virtual package has a default implementation.

Within the package, you will need to add an interface file `pkg.mbti`:

```moonbit
package "moonbit-community/language/packages/virtual"

fn log(String) -> Unit
```

The first line of the interface file need to be `package "full-package-name"`. Then comes the declarations.
The `pub` keyword for [access control]() and the function parameter names should be omitted.

##### Implementing a virtual package

A virtual package can have a default implementation. By defining [`virtual.has-default`](../toolchain/moon/package.md#declarations) as `true`, you can implement the code as usual within the same package.

```moonbit
///|
pub fn log(s : String) -> Unit {
  println(s)
}
```

A virtual package can also be implemented by a third party. By defining [`implements`](../toolchain/moon/package.md#implementations) as the target package's full name, the compiler can warn you about the missing implementations or the mismatched implementations.

```json
{
  "implement": "moonbit-community/language/packages/virtual"
}
```

```moonbit
///|
pub fn log(string : String) -> Unit {
  ignore(string)
}
```

##### Using a virtual package

To use a virtual package, it's the same as other packages: define [`import`](../toolchain/moon/package.md#import) field in the package where you want to use it.

##### Overriding a virtual package

If a virtual package has a default implementation and that is your choice, there's no extra configurations.

Otherwise, you may define the [`overrides`](../toolchain/moon/package.md#overriding-implementations) field by providing an array of implementations that you would like to use.

```json
{
  "overrides": ["moonbit-community/language/packages/implement"],
  "import": [
    "moonbit-community/language/packages/virtual"
  ],
  "is-main": true
}
```

You should reference the virtual package when using the entities.

```moonbit
///|
fn main {
  @virtual.log("Hello")
}
```

