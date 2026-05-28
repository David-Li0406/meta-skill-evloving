# Maven Lifecycle Phases

## Default Lifecycle

```xml
<!-- Phase order: validate → compile → test → package → verify → install → deploy -->

<!-- Skip tests during build -->
<properties>
    <maven.test.skip>true</maven.test.skip>
    <!-- Or just skip execution, still compile -->
    <skipTests>true</skipTests>
</properties>
```

## Common Commands

```bash
# Clean and build
mvn clean install

# Build without tests
mvn clean install -DskipTests

# Run specific phase
mvn compile
mvn test
mvn package

# Run with profile
mvn clean install -Pproduction

# Debug output
mvn clean install -X

# Dependency tree
mvn dependency:tree

# Effective POM
mvn help:effective-pom
```

## Plugin Configuration

```xml
<build>
    <plugins>
        <!-- Compiler plugin -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.11.0</version>
            <configuration>
                <source>21</source>
                <target>21</target>
                <compilerArgs>
                    <arg>--enable-preview</arg>
                </compilerArgs>
            </configuration>
        </plugin>

        <!-- Surefire for unit tests -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.1.2</version>
            <configuration>
                <includes>
                    <include>**/*Test.java</include>
                </includes>
            </configuration>
        </plugin>

        <!-- Failsafe for integration tests -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-failsafe-plugin</artifactId>
            <version>3.1.2</version>
            <executions>
                <execution>
                    <goals>
                        <goal>integration-test</goal>
                        <goal>verify</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

## Multi-Module Project

```xml
<!-- Parent POM -->
<project>
    <groupId>com.example</groupId>
    <artifactId>parent</artifactId>
    <version>1.0.0</version>
    <packaging>pom</packaging>

    <modules>
        <module>core</module>
        <module>api</module>
        <module>web</module>
    </modules>

    <dependencyManagement>
        <dependencies>
            <!-- Centralize versions here -->
        </dependencies>
    </dependencyManagement>
</project>
```
