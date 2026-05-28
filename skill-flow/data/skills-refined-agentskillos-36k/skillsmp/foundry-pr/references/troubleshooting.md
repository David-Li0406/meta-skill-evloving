# Troubleshooting

## "Spec missing git.branch_name metadata"

**Problem**: Spec doesn't have branch information

**Solution**: Ensure git integration is enabled when creating the spec. The spec must have branch metadata.

## "Branch push failed"

**Problem**: Git push errors

**Solution**:
```bash
# Check remote
git remote -v

# Check credentials
git push -u origin <branch-name>
```

## "Diff too large"

**Problem**: Git diff exceeds size limit

**Solution**: Skill automatically shows file-level summary instead of full diff when it's too large.
