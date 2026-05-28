# Faker Plugin - Complete Generator Reference

## Shorthand Generators

These are available without a prefix:

| Generator | Description |
|-----------|-------------|
| `uuid()` | UUID v4 string |
| `email()` | Email address |
| `phone(format?)` | Phone number (format: "human", "national", "international") |
| `firstName()` | First name |
| `lastName()` | Last name |
| `fullName()` | Full name |
| `companyName()` | Company name |
| `streetAddress()` | Street address |
| `city()` | City name |
| `country()` | Country name |
| `countryCode()` | ISO country code |
| `zipCode()` | Postal/ZIP code |
| `url()` | URL |
| `avatar()` | Avatar image URL |
| `iban()` | Bank IBAN |
| `currencyCode()` | Currency code (USD, EUR, etc.) |
| `pastDate()` | ISO date in the past |
| `futureDate()` | ISO date in the future |
| `recentDate()` | Recent ISO date |
| `sentence()` | Lorem ipsum sentence |
| `paragraph()` | Lorem ipsum paragraph |

## Full Namespace Generators

Use `faker.module.method()` syntax for these:

### String (`faker.string.*`)

| Generator | Description |
|-----------|-------------|
| `faker.string.uuid()` | UUID v4 |
| `faker.string.alphanumeric(length?)` | Alphanumeric string |
| `faker.string.nanoid(length?)` | Nano ID |

### Person (`faker.person.*`)

| Generator | Description |
|-----------|-------------|
| `faker.person.firstName(sex?)` | First name (sex: "male" or "female") |
| `faker.person.lastName(sex?)` | Last name |
| `faker.person.fullName(options?)` | Full name |
| `faker.person.jobTitle()` | Job title |
| `faker.person.jobType()` | Job type |
| `faker.person.gender()` | Gender |
| `faker.person.prefix()` | Name prefix (Mr., Mrs., etc.) |
| `faker.person.suffix()` | Name suffix (Jr., Sr., etc.) |

### Internet (`faker.internet.*`)

| Generator | Description |
|-----------|-------------|
| `faker.internet.email(options?)` | Email address |
| `faker.internet.userName()` | Username |
| `faker.internet.url()` | URL |
| `faker.internet.domainName()` | Domain name |
| `faker.internet.ip()` | IPv4 address |
| `faker.internet.ipv6()` | IPv6 address |
| `faker.internet.mac()` | MAC address |
| `faker.internet.password(length?)` | Password |

### Phone (`faker.phone.*`)

| Generator | Description |
|-----------|-------------|
| `faker.phone.number(format?)` | Phone number |
| `faker.phone.imei()` | IMEI number |

### Company (`faker.company.*`)

| Generator | Description |
|-----------|-------------|
| `faker.company.name()` | Company name |
| `faker.company.catchPhrase()` | Catch phrase |
| `faker.company.buzzPhrase()` | Buzz phrase |

### Location (`faker.location.*`)

| Generator | Description |
|-----------|-------------|
| `faker.location.streetAddress(useFullAddress?)` | Street address |
| `faker.location.city()` | City |
| `faker.location.state()` | State |
| `faker.location.zipCode(format?)` | ZIP/postal code |
| `faker.location.country()` | Country |
| `faker.location.countryCode()` | Country code |
| `faker.location.latitude()` | Latitude |
| `faker.location.longitude()` | Longitude |

### Date (`faker.date.*`)

| Generator | Description |
|-----------|-------------|
| `faker.date.past(options?)` | Past date (ISO string) |
| `faker.date.future(options?)` | Future date (ISO string) |
| `faker.date.recent(options?)` | Recent date (ISO string) |
| `faker.date.birthdate(options?)` | Birthdate (YYYY-MM-DD) |

### Finance (`faker.finance.*`)

| Generator | Description |
|-----------|-------------|
| `faker.finance.accountNumber(length?)` | Account number |
| `faker.finance.iban()` | IBAN |
| `faker.finance.bic()` | BIC/SWIFT code |
| `faker.finance.creditCardNumber(issuer?)` | Credit card number |
| `faker.finance.creditCardCVV()` | CVV |
| `faker.finance.currency()` | Currency object |
| `faker.finance.currencyCode()` | Currency code |
| `faker.finance.amount(min?, max?, dec?)` | Amount |
| `faker.finance.transactionType()` | Transaction type |

### Commerce (`faker.commerce.*`)

| Generator | Description |
|-----------|-------------|
| `faker.commerce.department()` | Department |
| `faker.commerce.productName()` | Product name |
| `faker.commerce.price(options?)` | Price |
| `faker.commerce.productDescription()` | Product description |

### Lorem (`faker.lorem.*`)

| Generator | Description |
|-----------|-------------|
| `faker.lorem.word()` | Single word |
| `faker.lorem.words(count?)` | Multiple words |
| `faker.lorem.sentence(wordCount?)` | Sentence |
| `faker.lorem.sentences(count?)` | Multiple sentences |
| `faker.lorem.paragraph(sentenceCount?)` | Paragraph |
| `faker.lorem.paragraphs(count?)` | Multiple paragraphs |

### Image (`faker.image.*`)

| Generator | Description |
|-----------|-------------|
| `faker.image.avatar()` | Avatar URL |
| `faker.image.url(options?)` | Image URL |

### Database (`faker.database.*`)

| Generator | Description |
|-----------|-------------|
| `faker.database.column()` | Column name |
| `faker.database.type()` | Database type |
| `faker.database.collation()` | Collation |
| `faker.database.engine()` | Database engine |
| `faker.database.mongodbObjectId()` | MongoDB ObjectId |

### Git (`faker.git.*`)

| Generator | Description |
|-----------|-------------|
| `faker.git.branch()` | Branch name |
| `faker.git.commitSha()` | Commit SHA |
| `faker.git.commitMessage()` | Commit message |

### Hacker (`faker.hacker.*`)

| Generator | Description |
|-----------|-------------|
| `faker.hacker.abbreviation()` | Tech abbreviation |
| `faker.hacker.adjective()` | Hacker adjective |
| `faker.hacker.noun()` | Hacker noun |
| `faker.hacker.verb()` | Hacker verb |
| `faker.hacker.phrase()` | Hacker phrase |

### Color (`faker.color.*`)

| Generator | Description |
|-----------|-------------|
| `faker.color.rgb()` | RGB color |
| `faker.color.human()` | Human-readable color name |

### Number (`faker.number.*`)

| Generator | Description |
|-----------|-------------|
| `faker.number.int(options?)` | Integer |
| `faker.number.float(options?)` | Float |

### Datatype (`faker.datatype.*`)

| Generator | Description |
|-----------|-------------|
| `faker.datatype.boolean()` | Boolean |

### Airline (`faker.airline.*`)

| Generator | Description |
|-----------|-------------|
| `faker.airline.airline()` | Airline object |
| `faker.airline.airport()` | Airport object |
| `faker.airline.flightNumber()` | Flight number |

### Vehicle (`faker.vehicle.*`)

| Generator | Description |
|-----------|-------------|
| `faker.vehicle.vehicle()` | Full vehicle description |
| `faker.vehicle.manufacturer()` | Manufacturer |
| `faker.vehicle.model()` | Model |
| `faker.vehicle.vin()` | VIN |
| `faker.vehicle.vrm()` | VRM (UK registration) |

## Examples

### Basic User Schema

```vague
schema User {
  id: uuid()
  firstName: firstName()
  lastName: lastName()
  email: email()
  phone: phone()
  avatar: avatar()
  createdAt: pastDate()
}
```

### E-commerce Product

```vague
schema Product {
  id: uuid()
  name: faker.commerce.productName()
  description: faker.commerce.productDescription()
  price: faker.commerce.price()
  department: faker.commerce.department()
}
```

### Address

```vague
schema Address {
  street: streetAddress()
  city: city()
  state: faker.location.state()
  zipCode: zipCode()
  country: country()
  lat: faker.location.latitude()
  lng: faker.location.longitude()
}
```

### Financial Record

```vague
schema Transaction {
  id: uuid()
  iban: iban()
  amount: faker.finance.amount(10, 1000, 2)
  currency: currencyCode()
  type: faker.finance.transactionType()
  timestamp: recentDate()
}
```
