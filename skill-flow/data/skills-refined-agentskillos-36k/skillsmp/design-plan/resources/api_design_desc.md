# API開発: API仕様設計

API（Application Programming Interface）開発における設計ドキュメントの作成ガイドです。

## 作成する設計ドキュメント

`docs/design/api-specification.md` および OpenAPI仕様ファイルを作成:

- **エンドポイント一覧**: すべてのAPIエンドポイント
- **HTTPメソッド**: GET, POST, PUT, DELETE等
- **パス**: URLパターンとパスパラメータ
- **リクエスト形式**: ヘッダー、ボディ、パラメータ
- **レスポンス形式**: ステータスコード、ボディスキーマ
- **認証・認可**: 認証方法と必要な権限
- **エラーハンドリング**: エラーレスポンスの形式

## 補助ツール（基本: Swagger UI / OpenAPI）

- **Swagger UI / OpenAPI Specification**: RESTful API仕様の定義と可視化（基本）
- **Postman Collections**: API テスト・ドキュメンテーション
- **API Blueprint**: APIドキュメント記述フォーマット
- **GraphQL Playground / GraphiQL**: GraphQL APIの場合
- **Stoplight Studio**: OpenAPIの視覚的エディタ

## OpenAPI仕様ファイル例

`docs/design/openapi.yaml`:

```yaml
openapi: 3.0.0
info:
  title: [API名]
  version: 1.0.0
  description: |
    [API説明]

    ## 認証
    このAPIはJWT Bearer トークンを使用します。

  contact:
    name: API Support
    email: support@example.com

servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server

security:
  - bearerAuth: []

paths:
  /users:
    get:
      summary: ユーザー一覧を取得
      description: 登録されているユーザーの一覧を取得します
      tags:
        - Users
      parameters:
        - name: limit
          in: query
          description: 取得する最大件数
          required: false
          schema:
            type: integer
            default: 10
            minimum: 1
            maximum: 100
        - name: offset
          in: query
          description: スキップする件数
          required: false
          schema:
            type: integer
            default: 0
            minimum: 0
      responses:
        "200":
          description: 成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: "#/components/schemas/User"
                  pagination:
                    $ref: "#/components/schemas/Pagination"
        "401":
          $ref: "#/components/responses/UnauthorizedError"
        "500":
          $ref: "#/components/responses/InternalServerError"

    post:
      summary: ユーザーを作成
      description: 新しいユーザーを作成します
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/UserInput"
            examples:
              example1:
                summary: 基本的なユーザー作成
                value:
                  name: "John Doe"
                  email: "john@example.com"
      responses:
        "201":
          description: 作成成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
        "400":
          $ref: "#/components/responses/BadRequestError"
        "401":
          $ref: "#/components/responses/UnauthorizedError"
        "409":
          description: コンフリクト（すでに存在する）
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
              example:
                error:
                  code: "CONFLICT"
                  message: "User with this email already exists"

  /users/{userId}:
    get:
      summary: ユーザー詳細を取得
      description: 指定されたIDのユーザー情報を取得します
      tags:
        - Users
      parameters:
        - name: userId
          in: path
          required: true
          description: ユーザーID
          schema:
            type: integer
      responses:
        "200":
          description: 成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
        "404":
          $ref: "#/components/responses/NotFoundError"

    put:
      summary: ユーザー情報を更新
      description: 指定されたIDのユーザー情報を更新します
      tags:
        - Users
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/UserInput"
      responses:
        "200":
          description: 更新成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
        "404":
          $ref: "#/components/responses/NotFoundError"

    delete:
      summary: ユーザーを削除
      description: 指定されたIDのユーザーを削除します
      tags:
        - Users
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: integer
      responses:
        "204":
          description: 削除成功
        "404":
          $ref: "#/components/responses/NotFoundError"

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    User:
      type: object
      required:
        - id
        - name
        - email
      properties:
        id:
          type: integer
          description: ユーザーID
          example: 1
        name:
          type: string
          description: ユーザー名
          example: "John Doe"
        email:
          type: string
          format: email
          description: メールアドレス
          example: "john@example.com"
        createdAt:
          type: string
          format: date-time
          description: 作成日時
          example: "2024-01-01T00:00:00Z"
        updatedAt:
          type: string
          format: date-time
          description: 更新日時
          example: "2024-01-01T00:00:00Z"

    UserInput:
      type: object
      required:
        - name
        - email
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
          description: ユーザー名
          example: "John Doe"
        email:
          type: string
          format: email
          description: メールアドレス
          example: "john@example.com"

    Pagination:
      type: object
      properties:
        total:
          type: integer
          description: 全体の件数
          example: 100
        limit:
          type: integer
          description: 1ページあたりの件数
          example: 10
        offset:
          type: integer
          description: スキップした件数
          example: 0

    Error:
      type: object
      required:
        - error
      properties:
        error:
          type: object
          required:
            - code
            - message
          properties:
            code:
              type: string
              description: エラーコード
              example: "VALIDATION_ERROR"
            message:
              type: string
              description: エラーメッセージ
              example: "Invalid input"
            details:
              type: array
              description: 詳細なエラー情報
              items:
                type: object
                properties:
                  field:
                    type: string
                  message:
                    type: string

  responses:
    BadRequestError:
      description: バリデーションエラー
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"
          example:
            error:
              code: "VALIDATION_ERROR"
              message: "Validation failed"
              details:
                - field: "email"
                  message: "Invalid email format"

    UnauthorizedError:
      description: 認証エラー
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"
          example:
            error:
              code: "UNAUTHORIZED"
              message: "Authentication required"

    NotFoundError:
      description: リソースが見つからない
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"
          example:
            error:
              code: "NOT_FOUND"
              message: "Resource not found"

    InternalServerError:
      description: サーバーエラー
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"
          example:
            error:
              code: "INTERNAL_SERVER_ERROR"
              message: "An unexpected error occurred"
```

## Swagger UIのセットアップ

`docs/design/README.md`:

```markdown
# API設計ドキュメント

## Swagger UIでの確認

### 方法1: Prismを使用（モックサーバー付き）

\`\`\`bash

# Prismをインストール

npm install -g @stoplight/prism-cli

# モックサーバーを起動

prism mock openapi.yaml

# ブラウザで http://127.0.0.1:4010 を開く

\`\`\`

### 方法2: Swagger UIをDockerで起動

\`\`\`bash
docker run -p 8080:8080 \
 -e SWAGGER_JSON=/api/openapi.yaml \
 -v $(pwd):/api \
 swaggerapi/swagger-ui

# ブラウザで http://localhost:8080 を開く

\`\`\`

### 方法3: オンラインエディタ

https://editor.swagger.io/ にアクセスして openapi.yaml の内容を貼り付け
```

## API仕様書テンプレート（Markdown版）

`docs/design/api-specification.md`:

```markdown
# API仕様書: [API名]

## 概要

[APIの目的と概要説明]

## ベースURL

- **Production**: `https://api.example.com/v1`
- **Staging**: `https://staging-api.example.com/v1`

## 認証

このAPIは **JWT Bearer Token** 認証を使用します。

### 認証ヘッダー

\`\`\`
Authorization: Bearer <token>
\`\`\`

### トークン取得

\`\`\`bash
POST /auth/login
Content-Type: application/json

{
"email": "user@example.com",
"password": "password"
}
\`\`\`

## エンドポイント一覧

| メソッド | パス            | 説明               | 認証 |
| -------- | --------------- | ------------------ | ---- |
| GET      | /users          | ユーザー一覧を取得 | 必須 |
| POST     | /users          | ユーザーを作成     | 必須 |
| GET      | /users/{userId} | ユーザー詳細を取得 | 必須 |
| PUT      | /users/{userId} | ユーザー情報を更新 | 必須 |
| DELETE   | /users/{userId} | ユーザーを削除     | 必須 |

## エンドポイント詳細

### GET /users

ユーザー一覧を取得します。

#### リクエストパラメータ

| 名前   | 場所  | 型      | 必須 | 説明                               |
| ------ | ----- | ------- | ---- | ---------------------------------- |
| limit  | query | integer | No   | 取得する最大件数（デフォルト: 10） |
| offset | query | integer | No   | スキップする件数（デフォルト: 0）  |

#### レスポンス例

**200 OK**

\`\`\`json
{
"data": [
{
"id": 1,
"name": "John Doe",
"email": "john@example.com",
"createdAt": "2024-01-01T00:00:00Z",
"updatedAt": "2024-01-01T00:00:00Z"
}
],
"pagination": {
"total": 100,
"limit": 10,
"offset": 0
}
}
\`\`\`

**401 Unauthorized**

\`\`\`json
{
"error": {
"code": "UNAUTHORIZED",
"message": "Authentication required"
}
}
\`\`\`

### POST /users

新しいユーザーを作成します。

#### リクエストボディ

\`\`\`json
{
"name": "John Doe",
"email": "john@example.com"
}
\`\`\`

#### レスポンス例

**201 Created**

\`\`\`json
{
"id": 1,
"name": "John Doe",
"email": "john@example.com",
"createdAt": "2024-01-01T00:00:00Z",
"updatedAt": "2024-01-01T00:00:00Z"
}
\`\`\`

**400 Bad Request**

\`\`\`json
{
"error": {
"code": "VALIDATION_ERROR",
"message": "Validation failed",
"details": [
{
"field": "email",
"message": "Invalid email format"
}
]
}
}
\`\`\`

## エラーコード

| コード                | HTTPステータス | 説明                             |
| --------------------- | -------------- | -------------------------------- |
| VALIDATION_ERROR      | 400            | リクエストのバリデーションエラー |
| UNAUTHORIZED          | 401            | 認証が必要                       |
| FORBIDDEN             | 403            | 権限不足                         |
| NOT_FOUND             | 404            | リソースが見つからない           |
| CONFLICT              | 409            | リソースの競合                   |
| INTERNAL_SERVER_ERROR | 500            | サーバー内部エラー               |

## レート制限

- **制限**: 1000リクエスト/時間/ユーザー
- **ヘッダー**:
  - `X-RateLimit-Limit`: 制限値
  - `X-RateLimit-Remaining`: 残り回数
  - `X-RateLimit-Reset`: リセット時刻（UNIX timestamp）

## バージョニング

APIバージョンはURLパスに含めます: `/v1/users`

破壊的変更がある場合は新しいバージョンを作成します: `/v2/users`
```

## GraphQL APIの場合

GraphQL APIの設計では、スキーマ定義を作成します。

`docs/design/schema.graphql`:

```graphql
type Query {
  "ユーザー一覧を取得"
  users(limit: Int = 10, offset: Int = 0): UserConnection!

  "ユーザー詳細を取得"
  user(id: ID!): User
}

type Mutation {
  "ユーザーを作成"
  createUser(input: CreateUserInput!): User!

  "ユーザー情報を更新"
  updateUser(id: ID!, input: UpdateUserInput!): User!

  "ユーザーを削除"
  deleteUser(id: ID!): Boolean!
}

type User {
  id: ID!
  name: String!
  email: String!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

input CreateUserInput {
  name: String!
  email: String!
}

input UpdateUserInput {
  name: String
  email: String
}

scalar DateTime
```

## テスト設計の考慮事項

API のテストで確認すべき項目:

1. **正常系テスト**

   - 各エンドポイントが正しくレスポンスを返す
   - レスポンススキーマが仕様通りである

2. **異常系テスト**

   - バリデーションエラーが適切に返る
   - 認証エラーが適切に処理される
   - 存在しないリソースへのアクセスで404が返る

3. **境界値テスト**

   - ページネーションの境界値
   - リクエストボディの最大サイズ
   - レート制限の動作

4. **セキュリティテスト**
   - 認証なしでアクセスできないことを確認
   - 権限のないリソースにアクセスできないことを確認
   - SQLインジェクション対策

## 設計チェックリスト

- [ ] すべてのエンドポイントが文書化されているか
- [ ] リクエスト/レスポンススキーマが明確か
- [ ] エラーレスポンスが一貫した形式か
- [ ] 認証・認可の仕組みが明確か
- [ ] ページネーションの設計が適切か
- [ ] バージョニング戦略が定義されているか
- [ ] レート制限が考慮されているか
- [ ] CORS設定が文書化されているか
- [ ] HTTPステータスコードが適切に使用されているか
- [ ] RESTful な設計原則に従っているか
