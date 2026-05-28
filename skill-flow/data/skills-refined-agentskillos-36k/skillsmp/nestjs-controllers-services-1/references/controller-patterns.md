# NestJS Controller Patterns

## Basic Controller

```typescript
import { Controller, Get, Post, Body, Param, Query, HttpStatus } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse } from '@nestjs/swagger';

@ApiTags('users')
@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get()
  @ApiOperation({ summary: 'List all users' })
  async findAll(@Query() query: ListUsersDto) {
    return this.usersService.findAll(query);
  }

  @Get(':id')
  @ApiResponse({ status: 200, type: UserResponseDto })
  async findOne(@Param('id', ParseIntPipe) id: number) {
    return this.usersService.findOne(id);
  }

  @Post()
  @HttpCode(HttpStatus.CREATED)
  async create(@Body() createUserDto: CreateUserDto) {
    return this.usersService.create(createUserDto);
  }
}
```

## Request Handling

```typescript
// Path parameters
@Get(':id')
findOne(@Param('id') id: string) {}

// Multiple params
@Get(':userId/posts/:postId')
findPost(@Param('userId') userId: string, @Param('postId') postId: string) {}

// Query parameters
@Get()
findAll(@Query('page') page: number, @Query('limit') limit: number) {}

// Request body
@Post()
create(@Body() dto: CreateDto) {}

// Headers
@Get()
getWithHeader(@Headers('authorization') auth: string) {}

// Full request
@Get()
handleRequest(@Req() request: Request) {}
```

## Response Patterns

```typescript
// Standard response
@Get()
async findAll(): Promise<User[]> {
  return this.usersService.findAll();
}

// Custom status
@Post()
@HttpCode(201)
create() {}

// Redirect
@Get('old-path')
@Redirect('new-path', 301)
redirect() {}

// Custom headers
@Get()
@Header('Cache-Control', 'none')
findAll() {}

// Stream response
@Get('file')
getFile(@Res() res: Response) {
  const file = createReadStream(join(process.cwd(), 'file.txt'));
  file.pipe(res);
}
```

## Validation

```typescript
import { ValidationPipe, UsePipes } from '@nestjs/common';
import { IsString, IsEmail, MinLength } from 'class-validator';

class CreateUserDto {
  @IsString()
  @MinLength(2)
  name: string;

  @IsEmail()
  email: string;
}

@Post()
@UsePipes(new ValidationPipe({ transform: true, whitelist: true }))
create(@Body() dto: CreateUserDto) {}

// Global validation (main.ts)
app.useGlobalPipes(new ValidationPipe({
  whitelist: true,
  forbidNonWhitelisted: true,
  transform: true,
}));
```
