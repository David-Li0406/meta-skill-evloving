<!--
Copyright (c) 2025 Crash Override Inc. - https://crashoverride.com

SPDX-License-Identifier: GPL-3.0
-->

# Legal Review Knowledge Base

Comprehensive reference documentation for code legal review, license compliance, and content policy enforcement.

## Contents

### [License Compliance Guide](license-compliance-guide.md)
Open source license detection, compliance requirements, and compatibility analysis.

**Topics Covered**:
- License detection methods (SPDX, text matching)
- Common open source licenses (MIT, Apache, GPL, BSD, etc.)
- License compliance obligations
- License compatibility matrix
- Copyright and attribution requirements
- SPDX document generation
- Enterprise license management
- Best practices and automation

**Use Cases**:
- Detecting licenses in dependencies
- Ensuring license compliance
- Evaluating license compatibility
- M&A due diligence
- Open source policy enforcement

### [Content Policy Guide](content-policy-guide.md)
Detection of inappropriate content, legal risks, and policy violations in source code.

**Topics Covered**:
- Profanity and offensive language detection
- Hate speech and discriminatory content
- Legal and regulatory risks (ITAR, GDPR, CCPA, HIPAA)
- Trademark and patent concerns
- Trade secret exposure
- Hardcoded credentials and PII
- Inclusive language guidelines
- Detection techniques (regex, NLP, ML)
- Remediation strategies

**Use Cases**:
- Detecting inappropriate code
- Secret scanning
- Privacy compliance
- Inclusive language enforcement
- Security risk assessment

### [Legal Review Tools](legal-review-tools.md)
Tools and automation for automated legal review of source code.

**Topics Covered**:
- Open source scanners (ScanCode, Licensee, FOSSology, ORT)
- Secret detection (TruffleHog, detect-secrets)
- Content policy tools (alex, woke)
- Commercial platforms (FOSSA, Black Duck, Snyk)
- CI/CD integration examples
- Custom automation scripts
- Policy configuration
- Tool selection guidance

**Use Cases**:
- Selecting appropriate scanning tools
- CI/CD pipeline integration
- Pre-commit hook setup
- Policy automation
- Compliance dashboard creation

### [Claude AI Integration Guide](claude-ai-integration.md) 🤖
Phase 4 AI-enhanced legal analysis with Claude Sonnet for intelligent recommendations and risk assessment.

**Topics Covered**:
- Claude AI architecture and integration
- RAG-enhanced analysis with legal knowledge base
- License compatibility assessment with AI
- Context-aware content policy review
- Risk prioritization and remediation guidance
- API configuration and usage
- Cost optimization and best practices
- Performance benchmarks and troubleshooting

**Use Cases**:
- Pre-release legal audits with AI insights
- Complex license compatibility questions
- Intelligent remediation recommendations
- Context-aware content policy modernization
- M&A due diligence with AI analysis

## Quick Start

### For Legal Review Analysts

1. **Understand license obligations**
   - Read: [License Compliance Guide](license-compliance-guide.md)
   - Focus on: License types, compatibility matrix

2. **Set up scanning tools**
   - Read: [Legal Review Tools](legal-review-tools.md)
   - Start with: ScanCode for licenses, TruffleHog for secrets

3. **Define policies**
   - Create allowed/denied license lists
   - Configure content policy rules
   - Document exemption processes

### For Developers

1. **Learn license basics**
   - Read: Common licenses section in [License Compliance Guide](license-compliance-guide.md)
   - Understand: Attribution requirements, copyleft implications

2. **Install pre-commit hooks**
   - See: CI/CD integration in [Legal Review Tools](legal-review-tools.md)
   - Catch issues before commit

3. **Follow inclusive language guidelines**
   - Read: Inclusive language section in [Content Policy Guide](content-policy-guide.md)
   - Use: Recommended terminology

### For Security Engineers

1. **Secret detection**
   - Read: Secret detection section in [Content Policy Guide](content-policy-guide.md)
   - Tools: TruffleHog, detect-secrets

2. **PII scanning**
   - Read: Security & Privacy section in [Content Policy Guide](content-policy-guide.md)
   - Implement: GDPR/CCPA compliance checks

3. **Automation**
   - Read: [Legal Review Tools](legal-review-tools.md)
   - Integrate: CI/CD scanning pipelines

## Common Scenarios

### Scenario 1: Adding a new dependency

**Question**: Can I use this library?

**Process**:
1. Check license using `licensee` or `scancode`
2. Compare against approved license list
3. Review license obligations
4. Check compatibility with existing licenses
5. Document decision

**Reference**: [License Compliance Guide - License Compatibility](license-compliance-guide.md#license-compatibility)

### Scenario 2: Pre-release audit

**Question**: Is our code ready for release?

**Checklist**:
- [ ] All dependencies have licenses
- [ ] No denied licenses present
- [ ] Attribution files complete (NOTICE, ATTRIBUTION)
- [ ] No hardcoded secrets
- [ ] No PII exposure
- [ ] Inclusive language check passed
- [ ] SBOM generated

**Reference**: All three guides

### Scenario 3: M&A due diligence

**Question**: What are the legal risks in this codebase?

**Analysis**:
1. License scan (ScanCode/FOSSology)
2. Check for GPL/AGPL in proprietary context
3. Verify copyright ownership
4. Secret detection
5. Content policy review
6. Generate compliance report

**Reference**: [License Compliance Guide - Enterprise License Management](license-compliance-guide.md#enterprise-license-management)

### Scenario 4: Security incident

**Question**: Was sensitive data committed?

**Investigation**:
1. Run TruffleHog on full git history
2. Check for PII patterns
3. Review access logs
4. Rotate compromised credentials
5. Generate incident report

**Reference**: [Content Policy Guide - Security & Privacy](content-policy-guide.md#security--privacy)

## Integration with Zero

### Using with Legal Review Analyser

```bash
# Standard scan (no AI)
./utils/legal-review/legal-analyser.sh --path .

# With Claude AI analysis (Phase 4)
export ANTHROPIC_API_KEY='your-key'
./utils/legal-review/legal-analyser.sh --path . --claude

# License scan only with AI
./utils/legal-review/legal-analyser.sh --path . --licenses-only --claude

# Content policy with AI
./utils/legal-review/legal-analyser.sh --path . --content-only --claude
```

The legal analyser uses this RAG documentation to provide context-aware recommendations.

**See**: [Claude AI Integration Guide](claude-ai-integration.md) for detailed Phase 4 documentation.

### Using with Skills

The legal-review skill provides Claude AI access to this knowledge base:

```bash
# In Claude Code
@legal-review analyze licenses in this repo
@legal-review check for secrets
@legal-review review content policy violations
```

### Using with Prompts

Pre-configured prompts in `prompts/legal-review/`:
- `license-audit.md` - License compliance audit
- `secret-scan.md` - Secret detection and remediation
- `content-review.md` - Content policy enforcement
- `compliance-report.md` - Generate compliance report

## Best Practices

### 1. Continuous Monitoring
- **Pre-commit**: Catch issues early
- **CI/CD**: Block non-compliant code
- **Scheduled**: Weekly/monthly deep scans

### 2. Policy First
- Define clear policies before tooling
- Document approved/denied licenses
- Establish exemption process
- Regular policy review

### 3. Education
- Train developers on license implications
- Provide inclusive language guidelines
- Share compliance success stories
- Document lessons learned

### 4. Automation
- Integrate scanning into workflow
- Auto-fix where possible
- Generate actionable reports
- Track metrics over time

### 5. Risk-Based Approach
- Prioritize critical issues
- Accept managed risk for low severity
- Document risk acceptance
- Review quarterly

## Additional Resources

### Standards & Specifications
- **SPDX**: https://spdx.dev/
- **CycloneDX**: https://cyclonedx.org/
- **REUSE**: https://reuse.software/

### Legal Resources
- **Software Freedom Law Center**: https://softwarefreedom.org/
- **Free Software Foundation**: https://www.fsf.org/
- **OSI Approved Licenses**: https://opensource.org/licenses/
- **tl;drLegal**: https://tldrlegal.com/

### Tools & Projects
- **ScanCode**: https://github.com/nexB/scancode-toolkit
- **TruffleHog**: https://github.com/trufflesecurity/trufflehog
- **Inclusive Naming**: https://inclusivenaming.org/
- **TODO Group**: https://todogroup.org/

## Contributing

To improve this knowledge base:

1. Submit corrections via pull request
2. Suggest additional topics
3. Share real-world scenarios
4. Update tool references

See [CONTRIBUTING.md](../../../CONTRIBUTING.md) for guidelines.

## License

This documentation is licensed under GPL-3.0. See [LICENSE](../../../LICENSE) for details.

## Support

- [GitHub Issues](https://github.com/crashappsec/zero/issues)
- [Discussions](https://github.com/crashappsec/zero/discussions)
- [Main Documentation](../../../README.md)
