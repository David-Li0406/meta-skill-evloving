"""JSON schemas for LLM structured outputs.

These dataclasses define the structure of LLM responses and can generate
JSON Schema for use with OpenAI's structured outputs API.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# --- Claim Relations Schema ---

@dataclass
class ClaimRelation:
    """A relation between two claims."""
    from_uri: str
    type: str  # "extends" | "refutes" | "supports"
    to_uri: str


@dataclass
class ClaimRelationsResponse:
    """Response containing claim relations."""
    relations: list[ClaimRelation] = field(default_factory=list)

    @staticmethod
    def json_schema() -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "relations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "from_uri": {
                                "type": "string",
                                "description": "URI of the claim making the relation"
                            },
                            "type": {
                                "type": "string",
                                "enum": ["extends", "refutes", "supports"],
                                "description": "Type of relation"
                            },
                            "to_uri": {
                                "type": "string",
                                "description": "URI of the claim being related to"
                            }
                        },
                        "required": ["from_uri", "type", "to_uri"],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["relations"],
            "additionalProperties": False
        }


# --- Concept Extraction Schema ---

@dataclass
class ExtractedConcept:
    """A concept extracted from a paper."""
    name: str
    description: str
    broader: str | None = None
    partOf: str | None = None
    dependsOn: str | None = None


@dataclass
class ExtractedClaim:
    """A claim extracted from a paper."""
    text: str
    regarding: list[str] = field(default_factory=list)
    extends: str | None = None
    refutes: str | None = None
    supports: str | None = None


@dataclass
class ExtractionResponse:
    """Response containing extracted concepts and claims."""
    concepts: list[ExtractedConcept] = field(default_factory=list)
    claims: list[ExtractedClaim] = field(default_factory=list)

    @staticmethod
    def json_schema() -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "concepts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Concept name"},
                            "description": {
                                "type": "string",
                                "description": "Brief description of the concept (1-2 sentences)"
                            },
                            "broader": {
                                "type": ["string", "null"],
                                "description": "Parent concept (is-a relationship). e.g., CNN broader neural network"
                            },
                            "partOf": {
                                "type": ["string", "null"],
                                "description": "Whole that contains this concept. e.g., attention mechanism partOf transformer"
                            },
                            "dependsOn": {
                                "type": ["string", "null"],
                                "description": "Prerequisite concept. e.g., fine-tuning dependsOn pre-trained model"
                            }
                        },
                        "required": ["name", "description", "broader", "partOf", "dependsOn"],
                        "additionalProperties": False
                    },
                    "description": "Key technical concepts with their relationships"
                },
                "claims": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "A specific, verifiable statement about findings or contributions"
                            },
                            "regarding": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Concept names this claim is about (from concepts list above)"
                            },
                            "extends": {
                                "type": ["string", "null"],
                                "description": "URI of claim this builds upon or extends"
                            },
                            "refutes": {
                                "type": ["string", "null"],
                                "description": "URI of claim this contradicts or argues against"
                            },
                            "supports": {
                                "type": ["string", "null"],
                                "description": "URI of claim this provides evidence for"
                            }
                        },
                        "required": ["text", "regarding", "extends", "refutes", "supports"],
                        "additionalProperties": False
                    },
                    "description": "Claims made by the paper"
                }
            },
            "required": ["concepts", "claims"],
            "additionalProperties": False
        }
