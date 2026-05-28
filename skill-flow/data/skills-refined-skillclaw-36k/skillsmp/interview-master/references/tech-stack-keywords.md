# Technology Stack Keywords Database

This reference file contains keyword patterns for identifying technologies from git commits, file extensions, and code content.

## Programming Languages

### By File Extension
```
.js, .jsx -> JavaScript
.ts, .tsx -> TypeScript
.py -> Python
.java -> Java
.go -> Go/Golang
.rs -> Rust
.rb -> Ruby
.php -> PHP
.cs -> C#
.cpp, .cc, .cxx -> C++
.c, .h -> C
.swift -> Swift
.kt, .kts -> Kotlin
.scala -> Scala
.r, .R -> R
.m -> Objective-C
.dart -> Dart
.lua -> Lua
.pl -> Perl
.sh, .bash -> Shell/Bash
```

### By Content Keywords
```
Python: import, def, class, if __name__
Java: public class, package, import java
JavaScript: const, let, var, function, =>
TypeScript: interface, type, enum, as
Go: package main, func main, import "
Rust: fn main, use std, impl
```

## Frameworks & Libraries

### Frontend
```
react, React, useState, useEffect -> React
vue, Vue, v-if, v-for -> Vue.js
angular, Angular, @Component, ng -> Angular
svelte, Svelte, <script> -> Svelte
next, Next.js, getStaticProps -> Next.js
nuxt, Nuxt.js -> Nuxt.js
gatsby, Gatsby -> Gatsby
```

### Backend
```
express, Express, app.listen -> Express.js
fastapi, FastAPI, @app.get -> FastAPI
django, Django, models.Model -> Django
flask, Flask, @app.route -> Flask
spring, Spring, @SpringBootApplication -> Spring Boot
gin, gin-gonic -> Gin (Go)
actix, actix-web -> Actix (Rust)
rails, Ruby on Rails, ActiveRecord -> Rails
laravel, Laravel, Eloquent -> Laravel
nest, NestJS, @Module -> NestJS
```

### Mobile
```
react-native, React Native -> React Native
flutter, Flutter, Widget -> Flutter
swift, SwiftUI, UIKit -> iOS Native
kotlin, Android, Activity -> Android Native
ionic, Ionic -> Ionic
xamarin, Xamarin -> Xamarin
```

## Databases

### SQL Databases
```
mysql, MySQL, mysqli -> MySQL
postgres, postgresql, psycopg2, pg -> PostgreSQL
sqlite, sqlite3 -> SQLite
mssql, SQL Server, TSQL -> Microsoft SQL Server
oracle, Oracle Database -> Oracle
mariadb, MariaDB -> MariaDB
```

### NoSQL Databases
```
mongodb, mongo, mongoose -> MongoDB
redis, Redis -> Redis
cassandra, Cassandra -> Cassandra
dynamodb, DynamoDB -> DynamoDB
couchdb, CouchDB -> CouchDB
firebase, Firestore -> Firebase/Firestore
elasticsearch, Elasticsearch -> Elasticsearch
```

## DevOps & Infrastructure

### Containerization
```
docker, Dockerfile, docker-compose -> Docker
kubernetes, kubectl, k8s, pod, deployment -> Kubernetes
podman, Podman -> Podman
```

### CI/CD
```
jenkins, Jenkinsfile -> Jenkins
gitlab-ci, .gitlab-ci.yml -> GitLab CI
github actions, .github/workflows -> GitHub Actions
circleci, .circleci -> CircleCI
travis, .travis.yml -> Travis CI
azure pipelines, azure-pipelines.yml -> Azure Pipelines
```

### Cloud Platforms
```
aws, AWS, s3, lambda, ec2 -> AWS (Amazon Web Services)
azure, Azure, az -> Microsoft Azure
gcp, google cloud, gcloud -> Google Cloud Platform
heroku, Heroku -> Heroku
vercel, Vercel -> Vercel
netlify, Netlify -> Netlify
digitalocean, DigitalOcean -> DigitalOcean
```

### Infrastructure as Code
```
terraform, Terraform, .tf -> Terraform
ansible, Ansible, playbook -> Ansible
pulumi, Pulumi -> Pulumi
cloudformation, CloudFormation -> AWS CloudFormation
```

## Testing Frameworks

```
jest, Jest, describe, it -> Jest
pytest, pytest, test_ -> Pytest
junit, JUnit, @Test -> JUnit
mocha, Mocha, describe -> Mocha
chai, Chai, expect -> Chai
cypress, Cypress, cy. -> Cypress
selenium, Selenium, WebDriver -> Selenium
testing-library, @testing-library -> Testing Library
vitest, Vitest -> Vitest
```

## Build Tools & Package Managers

```
webpack, Webpack, webpack.config -> Webpack
vite, Vite, vite.config -> Vite
parcel, Parcel -> Parcel
rollup, Rollup -> Rollup
npm, package.json -> NPM
yarn, yarn.lock -> Yarn
pnpm, pnpm-lock.yaml -> PNPM
pip, requirements.txt -> Pip
poetry, pyproject.toml, poetry.lock -> Poetry
maven, pom.xml -> Maven
gradle, build.gradle -> Gradle
cargo, Cargo.toml -> Cargo (Rust)
```

## Version Control & Collaboration

```
git, .gitignore, .git/ -> Git
github, GitHub -> GitHub
gitlab, GitLab -> GitLab
bitbucket, Bitbucket -> Bitbucket
```

## API & Data Formats

```
rest, RESTful, REST API -> REST API
graphql, GraphQL, gql -> GraphQL
grpc, gRPC, protobuf -> gRPC
json, JSON.parse, JSON.stringify -> JSON
xml, XML -> XML
yaml, YAML, .yml -> YAML
protobuf, Protocol Buffers, .proto -> Protocol Buffers
```

## State Management

```
redux, Redux, createStore -> Redux
mobx, MobX, observable -> MobX
zustand, Zustand -> Zustand
recoil, Recoil -> Recoil
vuex, Vuex, store -> Vuex
pinia, Pinia -> Pinia
context, React Context, createContext -> React Context
```

## Authentication & Security

```
jwt, JWT, jsonwebtoken -> JWT (JSON Web Tokens)
oauth, OAuth, oauth2 -> OAuth
passport, Passport.js -> Passport.js
auth0, Auth0 -> Auth0
keycloak, Keycloak -> Keycloak
bcrypt, bcrypt -> Bcrypt
helmet, Helmet -> Helmet.js
```

## CSS & Styling

```
css, .css, style.css -> CSS
sass, scss, .scss -> Sass/SCSS
less, .less -> Less
tailwind, Tailwind CSS, @apply -> Tailwind CSS
bootstrap, Bootstrap, .container -> Bootstrap
material-ui, MUI, @mui -> Material-UI
styled-components, styled-components -> Styled Components
emotion, @emotion -> Emotion
css-modules, .module.css -> CSS Modules
```

## Monitoring & Logging

```
sentry, Sentry -> Sentry
datadog, Datadog -> Datadog
newrelic, New Relic -> New Relic
prometheus, Prometheus -> Prometheus
grafana, Grafana -> Grafana
logstash, Logstash -> Logstash
winston, Winston -> Winston
pino, Pino -> Pino
```

## Message Queues & Streaming

```
kafka, Kafka, kafka-python -> Apache Kafka
rabbitmq, RabbitMQ -> RabbitMQ
redis, Redis Queue, rq -> Redis Queue
celery, Celery -> Celery
activemq, ActiveMQ -> ActiveMQ
aws sqs, SQS -> AWS SQS
```

## Detection Strategy

When analyzing git commits and code:

1. **File Extension Scan**: Check all modified files for language identification
2. **Package File Analysis**: Parse package.json, requirements.txt, pom.xml, etc.
3. **Import Statement Scan**: Analyze import/require statements in code
4. **Configuration File Detection**: Identify Docker, CI/CD, IaC files
5. **Keyword Frequency**: Count keyword occurrences across commits
6. **Commit Message Mining**: Extract technology mentions from commit messages

## Scoring Logic

Assign confidence scores based on:
- **High Confidence (0.9-1.0)**: Package file dependency, file extension match
- **Medium Confidence (0.6-0.8)**: Import statements, config files
- **Low Confidence (0.3-0.5)**: Commit message mentions, comments

## Output Format

```json
{
  "languages": [
    {"name": "TypeScript", "confidence": 0.95, "file_count": 47},
    {"name": "Python", "confidence": 0.80, "file_count": 12}
  ],
  "frameworks": [
    {"name": "React", "confidence": 0.98, "evidence": ["package.json", "47 .tsx files"]},
    {"name": "FastAPI", "confidence": 0.85, "evidence": ["requirements.txt", "app/main.py"]}
  ],
  "tools": [
    {"name": "Docker", "confidence": 1.0, "evidence": ["Dockerfile", "docker-compose.yml"]},
    {"name": "GitHub Actions", "confidence": 1.0, "evidence": [".github/workflows/ci.yml"]}
  ]
}
```

## Notes

- Update this keyword database regularly as new technologies emerge
- For ambiguous cases (e.g., "model" could be Django or ML), check context
- Consider commit timestamps to identify primary vs. legacy tech stack
- Weight recent commits higher for active skills vs. historical experience
