# Simplify Your Code: Functional Core, Imperative Shell

**Author:** Arham Jain  
**Date:** October 20, 2025  
**Source:** [Google Testing Blog](https://testing.googleblog.com/2025/10/simplify-your-code-functional-core.html)

---

*This article was adapted from a Google [Tech on the Toilet](https://testing.googleblog.com/2024/12/tech-on-toilet-driving-software.html) (TotT) episode. You can download a [printer-friendly version](https://docs.google.com/document/d/1uSSL90h0vM6tLvdlnk04nZZLKfPI3By1tFdKXz_IUl8/edit?tab=t.0) of this TotT episode and post it in your office.*

## Is your code a tangled mess of business logic and side effects?

Mixing database calls, network requests, and other external interactions directly with your core logic can lead to code that's difficult to test, reuse, and understand. Instead, consider writing a **functional core** that's called from an **imperative shell**.

![Diagram of functional core, imperative shell](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjcjlaWnIXkXzahgFw3l6gXUaZaX6eAS1brqLf38XD5n6JhEup-D6UDNJB5VrDqtMMsqjhyphenhyphenQEJ3ZlnOTkpGWosz4uzOJVrRoFvnLvC5gH0m3Lcs7rHV5PLRWmd1lxiHqSkVl15v-FpHCiJwMg4w7Azo8y-ipNuN6wvOjqHFjHme-X9m8V5gwrw2/s320/Screenshot%202025-10-20%20at%208.51.55%E2%80%AFAM.png)

## Separating your code into functional cores and imperative shells makes it more testable, maintainable, and adaptable

The core logic can be tested in isolation, and the imperative shell can be swapped out or modified as needed. Here's some messy example code that mixes logic and side effects to send expiration notification emails to users:

```typescript
// Bad: Logic and side effects are mixed
function sendUserExpiryEmail(): void {
  for (const user of db.getUsers()) {
    if (user.subscriptionEndDate > Date.now()) continue;
    if (user.isFreeTrial) continue;
    email.send(user.email, "Your account has expired " + user.name + ".");
  }
}
```

## A functional core should contain pure, testable business logic

A functional core is free of side effects (such as I/O or external state mutation). It operates only on the data it is given.

## An imperative shell is responsible for side effects

An imperative shell handles database calls and sending emails. It uses the functions in your functional core to perform the business logic.

Rewriting the above code to follow the functional core / imperative shell pattern might look like:

**Functional core**

```typescript
function getExpiredUsers(users: User[], cutoff: Date): User[] {
  return users.filter(user => user.subscriptionEndDate <= cutoff && !user.isFreeTrial);
}

function generateExpiryEmails(users: User[]): Array<[string, string]> {
  return users.map(user => 
    ([user.email, "Your account has expired " + user.name + "."])
  );
}
```

**Imperative shell**

```typescript
email.bulkSend(generateExpiryEmails(getExpiredUsers(db.getUsers(), Date.now())));
```

Now that the code is following this pattern, adding a feature to send a new type of email is as simple as writing a new pure function and reusing `getExpiredUsers`:

```typescript
// Sending a reminder email to users
function generateReminderEmails(users: User[], cutoff: Date): Array<[string, string]> {...}

const fiveDaysFromNow = ...
email.bulkSend(generateReminderEmails(getExpiredUsers(db.getUsers(), fiveDaysFromNow)));
```

Learn more in Gary Bernhardt's [original talk about functional core, imperative shell](https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell).
