# Privacy Guardian

## Patterns


---
  #### **Name**
Differential Privacy for Federation
  #### **Description**
Privacy-preserving pattern sharing with mathematical guarantees
  #### **When**
Sharing aggregated patterns across users without leaking individuals
  #### **Example**
    from opendp.mod import enable_features
    from opendp.measurements import make_base_laplace
    from opendp.transformations import make_clamp, make_bounded_mean
    import numpy as np
    from dataclasses import dataclass
    from uuid import uuid4
    
    enable_features("contrib")
    
    @dataclass
    class SanitizedPattern:
        pattern_id: UUID
        trigger_type: str  # Abstracted, no specific content
        response_strategy: str
        outcome_improvement: float  # Noisy value
        source_count: int
        epsilon: float  # Privacy budget used
        delta: float
    
    class DifferentiallyPrivateFederator:
        """Federate patterns with ε-differential privacy guarantees."""
    
        # Privacy parameters
        EPSILON = 0.1  # Privacy budget per pattern
        DELTA = 1e-5   # Failure probability
    
        # Aggregation thresholds for k-anonymity
        MIN_SOURCES = 100
        MIN_USERS = 10
    
        async def sanitize_for_federation(
            self,
            pattern: LocalPattern,
        ) -> Optional[SanitizedPattern]:
            """Transform local pattern to privacy-safe version."""
    
            # 1. Check aggregation thresholds
            if pattern.source_count < self.MIN_SOURCES:
                logger.info("Below source threshold, not federating")
                return None
    
            if pattern.unique_users < self.MIN_USERS:
                logger.info("Below user threshold, not federating")
                return None
    
            # 2. Abstract content to remove specifics
            abstracted = self._abstract_pattern(pattern)
    
            # 3. Apply differential privacy to numeric values
            noisy_improvement = self._add_laplace_noise(
                value=pattern.outcome_improvement,
                sensitivity=1.0,  # Bounded by design
                epsilon=self.EPSILON,
            )
    
            # 4. Validate no PII remains
            if self._contains_pii(abstracted):
                logger.warning("PII detected, not federating")
                return None
    
            return SanitizedPattern(
                pattern_id=uuid4(),  # New ID, no link to original
                trigger_type=abstracted.trigger_type,
                response_strategy=abstracted.response_strategy,
                outcome_improvement=noisy_improvement,
                source_count=pattern.source_count,
                epsilon=self.EPSILON,
                delta=self.DELTA,
            )
    
        def _add_laplace_noise(
            self,
            value: float,
            sensitivity: float,
            epsilon: float,
        ) -> float:
            """Add Laplace noise for ε-differential privacy."""
            scale = sensitivity / epsilon
            noise = np.random.laplace(0, scale)
            return value + noise
    

---
  #### **Name**
Field-Level Encryption
  #### **Description**
Encrypt sensitive fields while allowing queries on non-sensitive data
  #### **When**
Storing memory content that needs protection at rest
  #### **Example**
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    import base64
    import os
    
    class EncryptedMemoryStore:
        """Memory store with field-level encryption."""
    
        ENCRYPTED_FIELDS = ["content", "entities", "personal_data"]
        QUERYABLE_FIELDS = ["memory_id", "user_id", "temporal_level", "embedding"]
    
        def __init__(self, master_key: bytes):
            self.fernet = Fernet(master_key)
    
        async def store(self, memory: Memory) -> None:
            """Store memory with encrypted sensitive fields."""
    
            encrypted_content = self.fernet.encrypt(
                memory.content.encode('utf-8')
            )
    
            await self.db.execute(
                """
                INSERT INTO memories (
                    memory_id, user_id,
                    encrypted_content,  -- Encrypted
                    embedding,          -- Not encrypted (for search)
                    temporal_level,     -- Not encrypted (for queries)
                    created_at
                ) VALUES ($1, $2, $3, $4, $5, $6)
                """,
                memory.memory_id,
                memory.user_id,
                encrypted_content,
                memory.embedding,
                memory.temporal_level,
                memory.created_at,
            )
    
        async def retrieve(self, memory_id: UUID) -> Memory:
            """Retrieve and decrypt memory."""
    
            row = await self.db.fetchone(
                "SELECT * FROM memories WHERE memory_id = $1",
                memory_id,
            )
    
            decrypted_content = self.fernet.decrypt(
                row['encrypted_content']
            ).decode('utf-8')
    
            return Memory(
                memory_id=row['memory_id'],
                content=decrypted_content,
                embedding=row['embedding'],
                temporal_level=row['temporal_level'],
            )
    

---
  #### **Name**
PII Detection and Sanitization
  #### **Description**
Detect and remove personally identifiable information
  #### **When**
Processing any user content before storage or federation
  #### **Example**
    import re
    from typing import List, Tuple
    from dataclasses import dataclass
    
    @dataclass
    class PIIMatch:
        type: str
        value: str
        start: int
        end: int
        confidence: float
    
    class PIIDetector:
        """Detect and sanitize PII from text content."""
    
        PATTERNS = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}\b',
            "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
            "credit_card": r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
            "ip_address": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            "date_of_birth": r'\b(?:0?[1-9]|1[0-2])[/-](?:0?[1-9]|[12]\d|3[01])[/-](?:19|20)\d{2}\b',
        }
    
        # Names are harder - use NER model
        def __init__(self, ner_model=None):
            self.ner_model = ner_model
    
        async def detect_pii(self, text: str) -> List[PIIMatch]:
            """Detect all PII in text."""
            matches = []
    
            # Regex patterns
            for pii_type, pattern in self.PATTERNS.items():
                for match in re.finditer(pattern, text, re.IGNORECASE):
                    matches.append(PIIMatch(
                        type=pii_type,
                        value=match.group(),
                        start=match.start(),
                        end=match.end(),
                        confidence=0.95,
                    ))
    
            # NER for names
            if self.ner_model:
                entities = await self.ner_model.extract(text)
                for entity in entities:
                    if entity.label in ["PERSON", "ORG", "GPE"]:
                        matches.append(PIIMatch(
                            type=entity.label.lower(),
                            value=entity.text,
                            start=entity.start,
                            end=entity.end,
                            confidence=entity.score,
                        ))
    
            return matches
    
        async def sanitize(
            self,
            text: str,
            replacement: str = "[REDACTED]",
        ) -> Tuple[str, List[PIIMatch]]:
            """Remove all PII from text."""
            matches = await self.detect_pii(text)
    
            # Sort by position descending to replace without offset issues
            matches.sort(key=lambda m: m.start, reverse=True)
    
            sanitized = text
            for match in matches:
                sanitized = (
                    sanitized[:match.start] +
                    f"[{match.type.upper()}]" +
                    sanitized[match.end:]
                )
    
            return sanitized, matches
    

---
  #### **Name**
Audit Trail with Immutability
  #### **Description**
Log all access with tamper-evident records
  #### **When**
Tracking who accessed what data and when
  #### **Example**
    import hashlib
    from datetime import datetime
    from dataclasses import dataclass
    from typing import Optional
    from uuid import UUID
    
    @dataclass
    class AuditEntry:
        entry_id: UUID
        timestamp: datetime
        user_id: UUID
        action: str  # "read", "write", "delete", "export"
        resource_type: str
        resource_id: UUID
        ip_address: str
        user_agent: str
        previous_hash: str
        entry_hash: str
    
    class ImmutableAuditLog:
        """Append-only audit log with hash chain."""
    
        async def log(
            self,
            user_id: UUID,
            action: str,
            resource_type: str,
            resource_id: UUID,
            request_context: RequestContext,
        ) -> AuditEntry:
            # Get previous entry hash for chain
            previous = await self.db.fetchone(
                "SELECT entry_hash FROM audit_log ORDER BY timestamp DESC LIMIT 1"
            )
            previous_hash = previous['entry_hash'] if previous else "genesis"
    
            # Create entry
            entry = AuditEntry(
                entry_id=uuid4(),
                timestamp=datetime.utcnow(),
                user_id=user_id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                ip_address=request_context.ip,
                user_agent=request_context.user_agent,
                previous_hash=previous_hash,
                entry_hash="",  # Computed next
            )
    
            # Compute hash of entry content
            entry.entry_hash = self._compute_hash(entry)
    
            # Append-only insert
            await self.db.execute(
                """
                INSERT INTO audit_log (
                    entry_id, timestamp, user_id, action,
                    resource_type, resource_id, ip_address,
                    user_agent, previous_hash, entry_hash
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                """,
                entry.entry_id, entry.timestamp, entry.user_id,
                entry.action, entry.resource_type, entry.resource_id,
                entry.ip_address, entry.user_agent,
                entry.previous_hash, entry.entry_hash,
            )
    
            return entry
    
        def _compute_hash(self, entry: AuditEntry) -> str:
            content = f"{entry.timestamp}{entry.user_id}{entry.action}{entry.previous_hash}"
            return hashlib.sha256(content.encode()).hexdigest()
    
        async def verify_chain(self) -> bool:
            """Verify audit log hasn't been tampered with."""
            entries = await self.db.fetch(
                "SELECT * FROM audit_log ORDER BY timestamp ASC"
            )
    
            for i, entry in enumerate(entries):
                # Verify hash
                computed = self._compute_hash(entry)
                if computed != entry['entry_hash']:
                    logger.error(f"Hash mismatch at entry {entry['entry_id']}")
                    return False
    
                # Verify chain
                if i > 0:
                    if entry['previous_hash'] != entries[i-1]['entry_hash']:
                        logger.error(f"Chain broken at entry {entry['entry_id']}")
                        return False
    
            return True
    

## Anti-Patterns


---
  #### **Name**
PII in Logs
  #### **Description**
Logging user content or identifiers to application logs
  #### **Why**
Logs are often less protected than databases. PII in logs is a breach waiting to happen.
  #### **Instead**
Log only anonymized identifiers and aggregate metrics

---
  #### **Name**
Hardcoded Secrets
  #### **Description**
API keys, encryption keys, or passwords in code
  #### **Why**
Secrets in code end up in version control, logs, error messages.
  #### **Instead**
Use secret management (Vault, AWS Secrets Manager, env vars)

---
  #### **Name**
Encryption Without Key Rotation
  #### **Description**
Using same encryption key forever
  #### **Why**
Compromised keys have unlimited blast radius without rotation.
  #### **Instead**
Implement key rotation with envelope encryption

---
  #### **Name**
Federation Without Privacy Guarantees
  #### **Description**
Sharing patterns without differential privacy or aggregation
  #### **Why**
Individual patterns can be reversed to identify users.
  #### **Instead**
Apply ε-differential privacy with proper budget tracking

---
  #### **Name**
No Data Retention Policy
  #### **Description**
Keeping all data forever without cleanup
  #### **Why**
Old data is liability. Compliance requires deletion capability.
  #### **Instead**
Implement retention policies with automated cleanup