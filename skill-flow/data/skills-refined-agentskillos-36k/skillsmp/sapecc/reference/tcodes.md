# SAP Transaction Code Quick Reference

## Materials Management (MM)

### Material Master
| T-Code | Description |
|--------|-------------|
| MM01 | Create Material |
| MM02 | Change Material |
| MM03 | Display Material |
| MM04 | Display Changes |
| MM06 | Flag for Deletion |
| MM17 | Mass Maintenance |
| MM50 | Extend Material |
| MM60 | Analysis of Materials |
| MMBE | Stock Overview |

### Purchasing
| T-Code | Description |
|--------|-------------|
| ME21N | Create Purchase Order |
| ME22N | Change Purchase Order |
| ME23N | Display Purchase Order |
| ME27 | Create Stock Transport Order |
| ME28 | Release Purchase Order |
| ME29N | Release PO (Coll) |
| ME2L | POs by Vendor |
| ME2M | POs by Material |
| ME2N | POs by PO Number |
| ME31K | Create Contract |
| ME32K | Change Contract |
| ME33K | Display Contract |
| ME51N | Create Purchase Requisition |
| ME52N | Change Purchase Requisition |
| ME53N | Display Purchase Requisition |
| ME54N | Release Purchase Requisition |
| ME55 | Collective Release |
| ME5A | List Display PRs |
| ME57 | Assign and Process PRs |
| ME59N | Auto PO Generation |

### Vendor Master
| T-Code | Description |
|--------|-------------|
| XK01 | Create Vendor (Centrally) |
| XK02 | Change Vendor (Centrally) |
| XK03 | Display Vendor (Centrally) |
| MK01 | Create Vendor (Purchasing) |
| MK02 | Change Vendor (Purchasing) |
| MK03 | Display Vendor (Purchasing) |

### Inventory Management
| T-Code | Description |
|--------|-------------|
| MIGO | Goods Movement |
| MB01 | Post Goods Receipt for PO |
| MB02 | Change Material Document |
| MB03 | Display Material Document |
| MB1A | Goods Issue |
| MB1B | Transfer Posting |
| MB1C | Other Goods Receipts |
| MB11 | Goods Movement |
| MB21 | Create Reservation |
| MB22 | Change Reservation |
| MB23 | Display Reservation |
| MB24 | Reservations by Material |
| MB31 | Goods Receipt for Prod Order |
| MB51 | Material Document List |
| MB52 | Warehouse Stocks |
| MB53 | Display Plant Stock Availability |
| MB54 | Consignment Stocks |
| MB58 | Cons. and Ret. Packaging at Customer |
| MI01 | Create Physical Inventory Doc |
| MI02 | Change Physical Inventory Doc |
| MI03 | Display Physical Inventory Doc |
| MI04 | Enter Count with Reference |
| MI05 | Change Count |
| MI06 | Display Count |
| MI07 | Process Difference List |
| MI08 | Create List of Differences |
| MI09 | Enter Count without Reference |
| MI10 | Create List with Count |
| MI11 | Recount Physical Inventory Doc |
| MI20 | Print List |
| MI21 | Print Physical Inventory Doc |
| MI31 | Batch Input: Create |
| MI32 | Batch Input: Block |
| MI33 | Batch Input: Freeze Book Inv |
| MI34 | Batch Input: Enter Count |
| MI35 | Batch Input: Post |
| MI37 | Batch Input: Freeze Stocks |
| MI38 | Batch Input: Unfreeze |
| MI39 | Batch Input: Enter Count and Diff |
| MI40 | Batch Input: Enter Recount |
| MIDO | Print Physical Inventory Doc |
| MIK1 | Batch Input: Phys. Inv. Vendor Cons. |
| MIQ1 | Batch Input: Phys. Inv. Project Stock |

### Invoice Verification
| T-Code | Description |
|--------|-------------|
| MIRO | Enter Invoice |
| MIR4 | Display Invoice |
| MIR5 | Display Invoice List |
| MIR6 | Invoice Overview |
| MIR7 | Park Invoice |
| MIRA | Enter Invoice - Fast Entry |
| MRRL | Evaluate Ret. Reqs |

### Source Determination
| T-Code | Description |
|--------|-------------|
| ME01 | Maintain Source List |
| ME03 | Display Source List |
| ME04 | Changes to Source List |
| ME05 | Generate Source List |
| ME06 | Analyze Source List |
| ME07 | Reorg Source List |
| ME08 | Send Source List |
| ME0M | Source List for Material |

---

## Production Planning (PP)

### Bill of Materials
| T-Code | Description |
|--------|-------------|
| CS01 | Create Material BOM |
| CS02 | Change Material BOM |
| CS03 | Display Material BOM |
| CS05 | Change BOM Group |
| CS06 | Display BOM Group |
| CS07 | Allocate Material BOM |
| CS08 | Change BOM Link to Mat |
| CS09 | Display BOM Link to Mat |
| CS11 | Display BOM Level by Level |
| CS12 | Multi-level BOM |
| CS13 | Summarized BOM |
| CS14 | BOM Comparison |
| CS15 | Single-Level Where-Used |
| CS20 | Mass Change |
| CS40 | Create Link to Config BOM |
| CS80 | Change Documents for BOM |

### Work Centers
| T-Code | Description |
|--------|-------------|
| CR01 | Create Work Center |
| CR02 | Change Work Center |
| CR03 | Display Work Center |
| CR05 | Workcenter List |
| CR06 | Workcenter Where-Used |
| CR07 | Workcenter Hierarchy |
| CR08 | Capacity Overview |

### Routings
| T-Code | Description |
|--------|-------------|
| CA01 | Create Routing |
| CA02 | Change Routing |
| CA03 | Display Routing |
| CA80 | Change Documents for Routings |

### Production Orders
| T-Code | Description |
|--------|-------------|
| CO01 | Create Production Order |
| CO02 | Change Production Order |
| CO03 | Display Production Order |
| CO04 | Rescheduling |
| CO05 | Collective Release |
| CO06 | Pick List |
| CO07 | Order With Auto GR |
| CO08 | Order Without Material |
| CO11N | Enter Confirmation |
| CO12 | Collective Confirmation |
| CO13 | Cancel Confirmation |
| CO14 | Display Confirmation |
| CO15 | Enter Confirmation (Auto GR) |
| CO16 | Display Processing |
| COFC | Execute Function |
| COGI | Automatic GI Errors |
| CO88 | Actual Settlement |
| CORK | Automatic Actual Cost Calc |
| KKS1 | Activity Price Revaluation |
| MF60 | Backflush |

### MRP
| T-Code | Description |
|--------|-------------|
| MD01 | MRP Run |
| MD02 | MRP - Single Item, Single Level |
| MD03 | MRP - Single Item, Multi Level |
| MD04 | Display Stock/Requirements List |
| MD05 | Display MRP List |
| MD06 | Collective Display MRP List |
| MD07 | Parts Overview |
| MD11 | Create Planned Order |
| MD12 | Change Planned Order |
| MD13 | Display Planned Order |
| MD14 | Collective Conversion |
| MD15 | Convert Planned Order to PO |
| MD16 | Convert Planned Order to Prod Order |
| MD20 | Create Planning File |
| MD21 | Display Planning File |
| MDAB | Set Up Planning File Entry |
| MDBT | MRP Evaluation |
| MDLD | Print MRP List |
| MDVP | Planning Result (VC) |

### Capacity Planning
| T-Code | Description |
|--------|-------------|
| CM01 | Capacity Planning |
| CM02 | Capacity Planning (Work Center) |
| CM04 | Capacity Requirements (Ind. Order) |
| CM05 | Capacity Planning (Work Center) |
| CM07 | Planning Table |
| CM21 | Capacity Leveling |
| CM22 | Variable View |
| CM25 | Extended Evaluation |
| CM50 | Capacity Leveling |
| CM51 | Capacity Leveling (Work Center) |

---

## Sales & Distribution (SD)

### Sales Orders
| T-Code | Description |
|--------|-------------|
| VA01 | Create Sales Order |
| VA02 | Change Sales Order |
| VA03 | Display Sales Order |
| VA05 | List of Sales Orders |
| VA11 | Create Inquiry |
| VA12 | Change Inquiry |
| VA13 | Display Inquiry |
| VA21 | Create Quotation |
| VA22 | Change Quotation |
| VA23 | Display Quotation |
| VA31 | Create Scheduling Agreement |
| VA32 | Change Scheduling Agreement |
| VA33 | Display Scheduling Agreement |
| VA41 | Create Contract |
| VA42 | Change Contract |
| VA43 | Display Contract |

### Delivery
| T-Code | Description |
|--------|-------------|
| VL01N | Create Outbound Delivery |
| VL02N | Change Outbound Delivery |
| VL03N | Display Outbound Delivery |
| VL04 | Control Goods Movement |
| VL06G | Goods Issue for Multiple Deliveries |
| VL06O | Outbound Deliveries for Shipment |
| VL06P | Picking for Multiple Deliveries |
| VL10A | Deliveries by Sales Order |
| VL10B | Deliveries by Purchasing |
| VL10C | Deliveries by Shipping Point |
| VL10D | Delivery Due List |
| VL31N | Create Inbound Delivery |
| VL32N | Change Inbound Delivery |
| VL33N | Display Inbound Delivery |

### Billing
| T-Code | Description |
|--------|-------------|
| VF01 | Create Billing Document |
| VF02 | Change Billing Document |
| VF03 | Display Billing Document |
| VF04 | Process Billing Due List |
| VF05 | List of Billing Documents |
| VF11 | Cancel Billing Document |
| VF21 | Create Invoice List |
| VF31 | Billing Output |

### Customer Master
| T-Code | Description |
|--------|-------------|
| XD01 | Create Customer (Centrally) |
| XD02 | Change Customer (Centrally) |
| XD03 | Display Customer (Centrally) |
| VD01 | Create Customer (Sales) |
| VD02 | Change Customer (Sales) |
| VD03 | Display Customer (Sales) |

### Pricing
| T-Code | Description |
|--------|-------------|
| VK11 | Create Condition |
| VK12 | Change Condition |
| VK13 | Display Condition |
| VK14 | Create with Reference |
| VK15 | Create Multiple |
| VK16 | Change Multiple |
| VK17 | Display Multiple |

---

## Quality Management (QM)

### Inspection
| T-Code | Description |
|--------|-------------|
| QA01 | Create Inspection Lot |
| QA02 | Change Inspection Lot |
| QA03 | Display Inspection Lot |
| QA08 | Trigger Recurring Inspection |
| QA10L | Collective Processing |
| QA11 | Record Usage Decision |
| QA12 | Change Usage Decision |
| QA13 | Display Usage Decision |
| QA32 | Change Data for Insp. Lot |
| QA33 | Display Insp. Lot Status |
| QE51N | Record Results |
| QE70 | Mass Results Recording |
| QE71 | Evaluation Mode |

### Quality Notifications
| T-Code | Description |
|--------|-------------|
| QM01 | Create Quality Notification |
| QM02 | Change Quality Notification |
| QM03 | Display Quality Notification |
| QM10 | Change Notification List |
| QM11 | Display Notification List |
| QM12 | Display Task List |
| QM13 | Display Action Item List |
| QM50 | Set Completion Date |

### Quality Certificates
| T-Code | Description |
|--------|-------------|
| QC21 | Create Certificate |
| QC22 | Change Certificate |
| QC23 | Display Certificate |

### Master Data
| T-Code | Description |
|--------|-------------|
| QP01 | Create Inspection Plan |
| QP02 | Change Inspection Plan |
| QP03 | Display Inspection Plan |
| QS21 | Create Master Inspection Char |
| QS22 | Change Master Inspection Char |
| QS23 | Display Master Inspection Char |
| QS31 | Create Catalog |
| QS32 | Change Catalog |
| QS33 | Display Catalog |

---

## Plant Maintenance (PM)

### Equipment
| T-Code | Description |
|--------|-------------|
| IE01 | Create Equipment |
| IE02 | Change Equipment |
| IE03 | Display Equipment |
| IE05 | Change Equipment Time |
| IE07 | Equipment List |
| IE08 | Equipment Installed Base |
| IE4N | Equipment Installation/Removal |

### Functional Locations
| T-Code | Description |
|--------|-------------|
| IL01 | Create Functional Location |
| IL02 | Change Functional Location |
| IL03 | Display Functional Location |
| IL04 | FL Structure Display |
| IL05 | Change FL Time |
| IL06 | Multi-Level FL |
| IL07 | FL List by Structure |

### Maintenance Orders
| T-Code | Description |
|--------|-------------|
| IW31 | Create Maintenance Order |
| IW32 | Change Maintenance Order |
| IW33 | Display Maintenance Order |
| IW34 | Create Order without Notification |
| IW36 | Create Order for Notification |
| IW37N | List Edit PM Order |
| IW38 | Change Orders |
| IW39 | Display Orders |
| IW41 | Enter PM Confirmation |
| IW42 | Overall Completion Confirm |
| IW44 | Display Confirmation |
| IW45 | Cancel PM Confirmation |

### Notifications
| T-Code | Description |
|--------|-------------|
| IW21 | Create PM Notification |
| IW22 | Change PM Notification |
| IW23 | Display PM Notification |
| IW24 | Create PM Notification (Malfunction) |
| IW25 | Create PM Notification (Activity) |
| IW26 | Create PM Notification (Service) |
| IW28 | Change Notifications |
| IW29 | Display Notifications |

### Preventive Maintenance
| T-Code | Description |
|--------|-------------|
| IP01 | Create Maintenance Plan |
| IP02 | Change Maintenance Plan |
| IP03 | Display Maintenance Plan |
| IP10 | Schedule Maintenance Plan |
| IP11 | Maintenance Plan Scheduling |
| IP15 | Change Item Manually |
| IP16 | Fiscal Year Change |
| IP17 | Deadline Overview |
| IP19 | Maintenance Scheduling Overview |
| IP24 | Call Maintenance Plan Schedule |
| IP30 | Deadline Monitoring |
| IP42 | Change Multiple Counter Plan |
| IP43 | Display Multiple Counter Plan |

---

## Finance (FI)

### General Ledger
| T-Code | Description |
|--------|-------------|
| FB01 | Post Document |
| FB02 | Change Document |
| FB03 | Display Document |
| FB05 | Post with Clearing |
| FB08 | Reverse Document |
| FB09 | Change Line Items |
| FB50 | Enter G/L Account Posting |
| FBL3N | G/L Line Item Display |
| FS10N | G/L Account Balance |

### Accounts Payable
| T-Code | Description |
|--------|-------------|
| FB60 | Enter Vendor Invoice |
| FB65 | Enter Vendor Credit Memo |
| FBL1N | Vendor Line Items |
| FK10N | Vendor Balance Display |
| F110 | Automatic Payment |

### Accounts Receivable
| T-Code | Description |
|--------|-------------|
| FB70 | Enter Customer Invoice |
| FB75 | Enter Customer Credit Memo |
| FBL5N | Customer Line Items |
| FD10N | Customer Balance Display |
| F-28 | Post Incoming Payment |

---

## Controlling (CO)

### Cost Centers
| T-Code | Description |
|--------|-------------|
| KS01 | Create Cost Center |
| KS02 | Change Cost Center |
| KS03 | Display Cost Center |
| KSB1 | Cost Center Line Items |
| KSBT | Cost Center Actual Totals |

### Internal Orders
| T-Code | Description |
|--------|-------------|
| KO01 | Create Internal Order |
| KO02 | Change Internal Order |
| KO03 | Display Internal Order |
| KOB1 | Order Line Items |
| KO88 | Order Settlement |

### Product Costing
| T-Code | Description |
|--------|-------------|
| CK11N | Create Cost Estimate |
| CK13N | Display Cost Estimate |
| CK24 | Cost Estimate without Quantity |
| CK40N | Costing Run |
| CKMLCP | Actual Costing Cockpit |

---

## Reporting

### Material Reports
| T-Code | Description |
|--------|-------------|
| MB52 | Warehouse Stocks |
| MBBS | Display Valuated Special Stock |
| MC.9 | Material Analysis |
| MC44 | Inventory Turnover |
| MC46 | Slow/Non-Moving Inventory |
| MC48 | Stock Analysis |
| MC50 | Usage Analysis |
| MCBA | Inventory Controlling |

### Production Reports
| T-Code | Description |
|--------|-------------|
| COOIS | Production Order Info System |
| CO03 | Display Order (Mass) |
| MF25 | Display Production List |
| MF26 | Selection Using Object List |

### Purchasing Reports
| T-Code | Description |
|--------|-------------|
| ME2L | POs by Vendor |
| ME2M | POs by Material |
| ME2N | POs by PO Number |
| ME2W | POs by Supplying Plant |
| ME80FN | Purchasing Reporting |
| ME1M | Quotation Price History |

---

## System Administration

| T-Code | Description |
|--------|-------------|
| SE16 | Data Browser |
| SE37 | Function Builder |
| SE38 | ABAP Editor |
| SE80 | Object Navigator |
| SM21 | System Log |
| SM37 | Background Job Overview |
| SM50 | Work Process Overview |
| SU01 | User Maintenance |
| SU3 | Maintain Own User Profile |
| SPRO | IMG (Customizing) |
