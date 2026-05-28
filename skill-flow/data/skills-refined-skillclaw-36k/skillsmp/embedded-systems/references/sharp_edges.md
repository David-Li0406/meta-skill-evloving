# Embedded Systems - Sharp Edges

## Missing Volatile Causes Compiler to Optimize Away Reads

### **Id**
volatile-omission
### **Severity**
critical
### **Summary**
Compiler caches variable in register, ISR updates memory, main loop never sees change
### **Symptoms**
  - Flag set in ISR but main loop never detects it
  - Works with -O0, fails with -O2
  - Adding printf makes it work (timing change)
### **Why**
  Without 'volatile', the compiler assumes no external modification.
  It optimizes by reading the variable once into a register.
  
  The ISR modifies memory, but main loop reads stale register.
  This is the most common embedded bug and hardest to debug
  because it works at -O0 and fails at -O2.
  
### **Gotcha**
  // ISR sets flag
  void TIMER_IRQHandler(void) {
      data_ready = true;  // Writes to memory
  }
  
  // Main loop - compiler caches in register
  bool data_ready = false;  // NOT volatile!
  
  while (1) {
      if (data_ready) {  // Compiler reads once, caches in r0
          process_data();
          data_ready = false;
      }
      // Never sees ISR's write - infinite loop!
  }
  
### **Solution**
  // Always use volatile for ISR-shared variables
  volatile bool data_ready = false;
  
  // For multi-word data, volatile alone isn't enough
  // Need critical section too (see race-condition edge)
  
  // Rule: If ANY interrupt can modify it, it's volatile
  

## Silent Stack Overflow Corrupts Memory

### **Id**
stack-overflow
### **Severity**
critical
### **Summary**
Stack grows into heap/data, no error, random crashes later
### **Symptoms**
  - Random crashes, different each time
  - Works until you add a local array
  - Crashes in unrelated functions
  - Works in debug, fails in release
### **Why**
  Embedded systems have small stacks (often 1-4KB).
  Stack overflow doesn't trigger an error - it just
  writes over whatever memory is below the stack.
  
  This corrupts heap, global variables, or other stacks.
  Symptoms appear far from the actual overflow point.
  
  Common causes:
  - Large local arrays
  - Deep recursion
  - Printf (uses 1KB+ stack)
  - Nested interrupts
  
### **Gotcha**
  void process_image(void) {
      uint8_t buffer[2048];  // Stack is only 1KB!
      // Stack overflow - corrupts heap
  
      process_buffer(buffer);
      // Crash happens later in malloc() or another function
  }
  
  // Or deep call chains
  void parse_json(char* data) {
      parse_value(data);  // -> parse_object -> parse_array -> parse_value...
      // 10 levels deep = 10 stack frames
  }
  
### **Solution**
  // 1. Use static/global for large buffers
  static uint8_t buffer[2048];  // In .bss, not stack
  
  // 2. Monitor stack usage
  void init_stack_monitor(void) {
      extern uint32_t _estack, _Min_Stack_Size;
      uint32_t* bottom = &_estack - (uint32_t)&_Min_Stack_Size/4;
      for (uint32_t* p = bottom; p < &_estack - 64; p++)
          *p = 0xDEADBEEF;  // Canary pattern
  }
  
  uint32_t check_stack_usage(void) {
      extern uint32_t _estack, _Min_Stack_Size;
      uint32_t* p = &_estack - (uint32_t)&_Min_Stack_Size/4;
      while (*p == 0xDEADBEEF) p++;
      return (&_estack - p) * 4;  // Bytes used
  }
  
  // 3. Use -fstack-usage compiler flag
  // Generates .su files with per-function stack usage
  

## Multi-Word Access Race Condition

### **Id**
race-condition
### **Severity**
critical
### **Summary**
ISR interrupts between reading high/low bytes, corrupted value
### **Symptoms**
  - Occasional wrong values (1 in 1000)
  - Values jump unexpectedly
  - 32-bit value has wrong upper 16 bits
### **Why**
  On 32-bit MCU, 64-bit access is two instructions.
  On 8-bit MCU, even 16-bit is two instructions.
  
  If ISR fires between instructions, you get:
  - Old high byte + new low byte, or
  - New high byte + old low byte
  
  Result: Completely wrong value, hard to reproduce.
  
### **Gotcha**
  volatile uint32_t timestamp;    // Updated in ISR
  volatile int16_t sensor_value;  // Updated in ISR
  
  void ISR(void) {
      timestamp = get_time();     // 32-bit write
      sensor_value = read_adc();  // 16-bit write
  }
  
  void main_loop(void) {
      // On 8-bit MCU, this is 4 separate byte reads
      uint32_t ts = timestamp;
      // ISR fires here - timestamp changes mid-read!
  
      // ts = corrupted mix of old and new value
  }
  
### **Solution**
  // Use critical sections for multi-word access
  uint32_t read_timestamp_safe(void) {
      uint32_t primask = __get_PRIMASK();
      __disable_irq();
  
      uint32_t ts = timestamp;  // Now atomic
  
      __set_PRIMASK(primask);
      return ts;
  }
  
  // Or use double-read pattern (no interrupt disable)
  uint32_t read_timestamp_lockfree(void) {
      uint32_t a, b;
      do {
          a = timestamp;
          b = timestamp;
      } while (a != b);  // Retry if ISR interrupted
      return a;
  }
  
  // For structs, copy entire struct atomically
  typedef struct {
      uint32_t timestamp;
      int16_t x, y, z;
  } sensor_data_t;
  
  sensor_data_t read_sensor_safe(void) {
      sensor_data_t copy;
      __disable_irq();
      copy = sensor_data;  // Struct copy
      __enable_irq();
      return copy;
  }
  

## Watchdog Reset from Long Operations

### **Id**
watchdog-starvation
### **Severity**
high
### **Summary**
Blocking operation exceeds watchdog timeout, system resets
### **Symptoms**
  - Random resets during certain operations
  - Resets when processing large data
  - Works with watchdog disabled
### **Why**
  Watchdog must be fed within timeout (typically 1-10 seconds).
  Long operations (flash writes, crypto, large transfers)
  can exceed this, causing unexpected reset.
  
  Worse: Reset clears evidence of what happened.
  
### **Gotcha**
  void update_firmware(uint8_t* data, size_t len) {
      flash_erase_sector(0x08010000);  // Takes 400ms
  
      for (int i = 0; i < len; i += 256) {
          flash_write_page(0x08010000 + i, &data[i], 256);  // 10ms each
      }
      // 100KB = 400 pages = 4 seconds
      // Watchdog times out at 2 seconds - RESET!
  }
  
### **Solution**
  void update_firmware_safe(uint8_t* data, size_t len) {
      flash_erase_sector(0x08010000);
      watchdog_feed();  // Feed after each long operation
  
      for (int i = 0; i < len; i += 256) {
          flash_write_page(0x08010000 + i, &data[i], 256);
  
          if (i % 2048 == 0) {  // Every 8 pages
              watchdog_feed();
          }
      }
      watchdog_feed();
  }
  
  // For unpredictable operations, use windowed watchdog
  // or feed from timer ISR (risky - can mask hangs)
  

## Printf in ISR Causes Crashes

### **Id**
printf-in-isr
### **Severity**
high
### **Summary**
Printf is not reentrant, ISR corrupts main code's printf state
### **Symptoms**
  - Crash during printf
  - Garbled output
  - Deadlock waiting for UART
  - Works sometimes, crashes other times
### **Why**
  Printf maintains internal state (buffers, format parsing).
  It's not reentrant - calling from ISR while main uses it
  corrupts that state.
  
  Also: Printf typically blocks waiting for UART, which
  defeats the purpose of a quick ISR.
  
### **Gotcha**
  void UART_IRQHandler(void) {
      printf("Received: %c\n", UART->DR);  // CRASH!
      // - Not reentrant (corrupts main's printf state)
      // - Blocks waiting for UART TX (delays ISR)
      // - Uses 1KB+ stack (may overflow ISR stack)
  }
  
### **Solution**
  // Option 1: Buffer for deferred printing
  volatile char debug_buffer[64];
  volatile uint8_t debug_head = 0;
  
  void UART_IRQHandler(void) {
      debug_buffer[debug_head++] = UART->DR;
      debug_head &= 0x3F;  // Wrap
  }
  
  void main_loop(void) {
      // Print from main context
      static uint8_t debug_tail = 0;
      while (debug_tail != debug_head) {
          printf("Received: %c\n", debug_buffer[debug_tail++]);
          debug_tail &= 0x3F;
      }
  }
  
  // Option 2: SEGGER RTT (non-blocking, ISR-safe)
  #include "SEGGER_RTT.h"
  void UART_IRQHandler(void) {
      SEGGER_RTT_printf(0, "RX: %c\n", UART->DR);  // Safe!
  }
  
  // Option 3: Toggle GPIO pin for timing debug
  void UART_IRQHandler(void) {
      GPIO_SET(DEBUG_PIN);   // Scope can measure
      // ... handler code ...
      GPIO_CLEAR(DEBUG_PIN);
  }
  

## Peripheral Access Before Clock Enable

### **Id**
uninitialized-peripheral
### **Severity**
high
### **Summary**
Accessing peripheral before enabling its clock causes hard fault
### **Symptoms**
  - Hard fault on first peripheral access
  - Bus error at specific address
  - Works after reset, fails on warm boot
### **Why**
  Peripherals are clock-gated for power savings.
  Accessing a peripheral with clock disabled causes
  a bus fault - the peripheral literally doesn't respond.
  
  Easy to forget clock enable, especially when copy-pasting code.
  
### **Gotcha**
  void init_uart(void) {
      // Forgot clock enable!
      USART1->BRR = 0x1A1;  // Hard fault! USART1 clock is off
      USART1->CR1 = USART_CR1_TE | USART_CR1_RE | USART_CR1_UE;
  }
  
### **Solution**
  void init_uart(void) {
      // Always enable clock FIRST
      RCC->APB2ENR |= RCC_APB2ENR_USART1EN;
  
      // Small delay for clock to stabilize
      __NOP(); __NOP();
  
      // Now safe to access
      USART1->BRR = 0x1A1;
      USART1->CR1 = USART_CR1_TE | USART_CR1_RE | USART_CR1_UE;
  }
  
  // Use HAL functions that handle this automatically
  __HAL_RCC_USART1_CLK_ENABLE();
  

## Unaligned Memory Access Fault

### **Id**
alignment-fault
### **Severity**
medium
### **Summary**
Casting byte pointer to word pointer causes alignment fault
### **Symptoms**
  - Hard fault on memory access
  - Works on x86, fails on ARM
  - Crashes when buffer address is odd
### **Why**
  ARM Cortex-M (and many other CPUs) require aligned access:
  - 32-bit access must be 4-byte aligned
  - 16-bit access must be 2-byte aligned
  
  Casting a byte buffer to uint32_t* and dereferencing
  causes hard fault if buffer isn't aligned.
  
### **Gotcha**
  void process_packet(uint8_t* data) {
      // data might be at odd address!
      uint32_t* header = (uint32_t*)data;
      uint32_t magic = *header;  // HARD FAULT if data not 4-byte aligned
  }
  
  // Also fails:
  uint8_t buffer[10];
  uint32_t* ptr = (uint32_t*)&buffer[1];  // Misaligned!
  *ptr = 0x12345678;  // CRASH
  
### **Solution**
  // Option 1: Use memcpy (compiler handles alignment)
  void process_packet(uint8_t* data) {
      uint32_t magic;
      memcpy(&magic, data, sizeof(magic));  // Safe!
  }
  
  // Option 2: Use packed struct with attribute
  typedef struct __attribute__((packed)) {
      uint32_t magic;
      uint16_t length;
      uint8_t data[];
  } packet_t;
  
  // Option 3: Ensure alignment at allocation
  uint8_t buffer[10] __attribute__((aligned(4)));
  
  // Option 4: Use byte-by-byte access
  uint32_t read_u32_unaligned(uint8_t* p) {
      return p[0] | (p[1] << 8) | (p[2] << 16) | (p[3] << 24);
  }
  