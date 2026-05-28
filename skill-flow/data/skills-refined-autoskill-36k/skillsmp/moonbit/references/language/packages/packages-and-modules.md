### Managing Projects with Packages

#### Packages and modules

In MoonBit, the most important unit for code organization is a package, which consists of a number of source code files and a single `moon.pkg.json` configuration file.
A package can either be a `main` package, consisting a `main` function, or a package that serves as a library, identified by the [`is-main`](../toolchain/moon/package.md#is-main) field.

A project, corresponding to a module, consists of multiple packages and a single `moon.mod.json` configuration file.

A module is identified by the [`name`](../toolchain/moon/module.md#name) field, which usually consists to parts, seperated by `/`: `user-name/project-name`.
A package is identified by the relative path to the source root defined by the [`source`](../toolchain/moon/module.md#source-directory) field. The full identifier would be `user-name/project-name/path-to-pkg`.

When using things from another package, the dependency between modules should first be declared inside the `moon.mod.json` by the [`deps`](../toolchain/moon/module.md#dependency-management) field.
The dependency between packages should then be declared in side the `moon.pkg.json` by the [`import`](../toolchain/moon/package.md#import) field.

<a id="default-alias"></a>

The **default alias** of a package is the last part of the identifier split by `/`.
One can use `@pkg_alias` to access the imported entities, where `pkg_alias` is either the full identifier or the default alias.
A custom alias may also be defined with the [`import`](../toolchain/moon/package.md#import) field.

```json
{
    "import": [
        "moonbit-community/language/packages/pkgA",
        {
            "path": "moonbit-community/language/packages/pkgC",
            "alias": "c"
        }
    ]
}
```

```moonbit
///|
pub fn add1(x : Int) -> Int {
  @moonbitlang/core/int.abs(@c.incr(@pkgA.incr(x)))
}
```

##### Internal Packages

You can define internal packages that are only available for certain packages.

Code in `a/b/c/internal/x/y/z` are only available to packages `a/b/c` and `a/b/c/**`.

##### Using

You can use `using` syntax to import symbols defined in another package.

```moonbit
///|
pub using @pkgA {incr, trait Trait, type Type}
```

By having `pub` modifier, it is considered as reexportation.

