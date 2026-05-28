---
name: Quarkus Reactive
description: Mutiny reactive types, reactive routes, and non-blocking I/O.
metadata:
  labels: [java, quarkus, reactive, mutiny]
  triggers:
    files: ['**/*.java']
    keywords: [Mutiny, Uni, Multi, '@Route', reactive, SmallRye, '@NonBlocking']
---

# Quarkus Reactive Standards

## Mutiny Types

```java
// Uni - 0 or 1 item (like CompletableFuture)
public Uni<User> findById(Long id) {
    return Uni.createFrom().item(() -> repository.findById(id))
        .onFailure().recoverWithItem(User.unknown());
}

// Multi - 0 to N items (like Stream)
public Multi<User> streamAll() {
    return Multi.createFrom().items(repository.findAll().stream())
        .filter(User::isActive);
}

// Transformations
Uni<String> name = findById(1L)
    .map(User::getName)
    .onItem().ifNull().failWith(new NotFoundException());

// Combining
Uni<UserProfile> profile = Uni.combine().all()
    .unis(findUser(id), findOrders(id), findPreferences(id))
    .with((user, orders, prefs) -> new UserProfile(user, orders, prefs));
```

## Reactive REST Endpoints

```java
@Path("/users")
public class UserResource {

    @GET
    @Path("/{id}")
    public Uni<User> get(@PathParam("id") Long id) {
        return userService.findById(id);
    }

    @GET
    @Produces(MediaType.SERVER_SENT_EVENTS)
    public Multi<User> stream() {
        return userService.streamAll();
    }

    @POST
    public Uni<Response> create(CreateUserRequest request) {
        return userService.create(request)
            .map(user -> Response.created(URI.create("/users/" + user.id())).build());
    }
}
```

## References

- [Mutiny Patterns](references/mutiny-patterns.md) - Error handling, timeouts, combining
