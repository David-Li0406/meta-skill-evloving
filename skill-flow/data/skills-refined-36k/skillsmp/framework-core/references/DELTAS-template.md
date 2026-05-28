# Delta Inventory

Deltas (work items) extracted from VISION.md for [project name].

## Status Tracking

Deltas track their progress through the development workflow using a status field:

- **✗ Defined** - Delta extracted and documented (initial state)
- **⧗ Spec** - Specification in progress (`/spec-delta` started)
- **✓ Spec** - Specification complete (`/spec-delta` done)
- **⧗ Design** - Design rationale in progress (`/design-delta` started)
- **✓ Design** - Design complete (`/design-delta` done)
- **⧗ Plan** - Implementation plan in progress (`/plan-delta` started)
- **✓ Plan** - Implementation plan complete (`/plan-delta` done)
- **⧗ Implementation** - Delta implementation in progress (`/implement-delta` started)
- **✓ Implementation** - Delta complete and tested (`/implement-delta` done)
- **✓ Reconciled** - Feature documentation updated (`/reconcile-delta` done)

Commands automatically update status as they progress. To manually update:
```bash
python scripts/deltas.py status set DELTA-ID "STATUS"
```

Query status:
```bash
python scripts/deltas.py status list                    # All deltas
python scripts/deltas.py status list --complexity Easy  # Filter by complexity
python scripts/deltas.py status show DELTA-ID           # Detailed view
```

---

## Deltas

### DLT-001: [Delta name]
**Status**: ✗ Defined
**Complexity**: [Easy/Medium/Hard]
**Description**: [Comprehensive description that explains what the delta does and why it's needed. Should be self-explanatory without reading the spec.]

### DLT-002: [Delta name]
**Status**: ✗ Defined
**Complexity**: [Easy/Medium/Hard]
**Description**: [Comprehensive description that explains what the delta does and why it's needed. Should be self-explanatory without reading the spec.]

---

## Notes

- [Relevant notes about delta relationships]
- [Dependencies or interactions to be aware of]
