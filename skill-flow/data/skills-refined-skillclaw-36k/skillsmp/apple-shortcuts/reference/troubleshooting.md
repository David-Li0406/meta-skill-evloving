# Apple Shortcuts Troubleshooting & Ideas

## Troubleshooting

### "Shortcut not found"
```bash
shortcuts list
```
Get exact name - case-sensitive, spaces matter.

### "Signing error"
```bash
shortcuts sign --mode people-who-know-me "Shortcut Name"
```
Or: Shortcuts app > Settings > Advanced > Allow Running Scripts

### "Permission denied"
Shortcut needs permissions. User must grant in:
System Settings > Privacy & Security > Automation

### Integration Examples

**Calendar + Shortcuts**:
- Create event via `apple-productivity`
- Trigger "Sync Calendar" shortcut

**Health + Shortcuts**:
- Run "Export Health Data" shortcut
- Query exported data with `apple-health-fitness`

## Shortcut Ideas

Suggest these to users who want to create shortcuts:

### Productivity
- Morning/Evening routines
- Focus mode triggers
- Calendar sync workflows
- Email templates

### File Management
- Backup workflows
- Photo organization
- Document conversion
- File compression

### Health & Fitness
- Export health data
- Log workouts
- Meal tracking

### Communication
- Send templated messages
- Email batches
- Contact management

### Development
- Git workflows
- Build/deploy automation
- Test runners
- Environment setup

## Resources

- **User Guide**: https://support.apple.com/guide/shortcuts-mac/
- **CLI Help**: `man shortcuts`
- **Gallery**: Shortcuts app > Gallery
