# SAP ECC Expert - Extended Context

**Deep dive guidance for SAP ECC operations in automotive manufacturing environments.**

---

## Table of Contents

1. [System Architecture Understanding](#system-architecture-understanding)
2. [Master Data Best Practices](#master-data-best-practices)
3. [End-to-End Process Flows](#end-to-end-process-flows)
4. [Integration Scenarios](#integration-scenarios)
5. [Troubleshooting Guide](#troubleshooting-guide)
6. [Configuration Essentials](#configuration-essentials)
7. [Automotive-Specific Considerations](#automotive-specific-considerations)
8. [Performance Optimization](#performance-optimization)

---

## System Architecture Understanding

### SAP ECC Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                      SAP ECC SYSTEM                             │
├─────────────────────────────────────────────────────────────────┤
│  PRESENTATION LAYER                                             │
│  ├── SAP GUI (Windows/Java/HTML)                               │
│  ├── Web Dynpro Applications                                    │
│  └── SAP Fiori (if enabled)                                    │
├─────────────────────────────────────────────────────────────────┤
│  APPLICATION LAYER                                              │
│  ├── Business Logic (ABAP)                                     │
│  ├── Work Processes (Dialog, Background, Update, Spool)        │
│  └── Application Services                                       │
├─────────────────────────────────────────────────────────────────┤
│  DATABASE LAYER                                                 │
│  ├── SAP Tables (Transparent, Pool, Cluster)                   │
│  ├── Database Views                                            │
│  └── Database Indexes                                          │
└─────────────────────────────────────────────────────────────────┘
```

### Organizational Structure

```
Client (Mandt)
    │
    ├── Company Code (BUKRS)
    │       │
    │       └── Controlling Area (KOKRS)
    │               │
    │               └── Cost Centers, Profit Centers
    │
    ├── Plant (WERKS)
    │       │
    │       ├── Storage Locations (LGORT)
    │       │
    │       └── Shipping Points (VSTEL)
    │
    ├── Purchasing Organization (EKORG)
    │       │
    │       └── Purchasing Groups (EKGRP)
    │
    └── Sales Organization (VKORG)
            │
            ├── Distribution Channel (VTWEG)
            │
            └── Division (SPART)
```

### Key Tables Reference

| Area | Table | Description |
|------|-------|-------------|
| Material | MARA | General Material Data |
| Material | MARC | Plant Data for Material |
| Material | MARD | Storage Location Data |
| Material | MBEW | Material Valuation |
| BOM | STKO | BOM Header |
| BOM | STPO | BOM Items |
| Routing | PLKO | Routing Header |
| Routing | PLPO | Routing Operations |
| Purchase | EKKO | PO Header |
| Purchase | EKPO | PO Line Items |
| Production | AUFK | Order Master Data |
| Production | AFKO | Order Header Data |
| Production | AFPO | Order Item Data |
| Inventory | MKPF | Material Doc Header |
| Inventory | MSEG | Material Doc Items |
| Quality | QALS | Inspection Lot Header |
| Quality | QAVE | Inspection Lot Usage Decision |

---

## Master Data Best Practices

### Material Master Strategy

**Creation Workflow:**
1. Define material type (ROH, HALB, FERT, etc.)
2. Determine required views based on usage
3. Complete mandatory fields for each view
4. Validate with cross-functional team
5. Mass extend to additional plants if needed

**View Selection by Material Type:**

| Mat Type | Basic | Purch | MRP | Acc | Costing | Sales | QM |
|----------|-------|-------|-----|-----|---------|-------|-----|
| ROH (Raw) | ✓ | ✓ | ✓ | ✓ | ✓ | | ✓ |
| HALB (Semi) | ✓ | | ✓ | ✓ | ✓ | | ✓ |
| FERT (Finished) | ✓ | | ✓ | ✓ | ✓ | ✓ | ✓ |
| HAWA (Trading) | ✓ | ✓ | ✓ | ✓ | | ✓ | |

**Critical Fields by View:**

**MRP 1:**
- MRP Type (DISMM): Controls planning behavior
- MRP Controller (DISPO): Responsible planner
- Lot Size (DISLS): Determines order quantities

**MRP 2:**
- Procurement Type (BESKZ): E=In-house, F=External
- Safety Stock (EISBE): Buffer quantity
- Planned Delivery Time (PLIFZ): Vendor lead time

**MRP 3:**
- Strategy Group (STRGR): Planning strategy
- Consumption Mode (VRMOD): Backward/Forward

**MRP 4:**
- Scheduling Margin Key (FHORI): Float times
- In-house Production Time (DZEIT): Manufacturing lead time

### BOM Best Practices

**Structure Guidelines:**
- Use phantom assemblies for intermediate sub-assemblies
- Set correct BOM usage (1=Production, 2=Engineering)
- Maintain valid-from/valid-to dates
- Use alternative BOMs for variant products
- Link to change numbers for traceability

**Component Data:**
- Accurate quantities with correct UoM
- Operation assignment for backflushing
- Scrap percentage where applicable
- Bulk material flag for consumables

### Routing Best Practices

**Operation Setup:**
- Realistic standard values (setup, machine, labor)
- Correct work center assignment
- Control key for confirmation behavior
- Operation scrap for yield loss

**Work Center Configuration:**
- Capacity category (001=labor, 002=machine)
- Available capacity hours
- Efficiency rate/utilization
- Cost center assignment
- Formulas for activity calculation

---

## End-to-End Process Flows

### Procure-to-Pay (P2P)

```
1. REQUIREMENT DETERMINATION
   └── MRP creates planned orders or manual PR (ME51N)

2. SOURCE DETERMINATION
   └── Check source list, contracts, info records
   └── Assign supplier

3. PURCHASE ORDER CREATION
   └── Convert PR to PO (ME21N) or auto-generate (ME59N)
   └── PO Release (ME28) if strategy configured

4. GOODS RECEIPT
   └── Post GR against PO (MIGO - 101)
   └── If QM active: Stock to Quality Inspection
   └── Usage Decision (QA11): Release to unrestricted

5. INVOICE VERIFICATION
   └── Enter invoice (MIRO)
   └── 3-way match: PO vs GR vs Invoice
   └── Handle variances (price, quantity)

6. PAYMENT
   └── Automatic payment run (F110)
   └── Consider early payment discounts
```

**Key Control Points:**
- Purchase order release strategy
- Goods receipt tolerance
- Invoice tolerance
- Payment block handling

### Plan-to-Produce

```
1. DEMAND PLANNING
   └── Sales orders, forecasts, stock requirements
   └── Independent requirements (MD61)

2. MRP RUN
   └── Total planning (MD01) or single-item (MD02)
   └── Generates planned orders for materials

3. ORDER CREATION
   └── Convert planned orders to production orders
   └── CO01 (manual) or MD04 (from list)

4. ORDER RELEASE
   └── Release order (CO02) to production
   └── Print shop papers, pick lists

5. MATERIAL STAGING
   └── Issue components to order (MIGO - 261)
   └── Pick list creation (CO27)

6. PRODUCTION EXECUTION
   └── Operations on shop floor
   └── Time confirmations (CO11N)

7. GOODS RECEIPT
   └── Receive finished goods (MIGO - 101)
   └── Stock posting to finished goods

8. ORDER COMPLETION
   └── Technical completion (TECO)
   └── Settlement to cost object (CO88)
   └── Close order (CLSD)
```

**Key Control Points:**
- MRP controller workload
- Capacity availability
- Material availability
- Order status management

### Order-to-Cash (O2C)

```
1. PRE-SALES
   └── Inquiry (VA11), Quotation (VA21)

2. ORDER ENTRY
   └── Create sales order (VA01)
   └── Pricing, availability check, credit check

3. DELIVERY
   └── Create delivery (VL01N)
   └── Picking, packing
   └── Goods issue (VL02N)

4. BILLING
   └── Create invoice (VF01)
   └── Accounting document created

5. PAYMENT
   └── Post incoming payment (F-28)
   └── Clear customer open item
```

---

## Integration Scenarios

### MM-PP Integration

| Trigger | MM Action | PP Action |
|---------|-----------|-----------|
| MRP Run | Creates PRs | Creates Planned Orders |
| Prod Order Release | - | Triggers availability check |
| GI to Prod Order | 261 movement | Reduces reservation |
| GR from Prod Order | 101 movement | Updates order |

### MM-QM Integration

| Trigger | MM Action | QM Action |
|---------|-----------|-----------|
| GR with Inspection | Stock to QI (103) | Creates Inspection Lot |
| Usage Decision | Stock posting | Records decision |
| Vendor Evaluation | - | Updates vendor score |

### PP-CO Integration

| Trigger | PP Action | CO Action |
|---------|-----------|-----------|
| Order Creation | - | Creates CO order |
| Confirmations | Activity postings | Cost allocation |
| Settlement | - | Variance analysis |

### SD-MM Integration

| Trigger | SD Action | MM Action |
|---------|-----------|-----------|
| Sales Order | ATP Check | Checks stock |
| Delivery | - | Reserves stock |
| Goods Issue | - | 601 movement |

---

## Troubleshooting Guide

### MRP Issues

**Problem: MRP not generating planned orders**
1. Check planning file entry (MD21)
2. Verify MRP type in material master
3. Check lot size procedure
4. Review MRP area configuration
5. Check for fixed planned orders

**Problem: Wrong quantities proposed**
1. Review lot size parameters
2. Check rounding values
3. Verify scrap percentages
4. Review safety stock settings

### Production Order Issues

**Problem: Cannot release order**
1. Check component availability (CO02 - Components)
2. Verify material status (blocked, not active)
3. Check capacity availability
4. Review order type configuration

**Problem: GI posting fails (COGI)**
1. Check available stock (MMBE)
2. Verify storage location determination
3. Check for blocked stock
4. Review backflush errors

### Inventory Issues

**Problem: Negative stock**
1. Check posting sequence
2. Review goods movements
3. Verify reservation status
4. Check for parallel postings

**Problem: Stock doesn't match**
1. Run inventory report (MB52)
2. Check material documents (MB51)
3. Review blocked/QI stock
4. Verify storage location

### Purchase Order Issues

**Problem: PO blocked for release**
1. Check release strategy (ME28)
2. Verify release codes
3. Review approval workflow
4. Check document changes

**Problem: GR blocked**
1. Verify QM inspection type
2. Check delivery tolerance
3. Review PO item status
4. Check material block

---

## Configuration Essentials

### Key IMG Paths

**Materials Management:**
```
SPRO → MM → Purchasing → Purchase Order
SPRO → MM → Inventory Management → Goods Receipt
SPRO → MM → Logistics Invoice Verification
```

**Production Planning:**
```
SPRO → Production → Shop Floor Control → Operations
SPRO → Production → MRP → Plant Parameters
SPRO → Production → Basic Data → Work Centers
```

**Sales & Distribution:**
```
SPRO → SD → Basic Functions → Pricing
SPRO → SD → Sales → Sales Documents
SPRO → SD → Shipping → Deliveries
```

### Critical Configuration Tables

| Table | Description |
|-------|-------------|
| T001 | Company Codes |
| T001W | Plants |
| T001K | Valuation Areas |
| T001L | Storage Locations |
| T024 | Purchasing Groups |
| T156 | Movement Types |
| T134 | Material Types |
| T438 | Production Scheduling Profile |

---

## Automotive-Specific Considerations

### JIT/JIS (Just-in-Time/Just-in-Sequence)

**SAP Modules:**
- JIT Inbound Processing
- JIT Outbound Processing (SD)
- Sequenced delivery scheduling

**Key Transactions:**
- JITOM: JIT Outbound Monitor
- JITIM: JIT Inbound Monitor

### EDI Integration

**Common IDOC Types:**
- ORDERS: Purchase Orders
- DESADV: Delivery Schedule
- INVOIC: Invoice
- DELFOR: Delivery Forecast

### Batch Management

**Key Considerations:**
- Batch determination in production
- Shelf life management (FIFO)
- Batch traceability for recalls
- Batch protocols for quality

**Configuration:**
- Batch level (plant/material)
- Batch number assignment
- Classification for batch search

### Serial Number Management

**Use Cases:**
- High-value components
- Warranty tracking
- Traceability requirements

**Configuration:**
- Serial number profiles
- Serialization procedures
- Stock/equipment serialization

---

## Performance Optimization

### MRP Performance

**Best Practices:**
1. Use planning file regeneration off-peak
2. Set up MRP controllers by material groups
3. Use parallel processing (MDCPS)
4. Clean up planned orders regularly
5. Optimize lot sizes to reduce nervousness

### Report Performance

**Optimization Tips:**
1. Use variants with narrow selections
2. Schedule long reports in background
3. Use ALV layouts efficiently
4. Archive old documents
5. Index frequently searched fields

### Data Volume Management

**Key Areas:**
- Document archiving (purchase orders, material docs)
- Reorganization of transactional data
- Index optimization
- Table partitioning

---

## Quick Reference Cards

### Daily Operations Checklist

**Morning:**
- [ ] Check COGI for backflush errors
- [ ] Review MRP exception messages (MD07)
- [ ] Check blocked invoices (MRBR)
- [ ] Review delivery due list (VL10)

**Throughout Day:**
- [ ] Process purchase requisitions
- [ ] Confirm production orders
- [ ] Handle goods receipts
- [ ] Address quality holds

**End of Day:**
- [ ] Check unprocessed orders
- [ ] Review open deliveries
- [ ] Check payment blocks
- [ ] Plan next day workload

### Month-End Checklist

- [ ] Complete all goods movements
- [ ] Process invoice backlog
- [ ] Run CKMG (Material Ledger close)
- [ ] Execute CO88 (Order settlement)
- [ ] Verify inventory accuracy
- [ ] Run financial close transactions

---

## Integration with PAI Skills

### AutomotiveManufacturing
- Work instructions reference SAP t-codes
- Quality procedures link to QM transactions
- Control plans connect to inspection plans

### SupplyChain
- Purchasing strategies align with MM processes
- Supplier management uses QM data
- Inventory optimization through MRP tuning

### A3CriticalThinking
- Root cause analysis for SAP process failures
- Priority hierarchy for system change decisions
- Structured problem-solving for integration issues

---

## Resources

**Transaction Code Reference:**
`read ~/.claude/skills/SapEcc/reference/tcodes.md`

**SAP Documentation:**
- SAP Help Portal (help.sap.com)
- SAP Community Network
- SAP Notes (service.sap.com)

**Internal Standards:**
- Company-specific procedures
- Naming conventions
- Change management process
