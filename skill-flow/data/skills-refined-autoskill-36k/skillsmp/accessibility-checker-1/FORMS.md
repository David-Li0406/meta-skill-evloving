# Accessible Forms Reference

## Labels

Every form control MUST have a label:

### Explicit Association (Preferred)

```html
<label for="username">Username</label>
<input type="text" id="username" name="username"/>
```

### Implicit Association

```html
<label>
  Username
  <input type="text" name="username"/>
</label>
```

### Hidden Labels (when visual label exists elsewhere)

```html
<label for="search" class="visually-hidden">Search</label>
<input type="search" id="search" name="q" placeholder="Search..."/>
<button type="submit">Search</button>
```

## Fieldsets and Legends

Group related controls:

```html
<fieldset>
  <legend>Contact Preferences</legend>

  <label>
    <input type="checkbox" name="contact" value="email"/>
    Email
  </label>

  <label>
    <input type="checkbox" name="contact" value="phone"/>
    Phone
  </label>

  <label>
    <input type="checkbox" name="contact" value="mail"/>
    Mail
  </label>
</fieldset>
```

## Radio Groups

```html
<fieldset>
  <legend>Shipping Method</legend>

  <label>
    <input type="radio" name="shipping" value="standard"/>
    Standard (5-7 days)
  </label>

  <label>
    <input type="radio" name="shipping" value="express"/>
    Express (2-3 days)
  </label>

  <label>
    <input type="radio" name="shipping" value="overnight"/>
    Overnight
  </label>
</fieldset>
```

## Required Fields

```html
<label for="email">
  Email Address
  <span aria-hidden="true">*</span>
</label>
<input type="email" id="email" name="email" required="" aria-required="true"/>
```

## Error Messages

```html
<label for="password">Password</label>
<input type="password" id="password" name="password"
       aria-describedby="password-error" aria-invalid="true"/>
<p id="password-error" role="alert">
  Password must be at least 8 characters
</p>
```

## Help Text

```html
<label for="dob">Date of Birth</label>
<input type="date" id="dob" name="dob" aria-describedby="dob-hint"/>
<p id="dob-hint">Format: MM/DD/YYYY</p>
```

## Complete Form Example

```html
<form action="/register" method="post">
  <h2>Create Account</h2>

  <fieldset>
    <legend>Account Information</legend>

    <label for="email">Email Address <span aria-hidden="true">*</span></label>
    <input type="email" id="email" name="email" required="" autocomplete="email"/>

    <label for="password">Password <span aria-hidden="true">*</span></label>
    <input type="password" id="password" name="password" required=""
           aria-describedby="password-requirements" autocomplete="new-password"/>
    <p id="password-requirements">
      Must be at least 8 characters with one number
    </p>
  </fieldset>

  <fieldset>
    <legend>Preferences</legend>

    <label>
      <input type="checkbox" name="newsletter" value="yes"/>
      Subscribe to newsletter
    </label>
  </fieldset>

  <button type="submit">Create Account</button>
</form>
```

## Autocomplete

Use autocomplete for common fields:

| Field | Autocomplete Value |
|-------|-------------------|
| Name | `name` |
| Email | `email` |
| Phone | `tel` |
| Address | `street-address` |
| City | `address-level2` |
| State | `address-level1` |
| ZIP | `postal-code` |
| Country | `country-name` |
| Credit Card | `cc-number` |
| Password | `current-password` or `new-password` |
