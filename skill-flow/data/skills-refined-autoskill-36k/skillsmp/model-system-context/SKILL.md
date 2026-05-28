---
name: model-system-context
description: Model C1 Context - define system boundary, identify external actors, external systems, and relationships. Establishes "what is the system and who uses it?"
---

# Model System Context (C1)

Use this skill to design the C1 Context diagram - the highest-level view of your system.

**Prerequisite:** Read `create-element` for basic element creation.

## What is C1 Context?

C1 answers: **"What is the system, who uses it, and what external systems does it interact with?"**

**Audience:** Everyone (business, technical, non-technical stakeholders)  
**Detail Level:** Highest overview - just system boundary and external interactions

## Step 1: Define the System

Define what the system IS and what it DOES:

```likec4
model {
  mySystem = System 'My Product' {
    description 'Core business system serving customers with secure file storage and processing'
  }
  
  // OR with more detail
  vault = System 'Secure Vault' {
    #production #security
    technology 'Distributed microservices'
    
    description """
      Secure file storage and processing system for enterprise clients.
      
      **Provides:**
      - Encrypted file storage
      - Automated malware scanning
      - Asynchronous job processing
      
      **Used by:** Customers and administrators
    """
  }
}
```

**Key:** Be clear about PURPOSE and SCOPE in description.

## Step 2: Identify External Actors

Determine WHO interacts with the system (primary actors/roles):

```likec4
model {
  // Individual people
  customer = Actor_Person 'Customer' {
    description 'End user uploading and retrieving files'
  }
  
  admin = Actor_Person 'Administrator' {
    description 'System administrator managing configuration and access'
  }
  
  // Automated users (bots, services)
  scanner = Actor_System 'Virus Scanner' {
    description 'External security scanning service'
  }
  
  // Infrastructure/access devices
  browser = Container_Browser 'Web Browser' {
    technology 'Chrome / Firefox / Safari'
    description 'User web browser for accessing the system'
  }
}
```

**Good practices:**
- Give each actor a clear, meaningful name
- Describe their role and why they interact with the system
- Distinguish between humans (Person) and automated/external systems
- Include access devices (browsers, mobile apps) if significant

## Step 3: Identify External Systems

Determine WHAT other systems your system integrates with:

```likec4
model {
  // Payment processing
  paymentGateway = System_Existing 'Payment Gateway' {
    description 'Third-party payment processing (Stripe)'
    #external
  }
  
  // Data integration
  warehouse = System_Existing 'Data Warehouse' {
    description 'Cloud data warehouse for analytics and reporting'
    #external
  }
  
  // Communication
  emailService = System_Existing 'Email Service' {
    description 'Third-party email delivery service'
    #external
  }
}
```

**Types of external systems:**
- ✅ SaaS services (payment, email, analytics)
- ✅ Partner systems (data exchanges, integrations)
- ✅ Legacy systems (mainframes, older applications)
- ✅ Infrastructure services (monitoring, logging)

## Step 4: Create C1 Relationships

Connect actors to your system and external systems:

```likec4
model {
  // Users interact with system
  customer -> vault 'Uses system to upload and retrieve files'
  admin -> vault 'Administers users and configuration'
  
  // External systems interact with your system
  vault -> paymentGateway 'Processes customer payments via'
  vault -> warehouse 'Sends analytics data to'
  vault -> emailService 'Sends notifications via'
  
  // External services interact with your system
  scanner -> vault 'Scans files in for malware'
}
```

**Relationship descriptions should be clear and specific:**
- ✅ "Uses system to upload and retrieve files"
- ✅ "Processes customer payments via"
- ❌ "Calls"
- ❌ "Communicates"

## C1 Complete Example

```likec4
model {
  // System
  vault = System 'Secure Vault' {
    #production #security
    description 'Secure file storage and processing system'
  }
  
  // Actors (who)
  customer = Actor_Person 'Customer' {
    description 'End user uploading and retrieving files'
  }
  
  admin = Actor_Person 'Administrator' {
    description 'System administrator managing configuration'
  }
  
  browser = Container_Browser 'Web Browser' {
    technology 'Chrome, Firefox, Safari'
    description 'User web browser for system access'
  }
  
  // External systems (what)
  scanner = Actor_System 'Virus Scanner' {
    description 'VirusTotal - external malware scanning service'
  }
  
  paymentGateway = System_Existing 'Payment Gateway' {
    #external
    description 'Stripe - payment processing'
  }
  
  // Relationships
  customer -> browser 'Uses'
  browser -> vault 'Uploads and retrieves files via'
  admin -> vault 'Administers'
  vault -> scanner 'Scans files via'
  vault -> paymentGateway 'Processes payments via'
}
```

## C1 View

Create the C1 Context view to visualize the boundary:

```likec4
views {
  view c1_context {
    title 'C1 / Secure Vault System'
    description 'System boundary with external users and integrations'
    
    include customer, browser, admin
    include vault
    include scanner, paymentGateway
    
    rank source { customer, admin }  // Users on top
    rank sink { scanner }             // External services below
  }
}
```

## C1 Design Checklist

- [ ] System clearly defined with purpose
- [ ] All primary actors (users/roles) identified
- [ ] All external systems identified
- [ ] All major relationships documented with clear labels
- [ ] One C1 Context view created
- [ ] View title and description explain what is shown
- [ ] External elements marked with `#external` tag

## Common Mistakes

| ❌ Don't | ✅ Do | Why |
|---|---|---|
| Vague system description | Clear purpose and scope | Viewers must understand what system does |
| Too many actors (one per user) | Group actors by role | C1 stays high-level, not detailed |
| Missing external systems | List all significant integrations | Gives complete picture of system interactions |
| Generic relationship labels | Specific labels describing interaction | "Uses payment service via Stripe" not just "Uses" |
| Skip C1 and start with C2 | Always do C1 first | Sets foundation for all subsequent levels |

## Next Steps

After defining C1:
1. Read `model-system-containers` to design C2 internals
2. Use `design-view` to organize the C1 view properly

## Related Skills

- `model-system-containers` - C2 Container design
- `create-element` - Creating individual elements
- `create-relationship` - Defining relationships
