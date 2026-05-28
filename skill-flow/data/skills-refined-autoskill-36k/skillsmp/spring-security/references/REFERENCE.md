# Spring Security References

## References

- [**JWT Auth Flow**](jwt-auth-flow.md) - Token generation, validation, refresh pattern
- [**OAuth2 Resource Server**](oauth2-resource-server.md) - JWT decoder, extracting claims
- [**Security Filter Chain**](security-filter-chain.md) - Filter ordering, custom filters

## Quick Checks

- [ ] BCrypt password encoder (cost 10-12)
- [ ] Stateless session for REST APIs
- [ ] JWT validation on every request
- [ ] CORS configured for allowed origins only
- [ ] CSRF disabled only for stateless APIs
- [ ] Method security for fine-grained authorization
