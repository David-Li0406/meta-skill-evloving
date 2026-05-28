# Common Errors and Fixes

This guide provides comprehensive documentation of errors you may encounter when creating and validating blueprints, along with their fixes.

## Error Code Reference

Errors are categorized with codes:
- **Pxxx**: Parser errors during blueprint loading
- **Vxxx**: Validation errors (blueprint structure issues)
- **Rxxx**: Runtime errors during planning and execution
- **Sxxx**: SDK/Provider errors during producer invocation
- **Wxxx**: Soft warnings that don't block execution

---

## Parser Errors (P001-P099)

These errors occur when loading and parsing blueprint YAML files.

### P001: Invalid YAML Document
**Error:** The YAML file is malformed or contains syntax errors.

**Example:**
```yaml
meta:
  name: test
  inputs:  # Missing colon or incorrect indentation
    - name value  # Invalid YAML syntax
```

**Fix:** Validate YAML syntax using a YAML linter.

---

### P002: Missing Required Section
**Error:** The blueprint is missing a required section (meta, artifacts).

**Example:**
```yaml
# Missing meta section
artifacts:
  - name: Output
    type: video
```

**Fix:** Add the required section:
```yaml
meta:
  name: MyBlueprint
  version: 1.0.0

artifacts:
  - name: Output
    type: video
```

---

### P010: Invalid Loop Entry
**Error:** A loop definition is invalid or missing required fields.

**Fix:** Ensure loops have `name` and `countInput`:
```yaml
loops:
  - name: segment
    countInput: NumOfSegments
```

---

### P020-P029: Input/Artifact Parsing Errors

### P020: Invalid Input Entry
**Error:** An input entry has invalid syntax or missing required fields.

**Fix:** Ensure inputs have `name` and `type`:
```yaml
inputs:
  - name: Prompt
    type: string
    required: true
```

### P021: Invalid Artifact Entry
**Error:** An artifact entry has invalid syntax.

**Fix:** Ensure artifacts have `name` and `type`:
```yaml
artifacts:
  - name: Video
    type: video
```

---

### P030-P039: Producer Parsing Errors

### P030: Invalid Producer Entry
**Error:** A producer entry has invalid syntax.

### P031: Producer Path and Name Conflict
**Error:** Both `path` and `producer` are specified for the same producer.

**Fix:** Use only one method:
```yaml
producers:
  - name: MyProducer
    path: producers/asset/image.yaml  # Either path
    # OR
    # producer: ImageGenerator  # Or producer reference
```

### P033: Unknown Producer Reference
**Error:** A `producer:` reference doesn't match any catalog entry.

**Fix:** Check the catalog for available producers.

---

### P040-P049: Connection Parsing Errors

### P040: Invalid Connection Entry
**Error:** A connection has invalid syntax.

**Fix:** Ensure connections have `from` and `to`:
```yaml
connections:
  - from: Input
    to: Producer.InputField
```

### P042: Invalid Dimension Selector Syntax
**Error:** A dimension selector like `[segment]` has invalid syntax.

**Valid syntax:**
- `[segment]` - Loop variable
- `[0]` - Numeric index
- `[segment+1]` - Offset expression

---

## Validation Errors (V001-V099)

These errors are detected during blueprint validation.

### V001: Invalid Connection Source
**Error:** The source of a connection references an invalid endpoint.

**Example:**
```yaml
connections:
  - from: InvalidSource.Output  # V001: InvalidSource doesn't exist
    to: Producer.Input
```

**Fix:** Ensure the source references a valid input, artifact, or producer output.

---

### V002: Invalid Connection Target
**Error:** The target of a connection references an invalid endpoint.

**Example:**
```yaml
connections:
  - from: Input
    to: InvalidTarget.Input  # V002: InvalidTarget doesn't exist
```

**Fix:** Ensure the target references a valid artifact, input (for fan-in), or producer input.

---

### V003: Producer Not Found
**Error:** A connection references a producer that is not declared in the `producers[]` section.

**Example:**
```yaml
producers:
  - name: AudioProducer
    path: producers/asset/audio-tts.yaml

connections:
  - from: Input
    to: VideoProducer.Prompt  # V003: VideoProducer not in producers[]
```

**Fix:** Add the missing producer to the `producers[]` section:
```yaml
producers:
  - name: AudioProducer
    path: producers/asset/audio-tts.yaml
  - name: VideoProducer
    path: producers/asset/video-generator.yaml
```

---

### V004: Input Not Found
**Error:** A connection's `from` references an input that is not declared in `inputs[]` and is not a system input.

**Example:**
```yaml
inputs:
  - name: Prompt
    type: string

connections:
  - from: UndeclaredInput  # V004: UndeclaredInput not in inputs[]
    to: Producer.TextInput
```

**System Inputs:** The following inputs are automatically available and don't need declaration:
- `Duration` - Total video duration in seconds
- `NumOfSegments` - Number of segments
- `SegmentDuration` - Duration per segment (computed)
- `AspectRatio` - Video aspect ratio
- `Resolution` - Video resolution

**Fix:** Either declare the input or use a system input:
```yaml
inputs:
  - name: UndeclaredInput
    type: string
    required: true
```

---

### V005: Artifact Not Found
**Error:** A connection's `to` references an artifact that is not declared in `artifacts[]`.

**Example:**
```yaml
artifacts:
  - name: GeneratedVideo
    type: video

connections:
  - from: Producer.Output
    to: MissingArtifact  # V005: MissingArtifact not in artifacts[]
```

**Fix:** Declare the artifact:
```yaml
artifacts:
  - name: GeneratedVideo
    type: video
  - name: MissingArtifact
    type: string
```

---

### V006: Invalid Nested Path / Unknown Loop Dimension
**Error:** A dimension reference (e.g., `[segment]`) uses an undeclared loop name.

**Example:**
```yaml
loops:
  - name: segment
    countInput: NumOfSegments

connections:
  - from: Input
    to: Producer[undeclaredLoop].Input  # V006: undeclaredLoop not in loops[]
```

**Fix:** Either fix the typo or declare the loop:
```yaml
loops:
  - name: segment
    countInput: NumOfSegments
  - name: undeclaredLoop
    countInput: SomeCount
```

---

### V007: Dimension Mismatch
**Error:** A connection has more dimensions on the source than the target without a collector.

**Example:**
```yaml
loops:
  - name: segment
    countInput: NumOfSegments

connections:
  - from: ImageProducer[segment].GeneratedImage  # Has [segment] dimension
    to: TimelineComposer.ImageInput              # No dimension - mismatch!
```

**Fix:** Either add matching dimensions to the target, or add BOTH a connection AND a collector:
```yaml
connections:
  - from: ImageProducer[segment].GeneratedImage
    to: TimelineComposer.ImageSegments

collectors:
  - name: TimelineImages
    from: ImageProducer[segment].GeneratedImage
    into: TimelineComposer.ImageSegments
    groupBy: segment
```

---

### V010: Producer Input Mismatch
**Error:** A connection targets a producer input that doesn't exist in that producer's blueprint.

**Example:**
```yaml
# Producer blueprint has inputs: [Prompt, Style]
connections:
  - from: UserText
    to: ImageProducer.NonExistentInput  # V010: Producer doesn't have this input
```

**Fix:** Check the producer's YAML file for available inputs.

---

### V011: Producer Output Mismatch
**Error:** A connection sources from a producer artifact that doesn't exist in that producer's blueprint.

**Example:**
```yaml
# Producer blueprint has artifacts: [GeneratedImage]
connections:
  - from: ImageProducer.NonExistentOutput  # V011: Producer doesn't have this artifact
    to: Timeline.ImageInput
```

**Fix:** Check the producer's YAML file for available artifacts.

---

### V020: Loop countInput Not Found
**Error:** A loop's `countInput` references an input that doesn't exist.

**Example:**
```yaml
loops:
  - name: segment
    countInput: MissingCountInput  # V020: Input doesn't exist
```

**Fix:** Declare the count input or use a system input:
```yaml
inputs:
  - name: MissingCountInput
    type: int
    required: true

loops:
  - name: segment
    countInput: MissingCountInput
```

---

### V021: Producer Cycle Detected
**Error:** The producer dependency graph contains a circular dependency.

**Example:**
```yaml
connections:
  - from: ProducerA.Output
    to: ProducerB.Input
  - from: ProducerB.Output
    to: ProducerC.Input
  - from: ProducerC.Output
    to: ProducerA.Input  # Creates cycle: A -> B -> C -> A
```

**Fix:** Remove one of the connections to break the cycle.

---

### V030: Artifact countInput Not Found
**Error:** An array artifact's `countInput` references an input that doesn't exist.

**Fix:** Declare the count input:
```yaml
inputs:
  - name: ImageCount
    type: int
    required: true

artifacts:
  - name: Images
    type: array
    itemType: image
    countInput: ImageCount
```

---

### V040-V042: Collector Validation Errors

### V040: Collector Source Invalid
**Error:** A collector's `from` references an unknown producer.

### V041: Collector Target Invalid
**Error:** A collector's `into` references an unknown producer.

### V042: Collector Missing Connection (CRITICAL)
**Error:** A collector is defined but there's no corresponding connection.

**Example (WRONG):**
```yaml
collectors:
  - name: TimelineImages
    from: ImageProducer[segment].GeneratedImage
    into: TimelineComposer.ImageSegments
    groupBy: segment
```

**Example (CORRECT):**
```yaml
connections:
  - from: ImageProducer[segment].GeneratedImage
    to: TimelineComposer.ImageSegments

collectors:
  - name: TimelineImages
    from: ImageProducer[segment].GeneratedImage
    into: TimelineComposer.ImageSegments
    groupBy: segment
```

**Why both are needed:**
- The **connection** creates the data flow edge in the graph
- The **collector** tells the runtime HOW to group and order the data

---

### V050: Condition Path Invalid
**Error:** A condition's `when` path references an unknown producer.

**Fix:** Ensure the producer is declared and the path is valid.

---

### V060-V062: Type Validation Errors

### V060: Invalid Input Type
**Valid input types:** `string`, `int`, `integer`, `number`, `boolean`, `array`, `collection`, `image`, `video`, `audio`, `json`

### V061: Invalid Artifact Type
**Valid artifact types:** `string`, `image`, `video`, `audio`, `json`, `array`, `multiDimArray`

### V062: Invalid Item Type
**Valid item types:** `string`, `image`, `video`, `audio`, `json`, `number`, `integer`, `boolean`

---

## Runtime Errors (R001-R099)

These errors occur during planning and execution.

### R001: Manifest Not Found
**Error:** The manifest file for a movie/build doesn't exist.

**Fix:** Ensure the build was created before attempting to resume.

---

### R002: Manifest Hash Conflict
**Error:** A content-addressed manifest hash conflict occurred.

**Fix:** This is rare. Contact support if it persists.

---

### R010: Cyclic Dependency Detected
**Error:** The planning engine detected a cycle in the dependency graph.

**Fix:** Review connections to ensure data flows in one direction (DAG).

---

### R020: Missing Blob Payload
**Error:** An artifact is marked as succeeded but has no blob data.

**Fix:** Ensure the producer properly returns blob data for binary artifacts.

---

### R030: Missing Output Schema
**Error:** The producer model doesn't have an output schema defined.

**Fix:** Add an output schema to the model's schema file.

---

### R050: Invalid JSON Path
**Error:** A JSON path expression is malformed.

**Fix:** Use valid dot-notation paths like `$.field.nested`.

---

## SDK/Provider Errors (S001-S099)

These errors occur during producer invocation.

### S001: Invalid Configuration
**Error:** The producer configuration is invalid.

**Fix:** Review the producer's configuration requirements.

---

### S002: Missing Required Input
**Error:** `Missing required input "X" for field "Y". No schema default available.`

**Cause:** A producer expects a required input that wasn't provided.

**Fix:** Either:
1. Add the input to your inputs YAML file
2. Connect a blueprint input or producer output to the missing input

---

### S003: Missing Input Schema
**Error:** `Missing input schema for <provider> provider.`

**Cause:** The model doesn't have an associated JSON schema file.

**Fix:** Ensure the model is properly configured in the catalog with a schema file.

---

### S004: Unknown Artefact
**Error:** `Unknown artefact "X" for producer invoke.`

**Cause:** The producer is trying to produce an artifact not in its `produces` list.

**Fix:** Check that the producer's configuration includes all expected output artifacts.

---

### S010-S019: Timeline Producer Errors

### S010: Missing Segments
**Error:** Timeline producer requires segments to be specified.

### S012: Missing Storage Root
**Error:** Timeline producer requires storage root configuration.

**Fix:** Set the `StorageRoot` input or configure storage paths.

### S013: Unsupported Clip Kind
**Error:** The timeline producer doesn't support the specified clip kind.

### S014: Missing Asset
**Error:** Required asset not found for timeline track.

### S015: Missing Duration
**Error:** Timeline producer requires a positive Duration input.

---

### S020-S029: Export Producer Errors

### S020: Missing Manifest
**Error:** Export requires a valid manifest file.

### S021: Missing Timeline
**Error:** Export requires a timeline artefact.

### S023: FFmpeg Not Found
**Error:** FFmpeg binary not found at the configured path.

**Fix:** Install FFmpeg or configure the correct path.

### S024: Render Failed
**Error:** The render process failed.

**Fix:** Check the detailed error message for specific issues.

---

### S030-S039: API Errors

### S030: Rate Limited
**Error:** The provider API rate limit was exceeded.

**Fix:** Wait and retry, or reduce request frequency.

### S031: Provider Prediction Failed
**Error:** The provider API call failed.

**Fix:** Check API credentials and network connectivity.

---

### S040-S049: Mapping/Transform Errors

### S040: Missing Field Property
**Error:** `Mapping for "X" requires 'field' property`

**Fix:** Add the field property to the mapping:
```yaml
sdkMapping:
  Prompt:
    field: prompt
```

### S041: Cannot Expand Non-Object
**Error:** `Cannot expand non-object value for "X". expand:true requires the value to be an object.`

**Fix:** Only use `expand: true` for JSON/object inputs.

### S042: Invalid Condition Configuration
**Error:** `Invalid condition for input "X": must specify one of "equals", "notEmpty", or "empty".`

**Fix:** Add a condition operator:
```yaml
conditional:
  when:
    input: SomeInput
    notEmpty: true
  then:
    field: some_field
```

### S043: Blob Input Without Cloud Storage
**Error:** `Blob inputs (file: references) require cloud storage configuration.`

**Fix:** Set the required environment variables:
```bash
export S3_ENDPOINT="your-endpoint"
export S3_ACCESS_KEY_ID="your-key"
export S3_SECRET_ACCESS_KEY="your-secret"
export S3_BUCKET_NAME="your-bucket"
```

---

## Warnings (W001-W003)

### W001: Unused Input
**Warning:** An input is declared but never used in any connection or loop.

**Fix:** Either remove the unused input or connect it.

---

### W002: Unused Artifact
**Warning:** An artifact is declared but nothing connects to it.

**Fix:** Either remove the unused artifact or add a connection to it.

---

### W003: Unreachable Producer
**Warning:** A producer is declared but has no incoming connections.

**Fix:** Either remove the unused producer or add a connection to it.

---

## Quick Troubleshooting Checklist

1. **Run validation first:**
   ```bash
   renku blueprints:validate <blueprint.yaml>
   ```

2. **Check producer paths:** Ensure all `path:` values in `producers[]` point to existing YAML files.

3. **Verify connections:** Each `from` and `to` must reference valid:
   - Inputs (from local scope or system inputs)
   - Artifacts (from local scope)
   - Producer.Input or Producer.Output (from `producers[]`)

4. **Check loops:** Every dimension reference `[name]` must have a corresponding loop definition.

5. **Fan-in pattern:** Always include BOTH connection AND collector for array inputs.

6. **Test with dry-run:**
   ```bash
   renku generate --blueprint=<path> --inputs=<path> --dry-run
   ```

---

## See Also

- [Comprehensive Blueprint Guide](./comprehensive-blueprint-guide.md) - Full blueprint syntax reference
- [Models Guide](./models-guide.md) - Model selection guidance
- [Prompt Producer Guide](./prompt-producer-guide.md) - Creating prompt producers
