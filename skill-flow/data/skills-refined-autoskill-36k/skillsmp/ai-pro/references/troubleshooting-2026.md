# Troubleshooting & FAQ 2026

*Updated: January 22, 2026 - 15:18*

This guide addresses common technical hurdles and quality issues encountered when using the AI-Pro suite.

## 1. Quality & Resolution Issues

### "The output is pixelated or blurry"
- **Cause**: Many models (especially Flash/Nano) generate at lower internal resolutions (e.g., 512px) and use simple upscalers.
- **Solution**: 
    1.  Switch to `black-forest-labs/flux.2-pro`.
    2.  Explicitly state `native 4k resolution` in the prompt.
    3.  Run the `image-enhancer` workflow: `python scripts/enhance_image.py input.png`.

### "Faces look distorted or 'uncanny'"
- **Cause**: Poor latent space mapping for human features at certain angles.
- **Solution**:
    1.  Add `symmetrical facial features` to the prompt.
    2.  Use a reference image with `--cref`.
    3.  Apply a face-specific restore pass if available.

---

## 2. API & Connectivity Issues

### "Error 429: Too Many Requests"
- **Cause**: You have exceeded the rate limit for your OpenRouter tier.
- **Solution**:
    1.  Implement an exponential backoff in your integration.
    2.  Check your OpenRouter credit balance.
    3.  Switch to a less congested model like `gemini-3-flash`.

### "Error 400: Content Filter Triggered"
- **Cause**: Your prompt contains keywords that violate the model's safety guidelines.
- **Solution**:
    1.  Review the prompt for ambiguous terms that might be misinterpreted as violent or sexual.
    2.  Avoid using names of living public figures if the model's policy forbids it.

---

## 3. Script-Specific Problems

### "ModuleNotFoundError: No module named 'requests'"
- **Cause**: The `requests` library is not installed in your current Python environment.
- **Solution**: `pip install requests` or `bun install requests` (if using bun's python bridge).

### "API Key not found"
- **Cause**: The script cannot find the `.env` file or the environment variable.
- **Solution**:
    1.  Verify the `.env` file is in the project root.
    2.  Ensure it contains exactly `OPENROUTER_API_KEY=sk-or-v1-...`.
    3.  Try setting it directly in the shell: `export OPENROUTER_API_KEY=...`.

---

## 4. Prompt Logic & Hallucinations

### "The model ignored my 'No [Element]' instruction"
- **Cause**: Diffusion models often struggle with negative concepts in positive prompts (e.g., "no cars" might trigger "cars").
- **Solution**: Use the technical `negative prompt` field/flag.

### "Text is misspelled"
- **Cause**: Only specialized models (Flux, Ideogram) handle complex typography reliably.
- **Solution**: 
    1.  Limit text to short phrases.
    2.  Use double quotes: `"OPEN SOURCE"`.
    3.  Check if the model is `black-forest-labs/flux.2-pro`.
