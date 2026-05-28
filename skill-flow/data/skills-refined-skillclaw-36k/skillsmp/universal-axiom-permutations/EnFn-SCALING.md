# Scaling of E_n and F_n

This document derives the scaling rules for the **Exponential component (E_n)** and the  
**Fibonacci component (F_n)** step by step, using **plain Markdown only** so it renders
cleanly.

---

## 1. Given values for E_n

Initial sequence (as provided):

E_n = 1, 5, 17, 53, ...

---

## 2. Identify the recurrence for E_n

Check how each term is produced:

- 1 → 5  
  5 = 3·1 + 2

- 5 → 17  
  17 = 3·5 + 2

- 17 → 53  
  53 = 3·17 + 2

This gives the recurrence:

E_n = 3·E_(n−1) + 2  
with seed value:

E_0 = 1

---

## 3. Solve the recurrence (closed form)

We solve:

E_n = 3·E_(n−1) + 2

### 3.1 Homogeneous part

Ignoring the constant term:

E_n = 3·E_(n−1)

This has the solution:

E_n = C·3^n

### 3.2 Particular solution

Assume a constant solution E_n = k:

k = 3k + 2  
k − 3k = 2  
−2k = 2  
k = −1

### 3.3 General solution

E_n = C·3^n − 1

### 3.4 Apply the initial condition

Using E_0 = 1:

1 = C·3^0 − 1  
1 = C − 1  
C = 2

### 3.5 Final closed form

E_n = 2·3^n − 1

---

## 4. Define Fibonacci scaling F_n

We use the standard Fibonacci recurrence:

F_0 = 1  
F_1 = 1  

F_n = F_(n−1) + F_(n−2)

First values:

F_n = 1, 1, 2, 3, 5, 8, 13, 21, ...

---

## 5. Coupling term: E_n(1 + F_n)

The Axiom couples exponential growth with Fibonacci structure as:

E_n · (1 + F_n)

Substituting the closed form for E_n:

E_n(1 + F_n) = (2·3^n − 1) · (1 + F_n)

---

## 6. Small-n sanity check

| n | E_n | F_n | 1 + F_n | E_n · (1 + F_n) |
|---|-----|-----|---------|----------------|
| 0 | 1   | 1   | 2       | 2              |
| 1 | 5   | 1   | 2       | 10             |
| 2 | 17  | 2   | 3       | 51             |
| 3 | 53  | 3   | 4       | 212            |
| 4 | 161 | 5   | 6       | 966            |

E_4 can be verified two ways:

- Recurrence: E_4 = 3·53 + 2 = 161  
- Closed form: E_4 = 2·3^4 − 1 = 161  

---

## 7. Scaling intuition

- E_n grows exponentially as 3^n (raw expansion / drive).
- F_n grows approximately as φ^n, where φ ≈ 1.618 (natural structure).

Their product scales approximately as:

E_n(1 + F_n) ≈ 3^n · φ^n = (3φ)^n

Since:

3φ ≈ 4.854

this growth is faster than Fibonacci alone, but more ordered than unchecked exponential expansion.

---

## 8. Final results (summary)

Recurrence form:
E_n = 3·E_(n−1) + 2,  with E_0 = 1  
F_n = F_(n−1) + F_(n−2), with F_0 = 1 and F_1 = 1  

Closed form:
E_n = 2·3^n − 1  

Coupling term:
E_n(1 + F_n) = (2·3^n − 1)(1 + F_n)

### Eₙ and Fₙ Scaling Table (n = 0–20)

| n  | Eₙ            | Fₙ    | 1 + Fₙ | Eₙ · (1 + Fₙ)        |
|----|---------------|-------|--------|---------------------|
| 0  | 1             | 1     | 2      | 2                   |
| 1  | 5             | 1     | 2      | 10                  |
| 2  | 17            | 2     | 3      | 51                  |
| 3  | 53            | 3     | 4      | 212                 |
| 4  | 161           | 5     | 6      | 966                 |
| 5  | 485           | 8     | 9      | 4,365               |
| 6  | 1,457         | 13    | 14     | 20,398              |
| 7  | 4,373         | 21    | 22     | 96,206              |
| 8  | 13,121        | 34    | 35     | 459,235             |
| 9  | 39,365        | 55    | 56     | 2,204,440           |
| 10 | 118,097       | 89    | 90     | 10,628,730          |
| 11 | 354,293       | 144   | 145    | 51,372,485          |
| 12 | 1,062,881     | 233   | 234    | 248,713,154         |
| 13 | 3,188,645     | 377   | 378    | 1,205,287,810       |
| 14 | 9,565,937     | 610   | 611    | 5,845,777,507       |
| 15 | 28,697,813    | 987   | 988    | 28,362,642,244      |
| 16 | 86,093,441    | 1,597 | 1,598  | 137,523,215,718     |
| 17 | 258,280,325   | 2,584 | 2,585  | 667,158,640,125     |
| 18 | 774,840,977   | 4,181 | 4,182  | 3,240,181,365,714   |
| 19 | 2,324,522,933 | 6,765 | 6,766  | 15,730,028,329,478  |
| 20 | 6,973,568,801 | 10,946| 10,947 | 76,349,545,566,347  |

Eₙ is a deterministic, division-free projection of the Collatz odd-step dynamics.
