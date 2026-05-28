import { Module } from '@nestjs/common';
import { VideoBookingController } from './video-booking.controller';
import { VideoBookingService } from './video-booking.service';
import { AuthModule } from '../auth/auth.module';
import { PrismaModule } from '../common/prisma/prisma.module';

@Module({
    imports: [AuthModule, PrismaModule],
    controllers: [VideoBookingController],
    providers: [VideoBookingService],
    exports: [VideoBookingService],
})
export class VideoBookingModule { }
