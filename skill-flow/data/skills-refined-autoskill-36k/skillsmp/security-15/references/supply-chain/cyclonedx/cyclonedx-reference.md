# CycloneDX Specification - Complete Reference

## Overview

**CycloneDX** is an OWASP Foundation project providing a full-stack Bill of Materials (BOM) standard supporting:
- **SBOM** - Software Bill of Materials
- **HBOM** - Hardware Bill of Materials
- **MBOM** - Manufacturing Bill of Materials
- **OBOM** - Operations Bill of Materials
- **SaaSBOM** - Software-as-a-Service Bill of Materials
- **CBOM** - Cryptography Bill of Materials
- **ML-BOM** - Machine Learning Bill of Materials
- **AI-BOM** - Artificial Intelligence Bill of Materials

**Current Version**: 1.6 (ECMA-424 Standard)
**Website**: https://cyclonedx.org
**Schema**: https://github.com/CycloneDX/specification

## Formats Supported

| Format | Extension | Use Case |
|--------|-----------|----------|
| JSON | `.cdx.json` | APIs, modern tooling |
| XML | `.cdx.xml` | Legacy systems |
| Protocol Buffers | `.cdx.pb` | High-performance |

## Core BOM Structure

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.6",
  "serialNumber": "urn:uuid:3e671687-395b-41f5-a30f-a58921a69b79",
  "version": 1,
  "metadata": { },
  "components": [ ],
  "services": [ ],
  "externalReferences": [ ],
  "dependencies": [ ],
  "compositions": [ ],
  "vulnerabilities": [ ],
  "annotations": [ ],
  "formulation": [ ],
  "declarations": [ ],
  "definitions": [ ]
}
```

## Metadata Object

```json
{
  "metadata": {
    "timestamp": "2024-12-24T10:00:00Z",
    "lifecycles": [
      { "phase": "build" }
    ],
    "tools": {
      "components": [
        {
          "type": "application",
          "name": "zero",
          "version": "3.7.0",
          "manufacturer": { "name": "Crash Override" }
        }
      ]
    },
    "authors": [
      { "name": "Security Team", "email": "security@example.com" }
    ],
    "component": {
      "type": "application",
      "name": "my-application",
      "version": "1.0.0"
    },
    "manufacture": { "name": "Example Corp" },
    "supplier": { "name": "Example Corp" }
  }
}
```

### Lifecycle Phases

| Phase | Description |
|-------|-------------|
| `design` | Requirements and architecture |
| `pre-build` | Source code before compilation |
| `build` | Compilation/bundling |
| `post-build` | After build, before deployment |
| `operations` | Runtime/production |
| `discovery` | Analysis of existing systems |
| `decommission` | End of life |

## Component Types

| Type | Description | Use Case |
|------|-------------|----------|
| `application` | Software application | Root project |
| `framework` | Software framework | Rails, Django, Spring |
| `library` | Reusable component | npm packages, Maven artifacts |
| `container` | Container image | Docker images |
| `platform` | Runtime environment | JVM, Node.js, Python |
| `operating-system` | OS | Linux, Windows |
| `device` | Hardware | IoT devices |
| `device-driver` | Driver software | USB drivers |
| `firmware` | Firmware | BIOS, UEFI |
| `file` | Individual file | Config files |
| `machine-learning-model` | ML model | PyTorch, TensorFlow models |
| `data` | Data collection | Datasets |
| `cryptographic-asset` | Crypto component | Algorithms, keys, certs |

## Component Structure

```json
{
  "type": "library",
  "bom-ref": "pkg:npm/express@4.18.2",
  "name": "express",
  "version": "4.18.2",
  "group": "expressjs",
  "description": "Fast, unopinionated, minimalist web framework",
  "scope": "required",
  "purl": "pkg:npm/express@4.18.2",
  "cpe": "cpe:2.3:a:expressjs:express:4.18.2:*:*:*:*:node.js:*:*",
  "swid": { },
  "hashes": [
    { "alg": "SHA-256", "content": "abc123..." }
  ],
  "licenses": [
    { "license": { "id": "MIT" } }
  ],
  "copyright": "Copyright Example Corp",
  "supplier": { "name": "expressjs" },
  "author": "TJ Holowaychuk",
  "properties": [
    { "name": "internal:team", "value": "platform" }
  ],
  "externalReferences": [
    { "type": "website", "url": "https://expressjs.com" },
    { "type": "vcs", "url": "https://github.com/expressjs/express" }
  ],
  "components": [ ],
  "evidence": { },
  "pedigree": { },
  "modelCard": { },
  "data": { },
  "cryptoProperties": { }
}
```

## Package URL (purl)

Standard component identification:

```
pkg:type/namespace/name@version?qualifiers#subpath
```

| Ecosystem | Example |
|-----------|---------|
| npm | `pkg:npm/express@4.18.2` |
| PyPI | `pkg:pypi/django@4.2` |
| Maven | `pkg:maven/org.springframework/spring-core@6.0.0` |
| Go | `pkg:golang/github.com/gin-gonic/gin@v1.9.0` |
| Cargo | `pkg:cargo/serde@1.0.0` |
| NuGet | `pkg:nuget/Newtonsoft.Json@13.0.0` |
| Docker | `pkg:docker/library/nginx@sha256:abc123` |
| OCI | `pkg:oci/hello-wasm@sha256:abc123` |

## Services (SaaSBOM)

```json
{
  "services": [
    {
      "bom-ref": "service:api-gateway",
      "name": "API Gateway",
      "description": "Main API entry point",
      "endpoints": [
        "https://api.example.com/v1"
      ],
      "authenticated": true,
      "x-trust-boundary": true,
      "trustZone": "external",
      "data": [
        {
          "classification": "PII",
          "flow": "bi-directional"
        }
      ],
      "licenses": [{ "license": { "id": "Proprietary" } }],
      "externalReferences": [
        { "type": "documentation", "url": "https://docs.example.com" }
      ],
      "services": [ ],
      "releaseNotes": { }
    }
  ]
}
```

## Dependencies

```json
{
  "dependencies": [
    {
      "ref": "pkg:npm/express@4.18.2",
      "dependsOn": [
        "pkg:npm/body-parser@1.20.0",
        "pkg:npm/cookie@0.5.0"
      ],
      "provides": [
        "pkg:npm/express-session@1.17.3"
      ]
    }
  ]
}
```

## Vulnerabilities

```json
{
  "vulnerabilities": [
    {
      "id": "CVE-2024-1234",
      "source": {
        "name": "NVD",
        "url": "https://nvd.nist.gov/"
      },
      "references": [
        { "id": "GHSA-xxxx-xxxx", "source": { "name": "GitHub" } }
      ],
      "ratings": [
        {
          "source": { "name": "NVD" },
          "score": 7.5,
          "severity": "high",
          "method": "CVSSv31",
          "vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N"
        }
      ],
      "cwes": [79, 89],
      "description": "Cross-site scripting vulnerability",
      "detail": "Detailed technical description",
      "recommendation": "Upgrade to version 4.18.3",
      "workaround": "Sanitize user input",
      "advisories": [
        "https://github.com/expressjs/express/security/advisories/GHSA-xxxx"
      ],
      "created": "2024-01-15T00:00:00Z",
      "published": "2024-01-16T00:00:00Z",
      "updated": "2024-01-20T00:00:00Z",
      "credits": {
        "individuals": [{ "name": "Security Researcher" }]
      },
      "tools": { },
      "analysis": {
        "state": "exploitable",
        "justification": "code_not_reachable",
        "response": ["will_not_fix"],
        "detail": "Analysis details"
      },
      "affects": [
        {
          "ref": "pkg:npm/express@4.18.2",
          "versions": [
            { "version": "4.18.2", "status": "affected" }
          ]
        }
      ]
    }
  ]
}
```

### Vulnerability Analysis States

| State | Description |
|-------|-------------|
| `resolved` | Vulnerability has been remediated |
| `resolved_with_pedigree` | Resolved with audit trail |
| `exploitable` | Confirmed exploitable |
| `in_triage` | Under investigation |
| `false_positive` | Not actually vulnerable |
| `not_affected` | Not impacted |

### VEX Justifications

| Justification | Description |
|---------------|-------------|
| `code_not_present` | Vulnerable code not in build |
| `code_not_reachable` | Code present but unreachable |
| `requires_configuration` | Needs specific config to exploit |
| `requires_dependency` | Needs additional dependency |
| `requires_environment` | Needs specific environment |
| `protected_by_compiler` | Compiler mitigates issue |
| `protected_at_runtime` | Runtime protection in place |
| `protected_at_perimeter` | Network protection in place |
| `protected_by_mitigating_control` | Other control mitigates |

## Compositions

```json
{
  "compositions": [
    {
      "bom-ref": "composition:complete",
      "aggregate": "complete",
      "assemblies": ["pkg:npm/express@4.18.2"],
      "dependencies": ["pkg:npm/body-parser@1.20.0"]
    }
  ]
}
```

### Aggregate Types

| Type | Description |
|------|-------------|
| `complete` | BOM represents full inventory |
| `incomplete` | Partial inventory |
| `incomplete_first_party_only` | Only first-party components |
| `incomplete_third_party_only` | Only third-party components |
| `unknown` | Completeness not known |
| `not_specified` | Not applicable |

## Formulation (Build Info)

```json
{
  "formulation": [
    {
      "bom-ref": "formulation:build",
      "components": [
        {
          "type": "application",
          "name": "gcc",
          "version": "12.0.0"
        }
      ],
      "workflows": [
        {
          "bom-ref": "workflow:ci",
          "uid": "build-123",
          "name": "CI Pipeline",
          "tasks": [
            {
              "bom-ref": "task:compile",
              "uid": "compile-1",
              "name": "Compile",
              "resourceReferences": [
                { "ref": "component:gcc" }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

## External References

| Type | Description |
|------|-------------|
| `vcs` | Version control system |
| `issue-tracker` | Issue/bug tracker |
| `website` | Project website |
| `advisories` | Security advisories |
| `bom` | Related BOMs |
| `mailing-list` | Mailing list |
| `social` | Social media |
| `chat` | Chat channel |
| `documentation` | Documentation |
| `support` | Support resources |
| `source-distribution` | Source code archive |
| `distribution` | Binary distribution |
| `distribution-intake` | Package intake |
| `license` | License file |
| `build-meta` | Build metadata |
| `build-system` | Build system |
| `release-notes` | Release notes |
| `security-contact` | Security contact |
| `model-card` | ML model card |
| `log` | Log file |
| `configuration` | Config file |
| `evidence` | Evidence/attestation |
| `formulation` | Build formulation |
| `attestation` | SLSA attestation |
| `threat-model` | Threat model |
| `adversary-model` | Adversary model |
| `risk-assessment` | Risk assessment |
| `vulnerability-assertion` | VEX assertion |
| `exploitability-statement` | Exploitability info |
| `pentest-report` | Penetration test |
| `static-analysis-report` | SAST report |
| `dynamic-analysis-report` | DAST report |
| `runtime-analysis-report` | IAST report |
| `component-analysis-report` | SCA report |
| `maturity-report` | Maturity assessment |
| `certification-report` | Certification |
| `quality-metrics` | Quality metrics |
| `codified-infrastructure` | IaC files |
| `poam` | Plan of Action |
| `electronic-signature` | Digital signature |
| `rfc-9116` | Security.txt |
| `other` | Other reference |

## Hash Algorithms

| Algorithm | Description |
|-----------|-------------|
| `MD5` | MD5 (deprecated) |
| `SHA-1` | SHA-1 (deprecated) |
| `SHA-256` | SHA-256 (recommended) |
| `SHA-384` | SHA-384 |
| `SHA-512` | SHA-512 |
| `SHA3-256` | SHA-3 256 |
| `SHA3-384` | SHA-3 384 |
| `SHA3-512` | SHA-3 512 |
| `BLAKE2b-256` | BLAKE2b 256 |
| `BLAKE2b-384` | BLAKE2b 384 |
| `BLAKE2b-512` | BLAKE2b 512 |
| `BLAKE3` | BLAKE3 |

## Attestations & Declarations

```json
{
  "declarations": {
    "assessors": [
      {
        "bom-ref": "assessor:security-team",
        "organization": { "name": "Security Team" }
      }
    ],
    "attestations": [
      {
        "summary": "SLSA Level 3 Attestation",
        "assessor": "assessor:security-team",
        "map": [
          {
            "requirement": "requirement:slsa-l3",
            "claims": ["claim:provenance-verified"]
          }
        ]
      }
    ],
    "claims": [
      {
        "bom-ref": "claim:provenance-verified",
        "target": "pkg:npm/express@4.18.2",
        "predicate": "Provenance verified via in-toto",
        "reasoning": "Build attestation validated"
      }
    ]
  }
}
```

## Version History

| Version | Release | Key Features |
|---------|---------|--------------|
| 1.6 | 2024 | CBOM, ML-BOM enhancements, attestations |
| 1.5 | 2023 | Formulation, licensing improvements |
| 1.4 | 2022 | Services, compositions |
| 1.3 | 2021 | External references, evidence |
| 1.2 | 2020 | Dependency graph |
| 1.1 | 2019 | SWID, pedigree |
| 1.0 | 2018 | Initial release |

## Tools

### Generation
- **cdxgen** - Multi-ecosystem generator (recommended)
- **trivy** - Security scanner with SBOM
- **CycloneDX CLI** - Official tool

### Validation
```bash
cyclonedx-cli validate --input-file sbom.cdx.json --fail-on-errors
```

### Conversion
```bash
# JSON to XML
cyclonedx-cli convert --input-file sbom.cdx.json --output-file sbom.cdx.xml

# Merge multiple SBOMs
cyclonedx-cli merge --input-files sbom1.json sbom2.json --output-file merged.json
```

## References

- [CycloneDX Specification](https://cyclonedx.org/specification/overview/)
- [JSON Schema](https://github.com/CycloneDX/specification/blob/master/schema/bom-1.6.schema.json)
- [Tool Center](https://cyclonedx.org/tool-center/)
- [Use Cases](https://cyclonedx.org/use-cases/)
- [ECMA-424 Standard](https://ecma-international.org/publications-and-standards/standards/ecma-424/)
