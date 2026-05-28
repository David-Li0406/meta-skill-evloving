# AAA 패턴 상세 가이드

AAA (Arrange-Act-Assert) 패턴은 테스트를 명확하게 구조화하는 표준 방법입니다.

## Arrange (준비)

테스트에 필요한 모든 것을 설정합니다.

### 테스트 데이터 생성

```typescript
// Arrange
const userId = 'user-123';
const createUserDto: CreateUserDto = {
  email: 'test@example.com',
  name: '테스트',
  password: 'password123',
};
```

### Mock 설정

```typescript
// Arrange
mockUserRepository.findByEmail.mockResolvedValue(null);  // 중복 없음
mockUserRepository.save.mockResolvedValue({ id: userId, ...createUserDto });
mockHashService.hash.mockResolvedValue('hashed_password');
```

### 초기 상태 설정

```typescript
// Arrange
await cache.clear();  // 캐시 초기화
mockConfigService.get.mockReturnValue('test-value');
```

## Act (실행)

테스트 대상 메서드를 단 한 번 호출합니다.

```typescript
// Act
const result = await service.createUser(createUserDto);
```

### 주의사항

- Act 섹션은 가능한 한 줄로 유지
- 여러 동작이 필요하면 테스트를 분리

```typescript
// ❌ Bad: Act에서 여러 동작
const user = await service.createUser(dto);
await service.verifyEmail(user.id);
await service.activateUser(user.id);

// ✅ Good: 각각 별도 테스트
it('should create user', async () => { ... });
it('should verify email', async () => { ... });
it('should activate user', async () => { ... });
```

## Assert (검증)

예상 결과를 검증합니다.

### 반환값 검증

```typescript
// Assert - 반환값
expect(result).toBeDefined();
expect(result.id).toBe(userId);
expect(result.email).toBe(createUserDto.email);
expect(result.password).toBeUndefined();  // 비밀번호는 반환하지 않음
```

### Mock 호출 검증

```typescript
// Assert - Mock 호출
expect(mockUserRepository.findByEmail).toHaveBeenCalledWith(createUserDto.email);
expect(mockUserRepository.save).toHaveBeenCalledTimes(1);
expect(mockHashService.hash).toHaveBeenCalledWith(createUserDto.password);
```

### 예외 검증

```typescript
// Assert - 예외
await expect(service.findById('invalid'))
  .rejects.toThrow(NotFoundException);

// 구체적인 에러 메시지 검증
await expect(service.findById('invalid'))
  .rejects.toThrow('User not found');
```

## 전체 예시

```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create a new user with hashed password', async () => {
      // Arrange
      const createUserDto: CreateUserDto = {
        email: 'test@example.com',
        name: '테스트',
        password: 'password123',
      };
      const hashedPassword = 'hashed_password_123';
      const savedUser = {
        id: 'user-123',
        email: createUserDto.email,
        name: createUserDto.name,
        password: hashedPassword,
        createdAt: new Date(),
      };

      mockUserRepository.findByEmail.mockResolvedValue(null);
      mockHashService.hash.mockResolvedValue(hashedPassword);
      mockUserRepository.save.mockResolvedValue(savedUser);

      // Act
      const result = await service.createUser(createUserDto);

      // Assert
      expect(result).toEqual({
        id: savedUser.id,
        email: savedUser.email,
        name: savedUser.name,
        createdAt: savedUser.createdAt,
      });
      expect(mockHashService.hash).toHaveBeenCalledWith(createUserDto.password);
      expect(mockUserRepository.save).toHaveBeenCalledWith(
        expect.objectContaining({
          email: createUserDto.email,
          password: hashedPassword,
        }),
      );
    });

    it('should throw ConflictException when email already exists', async () => {
      // Arrange
      const createUserDto: CreateUserDto = {
        email: 'existing@example.com',
        name: '테스트',
        password: 'password123',
      };
      mockUserRepository.findByEmail.mockResolvedValue({ id: 'existing-user' });

      // Act & Assert
      await expect(service.createUser(createUserDto))
        .rejects.toThrow(ConflictException);

      // 추가 검증: save가 호출되지 않았는지
      expect(mockUserRepository.save).not.toHaveBeenCalled();
    });
  });
});
```

## 팁

1. **주석 사용**: `// Arrange`, `// Act`, `// Assert` 주석으로 섹션 구분
2. **빈 줄 사용**: 각 섹션 사이에 빈 줄 추가
3. **Act은 짧게**: 테스트 대상 호출은 한 줄로
4. **Assert는 구체적으로**: 정확히 무엇을 검증하는지 명확하게
