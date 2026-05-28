---
name: controller-test-with-mockmvc
description: Create unit tests for REST Controller classes using MockMvc and Mockito. Use this skill when writing tests for Controller layer that mock Service dependencies, when testing HTTP endpoints, request/response handling, or when asked to create controller tests.
---

# Controller Test with MockMvc Skill

このスキルは、MockMvcを使用したControllerクラスのテストケース作成手順を提供します。

## プロジェクト構成

- **テストクラス**: `src/test/java/com/t0k0sh1/demo/controller/{ControllerName}{MethodName}Test.java`

## テストクラス作成手順

### 1. テストクラスの基本構成

```java
package com.t0k0sh1.demo.controller;

import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

/**
 * {ControllerName}.{methodName}のテストクラス
 */
@WebMvcTest({ControllerName}.class)
class {ControllerName}{MethodName}Test {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private {ServiceName} {serviceName};

    // テストメソッド
}
```

### 2. 必須アノテーション

| アノテーション | 目的 |
|--------------|------|
| `@WebMvcTest({Controller}.class)` | コントローラー層のみをテスト対象にする |
| `@MockitoBean` | Serviceクラスをモック化する |

### 3. 重要: Spring Boot 4.0でのimport

Spring Boot 4.0では以下のimportを使用すること:

```java
// Spring Boot 4.0
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
```

**注意**: Spring Boot 3.x以前とは異なるパッケージになっている

### 4. テストメソッドの命名規則

```
{methodName}_{条件}_{期待結果}
```

例:
- `getUser_existingUser_returnsOkWithUser`
- `getUser_nonExistingUser_returnsNotFound`
- `createUser_validInput_returnsCreated`
- `createUser_invalidInput_returnsBadRequest`

### 5. テストメソッドの構成（AAA パターン）

```java
@Test
@DisplayName("日本語でテストの説明を記述")
void {methodName}_{条件}_{期待結果}() throws Exception {
    // Arrange（準備）- Serviceのモック設定
    when(service.method(param)).thenReturn(expectedOutDto);

    // Act & Assert（実行と検証）
    mockMvc.perform(get("/api/v1/endpoint"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.field").value(expectedValue));
}
```

## HTTPメソッド別テスト例

### GET（1件取得）

```java
@Test
@DisplayName("存在するユーザーIDを指定した場合、200 OKとユーザー情報が返却されること")
void getUser_existingUser_returnsOkWithUser() throws Exception {
    // Arrange
    GetUserOutDto outDto = GetUserOutDto.builder()
            .resultCode(GetUserOutDto.ResultCode.SUCCESS)
            .id(1L)
            .username("testuser")
            .email("test@example.com")
            .build();
    when(userService.findById(1L)).thenReturn(outDto);

    // Act & Assert
    mockMvc.perform(get("/api/v1/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value(1))
            .andExpect(jsonPath("$.username").value("testuser"))
            .andExpect(jsonPath("$.email").value("test@example.com"));
}
```

### POST（登録）

```java
@Test
@DisplayName("正常なリクエストの場合、201 Createdとユーザー情報が返却されること")
void createUser_validInput_returnsCreated() throws Exception {
    // Arrange
    CreateUserOutDto outDto = CreateUserOutDto.builder()
            .resultCode(CreateUserOutDto.ResultCode.SUCCESS)
            .id(1L)
            .username("newuser")
            .email("new@example.com")
            .build();
    when(userService.create(any(CreateUserInDto.class))).thenReturn(outDto);

    String requestBody = """
            {
                "username": "newuser",
                "email": "new@example.com"
            }
            """;

    // Act & Assert
    mockMvc.perform(post("/api/v1/users")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(requestBody))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").value(1))
            .andExpect(jsonPath("$.username").value("newuser"));
}
```

### PUT（更新）

```java
@Test
@DisplayName("正常なリクエストの場合、200 OKと更新後のユーザー情報が返却されること")
void updateUser_validInput_returnsOk() throws Exception {
    // Arrange
    UpdateUserOutDto outDto = UpdateUserOutDto.builder()
            .resultCode(UpdateUserOutDto.ResultCode.SUCCESS)
            .id(1L)
            .username("updateduser")
            .email("updated@example.com")
            .build();
    when(userService.update(any(UpdateUserInDto.class))).thenReturn(outDto);

    String requestBody = """
            {
                "username": "updateduser",
                "email": "updated@example.com"
            }
            """;

    // Act & Assert
    mockMvc.perform(put("/api/v1/users/1")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(requestBody))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.username").value("updateduser"));
}
```

### DELETE（削除）

```java
@Test
@DisplayName("存在するユーザーIDを指定した場合、204 No Contentが返却されること")
void deleteUser_existingUser_returnsNoContent() throws Exception {
    // Arrange
    DeleteUserOutDto outDto = DeleteUserOutDto.builder()
            .resultCode(DeleteUserOutDto.ResultCode.SUCCESS)
            .build();
    when(userService.delete(1L)).thenReturn(outDto);

    // Act & Assert
    mockMvc.perform(delete("/api/v1/users/1"))
            .andExpect(status().isNoContent());
}
```

## 推奨テストケース

### 各エンドポイントで確認すべき観点

| HTTPステータス | テストケース |
|---------------|-------------|
| 200 OK | 正常系（取得・更新成功） |
| 201 Created | 正常系（登録成功） |
| 204 No Content | 正常系（削除成功） |
| 400 Bad Request | バリデーションエラー |
| 404 Not Found | リソースが存在しない |
| 409 Conflict | 重複エラー |
| 500 Internal Server Error | システムエラー |

## アサーションのベストプラクティス

### ステータスコードの検証

```java
.andExpect(status().isOk())           // 200
.andExpect(status().isCreated())      // 201
.andExpect(status().isNoContent())    // 204
.andExpect(status().isBadRequest())   // 400
.andExpect(status().isNotFound())     // 404
.andExpect(status().isConflict())     // 409
.andExpect(status().isInternalServerError()) // 500
```

### レスポンスボディの検証（JSONPath）

```java
.andExpect(jsonPath("$.id").value(1))
.andExpect(jsonPath("$.username").value("testuser"))
.andExpect(jsonPath("$.items").isArray())
.andExpect(jsonPath("$.items.length()").value(3))
.andExpect(jsonPath("$.items[0].name").value("item1"))
```

## 関連ファイル

- 実装例: [UserRestControllerGetUserTest.java](../../src/test/java/com/t0k0sh1/demo/controller/UserRestControllerGetUserTest.java)
