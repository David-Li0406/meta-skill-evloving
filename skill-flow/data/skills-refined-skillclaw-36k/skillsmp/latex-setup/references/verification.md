**Skill**: [LaTeX Environment Setup](../SKILL.md)

## Verification

### Check Installation

```bash
# Check TeX version
tex --version
# Expected: TeX 3.141592653 (TeX Live 2025)

# Check pdflatex
pdflatex --version

# Check latexmk
latexmk --version
# Expected: Latexmk, John Collins, version 4.86a
```

### Verify PATH

```bash
# TeX binaries should be in PATH
which pdflatex
# Expected: /Library/TeX/texbin/pdflatex

# Check environment
echo $PATH | grep -o '/Library/TeX/texbin'
```

### Test Basic Compilation

```bash
# Create test document
cat > test.tex <<'EOF'
\documentclass{article}
\begin{document}
Hello World!
\end{document}
EOF

# Compile
pdflatex test.tex

# Verify PDF created
ls test.pdf
```
