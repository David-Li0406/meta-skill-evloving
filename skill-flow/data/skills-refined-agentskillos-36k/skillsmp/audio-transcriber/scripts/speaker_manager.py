"""Speaker enrollment and re-identification system."""

import os
import json
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import faiss
import torch
from scipy.spatial.distance import cosine
from dataclasses import dataclass, asdict
from datetime import datetime
import librosa
import pickle

logger = logging.getLogger(__name__)


@dataclass
class EnrolledSpeaker:
    """Represents an enrolled speaker profile."""
    name: str
    id: str
    embedding: np.ndarray
    samples_count: int
    total_duration: float
    created_at: str
    updated_at: str
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (excluding embedding)."""
        data = asdict(self)
        data.pop('embedding')  # Don't include raw embedding in dict
        return data


class SpeakerManager:
    """Manage speaker enrollment and identification."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize speaker manager."""
        self.config = config
        self.embeddings_dir = Path(config.get('paths.embeddings_dir', './embeddings'))
        self.similarity_threshold = config.get('speaker.similarity_threshold', 0.7)
        self.min_samples = config.get('speaker.min_samples_per_speaker', 3)
        self.max_enrollment_duration = config.get('speaker.max_enrollment_duration_s', 120)
        self.embedding_dim = config.get('speaker.embedding_dim', 192)
        
        # Create directories
        self.embeddings_dir.mkdir(parents=True, exist_ok=True)
        
        # File paths
        self.registry_path = self.embeddings_dir / 'registry.yaml'
        self.embeddings_path = self.embeddings_dir / 'embeddings.npy'
        self.index_path = self.embeddings_dir / 'index.faiss'
        
        # Load or initialize data
        self.speakers = {}
        self.embeddings = None
        self.index = None
        
        self._load_registry()
        self._load_embeddings()
        self._build_index()
        
        # Load embedding model
        self.embedding_model = None
        self._load_embedding_model()
    
    def _load_embedding_model(self) -> None:
        """Load speaker embedding model."""
        try:
            from speechbrain.pretrained import EncoderClassifier
            
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            
            self.embedding_model = EncoderClassifier.from_hparams(
                source="speechbrain/spkrec-ecapa-voxceleb",
                savedir="models/speechbrain",
                run_opts={"device": device}
            )
            
            logger.info("Loaded speaker embedding model")
            
        except Exception as e:
            logger.error(f"Error loading embedding model: {str(e)}")
            # Try pyannote embedding as fallback
            try:
                from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
                
                device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
                self.embedding_model = PretrainedSpeakerEmbedding(
                    "speechbrain/spkrec-ecapa-voxceleb",
                    device=device
                )
                logger.info("Loaded pyannote speaker embedding model")
            except Exception as e2:
                logger.error(f"Error loading fallback embedding model: {str(e2)}")
                raise
    
    def _load_registry(self) -> None:
        """Load speaker registry from file."""
        if self.registry_path.exists():
            try:
                with open(self.registry_path, 'r') as f:
                    registry_data = yaml.safe_load(f) or {}
                
                # Convert to EnrolledSpeaker objects (without embeddings)
                for speaker_id, data in registry_data.items():
                    self.speakers[speaker_id] = data
                
                logger.info(f"Loaded {len(self.speakers)} enrolled speakers")
                
            except Exception as e:
                logger.error(f"Error loading speaker registry: {str(e)}")
                self.speakers = {}
    
    def _save_registry(self) -> None:
        """Save speaker registry to file."""
        try:
            # Convert speakers to serializable format
            registry_data = {}
            for speaker_id, speaker in self.speakers.items():
                if isinstance(speaker, EnrolledSpeaker):
                    registry_data[speaker_id] = speaker.to_dict()
                else:
                    registry_data[speaker_id] = speaker
            
            with open(self.registry_path, 'w') as f:
                yaml.dump(registry_data, f, default_flow_style=False)
            
            logger.info(f"Saved {len(registry_data)} speakers to registry")
            
        except Exception as e:
            logger.error(f"Error saving speaker registry: {str(e)}")
    
    def _load_embeddings(self) -> None:
        """Load speaker embeddings from file."""
        if self.embeddings_path.exists():
            try:
                self.embeddings = np.load(str(self.embeddings_path))
                logger.info(f"Loaded embeddings matrix: {self.embeddings.shape}")
            except Exception as e:
                logger.error(f"Error loading embeddings: {str(e)}")
                self.embeddings = None
    
    def _save_embeddings(self) -> None:
        """Save speaker embeddings to file."""
        if self.embeddings is not None:
            try:
                np.save(str(self.embeddings_path), self.embeddings)
                logger.info(f"Saved embeddings matrix: {self.embeddings.shape}")
            except Exception as e:
                logger.error(f"Error saving embeddings: {str(e)}")
    
    def _build_index(self) -> None:
        """Build FAISS index for fast similarity search."""
        if self.embeddings is not None and len(self.embeddings) > 0:
            try:
                # Create L2 normalized index for cosine similarity
                self.index = faiss.IndexFlatIP(self.embedding_dim)  # Inner product
                
                # Normalize embeddings for cosine similarity
                faiss.normalize_L2(self.embeddings)
                
                # Add to index
                self.index.add(self.embeddings)
                
                logger.info(f"Built FAISS index with {self.index.ntotal} embeddings")
                
            except Exception as e:
                logger.error(f"Error building FAISS index: {str(e)}")
                self.index = None
    
    def _save_index(self) -> None:
        """Save FAISS index to file."""
        if self.index is not None:
            try:
                faiss.write_index(self.index, str(self.index_path))
                logger.info("Saved FAISS index")
            except Exception as e:
                logger.error(f"Error saving FAISS index: {str(e)}")
    
    def extract_embedding(self, audio_path: Path) -> Optional[np.ndarray]:
        """
        Extract speaker embedding from audio file.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Speaker embedding vector
        """
        try:
            # Load audio
            audio, sr = librosa.load(str(audio_path), sr=16000)
            
            # Limit duration
            max_samples = int(self.max_enrollment_duration * sr)
            if len(audio) > max_samples:
                audio = audio[:max_samples]
            
            # Extract embedding
            if hasattr(self.embedding_model, 'encode_batch'):
                # SpeechBrain
                embedding = self.embedding_model.encode_batch(
                    torch.tensor(audio).unsqueeze(0)
                )
                return embedding.squeeze().cpu().numpy()
            else:
                # Pyannote
                embedding = self.embedding_model(
                    {'waveform': torch.tensor(audio).unsqueeze(0).unsqueeze(0),
                     'sample_rate': sr}
                )
                return embedding.squeeze().cpu().numpy()
            
        except Exception as e:
            logger.error(f"Error extracting embedding from {audio_path}: {str(e)}")
            return None
    
    def enroll_speaker(
        self,
        name: str,
        audio_files: List[Path],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, str]:
        """
        Enroll a new speaker or update existing.
        
        Args:
            name: Speaker name
            audio_files: List of audio files for enrollment
            metadata: Optional metadata
            
        Returns:
            Tuple of (success, speaker_id or error message)
        """
        if len(audio_files) < self.min_samples:
            return False, f"Need at least {self.min_samples} audio samples"
        
        # Extract embeddings from all files
        embeddings = []
        total_duration = 0
        
        for audio_path in audio_files:
            if not audio_path.exists():
                logger.warning(f"Audio file not found: {audio_path}")
                continue
            
            embedding = self.extract_embedding(audio_path)
            if embedding is not None:
                embeddings.append(embedding)
                
                # Get duration
                import soundfile as sf
                info = sf.info(str(audio_path))
                total_duration += info.duration
        
        if len(embeddings) < self.min_samples:
            return False, f"Could only extract {len(embeddings)} valid embeddings"
        
        # Compute mean embedding
        embeddings = np.array(embeddings)
        mean_embedding = np.mean(embeddings, axis=0)
        
        # Normalize
        mean_embedding = mean_embedding / np.linalg.norm(mean_embedding)
        
        # Generate speaker ID
        speaker_id = f"SPK_{name.upper().replace(' ', '_')}_{len(self.speakers):04d}"
        
        # Create speaker profile
        speaker = EnrolledSpeaker(
            name=name,
            id=speaker_id,
            embedding=mean_embedding,
            samples_count=len(embeddings),
            total_duration=total_duration,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            metadata=metadata or {}
        )
        
        # Add to registry
        self.speakers[speaker_id] = speaker
        
        # Update embeddings matrix
        if self.embeddings is None:
            self.embeddings = mean_embedding.reshape(1, -1)
        else:
            self.embeddings = np.vstack([self.embeddings, mean_embedding])
        
        # Rebuild index
        self._build_index()
        
        # Save everything
        self._save_registry()
        self._save_embeddings()
        self._save_index()
        
        logger.info(f"Enrolled speaker '{name}' with ID {speaker_id}")
        return True, speaker_id
    
    def identify_speaker(
        self,
        embedding: np.ndarray,
        threshold: Optional[float] = None
    ) -> Tuple[Optional[str], float]:
        """
        Identify speaker from embedding.
        
        Args:
            embedding: Speaker embedding
            threshold: Similarity threshold
            
        Returns:
            Tuple of (speaker_id, similarity_score)
        """
        if self.index is None or self.index.ntotal == 0:
            return None, 0.0
        
        threshold = threshold or self.similarity_threshold
        
        # Normalize embedding
        embedding = embedding / np.linalg.norm(embedding)
        
        # Search in index
        k = min(5, self.index.ntotal)  # Top 5 matches
        distances, indices = self.index.search(embedding.reshape(1, -1), k)
        
        # Get best match
        best_distance = distances[0][0]
        best_index = indices[0][0]
        
        # Cosine similarity from inner product (after normalization)
        similarity = best_distance
        
        if similarity >= threshold:
            # Find speaker ID from index
            speaker_ids = list(self.speakers.keys())
            if best_index < len(speaker_ids):
                speaker_id = speaker_ids[best_index]
                return speaker_id, similarity
        
        return None, similarity
    
    def identify_from_audio(
        self,
        audio_path: Path,
        threshold: Optional[float] = None
    ) -> Tuple[Optional[str], Optional[str], float]:
        """
        Identify speaker from audio file.
        
        Args:
            audio_path: Path to audio file
            threshold: Similarity threshold
            
        Returns:
            Tuple of (speaker_id, speaker_name, similarity)
        """
        embedding = self.extract_embedding(audio_path)
        if embedding is None:
            return None, None, 0.0
        
        speaker_id, similarity = self.identify_speaker(embedding, threshold)
        
        if speaker_id and speaker_id in self.speakers:
            speaker = self.speakers[speaker_id]
            if isinstance(speaker, EnrolledSpeaker):
                return speaker_id, speaker.name, similarity
            else:
                return speaker_id, speaker.get('name', 'Unknown'), similarity
        
        return None, None, similarity
    
    def map_diarization_to_enrolled(
        self,
        diarization_embeddings: Dict[str, np.ndarray],
        threshold: Optional[float] = None
    ) -> Dict[str, str]:
        """
        Map diarization speaker IDs to enrolled speakers.
        
        Args:
            diarization_embeddings: Dict of diarization speaker ID to embedding
            threshold: Similarity threshold
            
        Returns:
            Mapping from diarization ID to enrolled speaker name
        """
        mapping = {}
        
        for diar_id, embedding in diarization_embeddings.items():
            speaker_id, similarity = self.identify_speaker(embedding, threshold)
            
            if speaker_id and speaker_id in self.speakers:
                speaker = self.speakers[speaker_id]
                if isinstance(speaker, EnrolledSpeaker):
                    mapping[diar_id] = speaker.name
                else:
                    mapping[diar_id] = speaker.get('name', diar_id)
            else:
                # Keep original ID if no match
                mapping[diar_id] = diar_id
        
        return mapping
    
    def update_speaker(
        self,
        speaker_id: str,
        audio_files: Optional[List[Path]] = None,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Update enrolled speaker profile.
        
        Args:
            speaker_id: Speaker ID to update
            audio_files: New audio files to add
            name: New name
            metadata: New metadata
            
        Returns:
            Success status
        """
        if speaker_id not in self.speakers:
            logger.error(f"Speaker {speaker_id} not found")
            return False
        
        speaker = self.speakers[speaker_id]
        
        # Update name if provided
        if name:
            if isinstance(speaker, EnrolledSpeaker):
                speaker.name = name
            else:
                speaker['name'] = name
        
        # Update metadata if provided
        if metadata:
            if isinstance(speaker, EnrolledSpeaker):
                speaker.metadata.update(metadata)
            else:
                speaker['metadata'] = metadata
        
        # Add new audio samples if provided
        if audio_files:
            embeddings = []
            
            for audio_path in audio_files:
                embedding = self.extract_embedding(audio_path)
                if embedding is not None:
                    embeddings.append(embedding)
            
            if embeddings:
                # Update embedding (weighted average with existing)
                new_embeddings = np.array(embeddings)
                new_mean = np.mean(new_embeddings, axis=0)
                
                if isinstance(speaker, EnrolledSpeaker):
                    # Weighted average based on sample count
                    old_weight = speaker.samples_count
                    new_weight = len(embeddings)
                    total_weight = old_weight + new_weight
                    
                    speaker.embedding = (
                        speaker.embedding * old_weight + new_mean * new_weight
                    ) / total_weight
                    
                    speaker.samples_count += len(embeddings)
                    speaker.updated_at = datetime.now().isoformat()
                
                # Update in embeddings matrix
                speaker_ids = list(self.speakers.keys())
                idx = speaker_ids.index(speaker_id)
                if idx < len(self.embeddings):
                    if isinstance(speaker, EnrolledSpeaker):
                        self.embeddings[idx] = speaker.embedding
                
                # Rebuild index
                self._build_index()
        
        # Save changes
        self._save_registry()
        self._save_embeddings()
        self._save_index()
        
        return True
    
    def delete_speaker(self, speaker_id: str) -> bool:
        """
        Delete enrolled speaker.
        
        Args:
            speaker_id: Speaker ID to delete
            
        Returns:
            Success status
        """
        if speaker_id not in self.speakers:
            return False
        
        # Remove from registry
        del self.speakers[speaker_id]
        
        # Rebuild embeddings matrix
        if self.speakers:
            embeddings_list = []
            for sid, speaker in self.speakers.items():
                if isinstance(speaker, EnrolledSpeaker):
                    embeddings_list.append(speaker.embedding)
            
            if embeddings_list:
                self.embeddings = np.array(embeddings_list)
            else:
                self.embeddings = None
        else:
            self.embeddings = None
        
        # Rebuild index
        self._build_index()
        
        # Save changes
        self._save_registry()
        self._save_embeddings()
        self._save_index()
        
        logger.info(f"Deleted speaker {speaker_id}")
        return True
    
    def list_speakers(self) -> List[Dict[str, Any]]:
        """Get list of all enrolled speakers."""
        speakers_list = []
        
        for speaker_id, speaker in self.speakers.items():
            if isinstance(speaker, EnrolledSpeaker):
                speakers_list.append(speaker.to_dict())
            else:
                speakers_list.append(speaker)
        
        return speakers_list