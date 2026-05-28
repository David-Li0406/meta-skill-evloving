import { Module } from '@nestjs/common';
import { PrismaModule } from '../common/prisma/prisma.module';
import { AuthModule } from '../auth/auth.module';
import { ContractsController } from './contracts.controller';
import { ContractsService } from './contracts.service';

@Module({
    imports: [PrismaModule, AuthModule],
    controllers: [ContractsController],
    providers: [ContractsService],
})
export class ContractsModule { }
