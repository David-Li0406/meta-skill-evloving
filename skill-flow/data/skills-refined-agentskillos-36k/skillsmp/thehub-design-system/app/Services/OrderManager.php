<?php

namespace App\Services;

use App\Models\Order;
use App\Models\OrderItem;
use App\Models\EventRegistration;
use App\Models\SeriesRegistration;
use App\Models\SeriesRegistrationEvent;
use App\Models\ReservedRegistration;
use App\Models\DiscountCode;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Mail;
use Exception;

/**
 * OrderManager - Hanterar multi-rider registreringar
 * 
 * Användning:
 * $orderManager = new OrderManager();
 * $result = $orderManager->createOrder($buyerData, $items);
 */
class OrderManager
{
    private $pricingCalculator;
    private $registrationValidator;
    
    public function __construct()
    {
        $this->pricingCalculator = new PricingCalculator();
        $this->registrationValidator = new RegistrationValidator();
    }
    
    /**
     * Skapa order med flera registreringar
     * 
     * @param array $buyer_data ['name', 'email', 'phone', 'user_id']
     * @param array $items [['type' => 'event|series', 'rider_id', 'event_id|series_id', 'class_id'], ...]
     * @param string|null $discount_code
     * @return array ['success' => bool, 'order' => Order, 'errors' => array]
     */
    public function createOrder(array $buyer_data, array $items, ?string $discount_code = null)
    {
        DB::beginTransaction();
        
        try {
            // 1. Validera att items inte är tomma
            if (empty($items)) {
                throw new Exception('Inga registreringar att lägga till');
            }
            
            // 2. Skapa order
            $order = Order::create([
                'buyer_user_id' => $buyer_data['user_id'] ?? null,
                'buyer_name' => $buyer_data['name'],
                'buyer_email' => $buyer_data['email'],
                'buyer_phone' => $buyer_data['phone'] ?? null,
                'customer_name' => $buyer_data['name'], // Backwards compatibility
                'customer_email' => $buyer_data['email'],
                'subtotal' => 0,
                'payment_status' => 'pending',
                'ip_address' => request()->ip(),
                'user_agent' => request()->userAgent(),
                'session_id' => session()->getId(),
            ]);
            
            $subtotal = 0;
            $registrations = [];
            
            // 3. Skapa registreringar för varje item
            foreach ($items as $index => $item) {
                $result = $this->createRegistration($order->id, $item);
                
                if (!$result['success']) {
                    throw new Exception("Item {$index}: " . implode(', ', $result['errors']));
                }
                
                $subtotal += $result['price'];
                $registrations[] = $result['registration'];
                
                // Skapa order item
                $this->createOrderItem($order->id, $result);
            }
            
            // 4. Applicera rabattkod om angiven
            $discount_amount = 0;
            if ($discount_code) {
                $discount_result = $this->applyDiscountCode($order->id, $discount_code, $subtotal);
                if ($discount_result['success']) {
                    $discount_amount = $discount_result['discount_amount'];
                }
            }
            
            // 5. Beräkna avgifter
            $platform_fee = $this->calculatePlatformFee($subtotal - $discount_amount);
            $payment_gateway_fee = $this->calculateGatewayFee($subtotal - $discount_amount + $platform_fee);
            $total_amount = $subtotal - $discount_amount + $platform_fee + $payment_gateway_fee;
            
            // 6. Uppdatera order
            $order->update([
                'subtotal' => $subtotal,
                'discount' => $discount_amount,
                'platform_fee' => $platform_fee,
                'payment_gateway_fee' => $payment_gateway_fee,
                'total_amount' => $total_amount
            ]);
            
            // 7. Ta bort reservationer (om finns)
            $this->clearReservations(session()->getId());
            
            DB::commit();
            
            return [
                'success' => true,
                'order' => $order->fresh(['orderItems', 'eventRegistrations', 'seriesRegistrations']),
                'breakdown' => [
                    'subtotal' => $subtotal,
                    'discount' => $discount_amount,
                    'platform_fee' => $platform_fee,
                    'payment_gateway_fee' => $payment_gateway_fee,
                    'total' => $total_amount,
                    'items_count' => count($items)
                ]
            ];
            
        } catch (Exception $e) {
            DB::rollBack();
            
            return [
                'success' => false,
                'error' => $e->getMessage(),
                'errors' => [$e->getMessage()]
            ];
        }
    }
    
    /**
     * Skapa en enskild registrering (event eller serie)
     */
    private function createRegistration(int $order_id, array $item): array
    {
        if ($item['type'] === 'event') {
            return $this->createEventRegistration($order_id, $item);
        } elseif ($item['type'] === 'series') {
            return $this->createSeriesRegistration($order_id, $item);
        }
        
        throw new Exception('Invalid item type: ' . $item['type']);
    }
    
    /**
     * Skapa event-registrering
     */
    private function createEventRegistration(int $order_id, array $item): array
    {
        // Validera
        $validation = $this->registrationValidator->validateEventRegistration(
            $item['rider_id'],
            $item['event_id'],
            $item['class_id']
        );
        
        if (!$validation['valid']) {
            return [
                'success' => false,
                'errors' => $validation['errors']
            ];
        }
        
        // Beräkna pris
        $pricing = $this->pricingCalculator->calculateEventPrice(
            $item['event_id'],
            $item['rider_id'],
            $item['class_id']
        );
        
        // Skapa registrering
        $registration = EventRegistration::create([
            'order_id' => $order_id,
            'rider_id' => $item['rider_id'],
            'event_id' => $item['event_id'],
            'class_id' => $item['class_id'],
            'base_price' => $pricing['base_price'],
            'early_bird_discount' => $pricing['early_bird_discount'],
            'late_fee' => $pricing['late_fee'],
            'championship_fee' => $pricing['championship_fee'] ?? 0,
            'final_price' => $pricing['final_price'],
            'status' => 'registered',
            'payment_status' => 'pending'
        ]);
        
        return [
            'success' => true,
            'registration' => $registration,
            'type' => 'event_registration',
            'price' => $pricing['final_price'],
            'description' => $this->formatEventDescription($registration)
        ];
    }
    
    /**
     * Skapa serie-registrering
     */
    private function createSeriesRegistration(int $order_id, array $item): array
    {
        // Validera
        $validation = $this->registrationValidator->validateSeriesRegistration(
            $item['rider_id'],
            $item['series_id'],
            $item['class_id']
        );
        
        if (!$validation['valid']) {
            return [
                'success' => false,
                'errors' => $validation['errors']
            ];
        }
        
        // Beräkna pris
        $pricing = $this->pricingCalculator->calculateSeriesPrice(
            $item['series_id'],
            $item['rider_id'],
            $item['class_id']
        );
        
        // Skapa registrering
        $registration = SeriesRegistration::create([
            'order_id' => $order_id,
            'rider_id' => $item['rider_id'],
            'series_id' => $item['series_id'],
            'class_id' => $item['class_id'],
            'base_price' => $pricing['base_price'],
            'discount_percent' => $pricing['discount_percent'],
            'discount_amount' => $pricing['discount'],
            'final_price' => $pricing['final_price'],
            'payment_status' => 'pending'
        ]);
        
        // Skapa event-kopplingar
        $events = $this->getSeriesEvents($item['series_id']);
        foreach ($events as $event) {
            SeriesRegistrationEvent::create([
                'series_registration_id' => $registration->id,
                'event_id' => $event->id,
                'status' => 'registered'
            ]);
        }
        
        return [
            'success' => true,
            'registration' => $registration,
            'type' => 'series_registration',
            'price' => $pricing['final_price'],
            'description' => $this->formatSeriesDescription($registration)
        ];
    }
    
    /**
     * Skapa order item för kvitto
     */
    private function createOrderItem(int $order_id, array $data): OrderItem
    {
        return OrderItem::create([
            'order_id' => $order_id,
            'item_type' => $data['type'],
            'registration_id' => $data['type'] === 'event_registration' ? $data['registration']->id : null,
            'series_registration_id' => $data['type'] === 'series_registration' ? $data['registration']->id : null,
            'description' => $data['description'],
            'quantity' => 1,
            'unit_price' => $data['price'],
            'total_price' => $data['price']
        ]);
    }
    
    /**
     * Applicera rabattkod
     */
    private function applyDiscountCode(int $order_id, string $code, float $subtotal): array
    {
        $discountCode = DiscountCode::where('code', $code)
            ->where('is_active', true)
            ->first();
        
        if (!$discountCode) {
            return ['success' => false, 'error' => 'Ogiltig rabattkod'];
        }
        
        // Kolla giltighetstid
        if ($discountCode->valid_from && now()->lt($discountCode->valid_from)) {
            return ['success' => false, 'error' => 'Rabatten är inte giltig ännu'];
        }
        
        if ($discountCode->valid_until && now()->gt($discountCode->valid_until)) {
            return ['success' => false, 'error' => 'Rabatten har gått ut'];
        }
        
        // Kolla max_uses
        if ($discountCode->max_uses && $discountCode->uses_count >= $discountCode->max_uses) {
            return ['success' => false, 'error' => 'Rabatten är slut'];
        }
        
        // Kolla min_order_amount
        if ($discountCode->min_order_amount && $subtotal < $discountCode->min_order_amount) {
            return ['success' => false, 'error' => 'Orderbeloppet är för lågt för denna rabatt'];
        }
        
        // Beräkna rabatt
        $discount_amount = 0;
        if ($discountCode->discount_type === 'percentage') {
            $discount_amount = $subtotal * ($discountCode->discount_value / 100);
        } else {
            $discount_amount = $discountCode->discount_value;
        }
        
        // Koppla till order
        DB::table('order_discount_codes')->insert([
            'order_id' => $order_id,
            'discount_code_id' => $discountCode->id,
            'discount_amount' => $discount_amount
        ]);
        
        // Uppdatera räknare
        $discountCode->increment('uses_count');
        
        return [
            'success' => true,
            'discount_amount' => $discount_amount
        ];
    }
    
    /**
     * Markera order som betald
     */
    public function markOrderAsPaid(string $order_reference, array $payment_data): array
    {
        DB::beginTransaction();
        
        try {
            $order = Order::where('order_reference', $order_reference)->firstOrFail();
            
            $order->update([
                'payment_status' => 'paid',
                'payment_reference' => $payment_data['reference'] ?? null,
                'paid_at' => now()
            ]);
            
            // Uppdatera alla registreringar
            $order->eventRegistrations()->update(['payment_status' => 'paid']);
            $order->seriesRegistrations()->update(['payment_status' => 'paid']);
            
            // Skicka bekräftelse-mail
            $this->sendOrderConfirmation($order);
            
            DB::commit();
            
            return ['success' => true, 'order' => $order];
            
        } catch (Exception $e) {
            DB::rollBack();
            return ['success' => false, 'error' => $e->getMessage()];
        }
    }
    
    /**
     * Skicka bekräftelse-mail
     */
    private function sendOrderConfirmation(Order $order)
    {
        // Skicka till köparen
        Mail::to($order->buyer_email)->send(new \App\Mail\OrderConfirmation($order));
        
        // Skicka till varje rider
        $riders = [];
        
        foreach ($order->eventRegistrations as $reg) {
            if (!in_array($reg->rider_id, $riders)) {
                $riders[] = $reg->rider_id;
                Mail::to($reg->rider->email)->send(new \App\Mail\RiderRegistrationConfirmation($reg));
            }
        }
        
        foreach ($order->seriesRegistrations as $reg) {
            if (!in_array($reg->rider_id, $riders)) {
                $riders[] = $reg->rider_id;
                Mail::to($reg->rider->email)->send(new \App\Mail\RiderRegistrationConfirmation($reg));
            }
        }
    }
    
    /**
     * Beräkna plattformsavgift
     */
    private function calculatePlatformFee(float $amount): float
    {
        // 2.5% + 10 kr
        return round(($amount * 0.025) + 10, 2);
    }
    
    /**
     * Beräkna Swish/Stripe-avgift
     */
    private function calculateGatewayFee(float $amount): float
    {
        // Swish: ~1 kr fix
        // Stripe: 1.8% + 1.80 kr
        return 1.00; // Swish default
    }
    
    /**
     * Formatera event-beskrivning för kvitto
     */
    private function formatEventDescription(EventRegistration $registration): string
    {
        $rider = $registration->rider;
        $event = $registration->event;
        $class = $registration->class;
        
        return sprintf(
            "%s %s - %s - %s",
            $rider->firstname,
            $rider->lastname,
            $event->name,
            $class->name
        );
    }
    
    /**
     * Formatera serie-beskrivning för kvitto
     */
    private function formatSeriesDescription(SeriesRegistration $registration): string
    {
        $rider = $registration->rider;
        $series = $registration->series;
        $class = $registration->class;
        
        return sprintf(
            "%s %s - %s (Serie) - %s",
            $rider->firstname,
            $rider->lastname,
            $series->name,
            $class->name
        );
    }
    
    /**
     * Hämta events i en serie
     */
    private function getSeriesEvents(int $series_id): array
    {
        return \App\Models\Event::where('series_id', $series_id)
            ->where('is_active', true)
            ->orderBy('date', 'asc')
            ->get()
            ->toArray();
    }
    
    /**
     * Ta bort reservationer för session
     */
    private function clearReservations(string $session_id)
    {
        ReservedRegistration::where('session_id', $session_id)->delete();
    }
    
    /**
     * Avbryt order
     */
    public function cancelOrder(string $order_reference): array
    {
        DB::beginTransaction();
        
        try {
            $order = Order::where('order_reference', $order_reference)->firstOrFail();
            
            if ($order->payment_status === 'paid') {
                throw new Exception('Kan inte avbryta en betald order. Använd refund istället.');
            }
            
            $order->update([
                'payment_status' => 'cancelled',
                'cancelled_at' => now()
            ]);
            
            // Soft delete alla registreringar
            $order->eventRegistrations()->update(['deleted_at' => now()]);
            $order->seriesRegistrations()->update(['deleted_at' => now()]);
            
            DB::commit();
            
            return ['success' => true];
            
        } catch (Exception $e) {
            DB::rollBack();
            return ['success' => false, 'error' => $e->getMessage()];
        }
    }
}
