import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { PaymentsController } from './payments.controller';
import { PaymentsService } from './payments.service';
import { AuthModule } from '../auth/auth.module';
import { RolesGuard } from '../common/guards';

@Module({
    imports: [AuthModule, ConfigModule],
    controllers: [PaymentsController],
    providers: [PaymentsService, RolesGuard],
    exports: [PaymentsService],
})
export class PaymentsModule { }
