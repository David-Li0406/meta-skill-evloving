# GitLab CI 詳細リファレンス

## 目次
- 基本構文
- ステージとジョブ
- 変数とシークレット
- キャッシュとアーティファクト
- 環境とデプロイ
- ルールと条件

## 基本構文

```yaml
stages:
  - build
  - test
  - deploy

variables:
  NODE_VERSION: "20"

default:
  image: node:${NODE_VERSION}
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/

build:
  stage: build
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 hour

test:
  stage: test
  script:
    - npm test
  coverage: '/Coverage: \d+\.\d+%/'

deploy:
  stage: deploy
  script:
    - ./deploy.sh
  environment:
    name: production
    url: https://example.com
  only:
    - main
```

## 並列実行とマトリックス

```yaml
test:
  stage: test
  parallel:
    matrix:
      - NODE_VERSION: ["18", "20", "22"]
        DATABASE: ["postgres", "mysql"]
  image: node:${NODE_VERSION}
  script:
    - npm test
```

## ルールと条件

```yaml
deploy:
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual
      allow_failure: false
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      when: never
    - when: on_success
```

## 環境とレビューアプリ

```yaml
review:
  stage: deploy
  script:
    - ./deploy-review.sh
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    url: https://$CI_COMMIT_REF_SLUG.example.com
    on_stop: stop_review
    auto_stop_in: 1 week
  rules:
    - if: $CI_MERGE_REQUEST_ID

stop_review:
  stage: deploy
  script:
    - ./teardown-review.sh
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    action: stop
  when: manual
```

## DAGとneeds

```yaml
build_a:
  stage: build
  script: ./build_a.sh

build_b:
  stage: build
  script: ./build_b.sh

test_a:
  stage: test
  needs: [build_a]
  script: ./test_a.sh

deploy:
  stage: deploy
  needs: [test_a, build_b]
  script: ./deploy.sh
```

## インクルードとテンプレート

```yaml
include:
  - local: '/.gitlab/ci/build.yml'
  - template: Security/SAST.gitlab-ci.yml
  - project: 'my-group/my-templates'
    ref: main
    file: '/templates/deploy.yml'
```

## サービスコンテナ

```yaml
test:
  services:
    - postgres:15
    - redis:7
  variables:
    POSTGRES_DB: test
    POSTGRES_USER: test
    POSTGRES_PASSWORD: test
    DATABASE_URL: postgres://test:test@postgres/test
  script:
    - npm test
```
