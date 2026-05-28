# Error Handling Reference

| Error | Cause | Solution |
|-------|-------|----------|
| `SAML login failed` | Certificate mismatch | Re-upload IdP certificate |
| `SCIM sync failing` | Token expired | Generate new SCIM bearer token |
| `Team not seeing project` | Project not assigned | Add team to project via API or UI |
| `API token unauthorized` | Missing scopes | Create new token with required scopes |