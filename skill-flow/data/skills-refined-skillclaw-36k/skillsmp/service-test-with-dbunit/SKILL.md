---
name: service-test-with-dbunit
description: Create unit tests for Service classes using DBUnit and Spring Test DBUnit. Use this skill when writing integration tests for Service layer that require database setup with test data, when testing methods that interact with MyBatis mappers, or when asked to create service tests with actual database operations.
---

# Service Test with DBUnit Skill

このスキルは、DBUnitを使用したServiceクラスのテストケース作成手順を提供します。

## プロジェクト構成

- **テストクラス**: `src/test/java/com/t0k0sh1/demo/service/{ServiceName}{MethodName}Test.java`
- **テストデータ**: `src/test/resources/dbunit/{table_name}/{methodName}/setup.xml`
- **テスト設定**: `src/test/resources/application.yml`

## テストクラス作成手順

### 1. テストクラスの基本構成

```java
package com.t0k0sh1.demo.service;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.TestExecutionListeners;
import org.springframework.test.context.support.DependencyInjectionTestExecutionListener;
import org.springframework.test.context.support.DirtiesContextTestExecutionListener;
import org.springframework.transaction.annotation.Transactional;

import com.github.springtestdbunit.TransactionDbUnitTestExecutionListener;
import com.github.springtestdbunit.annotation.DatabaseSetup;

/**
 * {ServiceName}.{methodName}のテストクラス
 */
@SpringBootTest
@TestExecutionListeners({
        DependencyInjectionTestExecutionListener.class,
        DirtiesContextTestExecutionListener.class,
        TransactionDbUnitTestExecutionListener.class
})
@Transactional
class {ServiceName}{MethodName}Test {

    @Autowired
    private {ServiceName} {serviceName};

    // テストメソッド
}
```

### 2. 必須アノテーション

| アノテーション | 目的 |
|--------------|------|
| `@SpringBootTest` | Spring Boot統合テストを有効化 |
| `@TestExecutionListeners` | DBUnit用リスナーを設定 |
| `@Transactional` | テスト後にロールバックして他のテストに影響を与えない |
| `@DatabaseSetup` | テストデータをセットアップ |

### 3. テストメソッドの命名規則

```
{methodName}_{条件}_{期待結果}
```

例:
- `findById_existingUser_returnsUser`
- `findById_nonExistingUser_returnsNotFound`
- `findById_deletedUser_returnsNotFound`

### 4. テストメソッドの構成（AAA パターン）

```java
@Test
@DisplayName("日本語でテストの説明を記述")
@DatabaseSetup("/dbunit/{table_name}/{methodName}/setup.xml")
void {methodName}_{条件}_{期待結果}() {
    // Arrange（準備）- 必要に応じて入力を準備

    // Act（実行）
    var result = service.method(param);

    // Assert（検証）
    assertThat(result.getResultCode()).isEqualTo(ExpectedResultCode);
    assertThat(result.getField()).isEqualTo(expectedValue);
}
```

## テストデータ（DBUnit XML）作成手順

### 1. ファイル配置

```
src/test/resources/dbunit/{table_name}/{methodName}/setup.xml
```

例: `src/test/resources/dbunit/users/findById/setup.xml`

### 2. XMLフォーマット

1レコード1行で記述すること（可読性とdiff確認のため）:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<dataset>
    <{table_name} column1="value1" column2="value2" .../>
</dataset>
```

### 3. データ作成のポイント

- **正常系データ**: テスト対象の条件を満たすデータ
- **異常系データ**: 存在しないID、論理削除済みなど
- **境界値データ**: 必要に応じて境界値テスト用データ

### 4. usersテーブルの例

```xml
<?xml version="1.0" encoding="UTF-8"?>
<dataset>
    <!-- 正常データ -->
    <users id="1" username="testuser1" email="test1@example.com" created_by="1" created_at="2026-01-01 00:00:00" updated_by="1" updated_at="2026-01-01 00:00:00" is_deleted="false"/>
    <!-- 論理削除済みデータ -->
    <users id="3" username="deleteduser" email="deleted@example.com" created_by="1" created_at="2026-01-03 00:00:00" updated_by="1" updated_at="2026-01-03 00:00:00" is_deleted="true"/>
</dataset>
```

## 推奨テストケース

### 取得系メソッド（findById, findAll）

1. **正常系**: データが存在する場合
2. **異常系**: データが存在しない場合
3. **異常系**: 論理削除されたデータの場合

### 登録系メソッド（create）

1. **正常系**: 正常に登録できる場合
2. **異常系**: 重複エラー（ユニーク制約違反）
3. **異常系**: バリデーションエラー

### 更新系メソッド（update）

1. **正常系**: 正常に更新できる場合
2. **異常系**: 対象が存在しない場合
3. **異常系**: 論理削除済みの場合

### 削除系メソッド（delete）

1. **正常系**: 正常に削除できる場合
2. **異常系**: 対象が存在しない場合

## アサーションのベストプラクティス

### AssertJを使用

```java
import static org.assertj.core.api.Assertions.assertThat;

// 単一値
assertThat(result.getId()).isEqualTo(1L);

// null チェック
assertThat(result.getId()).isNull();
assertThat(result.getId()).isNotNull();

// 日時
assertThat(result.getCreatedAt()).isEqualTo(LocalDateTime.of(2026, 1, 1, 0, 0, 0));

// Enum
assertThat(result.getResultCode()).isEqualTo(ResultCode.SUCCESS);
```

## 関連ファイル

- テスト設定: [src/test/resources/application.yml](../../src/test/resources/application.yml)
- 実装例: [UserServiceFindByIdTest.java](../../src/test/java/com/t0k0sh1/demo/service/UserServiceFindByIdTest.java)
- テストデータ例: [setup.xml](../../src/test/resources/dbunit/users/findById/setup.xml)
