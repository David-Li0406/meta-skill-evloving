---
name: rental-workflow
description: Use this skill when managing the check-in and check-out processes for motorbike rentals, including damage documentation and renter registration.
---

# Rental Workflow

Check-in and check-out business logic for MotoRent.

## Workflow Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Reserved  │────>│   Active    │────>│  Completed  │     │  Cancelled  │
│             │     │             │     │             │     │             │
│ (Booking)   │     │ (Check-In)  │     │ (Check-Out) │     │ (Cancel)    │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

## Check-In Process

### Steps

1. **Select/Register Renter**
   - Search existing renters or register a new renter using OCR.

2. **Select Motorbike**
   - Show only available bikes and display daily rates and deposits.

3. **Choose Add-ons**
   - Offer optional insurance packages and accessories (helmets, phone holders).

4. **Collect Deposit**
   - Accept cash or card pre-authorization and record deposit details.

5. **Capture Before Photos**
   - Take photos of the front, back, and sides to document existing scratches or damage.

6. **Sign Agreement**
   - Display terms and conditions and capture a digital signature.

7. **Confirm & Receipt**
   - Generate a rental record and print or email the receipt.

### Check-In Service

```csharp
// Services/RentalService.cs
public class RentalService
{
    private readonly RentalDataContext m_context;

    public async Task<Rental> CheckInAsync(CheckInRequest request)
    {
        // Validate motorbike availability
        var motorbike = await m_context.LoadOneAsync<Motorbike>(
            m => m.MotorbikeId == request.MotorbikeId);

        if (motorbike is null)
            throw new ValidationException("Motorbike not found");

        if (motorbike.Status != "Available")
            throw new ValidationException("Motorbike is not available");

        // Create rental
        var rental = new Rental
        {
            ShopId = request.ShopId,
            RenterId = request.RenterId,
            MotorbikeId = request.MotorbikeId,
            StartDate = DateTimeOffset.Now,
            ExpectedEndDate = request.ExpectedEndDate,
            MileageStart = motorbike.Mileage,
            DailyRate = motorbike.DailyRate,
            Status = "Active",
            InsuranceId = request.InsuranceId
        };

        // Calculate total
        var days = (rental.ExpectedEndDate - rental.StartDate).Days;
        rental.TotalAmount = days * rental.DailyRate; // Ensure to complete this line
    }
}
```