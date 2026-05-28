name: rental-workflow
description: Business logic and workflow for motorbike check-in and check-out processes, including damage documentation.
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
   - Search existing renters
   - Or register new renter with OCR

2. **Select Motorbike**
   - Show available bikes only
   - Display daily rate, deposit

3. **Choose Add-ons**
   - Insurance package (optional)
   - Accessories (helmets, phone holders)

4. **Collect Deposit**
   - Cash or card pre-authorization
   - Record deposit details

5. **Capture Before Photos**
   - Front, back, sides
   - Document existing scratches/damage

6. **Sign Agreement**
   - Display terms and conditions
   - Capture digital signature

7. **Confirm & Receipt**
   - Generate rental record
   - Print/email receipt

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
        rental.TotalAmount = days * rental.DailyRate;

        // Add insurance if selected
        if (request.InsuranceId.HasValue)
        {
            var insurance = await m_context.LoadOneAsync<Insurance>(
                i => i.InsuranceId == request.InsuranceId);
            rental.TotalAmount += days * insurance!.DailyRate;
        }

        // Create deposit
        var deposit = new Deposit
        {
            DepositType = request.DepositType,
            Amount = request.DepositAmount,
            Status = "Held",
            CollectedOn = DateTimeOffset.Now,
            CardLast4 = request.CardLast4,
            TransactionRef = request.TransactionRef
        };

        // Update motorbike status
        motorbike.Status = "Rented";

        // Save all
        using var session = m_context.OpenSession();
        session.Attach(rental);
        session.Attach(deposit);
        session.Attach(motorbike);
        await session.SubmitChanges("CheckIn");

        // Link deposit to rental
        rental.DepositId = deposit.DepositId;
        session.Attach(rental);
        await session.SubmitChanges("LinkDeposit");

        return rental;
    }
}
```

### CheckInRequest Model

```csharp
public class CheckInRequest
{
    public int ShopId { get; set; }
    public int RenterId { get; set; }
    public int MotorbikeId { get; set; }
    public DateTimeOffset ExpectedEndDate { get; set; }
    public int? InsuranceId { get; set; }
    public List<int> AccessoryIds { get; set; } = [];

    // Deposit
    public string DepositType { get; set; } = "Cash";  // Cash, CardPreAuth
    public decimal DepositAmount { get; set; }
    public string? CardLast4 { get; set; }
    public string? TransactionRef { get; set; }
}
```

## Check-Out Process

### Steps

1. **Find Active Rental**
   - Search by renter or motorbike

2. **Record Return**
   - Enter end mileage
   - Note return time

3. **Capture After Photos**
   - Same angles as before
   - Document any new damage

4. **Damage Assessment**
   - Compare before/after photos
   - Document any damage
   - Estimate repair cost

5. **Calculate Final Charges**
   - Rental days (actual)
   - Extra days if overdue
   - Damage charges
   - Less insurance coverage

6. **Process Payment**
   - Collect balance due
   - Or refund overpayment

7. **Refund Deposit**
   - Full if no damage
   - Partial if damage deducted

8. **Complete Rental**
   - Update status
   - Generate receipt

### Check-Out Service

```csharp
public async Task<CheckOutResult> CheckOutAsync(CheckOutRequest request)
{
    var rental = await m_context.LoadOneAsync<Rental>(
        r => r.RentalId == request.RentalId);

    if (rental is null)
        throw new ValidationException("Rental not found");

    if (rental.Status != "Active")
        throw new ValidationException("Rental is not active");

    var motorbike = await m_context.LoadOneAsync<Motorbike>(
        m => m.MotorbikeId == rental.MotorbikeId);

    // Calculate actual rental period
    rental.ActualEndDate = DateTimeOffset.Now;
    rental.MileageEnd = request.MileageEnd;

    var actualDays = Math.Ceiling((rental.ActualEndDate.Value - rental.StartDate).TotalDays);
    var rentalAmount = (decimal)actualDays * rental.DailyRate;

    // Add insurance if applicable
    decimal insuranceAmount = 0;
    if (rental.InsuranceId.HasValue)
    {
        var insurance = await m_context.LoadOneAsync<Insurance>(
            i => i.InsuranceId == rental.InsuranceId);
        insuranceAmount = (decimal)actualDays * insurance!.DailyRate;
    }

    // Calculate damage charges
    decimal damageAmount = request.DamageCharges;

    // Calculate insurance coverage
    decimal insuranceCoverage = 0;
    if (rental.InsuranceId.HasValue && damageAmount > 0)
    {
        var insurance = await m_context.LoadOneAsync<Insurance>(
            i => i.InsuranceId == rental.InsuranceId);
        insuranceCoverage = Math.Min(damageAmount - insurance!.Deductible, insurance.MaxCoverage);
        insuranceCoverage = Math.Max(0, insuranceCoverage);
    }

    // Final calculation
    var totalCharges = rentalAmount + insuranceAmount + damageAmount - insuranceCoverage;
    var deposit = await m_context.LoadOneAsync<Deposit>(d => d.DepositId == rental.DepositId);
    var depositAmount = deposit?.Amount ?? 0;

    var balanceDue = totalCharges - depositAmount;

    // Update entities
    rental.TotalAmount = totalCharges;
    rental.Status = "Completed";

    motorbike!.Status = "Available";
    motorbike.Mileage = request.MileageEnd;

    if (deposit is not null)
    {
        deposit.Status = damageAmount > 0 ? "Forfeited" : "Refunded";
        deposit.RefundedOn = DateTimeOffset.Now;
    }

    // Save
    using var session = m_context.OpenSession();
    session.Attach(rental);
    session.Attach(motorbike);
    if (deposit is not null)
        session.Attach(deposit);
    await session.SubmitChanges("CheckOut");

    return new CheckOutResult
    {
        RentalDays = (int)actualDays,
        RentalAmount = rentalAmount,
        InsuranceAmount = insuranceAmount,
        DamageAmount = damageAmount,
        InsuranceCoverage = insuranceCoverage,
        TotalCharges = totalCharges,
        DepositAmount = depositAmount,
        BalanceDue = balanceDue
    };
}
```

## Damage Documentation

```csharp
public async Task<DamageReport> RecordDamageAsync(DamageRequest request)
{
    var damage = new DamageReport
    {
        RentalId = request.RentalId,
        MotorbikeId = request.MotorbikeId,
        Description = request.Description,
        Severity = request.Severity,  // Minor, Moderate, Major
        EstimatedCost = request.EstimatedCost,
        Status = "Pending",
        ReportedOn = DateTimeOffset.Now
    };

    using var session = m_context.OpenSession();
    session.Attach(damage);
    await session.SubmitChanges("RecordDamage");

    // Save photos
    foreach (var photo in request.Photos)
    {
        var damagePhoto = new DamagePhoto
        {
            DamageReportId = damage.DamageReportId,
            PhotoType = photo.Type,  // Before, After
            ImagePath = await SavePhotoAsync(photo.Stream),
            CapturedOn = DateTimeOffset.Now
        };
        session.Attach(damagePhoto);
    }
    await session.SubmitChanges("SaveDamagePhotos");

    return damage;
}
```

## Stepper UI Pattern

```razor
<MudStepper @ref="m_stepper" Linear="true">
    <MudStep Title="Select Renter" Icon="@Icons.Material.Filled.Person">
        <RenterSelector @bind-SelectedRenterId="m_renterId" />
    </MudStep>

    <MudStep Title="Select Bike" Icon="@Icons.Material.Filled.TwoWheeler">
        <MotorbikeSelector @bind-SelectedMotorbikeId="m_motorbikeId" ShopId="m_shopId" />
    </MudStep>

    <MudStep Title="Add-ons" Icon="@Icons.Material.Filled.AddCircle">
        <InsuranceSelector @bind-SelectedInsuranceId="m_insuranceId" />
        <AccessorySelector @bind-SelectedAccessoryIds="m_accessoryIds" />
    </MudStep>

    <MudStep Title="Deposit" Icon="@Icons.Material.Filled.Payment">
        <DepositForm @bind-DepositType="m_depositType" @bind-Amount="m_depositAmount" />
    </MudStep>

    <MudStep Title="Photos" Icon="@Icons.Material.Filled.CameraAlt">
        <BeforePhotoCapture MotorbikeId="m_motorbikeId" @bind-Photos="m_beforePhotos" />
    </MudStep>

    <MudStep Title="Agreement" Icon="@Icons.Material.Filled.Description">
        <AgreementSignature ShopId="m_shopId" @bind-SignaturePath="m_signaturePath" />
    </MudStep>

    <MudStep Title="Confirm" Icon="@Icons.Material.Filled.Check">
        <CheckInSummary Request="BuildRequest()" />
        <MudButton Variant="Variant.Filled" Color="Color.Primary" OnClick="CompleteCheckIn">
            Complete Check-In
        </MudButton>
    </MudStep>
</MudStepper>
```

## Source
- Business logic from: MotoRent requirements
