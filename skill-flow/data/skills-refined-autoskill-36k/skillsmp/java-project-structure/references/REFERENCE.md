# Java Project Structure References

## References

- [**Maven Project Layout**](maven-project-layout.md) - Standard directories, profiles, multi-module setup
- [**Module System**](module-system.md) - JPMS patterns, exports, opens, migration from classpath

## Quick Checks

- [ ] Standard Maven/Gradle layout (src/main/java, src/test/java)
- [ ] Reverse domain package naming (com.company.project.layer)
- [ ] Layer dependencies flow downward only
- [ ] DTOs separate from entities
- [ ] Test packages mirror source packages
- [ ] Configuration in src/main/resources
