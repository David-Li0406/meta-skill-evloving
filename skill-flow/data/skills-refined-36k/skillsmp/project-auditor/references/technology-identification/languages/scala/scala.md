# Scala

**Category**: languages
**Description**: Scala programming language - functional and object-oriented language for JVM with strong type system
**Homepage**: https://www.scala-lang.org

## Package Detection

### MAVEN
- `org.scala-lang:scala-library`
- `org.scala-lang:scala3-library`

### SBT
- `sbt`
- `org.typelevel:cats-core`
- `com.typesafe.akka:akka-actor`

## Configuration Files

- `build.sbt`
- `project/build.properties`
- `project/plugins.sbt`
- `.scalafmt.conf`
- `.scalafix.conf`
- `.sbtopts`
- `.jvmopts`

## File Extensions

- `.scala`
- `.sc` (Scala script/worksheet)
- `.sbt`

## Import Detection

### Scala
**Pattern**: `^package\s+[\w.]+`
- Package declaration
- Example: `package com.example.service`

**Pattern**: `^import\s+[\w.]+`
- Import statement
- Example: `import scala.concurrent.Future`

**Pattern**: `^(case\s+)?class\s+\w+`
- Class declaration
- Example: `case class User(name: String, age: Int)`

**Pattern**: `^(sealed\s+)?trait\s+\w+`
- Trait declaration
- Example: `sealed trait Result[+A]`

**Pattern**: `^object\s+\w+`
- Object declaration
- Example: `object Main extends App {}`

**Pattern**: `^def\s+\w+`
- Method declaration
- Example: `def process(input: String): Either[Error, Output]`

## Environment Variables

- `SCALA_HOME`
- `SBT_HOME`
- `SBT_OPTS`
- `JAVA_OPTS`

## Version Indicators

- Scala 3.x (current)
- Scala 2.13 (widely used)
- Scala 2.12 (legacy, still common)

## Detection Notes

- Look for `.scala` files in repository
- build.sbt indicates sbt build tool
- Check scala-library version in dependencies
- Scala 3 uses different syntax from Scala 2
- Often used with Akka, Play Framework, or Spark

## Detection Confidence

- **File Extension Detection**: 95% (HIGH)
- **build.sbt Detection**: 95% (HIGH)
- **Package Detection**: 90% (HIGH)
