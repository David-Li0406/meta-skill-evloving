# JUnit and Mockito Testing References

## References

- [**JUnit 5 Patterns**](junit5-patterns.md) - Test structure, parameterized tests, assertions
- [**Mockito Patterns**](mockito-patterns.md) - Mocking, stubbing, verification, spying
- [**Spring Boot Testing**](spring-boot-testing.md) - Slice tests, integration, Testcontainers

## Quick Checks

- [ ] Use @ExtendWith(MockitoExtension.class)
- [ ] @DisplayName for readable test names
- [ ] Parameterized tests for multiple inputs
- [ ] Slice tests (@WebMvcTest, @DataJpaTest) for focused testing
- [ ] Testcontainers for real database tests
