---
name: migrating-ast-node
description: Migrate an ast node definition from java to go
---

When migrating an ast node definition start with the machine migrated code in `./ballerina-lang-go/ast/migrated`.
There will be a go file corresponding to the java ast node already migrated. First copy the *relevant* content to the
corresponding go file. If the file you are migrating has dependency on some other ast node that haven't been migrated recursively migrate them as well.
*YOU SHOULD ALWAYS FULLY MIGRATE A FILE IN migrated DIRECTORY* not just parts you need. After migrating a file rename it from `go_todo` to `go_done`
- DON'T ADD RANDOM "PLACEHOLDER" INTERFACES OR STRUCTS. IF YOU CAN MIGRATE IT PROPERLY DON'T MIGRATE AT ALL.

## Determining what content to copy from migrated code
- You must copy the struct definition and interface type assertions (`var _ $Interface = &$Struct`).
- Then you should *only copy the methods required for satisfying the assertions* (compiler will tell what methods are missing based on the assertion).
    - DO NOT COPY RANDOM METHODS
    - When copying methods fallow the style on the file you are copying content to.
- Then you may need to fix up the struct definition. Sometimes they may have inclusions on interfaces and probably the struct will be something file $NameBase. Find that and use it.
    - structs should not use inclusion on interfaces
    - *DON'T GO AROUND CHANGING THE TYPES OF THE STRUCT FIELDS TO BE INTERFACES*
        - This would mean you may need to fix some of the getters and setters. Getters may need to return pointers or create new collections. Setters may need to add type assertions
    - Struct fields should not hold struct values instead they should hold pointers to structs to match java.
        - Slices and other collections should have structs instead of pointers to structs
- You may need to update the method definitions to use the interfaces instead of struct values.


### Adding interfaces
Sometimes the interface we are asserting may not have been defined already in that case.
- Find the corresponding the java interface and manually migrate that to the same file as you have the assertion.
- When migrating interfaces make sure all the parameters and return values are them self interfaces (This way you can turn generic methods to non-generic in go)
- If it is a simple marker interface adding a type alias is enough. Fallow the coding style in the file you are copying content to.
- *Interface must have all the same methods as the original and must have the same name*

## Determining the go file to put source code

To determine the corresponding go file check what package it belongs to. For example if it belong to
`org.wso2.ballerinalang.compiler.tree.bindingpatterns` then it should end up in `binding_patterns.go` file.
Those in top `org.wso2.ballerinalang.compiler.tree` ends up in `ast.go` file


+ When migrating interfaces and structs they *must* use the same name as the go source.
