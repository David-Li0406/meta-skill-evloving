---
title: Account Signup & Plan Selection Flow
author: @product-design
status: implemented
date: 2026-01-13
instruction: "Copy this template for multi-step user journeys. Include overview, flow diagram, each step with interactive examples, error handling, and success states."
tags: ["user-flow", "design", "UX"]
related-jtbd: "Prototype features"
---

# Account Signup & Plan Selection Flow

## Overview

New visitors land on our homepage, click a CTA, and enter our signup funnel. They provide email, select a plan tier, confirm their details, and are sent a confirmation email. Goal: get them from "curious visitor" to "paying customer" in under 3 minutes with zero friction.

**Entry point**: Homepage CTA button ("Get Started")  
**Goal**: Create account and select billing plan  
**Exit point**: Confirmation email sent, user can log in immediately

## Flow Diagram

```
[Entry] → Step 1 → Step 2 → Step 3 → [Success]
                ↓
            [Error Handling]
```

---
## Step 1: Welcome

*What happens in this step? What decisions does the user make?*

```jsx live
export default function Step1() {
  const [email, setEmail] = React.useState('');
  
  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow">
      <div className="text-sm text-gray-500 mb-4">Step 1 of 3</div>
      <h2 className="text-xl font-bold mb-4">Welcome! Let's get started</h2>
      <p className="text-gray-600 mb-6">
        First, we need some basic information.
      </p>
      <input 
        type="email" 
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Enter your email"
        className="w-full px-4 py-2 border rounded mb-4"
      />
      <button 
        className={`w-full py-2 rounded transition-colors ${
          email ? 'bg-blue-500 text-white hover:bg-blue-600' : 'bg-gray-300 text-gray-500 cursor-not-allowed'
        }`}
        disabled={!email}
      >
        Continue
      </button>
    </div>
  );
}
```

Users must provide a valid email—this is their account identity. The form validates on blur and displays errors inline so they know immediately if something's wrong. Continue is disabled until they've entered something in the email field.

---

## Step 2: Selection

*What happens next? What are the user's options?*

```jsx live
export default function Step2() {
  const [selected, setSelected] = React.useState(null);
  const options = [
    { id: 'personal', label: 'Personal', desc: 'For individual use' },
    { id: 'team', label: 'Team', desc: 'For small teams' },
    { id: 'enterprise', label: 'Enterprise', desc: 'For large organizations' },
  ];
  
  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow">
      <div className="text-sm text-gray-500 mb-4">Step 2 of 3</div>
      <h2 className="text-xl font-bold mb-4">Choose your plan</h2>
      <div className="space-y-3 mb-6">
        {options.map(opt => (
          <button
            key={opt.id}
            onClick={() => setSelected(opt.id)}
            className={`w-full p-4 border rounded-lg text-left transition-colors ${
              selected === opt.id ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <div className="font-medium">{opt.label}</div>
            <div className="text-sm text-gray-500">{opt.desc}</div>
          </button>
        ))}
      </div>
      <div className="flex gap-3">
        <button className="flex-1 py-2 border border-gray-300 rounded hover:bg-gray-50">Back</button>
        <button className={`flex-1 py-2 text-white rounded transition-colors ${
          selected ? 'bg-blue-500 hover:bg-blue-600' : 'bg-gray-300 cursor-not-allowed'
        }`} disabled={!selected}>
          Continue
        </button>
      </div>
    </div>
  );
}
```

**User can**:
- Select one of three plan types
- Review descriptions before selecting
- Navigate back or continue

**Validation**:
Three plan options are presented with clear descriptions of who each serves. Users compare and select. The Continue button won't activate until they've chosen—this prevents accidental progression. They can also go back to fix their email if they made a typo.

```jsx live
export default function Step3() {
  const [confirmed, setConfirmed] = React.useState(false);
  
  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow">
      <div className="text-sm text-gray-500 mb-4">Step 3 of 3</div>
      <h2 className="text-xl font-bold mb-4">Confirm your details</h2>
      <div className="bg-gray-50 p-4 rounded mb-6">
        <div className="text-sm text-gray-600 mb-2">Selected plan: <strong>Team</strong></div>
        <div className="text-sm text-gray-600">Monthly billing</div>
      </div>
      
      <label className="flex items-center gap-2 mb-6 cursor-pointer">
        <input
          type="checkbox"
          checked={confirmed}
          onChange={(e) => setConfirmed(e.target.checked)}
          className="w-4 h-4"
        />
        <span className="text-sm">I agree to the terms and conditions</span>
      </label>
      
      <div className="flex gap-3">
        <button className="flex-1 py-2 border border-gray-300 rounded hover:bg-gray-50">Back</button>
        <button 
          className={`flex-1 py-2 text-white rounded transition-colors ${
            confirmed ? 'bg-green-500 hover:bg-green-600' : 'bg-gray-300 cursor-not-allowed'
          }`}
          disabled={!confirmed}
        >
          Complete Setup
        </button>
      </div>
    </div>
  );
}
```

**User can**:
- Review their selections
- Agree to terms
- Complete the flow

---
This is the final confirmation step. The system shows them exactly what they selected (plan type and billing frequency). Checkbox for terms prevents accidental signup. Once they check the box and click "Complete Setup," we create their account, send a confirmation email, and they land on the dashboard.ds to invalid inputs or problems:

```jsx live
export default function ErrorState() {
  return (
    <div className="max-w-md mx-auto p-6 bg-red-50 rounded-lg border border-red-200 shadow">
      <div className="text-sm text-red-600 mb-4">⚠️ Validation Error</div>
      <h2 className="text-xl font-bold text-red-800 mb-4">Email format invalid</h2>
      <p className="text-red-700 mb-6">
        Please enter a valid email address (example@domain.com).
      </p>
      <button className="w-full py-2 bg-red-600 text-white rounded hover:bg-red-700">
        Try Again
      </button>
    </div>
  );
}
```

---

## Success State

What the user sees upon successful completion:

```jsx live
export default function SuccessState() {
  return (
    <div className="max-w-md mx-auto p-6 bg-green-50 rounded-lg border border-green-200 shadow">
      <div className="text-4xl mb-4">✅</div>
      <h2 className="text-2xl font-bold text-green-800 mb-2">Welcome!</h2>
      <p className="text-green-700 mb-6">
        Your account is all set. You now have access to all Team features.
      </p>
      <button className="w-full py-2 bg-green-600 text-white rounded hover:bg-green-700">
        Go to Dashboard
      </button>
    </div>
  );
}
```

---
*Created with [Reactive MD](https://marketplace.visualstudio.com/items?itemName=million-views.reactive-md)*
