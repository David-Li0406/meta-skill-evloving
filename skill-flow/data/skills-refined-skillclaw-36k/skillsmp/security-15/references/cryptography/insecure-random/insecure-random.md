# Insecure Random Number Generation

**Category**: cryptography/insecure-random
**Description**: Detection of non-cryptographic RNG used for security purposes
**CWE**: CWE-330, CWE-338

---

## Python Weak Random

### Python Random Import
**Pattern**: `^import random$`
**Type**: regex
**Severity**: medium
**Languages**: [python]
- Non-cryptographic random module (Mersenne Twister)
- CWE-330: Use of Insufficiently Random Values

### Python Random From Import
**Pattern**: `from random import`
**Type**: regex
**Severity**: medium
**Languages**: [python]
- Importing from non-secure random module

### Python Random Randint
**Pattern**: `random\.randint\(`
**Type**: regex
**Severity**: medium
**Languages**: [python]
- Predictable random integer generation

### Python Random Randrange
**Pattern**: `random\.randrange\(`
**Type**: regex
**Severity**: medium
**Languages**: [python]
- Predictable random range generation

### Python Random Choice
**Pattern**: `random\.choice\(`
**Type**: regex
**Severity**: high
**Languages**: [python]
- Predictable random selection (dangerous for token generation)

### Python Random Choices
**Pattern**: `random\.choices\(`
**Type**: regex
**Severity**: high
**Languages**: [python]
- Predictable random choices (dangerous for token generation)

### Python Random Float
**Pattern**: `random\.random\(\)`
**Type**: regex
**Severity**: medium
**Languages**: [python]
- Predictable random float [0.0, 1.0)

### Python Random Uniform
**Pattern**: `random\.uniform\(`
**Type**: regex
**Severity**: medium
**Languages**: [python]
- Predictable random float in range

### Python Random Shuffle
**Pattern**: `random\.shuffle\(`
**Type**: regex
**Severity**: medium
**Languages**: [python]
- Predictable shuffle operation

### Python Random Sample
**Pattern**: `random\.sample\(`
**Type**: regex
**Severity**: medium
**Languages**: [python]
- Predictable sample selection

### Python Random Getrandbits
**Pattern**: `random\.getrandbits\(`
**Type**: regex
**Severity**: high
**Languages**: [python]
- Predictable random bits (dangerous for crypto)

---

## JavaScript Weak Random

### JavaScript Math.random
**Pattern**: `Math\.random\(\)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- JavaScript's predictable Math.random (xorshift128+)
- CWE-338: Use of Cryptographically Weak PRNG

### JavaScript Random Integer Floor
**Pattern**: `Math\.floor\(Math\.random\(\)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Common pattern for random integers

### JavaScript Random Integer Round
**Pattern**: `Math\.round\(Math\.random\(\)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Random with rounding

### JavaScript Random Multiplication
**Pattern**: `\*\s*Math\.random\(\)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Multiplication with Math.random

---

## Java Weak Random

### Java Random Constructor
**Pattern**: `new Random\(\)`
**Type**: regex
**Severity**: high
**Languages**: [java, kotlin]
- Non-secure Java Random (uses LCG)
- CWE-338: Use of Cryptographically Weak PRNG

### Java Random Instance Call
**Pattern**: `Random\(\)\.next`
**Type**: regex
**Severity**: high
**Languages**: [java, kotlin]
- Random instance method call

### Java Time-Seeded Random
**Pattern**: `Random\(System\.currentTimeMillis\(\)\)`
**Type**: regex
**Severity**: critical
**Languages**: [java, kotlin]
- Time-seeded random (predictable seed)

### Java Random NextInt
**Pattern**: `\.nextInt\(`
**Type**: regex
**Severity**: medium
**Languages**: [java, kotlin]
- Random nextInt call (context-dependent)

### Java Random NextLong
**Pattern**: `\.nextLong\(`
**Type**: regex
**Severity**: medium
**Languages**: [java, kotlin]
- Random nextLong call (context-dependent)

### Java Random NextBytes
**Pattern**: `\.nextBytes\(`
**Type**: regex
**Severity**: high
**Languages**: [java, kotlin]
- Random nextBytes (not SecureRandom)

### Java Util Random Import
**Pattern**: `java\.util\.Random`
**Type**: regex
**Severity**: medium
**Languages**: [java, kotlin]
- Import of non-secure Random class

---

## Go Weak Random

### Go Math/Rand Seed
**Pattern**: `rand\.Seed\(`
**Type**: regex
**Severity**: high
**Languages**: [go]
- math/rand seeding (not crypto-safe)
- CWE-338: Use of Cryptographically Weak PRNG

### Go Math/Rand Int
**Pattern**: `rand\.Int\(`
**Type**: regex
**Severity**: high
**Languages**: [go]
- math/rand Int function

### Go Math/Rand Intn
**Pattern**: `rand\.Intn\(`
**Type**: regex
**Severity**: high
**Languages**: [go]
- math/rand bounded int

### Go Math/Rand Int63
**Pattern**: `rand\.Int63\(`
**Type**: regex
**Severity**: high
**Languages**: [go]
- math/rand 63-bit int

### Go Math/Rand Float64
**Pattern**: `rand\.Float64\(`
**Type**: regex
**Severity**: medium
**Languages**: [go]
- math/rand float

### Go Math/Rand Perm
**Pattern**: `rand\.Perm\(`
**Type**: regex
**Severity**: medium
**Languages**: [go]
- math/rand permutation

### Go Math/Rand Shuffle
**Pattern**: `rand\.Shuffle\(`
**Type**: regex
**Severity**: medium
**Languages**: [go]
- math/rand shuffle

### Go Math/Rand Read
**Pattern**: `rand\.Read\(`
**Type**: regex
**Severity**: critical
**Languages**: [go]
- math/rand Read (looks like crypto/rand but isn't)

### Go Math/Rand Import
**Pattern**: `"math/rand"`
**Type**: regex
**Severity**: medium
**Languages**: [go]
- Import of math/rand package

---

## Ruby Weak Random

### Ruby Rand Function
**Pattern**: `rand\(`
**Type**: regex
**Severity**: high
**Languages**: [ruby]
- Ruby's predictable rand (Mersenne Twister)
- CWE-338: Use of Cryptographically Weak PRNG

### Ruby Random New
**Pattern**: `Random\.new`
**Type**: regex
**Severity**: high
**Languages**: [ruby]
- Ruby Random class (non-cryptographic)

### Ruby Random Instance
**Pattern**: `\.rand\(`
**Type**: regex
**Severity**: high
**Languages**: [ruby]
- Random instance method

### Ruby Random Bytes
**Pattern**: `\.bytes\(`
**Type**: regex
**Severity**: high
**Languages**: [ruby]
- Random bytes (non-secure)

### Ruby Kernel Rand
**Pattern**: `Kernel\.rand`
**Type**: regex
**Severity**: high
**Languages**: [ruby]
- Kernel rand method

---

## PHP Weak Random

### PHP Rand Function
**Pattern**: `\brand\(`
**Type**: regex
**Severity**: high
**Languages**: [php]
- PHP's predictable rand function (libc rand)
- CWE-338: Use of Cryptographically Weak PRNG

### PHP Mt_rand Function
**Pattern**: `mt_rand\(`
**Type**: regex
**Severity**: high
**Languages**: [php]
- Mersenne Twister rand (not crypto-safe)

### PHP Array_rand Function
**Pattern**: `array_rand\(`
**Type**: regex
**Severity**: medium
**Languages**: [php]
- Non-secure array random selection

### PHP Shuffle Function
**Pattern**: `shuffle\(`
**Type**: regex
**Severity**: medium
**Languages**: [php]
- Non-secure shuffle

### PHP Str_shuffle Function
**Pattern**: `str_shuffle\(`
**Type**: regex
**Severity**: medium
**Languages**: [php]
- Non-secure string shuffle

---

## C/C++ Weak Random

### C Rand Function
**Pattern**: `\brand\(`
**Type**: regex
**Severity**: critical
**Languages**: [c, cpp]
- C standard library rand (very weak)
- CWE-338: Use of Cryptographically Weak PRNG

### C Srand Function
**Pattern**: `srand\(`
**Type**: regex
**Severity**: high
**Languages**: [c, cpp]
- Seeding weak rand

### C Random Function
**Pattern**: `\brandom\(`
**Type**: regex
**Severity**: high
**Languages**: [c, cpp]
- BSD random function

### C Srandom Function
**Pattern**: `srandom\(`
**Type**: regex
**Severity**: high
**Languages**: [c, cpp]
- Seeding BSD random

### C Drand48 Function
**Pattern**: `drand48\(`
**Type**: regex
**Severity**: high
**Languages**: [c, cpp]
- 48-bit random (weak)

### C Lrand48 Function
**Pattern**: `lrand48\(`
**Type**: regex
**Severity**: high
**Languages**: [c, cpp]
- 48-bit random long

### C Mrand48 Function
**Pattern**: `mrand48\(`
**Type**: regex
**Severity**: high
**Languages**: [c, cpp]
- 48-bit random signed

---

## Rust Weak Random

### Rust Rand ThreadRng
**Pattern**: `rand::thread_rng\(\)`
**Type**: regex
**Severity**: medium
**Languages**: [rust]
- Thread-local RNG (ChaCha12 - cryptographically secure but context matters)
- CWE-330: Use of Insufficiently Random Values

### Rust Rand SmallRng
**Pattern**: `SmallRng::from_`
**Type**: regex
**Severity**: high
**Languages**: [rust]
- Small, fast but non-cryptographic RNG
- CWE-338: Use of Cryptographically Weak PRNG

### Rust Rand StdRng Seed
**Pattern**: `StdRng::seed_from_u64`
**Type**: regex
**Severity**: high
**Languages**: [rust]
- Standard RNG with deterministic seed

### Rust Rand Random
**Pattern**: `rand::random::<`
**Type**: regex
**Severity**: medium
**Languages**: [rust]
- Random generation (context-dependent)

### Rust Rand Rng Trait
**Pattern**: `\.gen_range\(`
**Type**: regex
**Severity**: medium
**Languages**: [rust]
- RNG gen_range method (context-dependent)

### Rust XorShiftRng
**Pattern**: `XorShiftRng`
**Type**: regex
**Severity**: critical
**Languages**: [rust]
- XorShift RNG (weak, predictable)

### Rust Pcg32
**Pattern**: `Pcg32::seed_from_u64`
**Type**: regex
**Severity**: high
**Languages**: [rust]
- PCG32 with deterministic seed

---

## C# Weak Random

### CSharp Random Constructor
**Pattern**: `new Random\(`
**Type**: regex
**Severity**: high
**Languages**: [csharp]
- .NET Random (not cryptographically secure)
- CWE-338: Use of Cryptographically Weak PRNG

### CSharp Random Next
**Pattern**: `Random\.Next\(`
**Type**: regex
**Severity**: high
**Languages**: [csharp]
- Random.Next method

### CSharp Random NextDouble
**Pattern**: `Random\.NextDouble\(`
**Type**: regex
**Severity**: high
**Languages**: [csharp]
- Random.NextDouble method

### CSharp Random NextBytes
**Pattern**: `Random\.NextBytes\(`
**Type**: regex
**Severity**: critical
**Languages**: [csharp]
- Random.NextBytes (not secure)

---

## Seed Vulnerabilities

### Hardcoded Random Seed
**Pattern**: `(?:seed|Seed|SEED)\s*[=:(]\s*(\d{1,10})\s*[);]?`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- Hardcoded seed value makes random output predictable
- CWE-330: Use of Insufficiently Random Values

### Time-Based Seed
**Pattern**: `(?:seed|Seed)\s*[=:(].*(?:time|Time|Now|now|currentTimeMillis|UnixNano)`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Time-based seed is predictable if attacker knows approximate time

### Constant Seed Assignment
**Pattern**: `\bseed\s*=\s*[0-9]+\b`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- Constant seed makes all random values predictable

---

## Best Practices

### Secure Alternatives by Language

| Language | Weak | Secure Alternative |
|----------|------|-------------------|
| Python | `random` | `secrets`, `os.urandom()` |
| JavaScript | `Math.random()` | `crypto.randomBytes()`, `crypto.getRandomValues()` |
| Java | `java.util.Random` | `java.security.SecureRandom` |
| Go | `math/rand` | `crypto/rand` |
| Ruby | `rand`, `Random` | `SecureRandom` |
| PHP | `rand()`, `mt_rand()` | `random_bytes()`, `random_int()` |
| C/C++ | `rand()` | `getrandom()`, `/dev/urandom`, OpenSSL RAND |
| C# | `System.Random` | `System.Security.Cryptography.RandomNumberGenerator` |
| Rust | `SmallRng`, `XorShiftRng` | `OsRng`, `rand::rngs::OsRng` |

---

## References

- [CWE-330: Use of Insufficiently Random Values](https://cwe.mitre.org/data/definitions/330.html)
- [CWE-338: Use of Cryptographically Weak PRNG](https://cwe.mitre.org/data/definitions/338.html)
