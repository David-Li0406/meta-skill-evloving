# NestJS Microservices Transport Patterns

## TCP Transport

```typescript
// Microservice
import { NestFactory } from '@nestjs/core';
import { Transport, MicroserviceOptions } from '@nestjs/microservices';

async function bootstrap() {
  const app = await NestFactory.createMicroservice<MicroserviceOptions>(
    AppModule,
    {
      transport: Transport.TCP,
      options: { host: '0.0.0.0', port: 3001 },
    },
  );
  await app.listen();
}

// Handler
@Controller()
export class AppController {
  @MessagePattern({ cmd: 'get_user' })
  getUser(data: { id: string }) {
    return this.userService.findOne(data.id);
  }

  @EventPattern('user_created')
  handleUserCreated(data: User) {
    console.log('User created:', data);
  }
}

// Client
@Injectable()
export class ClientService {
  constructor(
    @Inject('USER_SERVICE') private client: ClientProxy,
  ) {}

  getUser(id: string) {
    return this.client.send({ cmd: 'get_user' }, { id });
  }

  emitUserCreated(user: User) {
    this.client.emit('user_created', user);
  }
}
```

## Redis Transport

```typescript
// Configuration
{
  transport: Transport.REDIS,
  options: {
    host: 'localhost',
    port: 6379,
  },
}

// Module registration
@Module({
  imports: [
    ClientsModule.register([{
      name: 'REDIS_SERVICE',
      transport: Transport.REDIS,
      options: { host: 'localhost', port: 6379 },
    }]),
  ],
})
```

## RabbitMQ Transport

```typescript
// Configuration
{
  transport: Transport.RMQ,
  options: {
    urls: ['amqp://localhost:5672'],
    queue: 'orders_queue',
    queueOptions: { durable: true },
  },
}

// Handler with acknowledgment
@MessagePattern('process_order')
async processOrder(@Payload() data: Order, @Ctx() context: RmqContext) {
  const channel = context.getChannelRef();
  const originalMsg = context.getMessage();

  try {
    await this.orderService.process(data);
    channel.ack(originalMsg);
  } catch (error) {
    channel.nack(originalMsg);
  }
}
```

## Kafka Transport

```typescript
// Configuration
{
  transport: Transport.KAFKA,
  options: {
    client: {
      brokers: ['localhost:9092'],
    },
    consumer: {
      groupId: 'orders-consumer',
    },
  },
}

// Handler
@MessagePattern('orders.created')
handleOrderCreated(@Payload() message: Order, @Ctx() context: KafkaContext) {
  const { offset, partition } = context.getMessage();
  console.log(`Processing offset ${offset} from partition ${partition}`);
  return this.orderService.process(message);
}
```

## gRPC Transport

```typescript
// Configuration
{
  transport: Transport.GRPC,
  options: {
    package: 'hero',
    protoPath: join(__dirname, 'hero.proto'),
    url: 'localhost:5000',
  },
}

// Service implementation
@GrpcMethod('HeroService', 'FindOne')
findOne(data: { id: number }): Hero {
  return this.heroService.findOne(data.id);
}

// Streaming
@GrpcStreamMethod('HeroService', 'FindMany')
findMany(data$: Observable<HeroById>): Observable<Hero> {
  return data$.pipe(
    mergeMap(({ id }) => this.heroService.findOne(id)),
  );
}
```

## Hybrid Application

```typescript
async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // HTTP
  app.connectMicroservice({ transport: Transport.TCP, options: { port: 3001 } });
  app.connectMicroservice({ transport: Transport.REDIS, options: { host: 'localhost' } });

  await app.startAllMicroservices();
  await app.listen(3000);
}
```
