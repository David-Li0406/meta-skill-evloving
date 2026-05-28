<batch_operations>
Updating descriptions for multiple revisions requires careful bash syntax.

<anti_pattern>
```bash
for rev in abc def ghi; do
  jj log -r $rev | sed 's/old/new/' | jj desc -r $rev --stdin
done
```

Issues:
1. Missing `-n1 --no-graph -T description` (gets formatted log)
2. Unquoted variables can break with special chars
3. Complex pipes are fragile
</anti_pattern>

<pattern name="intermediate_files">
```bash
for rev in abc def ghi; do
  jj log -r "$rev" -n1 --no-graph -T description > /tmp/desc_${rev}_old.txt
  sed 's/old/new/' /tmp/desc_${rev}_old.txt > /tmp/desc_${rev}_new.txt
  jj desc -r "$rev" --stdin < /tmp/desc_${rev}_new.txt
done
```

Benefits:
- Each step visible and debuggable
- Can inspect intermediate files
- Easy to retry individual revisions
</pattern>

<pattern name="sed_script_file">
```bash
cat > /tmp/replacements.sed << 'EOF'
s/pattern1/replacement1/g
s/pattern2/replacement2/g
EOF

for rev in abc def ghi; do
  jj log -r "$rev" -n1 --no-graph -T description | \
    sed -f /tmp/replacements.sed | \
    jj desc -r "$rev" --stdin
done
```
</pattern>

<jjtask_helper>
The `jjtask batch-desc` helper simplifies this:

```bash
jjtask batch-desc 's/old/new/' 'tasks_pending()'
```
</jjtask_helper>

<common_mistakes>
```bash
# Wrong: gets formatted log
jj log -r xyz | sed 's/old/new/'

# Correct: gets raw description
jj log -r xyz -n1 --no-graph -T description | sed 's/old/new/'

# Wrong: unquoted variables
for rev in a b c; do jj log -r $rev; done

# Correct: always quote
for rev in a b c; do jj log -r "$rev"; done
```
</common_mistakes>

<verification>
Always verify after batch operations:

```bash
for rev in abc def ghi; do
  echo "=== $rev ==="
  jj log -r "$rev" -n1 --no-graph -T description | head -3
done
```
</verification>
</batch_operations>
