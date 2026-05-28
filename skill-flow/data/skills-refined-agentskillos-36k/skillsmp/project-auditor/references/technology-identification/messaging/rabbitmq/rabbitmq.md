# RabbitMQ

**Category**: messaging
**Description**: RabbitMQ message broker
**Homepage**: https://www.rabbitmq.com

## Package Detection

### NPM
*RabbitMQ Node.js clients*

- `amqplib`
- `amqp-connection-manager`
- `rascal`

### PYPI
*RabbitMQ Python clients*

- `pika`
- `aio-pika`
- `celery`
- `kombu`

### MAVEN
*RabbitMQ Java clients*

- `com.rabbitmq:amqp-client`
- `org.springframework.amqp:spring-rabbit`

### GO
*RabbitMQ Go clients*

- `github.com/rabbitmq/amqp091-go`
- `github.com/streadway/amqp`

### RUBYGEMS
*RabbitMQ Ruby clients*

- `bunny`
- `sneakers`

### Related Packages
- `amqp`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]amqplib['"]`
- Type: esm_import

**Pattern**: `require\(['"]amqplib['"]\)`
- Type: commonjs_require

**Pattern**: `from\s+['"]amqp-connection-manager['"]`
- Type: esm_import

### Python

**Pattern**: `import\s+pika`
- Type: python_import

**Pattern**: `from\s+pika`
- Type: python_import

**Pattern**: `from\s+aio_pika`
- Type: python_import

**Pattern**: `from\s+kombu`
- Type: python_import

### Go

**Pattern**: `"github\.com/rabbitmq/amqp091-go"`
- Type: go_import

**Pattern**: `"github\.com/streadway/amqp"`
- Type: go_import

### Ruby

**Pattern**: `require\s+['"]bunny['"]`
- Type: ruby_require

## Environment Variables

*RabbitMQ connection URL*

*AMQP connection URL*

*CloudAMQP connection URL*

*RabbitMQ host*

*RabbitMQ port*

*RabbitMQ username*

*RabbitMQ password*

*RabbitMQ virtual host*

*RabbitMQ default username (Docker)*

*RabbitMQ default password (Docker)*


## Detection Notes

- Check for RABBITMQ_URL, AMQP_URL environment variables
- Look for amqp:// connection strings
- Often used with Celery in Python

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
