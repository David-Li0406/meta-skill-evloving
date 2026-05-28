# Maven

**Category**: developer-tools/build
**Description**: Apache Maven - build automation and project management tool for Java projects
**Homepage**: https://maven.apache.org

## Configuration Files

- `pom.xml`
- `.mvn/maven.config`
- `.mvn/extensions.xml`
- `.mvn/jvm.config`
- `mvnw`
- `mvnw.cmd`
- `settings.xml`

## Environment Variables

- `MAVEN_HOME`
- `M2_HOME`
- `MAVEN_OPTS`

## Detection Notes

- Standard build tool for Java projects
- Look for pom.xml in repository root
- Maven wrapper (mvnw) indicates project uses specific Maven version
- Multi-module projects have parent pom.xml with modules declaration

## Detection Confidence

- **Configuration File Detection**: 95% (HIGH)
