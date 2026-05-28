---
name: encrypting-and-decrypting-data
description: Use this skill when you need to encrypt or decrypt data to ensure confidentiality and integrity, such as securing sensitive information or accessing previously encrypted files.
---

# Skill body

## Overview

This skill empowers Claude to handle data encryption and decryption tasks seamlessly. It leverages the encryption-tool plugin to provide a secure way to protect sensitive information.

## How It Works

1. **Identify Request**: Analyze the user's request to determine if encryption or decryption is needed.
2. **Select Method**: Prompt the user to specify the desired encryption algorithm (e.g., AES, RSA). If not specified, a default secure method is chosen.
3. **Execute Operation**: Use the encryption-tool plugin to perform the encryption or decryption on the provided data or file.
4. **Return Result**: Present the encrypted or decrypted data to the user, or save the result to a file as requested.

## When to Use This Skill

This skill activates when you need to:
- Encrypt sensitive data before storage or transmission.
- Decrypt previously encrypted data for access or processing.
- Generate encrypted files for secure archiving.

## Examples

### Example 1: Encrypting a Text File

User request: "Encrypt the file 'sensitive_data.txt' using AES."

The skill will:
1. Activate the encryption-tool plugin.
2. Encrypt the contents of 'sensitive_data.txt' using AES encryption.
3. Save the encrypted data to a new file (e.g., 'sensitive_data.txt.enc').

### Example 2: Decrypting an Encrypted File

User request: "Decrypt the file 'confidential.txt.enc'."

The skill will:
1. Activate the encryption-tool plugin.
2. Decrypt the contents of 'confidential.txt.enc' using the appropriate decryption key (assumed to be available or prompted for).
3. Save the decrypted data to a new file (e.g., 'confidential.txt').

## Best Practices

- **Key Management**: Always store encryption keys securely and avoid hardcoding them in scripts.
- **Algorithm Selection**: Choose encryption algorithms based on the sensitivity of the data being protected.