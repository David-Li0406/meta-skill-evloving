# Test Templates by Change Type

## UI Component Change

```markdown
### UI Test: [Component Name]

1. **Static**: TypeScript, lint
   - [ ] `npx tsc --noEmit` passes
   - [ ] `npm run lint` passes

2. **Visual**: Browser navigation
   - [ ] Navigate to [route]
   - [ ] Element renders correctly
   - [ ] Styling matches design

3. **Interaction**: User actions
   - [ ] Click handlers work
   - [ ] Hover states work
   - [ ] Input accepts data

4. **Responsive**: Multiple viewports
   - [ ] Desktop (1280px+)
   - [ ] Tablet (768-1279px)
   - [ ] Mobile (<768px)

5. **Console**: No errors
   - [ ] No React warnings
   - [ ] No runtime errors
```

## Server Action Change

```markdown
### Server Action Test: [Action Name]

1. **Static**: TypeScript, lint
   - [ ] Type checks pass
   - [ ] No lint errors

2. **Unit**: Direct invocation (if possible)
   - [ ] Happy path returns expected result
   - [ ] Error cases handled

3. **Integration**: Via UI trigger
   - [ ] Action triggered correctly
   - [ ] Response handled by UI

4. **Data**: DB state verification
   - [ ] Expected records created/updated
   - [ ] No orphaned data
   - [ ] Timestamps correct

5. **Errors**: Failure cases
   - [ ] Invalid input rejected
   - [ ] Auth failures handled
   - [ ] Network errors graceful
```

## Schema Change

```markdown
### Schema Test: [Table/Column]

1. **Migration**: Clean apply
   - [ ] Migration runs without error
   - [ ] Rollback works

2. **Data**: Existing data
   - [ ] No data loss
   - [ ] Defaults applied correctly

3. **RLS**: Policies
   - [ ] New policies work
   - [ ] Existing policies unbroken

4. **Actions**: Affected server actions
   - [ ] All actions still function
   - [ ] New columns accessible

5. **UI**: Data display
   - [ ] New data renders
   - [ ] Forms updated
```

## Workflow Change

```markdown
### Workflow Test: [Workflow Name]

1. **Full workflow**: Start to finish
   - [ ] Can complete entire journey
   - [ ] Each step accessible

2. **Each step**: Individual verification
   - [ ] Step 1: [action] → [result]
   - [ ] Step 2: [action] → [result]
   - [ ] Step N: [action] → [result]

3. **Edge cases**: Invalid paths
   - [ ] Invalid input rejected
   - [ ] Cancellation works
   - [ ] Back navigation works

4. **State**: End state
   - [ ] Data saved correctly
   - [ ] UI reflects changes

5. **Cross-role**: Multiple roles (if applicable)
   - [ ] Role A can complete
   - [ ] Role B sees correct state
```
