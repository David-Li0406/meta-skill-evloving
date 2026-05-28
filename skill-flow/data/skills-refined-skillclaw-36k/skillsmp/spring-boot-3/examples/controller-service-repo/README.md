# Controller-Service-Repository Pattern Example

This example demonstrates the classic layered architecture pattern with clear separation of concerns.

## Architecture

```
UserController (HTTP layer)
    ↓
UserService (Business logic)
    ↓
UserRepository (Data access)
    ↓
Database
```

## Files

### UserController.java
```java
package com.example.demo.controller;

import com.example.demo.dto.UserDTO;
import com.example.demo.request.CreateUserRequest;
import com.example.demo.service.UserService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor  // Lombok generates constructor
public class UserController {

    private final UserService userService;

    @GetMapping("/{id}")
    public ResponseEntity<UserDTO> getById(@PathVariable Long id) {
        UserDTO user = userService.findById(id);
        return ResponseEntity.ok(user);
    }

    @GetMapping
    public ResponseEntity<List<UserDTO>> getAll() {
        List<UserDTO> users = userService.findAll();
        return ResponseEntity.ok(users);
    }

    @PostMapping
    public ResponseEntity<UserDTO> create(@Valid @RequestBody CreateUserRequest request) {
        UserDTO created = userService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    @PutMapping("/{id}")
    public ResponseEntity<UserDTO> update(
        @PathVariable Long id,
        @Valid @RequestBody CreateUserRequest request
    ) {
        UserDTO updated = userService.update(id, request);
        return ResponseEntity.ok(updated);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        userService.delete(id);
        return ResponseEntity.noContent().build();
    }
}
```

### UserService.java
```java
package com.example.demo.service;

import com.example.demo.dto.UserDTO;
import com.example.demo.entity.User;
import com.example.demo.exception.DuplicateResourceException;
import com.example.demo.exception.ResourceNotFoundException;
import com.example.demo.mapper.UserMapper;
import com.example.demo.repository.UserRepository;
import com.example.demo.request.CreateUserRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public UserDTO findById(Long id) {
        User user = userRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("User", id));
        return UserMapper.toDTO(user);
    }

    public List<UserDTO> findAll() {
        List<User> users = userRepository.findAll();
        return UserMapper.toDTOList(users);
    }

    public UserDTO create(CreateUserRequest request) {
        // Business validation
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new DuplicateResourceException("User", "email", request.getEmail());
        }

        // Create entity
        User user = new User();
        user.setEmail(request.getEmail());
        user.setPassword(passwordEncoder.encode(request.getPassword()));
        user.setFirstName(request.getFirstName());
        user.setLastName(request.getLastName());

        // Save
        User saved = userRepository.save(user);
        return UserMapper.toDTO(saved);
    }

    public UserDTO update(Long id, CreateUserRequest request) {
        User user = userRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("User", id));

        // Check email uniqueness
        if (!user.getEmail().equals(request.getEmail()) &&
            userRepository.existsByEmail(request.getEmail())) {
            throw new DuplicateResourceException("User", "email", request.getEmail());
        }

        // Update fields
        user.setEmail(request.getEmail());
        if (request.getPassword() != null) {
            user.setPassword(passwordEncoder.encode(request.getPassword()));
        }
        user.setFirstName(request.getFirstName());
        user.setLastName(request.getLastName());

        User updated = userRepository.save(user);
        return UserMapper.toDTO(updated);
    }

    public void delete(Long id) {
        if (!userRepository.existsById(id)) {
            throw new ResourceNotFoundException("User", id);
        }
        userRepository.deleteById(id);
    }
}
```

### UserRepository.java
```java
package com.example.demo.repository;

import com.example.demo.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    Optional<User> findByEmail(String email);
    boolean existsByEmail(String email);
}
```

### User.java (Entity)
```java
package com.example.demo.entity;

import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "users")
@Data  // Lombok generates getters/setters
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 100)
    private String email;

    @Column(nullable = false)
    private String password;

    @Column(name = "first_name")
    private String firstName;

    @Column(name = "last_name")
    private String lastName;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
}
```

### UserDTO.java
```java
package com.example.demo.dto;

import lombok.Data;

import java.time.LocalDateTime;

@Data
public class UserDTO {
    private Long id;
    private String email;
    private String firstName;
    private String lastName;
    private LocalDateTime createdAt;

    // Note: No password field!
}
```

### CreateUserRequest.java
```java
package com.example.demo.request;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Data;

@Data
public class CreateUserRequest {

    @NotBlank(message = "Email is required")
    @Email(message = "Email must be valid")
    private String email;

    @Size(min = 8, message = "Password must be at least 8 characters")
    private String password;

    @NotBlank(message = "First name is required")
    private String firstName;

    @NotBlank(message = "Last name is required")
    private String lastName;
}
```

### UserMapper.java
```java
package com.example.demo.mapper;

import com.example.demo.dto.UserDTO;
import com.example.demo.entity.User;
import com.example.demo.request.CreateUserRequest;

public class UserMapper {

    public static UserDTO toDTO(User user) {
        UserDTO dto = new UserDTO();
        dto.setId(user.getId());
        dto.setEmail(user.getEmail());
        dto.setFirstName(user.getFirstName());
        dto.setLastName(user.getLastName());
        dto.setCreatedAt(user.getCreatedAt());
        return dto;
    }

    public static User toEntity(CreateUserRequest request) {
        User user = new User();
        user.setEmail(request.getEmail());
        user.setPassword(request.getPassword());
        user.setFirstName(request.getFirstName());
        user.setLastName(request.getLastName());
        return user;
    }

    public static java.util.List<UserDTO> toDTOList(java.util.List<User> users) {
        return users.stream()
            .map(UserMapper::toDTO)
            .collect(java.util.stream.Collectors.toList());
    }
}
```

## Key Points

1. **Controller** - Thin layer, only handles HTTP mapping
2. **Service** - Contains all business logic and validation
3. **Repository** - Only data access, no business logic
4. **DTO** - Data Transfer Object for API (no password!)
5. **Entity** - Database model (with password)
6. **Mapper** - Converts between Entity and DTO

## Testing

```java
@SpringBootTest
@AutoConfigureMockMvc
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void createUser_ShouldReturn201() throws Exception {
        CreateUserRequest request = new CreateUserRequest();
        request.setEmail("test@example.com");
        request.setPassword("Password123");
        request.setFirstName("John");
        request.setLastName("Doe");

        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").exists())
            .andExpect(jsonPath("$.email").value("test@example.com"))
            .andExpect(jsonPath("$.password").doesNotExist());
    }
}
```
