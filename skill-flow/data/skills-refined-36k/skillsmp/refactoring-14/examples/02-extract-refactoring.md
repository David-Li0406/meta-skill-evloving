# Extract Method and Extract Class Refactoring

Practical examples of extract method and extract class refactoring techniques.

## 📝 Prompt

```
Show me extract method and extract class refactoring examples:

Context:
- E-commerce order processing code
- Payment handling logic
- Complex business rules
- Need to improve readability and testability

Include:
- Extract Method examples (5+ scenarios)
- Extract Class examples (3+ scenarios)
- Before and after code
- When to apply each technique
- Testing improvements
```

## 🔧 Extract Method Refactoring

### Example 1: Extract Complex Conditional

🔴 **Before:**
```typescript
class OrderProcessor {
    processOrder(order: Order): boolean {
        // Complex conditional buried in method
        if (order.total > 0 && 
            order.items.length > 0 && 
            order.status === 'pending' &&
            order.paymentMethod !== null &&
            order.shippingAddress !== null &&
            (order.customer.verified || order.total < 100)) {
            
            // Process order
            return true;
        }
        return false;
    }
}
```

🟢 **After:**
```typescript
class OrderProcessor {
    processOrder(order: Order): boolean {
        if (this.isOrderValid(order)) {
            // Process order
            return true;
        }
        return false;
    }
    
    private isOrderValid(order: Order): boolean {
        return this.hasValidAmount(order) &&
               this.hasItems(order) &&
               this.isPending(order) &&
               this.hasPaymentMethod(order) &&
               this.hasShippingAddress(order) &&
               this.isCustomerEligible(order);
    }
    
    private hasValidAmount(order: Order): boolean {
        return order.total > 0;
    }
    
    private hasItems(order: Order): boolean {
        return order.items.length > 0;
    }
    
    private isPending(order: Order): boolean {
        return order.status === 'pending';
    }
    
    private hasPaymentMethod(order: Order): boolean {
        return order.paymentMethod !== null;
    }
    
    private hasShippingAddress(order: Order): boolean {
        return order.shippingAddress !== null;
    }
    
    private isCustomerEligible(order: Order): boolean {
        return order.customer.verified || order.total < 100;
    }
}
```

**Benefits:**
- ✅ Self-documenting code
- ✅ Each condition can be tested independently
- ✅ Easy to modify validation rules
- ✅ Reusable validation methods

---

### Example 2: Extract Calculation Logic

🔴 **Before:**
```typescript
class OrderCalculator {
    calculateTotal(order: Order): number {
        let subtotal = 0;
        for (const item of order.items) {
            subtotal += item.price * item.quantity;
        }
        
        let discount = 0;
        if (order.customer.isPremium) {
            discount = subtotal * 0.10;
        } else if (order.items.length > 5) {
            discount = subtotal * 0.05;
        }
        
        let tax = (subtotal - discount) * 0.08;
        
        let shipping = 0;
        if (subtotal < 50) {
            shipping = 9.99;
        } else if (subtotal < 100) {
            shipping = 4.99;
        }
        
        return subtotal - discount + tax + shipping;
    }
}
```

🟢 **After:**
```typescript
class OrderCalculator {
    calculateTotal(order: Order): number {
        const subtotal = this.calculateSubtotal(order);
        const discount = this.calculateDiscount(order, subtotal);
        const tax = this.calculateTax(subtotal, discount);
        const shipping = this.calculateShipping(subtotal);
        
        return subtotal - discount + tax + shipping;
    }
    
    private calculateSubtotal(order: Order): number {
        return order.items.reduce(
            (sum, item) => sum + (item.price * item.quantity),
            0
        );
    }
    
    private calculateDiscount(order: Order, subtotal: number): number {
        if (order.customer.isPremium) {
            return subtotal * 0.10;
        }
        if (order.items.length > 5) {
            return subtotal * 0.05;
        }
        return 0;
    }
    
    private calculateTax(subtotal: number, discount: number): number {
        const taxableAmount = subtotal - discount;
        return taxableAmount * 0.08;
    }
    
    private calculateShipping(subtotal: number): number {
        if (subtotal >= 100) return 0;
        if (subtotal >= 50) return 4.99;
        return 9.99;
    }
}
```

---

### Example 3: Extract API Call Logic

🔴 **Before:**
```typescript
class PaymentService {
    async processPayment(order: Order): Promise<boolean> {
        try {
            const response = await fetch('https://api.stripe.com/v1/charges', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${process.env.STRIPE_KEY}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    amount: order.total * 100,
                    currency: 'usd',
                    source: order.paymentMethod.token,
                    description: `Order ${order.id}`
                })
            });
            
            if (!response.ok) {
                const error = await response.json();
                console.error('Payment failed:', error);
                return false;
            }
            
            const result = await response.json();
            order.paymentId = result.id;
            order.status = 'paid';
            
            return true;
        } catch (error) {
            console.error('Payment error:', error);
            return false;
        }
    }
}
```

🟢 **After:**
```typescript
class PaymentService {
    async processPayment(order: Order): Promise<boolean> {
        try {
            const charge = await this.createStripeCharge(order);
            this.updateOrderWithPayment(order, charge);
            return true;
        } catch (error) {
            this.handlePaymentError(error);
            return false;
        }
    }
    
    private async createStripeCharge(order: Order): Promise<StripeCharge> {
        const response = await fetch('https://api.stripe.com/v1/charges', {
            method: 'POST',
            headers: this.getStripeHeaders(),
            body: JSON.stringify(this.buildChargeRequest(order))
        });
        
        if (!response.ok) {
            throw new PaymentError(await response.json());
        }
        
        return response.json();
    }
    
    private getStripeHeaders(): Record<string, string> {
        return {
            'Authorization': `Bearer ${process.env.STRIPE_KEY}`,
            'Content-Type': 'application/json'
        };
    }
    
    private buildChargeRequest(order: Order): object {
        return {
            amount: this.convertToStripeAmount(order.total),
            currency: 'usd',
            source: order.paymentMethod.token,
            description: this.buildChargeDescription(order)
        };
    }
    
    private convertToStripeAmount(amount: number): number {
        return amount * 100; // Convert to cents
    }
    
    private buildChargeDescription(order: Order): string {
        return `Order ${order.id}`;
    }
    
    private updateOrderWithPayment(order: Order, charge: StripeCharge): void {
        order.paymentId = charge.id;
        order.status = 'paid';
    }
    
    private handlePaymentError(error: Error): void {
        console.error('Payment error:', error);
        // Could also log to monitoring service, send alerts, etc.
    }
}
```

---

## 📦 Extract Class Refactoring

### Example 1: Extract Order Validator

🔴 **Before:**
```typescript
class Order {
    id: string;
    items: OrderItem[];
    customer: Customer;
    total: number;
    shippingAddress: Address;
    paymentMethod: PaymentMethod;
    status: string;
    
    // Too many validation responsibilities in Order class
    validateOrder(): ValidationResult {
        const errors: string[] = [];
        
        if (!this.items || this.items.length === 0) {
            errors.push('Order must have at least one item');
        }
        
        for (const item of this.items) {
            if (item.quantity <= 0) {
                errors.push(`Invalid quantity for item ${item.id}`);
            }
            if (item.price < 0) {
                errors.push(`Invalid price for item ${item.id}`);
            }
        }
        
        if (!this.customer) {
            errors.push('Customer is required');
        }
        
        if (!this.shippingAddress) {
            errors.push('Shipping address is required');
        } else {
            if (!this.shippingAddress.street) {
                errors.push('Street address is required');
            }
            if (!this.shippingAddress.city) {
                errors.push('City is required');
            }
            if (!this.shippingAddress.postalCode) {
                errors.push('Postal code is required');
            }
        }
        
        if (!this.paymentMethod) {
            errors.push('Payment method is required');
        }
        
        if (this.total <= 0) {
            errors.push('Order total must be greater than zero');
        }
        
        return {
            isValid: errors.length === 0,
            errors
        };
    }
}
```

🟢 **After:**
```typescript
// Extracted validator class
class OrderValidator {
    validate(order: Order): ValidationResult {
        const errors: string[] = [];
        
        this.validateItems(order.items, errors);
        this.validateCustomer(order.customer, errors);
        this.validateShippingAddress(order.shippingAddress, errors);
        this.validatePaymentMethod(order.paymentMethod, errors);
        this.validateTotal(order.total, errors);
        
        return {
            isValid: errors.length === 0,
            errors
        };
    }
    
    private validateItems(items: OrderItem[], errors: string[]): void {
        if (!items || items.length === 0) {
            errors.push('Order must have at least one item');
            return;
        }
        
        items.forEach(item => {
            if (item.quantity <= 0) {
                errors.push(`Invalid quantity for item ${item.id}`);
            }
            if (item.price < 0) {
                errors.push(`Invalid price for item ${item.id}`);
            }
        });
    }
    
    private validateCustomer(customer: Customer, errors: string[]): void {
        if (!customer) {
            errors.push('Customer is required');
        }
    }
    
    private validateShippingAddress(address: Address, errors: string[]): void {
        if (!address) {
            errors.push('Shipping address is required');
            return;
        }
        
        if (!address.street) errors.push('Street address is required');
        if (!address.city) errors.push('City is required');
        if (!address.postalCode) errors.push('Postal code is required');
    }
    
    private validatePaymentMethod(paymentMethod: PaymentMethod, errors: string[]): void {
        if (!paymentMethod) {
            errors.push('Payment method is required');
        }
    }
    
    private validateTotal(total: number, errors: string[]): void {
        if (total <= 0) {
            errors.push('Order total must be greater than zero');
        }
    }
}

// Simplified Order class
class Order {
    id: string;
    items: OrderItem[];
    customer: Customer;
    total: number;
    shippingAddress: Address;
    paymentMethod: PaymentMethod;
    status: string;
    
    validate(): ValidationResult {
        const validator = new OrderValidator();
        return validator.validate(this);
    }
}
```

---

### Example 2: Extract Price Calculator

🔴 **Before:**
```typescript
class Product {
    id: string;
    name: string;
    basePrice: number;
    category: string;
    discounts: Discount[];
    taxRate: number;
    
    // Pricing logic mixed with product data
    calculateFinalPrice(quantity: number, customer: Customer): number {
        let price = this.basePrice * quantity;
        
        // Apply volume discount
        if (quantity >= 10) {
            price *= 0.9; // 10% off
        } else if (quantity >= 5) {
            price *= 0.95; // 5% off
        }
        
        // Apply customer discount
        if (customer.isPremium) {
            price *= 0.85; // 15% off for premium
        }
        
        // Apply category discount
        if (this.category === 'electronics') {
            price *= 0.90; // 10% off electronics
        }
        
        // Apply promotional discounts
        for (const discount of this.discounts) {
            if (this.isDiscountApplicable(discount)) {
                price -= (price * discount.percentage / 100);
            }
        }
        
        // Add tax
        price += (price * this.taxRate);
        
        return Math.round(price * 100) / 100;
    }
    
    private isDiscountApplicable(discount: Discount): boolean {
        const now = new Date();
        return now >= discount.startDate && now <= discount.endDate;
    }
}
```

🟢 **After:**
```typescript
// Extracted pricing calculator
class PriceCalculator {
    calculateFinalPrice(
        product: Product,
        quantity: number,
        customer: Customer
    ): Money {
        let price = this.calculateBasePrice(product, quantity);
        price = this.applyDiscounts(price, product, quantity, customer);
        price = this.applyTax(price, product.taxRate);
        
        return new Money(price);
    }
    
    private calculateBasePrice(product: Product, quantity: number): number {
        return product.basePrice * quantity;
    }
    
    private applyDiscounts(
        price: number,
        product: Product,
        quantity: number,
        customer: Customer
    ): number {
        price = this.applyVolumeDiscount(price, quantity);
        price = this.applyCustomerDiscount(price, customer);
        price = this.applyCategoryDiscount(price, product.category);
        price = this.applyPromotionalDiscounts(price, product.discounts);
        
        return price;
    }
    
    private applyVolumeDiscount(price: number, quantity: number): number {
        if (quantity >= 10) return price * 0.9;
        if (quantity >= 5) return price * 0.95;
        return price;
    }
    
    private applyCustomerDiscount(price: number, customer: Customer): number {
        return customer.isPremium ? price * 0.85 : price;
    }
    
    private applyCategoryDiscount(price: number, category: string): number {
        return category === 'electronics' ? price * 0.90 : price;
    }
    
    private applyPromotionalDiscounts(price: number, discounts: Discount[]): number {
        const applicableDiscounts = discounts.filter(d => this.isActive(d));
        
        for (const discount of applicableDiscounts) {
            price -= (price * discount.percentage / 100);
        }
        
        return price;
    }
    
    private isActive(discount: Discount): boolean {
        const now = new Date();
        return now >= discount.startDate && now <= discount.endDate;
    }
    
    private applyTax(price: number, taxRate: number): number {
        return price + (price * taxRate);
    }
}

// Money value object
class Money {
    private readonly amount: number;
    
    constructor(amount: number) {
        this.amount = Math.round(amount * 100) / 100;
    }
    
    toNumber(): number {
        return this.amount;
    }
    
    toString(): string {
        return `$${this.amount.toFixed(2)}`;
    }
}

// Simplified Product class
class Product {
    id: string;
    name: string;
    basePrice: number;
    category: string;
    discounts: Discount[];
    taxRate: number;
    
    calculateFinalPrice(quantity: number, customer: Customer): Money {
        const calculator = new PriceCalculator();
        return calculator.calculateFinalPrice(this, quantity, customer);
    }
}
```

---

### Example 3: Extract Email Builder

🔴 **Before:**
```typescript
class NotificationService {
    async sendOrderConfirmation(order: Order): Promise<void> {
        // Email building logic mixed with sending logic
        let html = '<html><body>';
        html += '<h1>Order Confirmation</h1>';
        html += `<p>Thank you for your order, ${order.customer.name}!</p>`;
        html += `<p>Order #: ${order.id}</p>`;
        html += '<h2>Order Details:</h2>';
        html += '<table>';
        
        for (const item of order.items) {
            html += '<tr>';
            html += `<td>${item.name}</td>`;
            html += `<td>${item.quantity}</td>`;
            html += `<td>$${item.price.toFixed(2)}</td>`;
            html += '</tr>';
        }
        
        html += '</table>';
        html += `<p><strong>Total: $${order.total.toFixed(2)}</strong></p>`;
        html += '<p>Your order will be shipped to:</p>';
        html += `<p>${order.shippingAddress.street}<br>`;
        html += `${order.shippingAddress.city}, ${order.shippingAddress.state} ${order.shippingAddress.postalCode}</p>`;
        html += '</body></html>';
        
        await this.emailService.send({
            to: order.customer.email,
            subject: `Order Confirmation - ${order.id}`,
            html
        });
    }
}
```

🟢 **After:**
```typescript
// Extracted email builder
class OrderConfirmationEmailBuilder {
    build(order: Order): Email {
        return new Email(
            order.customer.email,
            this.buildSubject(order),
            this.buildHtml(order)
        );
    }
    
    private buildSubject(order: Order): string {
        return `Order Confirmation - ${order.id}`;
    }
    
    private buildHtml(order: Order): string {
        return `
            <!DOCTYPE html>
            <html>
            <body>
                ${this.buildHeader(order)}
                ${this.buildOrderDetails(order)}
                ${this.buildShippingInfo(order)}
            </body>
            </html>
        `;
    }
    
    private buildHeader(order: Order): string {
        return `
            <h1>Order Confirmation</h1>
            <p>Thank you for your order, ${order.customer.name}!</p>
            <p>Order #: ${order.id}</p>
        `;
    }
    
    private buildOrderDetails(order: Order): string {
        return `
            <h2>Order Details:</h2>
            <table>
                ${order.items.map(item => this.buildItemRow(item)).join('')}
            </table>
            <p><strong>Total: ${this.formatMoney(order.total)}</strong></p>
        `;
    }
    
    private buildItemRow(item: OrderItem): string {
        return `
            <tr>
                <td>${item.name}</td>
                <td>${item.quantity}</td>
                <td>${this.formatMoney(item.price)}</td>
            </tr>
        `;
    }
    
    private buildShippingInfo(order: Order): string {
        return `
            <p>Your order will be shipped to:</p>
            <p>
                ${order.shippingAddress.street}<br>
                ${order.shippingAddress.city}, ${order.shippingAddress.state} ${order.shippingAddress.postalCode}
            </p>
        `;
    }
    
    private formatMoney(amount: number): string {
        return `$${amount.toFixed(2)}`;
    }
}

// Simplified notification service
class NotificationService {
    constructor(
        private emailService: EmailService,
        private emailBuilder: OrderConfirmationEmailBuilder
    ) {}
    
    async sendOrderConfirmation(order: Order): Promise<void> {
        const email = this.emailBuilder.build(order);
        await this.emailService.send(email);
    }
}
```

---

## 🎯 When to Use Each Technique

### Extract Method
**Use when:**
- Method is too long (>20 lines)
- Complex conditional logic
- Repeated code blocks
- Comments explaining code sections
- Multiple levels of abstraction

**Benefits:**
- Improved readability
- Easier testing
- Code reuse
- Self-documenting

### Extract Class
**Use when:**
- Class has too many responsibilities
- Group of methods/fields always used together
- Class is difficult to understand
- Changes affect unrelated parts

**Benefits:**
- Single Responsibility Principle
- Better organization
- Easier to test
- Reduced coupling

## 💡 Best Practices

1. **Name Methods Clearly**: Use descriptive names that explain what, not how
2. **Keep Methods Small**: Aim for < 10 lines per method
3. **Single Level of Abstraction**: Methods should operate at one level
4. **Avoid Side Effects**: Pure functions are easier to test
5. **Test After Each Step**: Ensure behavior hasn't changed
6. **Commit Often**: Small commits make it easy to revert
