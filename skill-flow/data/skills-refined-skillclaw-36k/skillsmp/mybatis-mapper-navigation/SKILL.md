---
name: mybatis-mapper-navigation
description: Navigate between MyBatis Mapper Java interfaces and their corresponding XML mapper files. Use this skill when working with MyBatis mappers, when you need to find the XML file for a Java mapper interface, or when you need to find the Java interface for an XML mapper file.
---

# MyBatis マッパーナビゲーションスキル

このスキルは、MyBatis MapperのJavaインターフェースと対応するXMLマッパーファイル間のナビゲーションを支援します。

## プロジェクト構成

- **Java Mapperインターフェース**: `src/main/java/com/t0k0sh1/demo/mapper/*.java`
- **XMLマッパーファイル**: `src/main/resources/com/t0k0sh1/demo/mapper/*.xml`

## ナビゲーションルール

### JavaからXMLへ

Javaマッパーインターフェース（例: `UsersMapper.java`）を扱う場合:
1. 対応するXMLファイルは同じ名前で拡張子が`.xml`
2. 配置場所: `src/main/resources/com/t0k0sh1/demo/mapper/UsersMapper.xml`
3. XMLのnamespaceはJavaインターフェースの完全修飾名と一致する必要がある

### XMLからJavaへ

XMLマッパーファイル（例: `UsersMapper.xml`）を扱う場合:
1. 対応するJavaインターフェースは同じ名前で拡張子が`.java`
2. 配置場所: `src/main/java/com/t0k0sh1/demo/mapper/UsersMapper.java`
3. `<mapper>`タグの`namespace`属性でJavaインターフェースを特定できる

## ファイルマッピング

| Javaインターフェース | XMLマッパー |
|---------------------|------------|
| `src/main/java/com/t0k0sh1/demo/mapper/UsersMapper.java` | `src/main/resources/com/t0k0sh1/demo/mapper/UsersMapper.xml` |

## 関連ファイル

マッパーを修正する際は、以下のファイルも考慮すること:
- **エンティティクラス**: `src/main/java/com/t0k0sh1/demo/bean/entity/users/UserEntity.java`
- **サービスクラス**: `src/main/java/com/t0k0sh1/demo/service/UserService.java`

## 使用例

依頼された場合:
- 「UsersMapperのXMLを探して」→ `src/main/resources/com/t0k0sh1/demo/mapper/UsersMapper.xml`へ移動
- 「UsersMapper.xmlのJavaインターフェースを探して」→ `src/main/java/com/t0k0sh1/demo/mapper/UsersMapper.java`へ移動
- 「UsersMapperに新しいクエリを追加して」→ JavaインターフェースとXMLファイルの両方を更新
