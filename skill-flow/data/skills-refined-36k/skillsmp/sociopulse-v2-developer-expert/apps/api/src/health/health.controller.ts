import { Controller, Get } from '@nestjs/common';
import { ApiOperation, ApiTags } from '@nestjs/swagger';

@ApiTags('health')
@Controller('health')
export class HealthController {
    @Get()
    @ApiOperation({ summary: 'Healthcheck API' })
    health() {
        return {
            status: 'ok',
            timestamp: new Date().toISOString(),
        };
    }
}
