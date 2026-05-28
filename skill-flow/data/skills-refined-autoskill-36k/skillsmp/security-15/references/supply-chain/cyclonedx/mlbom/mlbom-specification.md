# CycloneDX ML-BOM Specification Reference

## Overview

**ML-BOM** (Machine Learning Bill of Materials) is a CycloneDX capability for documenting AI/ML components including models, datasets, and their associated metadata.

**Specification Version**: 1.6+
**Component Type**: `machine-learning-model`
**Primary Object**: `modelCard`

## Component Type

```json
{
  "type": "machine-learning-model",
  "name": "my-model",
  "version": "1.0.0",
  "bom-ref": "model/my-model@1.0.0",
  "modelCard": { ... }
}
```

**Definition**: "A model based on training data that can make predictions or decisions without being explicitly programmed to do so."

## ModelCard Object Structure

The `modelCard` object contains comprehensive ML model documentation:

```json
{
  "modelCard": {
    "modelParameters": {
      "approach": {
        "type": "supervised"
      },
      "task": "text-to-speech",
      "architectureFamily": "transformer",
      "modelArchitecture": "encoder-decoder",
      "datasets": [
        {
          "type": "dataset",
          "ref": "dataset/training-data@1.0.0",
          "contents": {
            "url": "https://example.com/dataset"
          }
        }
      ],
      "inputs": [
        {
          "format": "string"
        }
      ],
      "outputs": [
        {
          "format": "audio/wav"
        }
      ]
    },
    "quantitativeAnalysis": {
      "performanceMetrics": [
        {
          "type": "accuracy",
          "value": "0.95",
          "confidenceInterval": {
            "lowerBound": "0.93",
            "upperBound": "0.97"
          }
        }
      ],
      "graphics": {
        "collection": []
      }
    },
    "considerations": {
      "users": ["speech synthesis applications"],
      "useCases": ["accessibility tools", "voice assistants"],
      "technicalLimitations": ["may struggle with rare languages"],
      "performanceTradeoffs": ["higher quality = slower inference"],
      "ethicalConsiderations": [
        {
          "name": "voice cloning risk",
          "mitigationStrategy": "watermarking output"
        }
      ],
      "fairnessAssessments": [
        {
          "groupAtRisk": "non-native speakers",
          "benefits": "improved accessibility",
          "harms": "potential accent bias",
          "mitigationStrategy": "diverse training data"
        }
      ]
    }
  }
}
```

## ModelParameters Fields

| Field | Type | Description |
|-------|------|-------------|
| `approach.type` | enum | Learning approach: `supervised`, `unsupervised`, `reinforcement-learning`, `semi-supervised`, `self-supervised` |
| `task` | string | Primary task (e.g., classification, generation, translation) |
| `architectureFamily` | string | Model family: `transformer`, `cnn`, `rnn`, `lstm`, `residual-network`, `generative-adversarial-network` |
| `modelArchitecture` | string | Specific architecture (e.g., GPT-4, LLaMA-3, ResNet-50, YOLOv3) |
| `datasets` | array | Training and evaluation datasets |
| `inputs` | array | Expected input formats |
| `outputs` | array | Output formats produced |

## Dataset Reference

```json
{
  "datasets": [
    {
      "type": "dataset",
      "ref": "dataset/imagenet@2012",
      "contents": {
        "url": "https://image-net.org",
        "properties": [
          {
            "name": "size",
            "value": "1.2M images"
          }
        ]
      },
      "classification": "training",
      "governance": {
        "license": {
          "id": "CC-BY-4.0"
        }
      }
    }
  ]
}
```

## QuantitativeAnalysis Fields

| Field | Type | Description |
|-------|------|-------------|
| `performanceMetrics` | array | Model performance measurements |
| `performanceMetrics[].type` | string | Metric type (accuracy, precision, recall, f1, auc, mae, mse) |
| `performanceMetrics[].value` | string | Metric value |
| `performanceMetrics[].confidenceInterval` | object | Statistical confidence bounds |
| `graphics` | object | Visual performance representations |

## Considerations Fields

| Field | Type | Description |
|-------|------|-------------|
| `users` | array | Intended user categories |
| `useCases` | array | Intended use cases |
| `technicalLimitations` | array | Known technical constraints |
| `performanceTradeoffs` | array | Speed/accuracy tradeoffs |
| `ethicalConsiderations` | array | Ethical risks and mitigations |
| `fairnessAssessments` | array | Impact on at-risk groups |

## Pedigree (Model Lineage)

Track model derivation and fine-tuning:

```json
{
  "pedigree": {
    "ancestors": [
      {
        "type": "machine-learning-model",
        "name": "base-model",
        "version": "1.0.0",
        "description": "Pre-trained foundation model"
      }
    ],
    "notes": "Fine-tuned on domain-specific data"
  }
}
```

## Complete ML-BOM Example

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.6",
  "serialNumber": "urn:uuid:3e671687-395b-41f5-a30f-a58921a69b79",
  "version": 1,
  "metadata": {
    "timestamp": "2024-12-24T10:00:00Z",
    "tools": [{
      "vendor": "Zero",
      "name": "tech-id-scanner",
      "version": "3.7.0"
    }]
  },
  "components": [
    {
      "type": "machine-learning-model",
      "name": "sentiment-classifier",
      "version": "2.1.0",
      "bom-ref": "model/sentiment-classifier@2.1.0",
      "description": "BERT-based sentiment analysis model",
      "licenses": [{
        "license": { "id": "Apache-2.0" }
      }],
      "externalReferences": [
        {
          "type": "website",
          "url": "https://huggingface.co/example/sentiment"
        }
      ],
      "modelCard": {
        "modelParameters": {
          "approach": { "type": "supervised" },
          "task": "sentiment-analysis",
          "architectureFamily": "transformer",
          "modelArchitecture": "BERT-base",
          "datasets": [
            {
              "type": "dataset",
              "ref": "dataset/imdb-reviews@1.0",
              "classification": "training"
            }
          ],
          "inputs": [{ "format": "string" }],
          "outputs": [{ "format": "application/json" }]
        },
        "quantitativeAnalysis": {
          "performanceMetrics": [
            { "type": "accuracy", "value": "0.92" },
            { "type": "f1", "value": "0.91" }
          ]
        },
        "considerations": {
          "useCases": ["product review analysis", "social media monitoring"],
          "technicalLimitations": ["English only", "max 512 tokens"],
          "ethicalConsiderations": [
            {
              "name": "sentiment manipulation detection",
              "mitigationStrategy": "ensemble with other signals"
            }
          ]
        }
      }
    }
  ]
}
```

## Mapping from Zero tech-id Scanner

| Zero Field | CycloneDX Field |
|------------|-----------------|
| `models[].name` | `component.name` |
| `models[].path` | `component.externalReferences[].url` |
| `models[].format` | `modelCard.modelParameters.architectureFamily` |
| `models[].framework` | `component.description` |
| `frameworks[].name` | Related component dependency |
| `datasets[].name` | `modelCard.modelParameters.datasets[].ref` |
| `ai_security[].severity` | `vulnerabilities[]` |

## References

- [CycloneDX ML-BOM Capability](https://cyclonedx.org/capabilities/mlbom/)
- [AI Models Use Case](https://cyclonedx.org/use-cases/ai-models-and-model-cards/)
- [CycloneDX 1.6 JSON Schema](https://github.com/CycloneDX/specification/blob/master/schema/bom-1.6.schema.json)
