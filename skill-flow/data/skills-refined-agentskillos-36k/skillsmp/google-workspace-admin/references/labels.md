# Data Classification Labels Reference

## Overview

Google Drive labels enable data classification for governance, DLP, and compliance. Labels are created in Admin Console but can be applied/queried via GAM.

## Label Types

**Badged Labels**: Visually emphasized, displayed next to file name. Only one badged label per file. Used for most important metadata (e.g., sensitivity classification).

**Standard Labels**: Multiple allowed per file. Can have multiple fields (text, date, selection, user).

## Creating Labels (Admin Console Only)

1. Admin Console > Security > Access and data control > Data classification
2. Click "Label Manager"
3. Click "+ New label"
4. Configure:
   - Label name (e.g., "Data Sensitivity")
   - Label type (badged or standard)
   - Fields (e.g., selection list: Public, Internal, Confidential, Restricted)
   - Who can view/apply

⚠️ **API Limitation**: Labels cannot be created via API—only Admin Console.

## GAM Label Commands

### List Labels
```bash
# All labels in domain
gam print drivelabels todrive

# Label details
gam info drivelabel labels/<label_id>

# Label fields
gam info drivelabel labels/<label_id> showfields
```

### Apply Labels to Files
```bash
# Apply label with selection field
gam user user@domain.com update drivefile id:<file_id> \
  addlabel labels/<label_id> field.<field_id> selection <choice_id>

# Apply label with text field
gam user user@domain.com update drivefile id:<file_id> \
  addlabel labels/<label_id> field.<field_id> text "Project Alpha"

# Apply label with date field
gam user user@domain.com update drivefile id:<file_id> \
  addlabel labels/<label_id> field.<field_id> date 2025-12-31

# Apply label with user field
gam user user@domain.com update drivefile id:<file_id> \
  addlabel labels/<label_id> field.<field_id> user owner@domain.com
```

### Query Files by Label
```bash
# Files with specific label
gam user user@domain.com print filelist query "labels/<label_id>" todrive

# Files with specific label value
gam user user@domain.com print filelist query "labels/<label_id>.fields.<field_id>.selection = '<choice_id>'" todrive

# All domain files with label (requires domain-wide delegation)
gam all users print filelist query "labels/<label_id>" todrive
```

### Remove Labels
```bash
gam user user@domain.com update drivefile id:<file_id> removelabel labels/<label_id>
```

### Bulk Operations
```bash
# CSV: user,file_id,label_id,field_id,choice_id
gam csv classify.csv gam user ~user update drivefile id:~file_id addlabel labels/~label_id field.~field_id selection ~choice_id

# Find and label (two-step)
# Step 1: Export files to CSV
gam user user@domain.com print filelist query "name contains 'Contract'" fields id,name todrive
# Step 2: Apply labels from CSV
gam csv contracts.csv gam user user@domain.com update drivefile id:~id addlabel labels/<label_id> field.<field_id> selection <choice_id>
```

## Data Tagging Project Workflow

### Phase 1: Setup
1. Define classification taxonomy (e.g., Public/Internal/Confidential/Restricted)
2. Create labels in Admin Console
3. Configure who can view/apply each label
4. Set default labels per OU if needed

### Phase 2: Discovery
```bash
# Export all files
gam all users print filelist fields id,name,mimeType,owners,permissions todrive

# Find externally shared
gam all users print filelist query "visibility='anyoneWithLink'" todrive

# Find files by type
gam all users print filelist query "mimeType='application/pdf'" todrive
```

### Phase 3: Classification
```bash
# Manual bulk classification from CSV
gam csv classified_files.csv gam user ~owner update drivefile id:~id addlabel labels/<label_id> field.<field_id> selection ~classification

# Consider DLP rules for auto-classification in Admin Console
```

### Phase 4: Enforcement
- Configure DLP rules to block sharing based on labels
- Set up alerts for label changes
- Regular audits via `gam report drive`

## DLP Integration

Labels can be used as DLP rule conditions/actions in Admin Console:
- **Condition**: "If file has label X, then..."
- **Action**: "Apply label X when content matches..."

DLP-applied labels take priority over user-applied labels.

## Audit & Compliance

```bash
# Label activity in Drive audit
gam report drive event label_applied start -30d todrive
gam report drive event label_removed start -30d todrive

# Files with specific classification
gam all users print filelist query "labels/<label_id>.fields.<field_id>.selection = '<restricted_choice_id>'" fields id,name,owners,permissions todrive
```

## Common Issues

**"Label not found"**: Verify label is published and user has permission to apply.

**"Field not found"**: Use `gam info drivelabel labels/<id> showfields` to get exact field IDs.

**"Cannot apply label"**: User needs edit access to file AND permission to apply the label.

**Rate limits**: For bulk operations, GAM handles throttling automatically but large batches may take time.
