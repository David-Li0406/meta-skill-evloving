# Semantic Semgrep Patterns for Code Security

**Category**: code-security
**Description**: Advanced Semgrep patterns using semantic analysis, dataflow, and pattern combinations
**Type**: semgrep-native

These patterns use Semgrep's advanced features beyond simple regex matching:
- Pattern-inside/pattern-not for context-aware matching
- Metavariable patterns for semantic analysis
- Dataflow patterns for taint tracking
- Multi-pattern rules for complex detection

---

## SQL Injection (Advanced)

### Python SQL Injection with f-string (Semantic)
**Type**: semgrep
**Severity**: critical
**Languages**: [python]
**CWE**: CWE-89

```yaml
patterns:
  - pattern-either:
      - pattern: |
          $CURSOR.execute(f"...{$VAR}...")
      - pattern: |
          $CURSOR.execute("..." + $VAR + "...")
      - pattern: |
          $CURSOR.execute("...%s..." % $VAR)
  - pattern-not-inside: |
      $VAR = $LITERAL
      ...
```

### Java PreparedStatement Misuse (Semantic)
**Type**: semgrep
**Severity**: critical
**Languages**: [java]
**CWE**: CWE-89

```yaml
patterns:
  - pattern: |
      $STMT = $CONN.prepareStatement("..." + $VAR + "...");
  - pattern-not: |
      $STMT = $CONN.prepareStatement($CONST);
```

### Go SQL Injection (Dataflow)
**Type**: semgrep
**Severity**: critical
**Languages**: [go]
**CWE**: CWE-89

```yaml
mode: taint
pattern-sources:
  - pattern: |
      $REQ.URL.Query().Get($KEY)
  - pattern: |
      $REQ.FormValue($KEY)
pattern-sinks:
  - pattern: |
      $DB.Query($QUERY, ...)
  - pattern: |
      $DB.Exec($QUERY, ...)
```

---

## Command Injection (Advanced)

### Python Subprocess with Shell (Semantic)
**Type**: semgrep
**Severity**: critical
**Languages**: [python]
**CWE**: CWE-78

```yaml
patterns:
  - pattern: |
      subprocess.$FUNC(..., shell=True, ...)
  - pattern-not: |
      subprocess.$FUNC($LITERAL, shell=True, ...)
  - metavariable-pattern:
      metavariable: $FUNC
      pattern-either:
        - pattern: call
        - pattern: run
        - pattern: Popen
```

### Node.js Child Process (Dataflow)
**Type**: semgrep
**Severity**: critical
**Languages**: [javascript, typescript]
**CWE**: CWE-78

```yaml
mode: taint
pattern-sources:
  - pattern: |
      $REQ.params.$PARAM
  - pattern: |
      $REQ.query.$PARAM
  - pattern: |
      $REQ.body.$PARAM
pattern-sinks:
  - pattern: |
      exec($CMD)
  - pattern: |
      execSync($CMD)
pattern-sanitizers:
  - pattern: |
      escapeShell($X)
```

---

## Cross-Site Scripting (Advanced)

### React dangerouslySetInnerHTML (Semantic)
**Type**: semgrep
**Severity**: high
**Languages**: [javascript, typescript]
**CWE**: CWE-79

```yaml
patterns:
  - pattern: |
      <$TAG dangerouslySetInnerHTML={{__html: $VAR}} />
  - pattern-not: |
      <$TAG dangerouslySetInnerHTML={{__html: DOMPurify.sanitize($VAR)}} />
  - pattern-not-inside: |
      const $VAR = DOMPurify.sanitize(...);
      ...
```

### Express Response with User Input (Dataflow)
**Type**: semgrep
**Severity**: high
**Languages**: [javascript, typescript]
**CWE**: CWE-79

```yaml
mode: taint
pattern-sources:
  - pattern: |
      $REQ.params
  - pattern: |
      $REQ.query
  - pattern: |
      $REQ.body
pattern-sinks:
  - pattern: |
      $RES.send($DATA)
  - pattern: |
      $RES.write($DATA)
pattern-sanitizers:
  - pattern: |
      escape($X)
  - pattern: |
      encode($X)
```

---

## Insecure Deserialization (Advanced)

### Python Pickle Load (Semantic)
**Type**: semgrep
**Severity**: critical
**Languages**: [python]
**CWE**: CWE-502

```yaml
patterns:
  - pattern-either:
      - pattern: pickle.load($FILE)
      - pattern: pickle.loads($DATA)
      - pattern: cPickle.load($FILE)
      - pattern: cPickle.loads($DATA)
  - pattern-not-inside: |
      # nosec
      ...
```

### Java ObjectInputStream (Semantic)
**Type**: semgrep
**Severity**: critical
**Languages**: [java]
**CWE**: CWE-502

```yaml
patterns:
  - pattern: |
      ObjectInputStream $OIS = new ObjectInputStream($INPUT);
      ...
      $OIS.readObject();
  - pattern-not-inside: |
      ObjectInputFilter $FILTER = ...;
      ...
```

### YAML Unsafe Load (Semantic)
**Type**: semgrep
**Severity**: critical
**Languages**: [python]
**CWE**: CWE-502

```yaml
patterns:
  - pattern: yaml.load($DATA, ...)
  - pattern-not: yaml.load($DATA, Loader=yaml.SafeLoader)
  - pattern-not: yaml.load($DATA, Loader=yaml.FullLoader)
```

---

## Hardcoded Secrets (Advanced)

### Password in Variable Assignment (Semantic)
**Type**: semgrep
**Severity**: critical
**Languages**: [python, javascript, typescript, java, go]

```yaml
patterns:
  - pattern: |
      $VAR = "..."
  - metavariable-regex:
      metavariable: $VAR
      regex: (?i)(password|passwd|pwd|secret|api_key|apikey|token|auth)
  - pattern-not: |
      $VAR = ""
  - pattern-not: |
      $VAR = os.environ.get(...)
  - pattern-not: |
      $VAR = process.env.$KEY
```

### AWS Credentials in Code (Semantic)
**Type**: semgrep
**Severity**: critical
**Languages**: [python, javascript, typescript]

```yaml
patterns:
  - pattern-either:
      - pattern: |
          aws_access_key_id = "AKIA..."
      - pattern: |
          AWS_ACCESS_KEY_ID = "AKIA..."
      - pattern: |
          accessKeyId: "AKIA..."
  - pattern-not-inside: |
      # Example credentials
      ...
  - pattern-not-inside: |
      // Test credentials
      ...
```

---

## Cryptographic Issues (Advanced)

### Weak TLS Version (Semantic)
**Type**: semgrep
**Severity**: high
**Languages**: [python]
**CWE**: CWE-326

```yaml
patterns:
  - pattern-either:
      - pattern: ssl.PROTOCOL_SSLv2
      - pattern: ssl.PROTOCOL_SSLv3
      - pattern: ssl.PROTOCOL_TLSv1
      - pattern: ssl.PROTOCOL_TLSv1_1
  - pattern-not-inside: |
      # Legacy compatibility required
      ...
```

### Hardcoded IV/Nonce (Semantic)
**Type**: semgrep
**Severity**: high
**Languages**: [python, javascript, java]
**CWE**: CWE-329

```yaml
patterns:
  - pattern-either:
      - pattern: |
          $CIPHER.encrypt($DATA, iv=b"...")
      - pattern: |
          AES.new($KEY, $MODE, iv=b"...")
      - pattern: |
          new IvParameterSpec($BYTES)
  - metavariable-pattern:
      metavariable: $BYTES
      pattern: |
        new byte[] { ... }
```

---

## Path Traversal (Advanced)

### File Operation with User Input (Dataflow)
**Type**: semgrep
**Severity**: high
**Languages**: [python]
**CWE**: CWE-22

```yaml
mode: taint
pattern-sources:
  - pattern: |
      request.args.get($KEY)
  - pattern: |
      request.form.get($KEY)
pattern-sinks:
  - pattern: |
      open($PATH, ...)
  - pattern: |
      os.path.join($BASE, $PATH)
pattern-sanitizers:
  - pattern: |
      os.path.basename($X)
  - pattern: |
      secure_filename($X)
```

### Node.js Path Traversal (Semantic)
**Type**: semgrep
**Severity**: high
**Languages**: [javascript, typescript]
**CWE**: CWE-22

```yaml
patterns:
  - pattern: |
      fs.readFile(path.join($BASE, $USER_INPUT), ...)
  - pattern-not-inside: |
      if (!$USER_INPUT.includes('..')) { ... }
  - pattern-not-inside: |
      $SAFE = path.normalize($USER_INPUT);
      ...
```

---

## SSRF (Advanced)

### Python Requests SSRF (Dataflow)
**Type**: semgrep
**Severity**: high
**Languages**: [python]
**CWE**: CWE-918

```yaml
mode: taint
pattern-sources:
  - pattern: |
      request.args.get($KEY)
  - pattern: |
      request.json.get($KEY)
pattern-sinks:
  - pattern: |
      requests.get($URL)
  - pattern: |
      requests.post($URL, ...)
  - pattern: |
      urllib.request.urlopen($URL)
pattern-sanitizers:
  - pattern: |
      validate_url($X)
```

### Node.js Fetch SSRF (Semantic)
**Type**: semgrep
**Severity**: high
**Languages**: [javascript, typescript]
**CWE**: CWE-918

```yaml
patterns:
  - pattern: |
      fetch($URL)
  - pattern-not: |
      fetch("...")
  - pattern-inside: |
      $URL = $REQ.$PROP
      ...
```

---

## Authentication Issues (Advanced)

### Missing Authentication Check (Semantic)
**Type**: semgrep
**Severity**: critical
**Languages**: [python]

```yaml
patterns:
  - pattern: |
      @app.route($PATH, methods=['POST', ...])
      def $FUNC(...):
          ...
  - pattern-not-inside: |
      @login_required
      ...
  - pattern-not-inside: |
      if not current_user.is_authenticated:
          ...
  - metavariable-regex:
      metavariable: $PATH
      regex: (/admin|/api/private|/internal)
```

### JWT Secret Hardcoded (Semantic)
**Type**: semgrep
**Severity**: critical
**Languages**: [python, javascript, typescript]

```yaml
patterns:
  - pattern-either:
      - pattern: jwt.encode($PAYLOAD, "...", ...)
      - pattern: jwt.sign($PAYLOAD, "...", ...)
      - pattern: jwt.decode($TOKEN, "...", ...)
      - pattern: jwt.verify($TOKEN, "...", ...)
  - pattern-not: |
      jwt.$FUNC($DATA, os.environ.get(...), ...)
  - pattern-not: |
      jwt.$FUNC($DATA, process.env.$KEY, ...)
```

---

## Usage Notes

These patterns require Semgrep's semantic analysis features. To use them:

1. Copy the YAML pattern block into a `.yaml` rule file
2. Add rule metadata (id, message, severity)
3. Run with `semgrep --config rule.yaml target/`

For dataflow (taint) patterns:
- Requires Semgrep Pro or Semgrep App
- Use `mode: taint` to enable dataflow analysis
- Define sources, sinks, and sanitizers

For pattern combinations:
- `pattern-inside` restricts matches to specific contexts
- `pattern-not` excludes safe patterns
- `metavariable-regex` adds regex constraints to captured variables
