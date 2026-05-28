"""Speaker diarization module using pyannote.audio."""

import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import torch
import numpy as np
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
from pyannote.core import Segment, Annotation
from sklearn.cluster import AgglomerativeClustering, SpectralClustering
import warnings

logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore", category=UserWarning)


class Diarizer:
    """Speaker diarization using pyannote.audio or SpeechBrain."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize diarizer with configuration."""
        self.config = config
        self.backend = config.get('diarization.backend', 'pyannote')
        self.model_name = config.get('diarization.model', 'pyannote/speaker-diarization-3.1')
        self.min_speakers = config.get('diarization.min_speakers', 1)
        self.max_speakers = config.get('diarization.max_speakers', 10)
        self.min_segment_duration = config.get('diarization.min_segment_duration', 0.5)
        
        self.pipeline = None
        self.embedding_model = None
        
        # Load models
        self._load_models()
    
    def _load_models(self) -> None:
        """Load diarization models."""
        if self.backend == 'pyannote':
            self._load_pyannote()
        elif self.backend == 'speechbrain':
            self._load_speechbrain()
        else:
            raise ValueError(f"Unsupported diarization backend: {self.backend}")
    
    def _load_pyannote(self) -> None:
        """Load pyannote.audio pipeline."""
        try:
            # Check for Hugging Face token
            hf_token = self.config.get('huggingface.token')
            
            if not hf_token:
                logger.warning(
                    "No Hugging Face token found. Some models may require authentication. "
                    "Set 'huggingface.token' in config or HF_TOKEN environment variable."
                )
            
            # Load pretrained pipeline
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            
            self.pipeline = Pipeline.from_pretrained(
                self.model_name,
                use_auth_token=hf_token
            )
            
            if device.type == 'cuda':
                self.pipeline.to(device)
            
            # Load embedding model for speaker comparison
            self.embedding_model = PretrainedSpeakerEmbedding(
                "speechbrain/spkrec-ecapa-voxceleb",
                device=device
            )
            
            logger.info(f"Loaded pyannote pipeline: {self.model_name}")
            
        except Exception as e:
            logger.error(f"Error loading pyannote pipeline: {str(e)}")
            logger.info("Falling back to embedding-based diarization")
            self._setup_embedding_diarization()
    
    def _load_speechbrain(self) -> None:
        """Load SpeechBrain models for diarization."""
        try:
            from speechbrain.pretrained import EncoderClassifier
            
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            
            # Load speaker embedding model
            self.embedding_model = EncoderClassifier.from_hparams(
                source="speechbrain/spkrec-ecapa-voxceleb",
                savedir="models/speechbrain",
                run_opts={"device": device}
            )
            
            logger.info("Loaded SpeechBrain embedding model for diarization")
            
        except Exception as e:
            logger.error(f"Error loading SpeechBrain model: {str(e)}")
            raise
    
    def _setup_embedding_diarization(self) -> None:
        """Setup embedding-based diarization as fallback."""
        try:
            from speechbrain.pretrained import EncoderClassifier
            
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            
            self.embedding_model = EncoderClassifier.from_hparams(
                source="speechbrain/spkrec-ecapa-voxceleb",
                savedir="models/speechbrain",
                run_opts={"device": device}
            )
            
            self.backend = 'embedding'
            logger.info("Using embedding-based diarization")
            
        except Exception as e:
            logger.error(f"Error setting up embedding diarization: {str(e)}")
            raise
    
    def diarize(
        self,
        audio_path: Path,
        num_speakers: Optional[int] = None,
        min_speakers: Optional[int] = None,
        max_speakers: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform speaker diarization on audio file.
        
        Args:
            audio_path: Path to audio file
            num_speakers: Exact number of speakers (if known)
            min_speakers: Minimum number of speakers
            max_speakers: Maximum number of speakers
            
        Returns:
            List of diarization segments
        """
        min_speakers = min_speakers or self.min_speakers
        max_speakers = max_speakers or self.max_speakers
        
        if self.backend == 'pyannote' and self.pipeline:
            return self._diarize_pyannote(audio_path, num_speakers, min_speakers, max_speakers)
        elif self.backend in ['speechbrain', 'embedding']:
            return self._diarize_embedding(audio_path, num_speakers, min_speakers, max_speakers)
        else:
            raise ValueError(f"No valid diarization method available")
    
    def _diarize_pyannote(
        self,
        audio_path: Path,
        num_speakers: Optional[int],
        min_speakers: int,
        max_speakers: int
    ) -> List[Dict[str, Any]]:
        """Diarize using pyannote pipeline."""
        try:
            # Prepare parameters
            params = {}
            if num_speakers:
                params['num_speakers'] = num_speakers
            else:
                params['min_speakers'] = min_speakers
                params['max_speakers'] = max_speakers
            
            # Run diarization
            diarization = self.pipeline(str(audio_path), **params)
            
            # Convert to segments
            segments = []
            for turn, _, speaker in diarization.itertracks(yield_label=True):
                if turn.duration >= self.min_segment_duration:
                    segments.append({
                        'start': turn.start,
                        'end': turn.end,
                        'duration': turn.duration,
                        'speaker': speaker
                    })
            
            # Sort by start time
            segments.sort(key=lambda x: x['start'])
            
            logger.info(f"Diarized {audio_path}: {len(segments)} segments, "
                       f"{len(set(s['speaker'] for s in segments))} speakers")
            
            return segments
            
        except Exception as e:
            logger.error(f"Error in pyannote diarization: {str(e)}")
            logger.info("Falling back to embedding-based diarization")
            return self._diarize_embedding(audio_path, num_speakers, min_speakers, max_speakers)
    
    def _diarize_embedding(
        self,
        audio_path: Path,
        num_speakers: Optional[int],
        min_speakers: int,
        max_speakers: int
    ) -> List[Dict[str, Any]]:
        """Diarize using embeddings and clustering."""
        try:
            import librosa
            
            # Load audio
            audio, sr = librosa.load(str(audio_path), sr=16000)
            
            # Segment audio into windows
            window_size = 1.5  # seconds
            hop_size = 0.75    # seconds
            
            windows = []
            timestamps = []
            
            for start in np.arange(0, len(audio) / sr, hop_size):
                end = min(start + window_size, len(audio) / sr)
                start_sample = int(start * sr)
                end_sample = int(end * sr)
                
                if end_sample - start_sample >= sr * 0.5:  # Min 0.5 seconds
                    windows.append(audio[start_sample:end_sample])
                    timestamps.append((start, end))
            
            if not windows:
                logger.warning(f"No valid windows extracted from {audio_path}")
                return []
            
            # Extract embeddings
            embeddings = []
            
            for window in windows:
                # Pad or trim to fixed size
                target_length = int(window_size * sr)
                if len(window) < target_length:
                    window = np.pad(window, (0, target_length - len(window)))
                else:
                    window = window[:target_length]
                
                # Get embedding
                if hasattr(self.embedding_model, 'encode_batch'):
                    # SpeechBrain
                    embedding = self.embedding_model.encode_batch(
                        torch.tensor(window).unsqueeze(0)
                    )
                    embeddings.append(embedding.squeeze().cpu().numpy())
                else:
                    # Pyannote embedding
                    embedding = self.embedding_model(
                        {'waveform': torch.tensor(window).unsqueeze(0).unsqueeze(0),
                         'sample_rate': sr}
                    )
                    embeddings.append(embedding.squeeze().cpu().numpy())
            
            embeddings = np.array(embeddings)
            
            # Determine number of clusters
            if num_speakers:
                n_clusters = num_speakers
            else:
                # Use silhouette score to find optimal number
                from sklearn.metrics import silhouette_score
                
                best_score = -1
                best_n = min_speakers
                
                for n in range(min_speakers, min(max_speakers + 1, len(embeddings))):
                    if n >= len(embeddings):
                        break
                    
                    clustering = AgglomerativeClustering(n_clusters=n)
                    labels = clustering.fit_predict(embeddings)
                    
                    if len(np.unique(labels)) > 1:
                        score = silhouette_score(embeddings, labels)
                        if score > best_score:
                            best_score = score
                            best_n = n
                
                n_clusters = best_n
            
            # Perform clustering
            clustering_method = self.config.get('diarization.clustering.method', 'agglomerative')
            
            if clustering_method == 'agglomerative':
                clustering = AgglomerativeClustering(
                    n_clusters=n_clusters,
                    linkage='ward'
                )
            else:
                clustering = SpectralClustering(
                    n_clusters=n_clusters,
                    affinity='nearest_neighbors'
                )
            
            labels = clustering.fit_predict(embeddings)
            
            # Create segments
            segments = []
            for i, (start, end) in enumerate(timestamps):
                segments.append({
                    'start': start,
                    'end': end,
                    'duration': end - start,
                    'speaker': f'SPEAKER_{labels[i]:02d}'
                })
            
            # Merge consecutive segments from same speaker
            merged_segments = []
            current_segment = None
            
            for segment in segments:
                if current_segment is None:
                    current_segment = segment.copy()
                elif (segment['speaker'] == current_segment['speaker'] and
                      segment['start'] - current_segment['end'] < 0.5):
                    # Merge
                    current_segment['end'] = segment['end']
                    current_segment['duration'] = current_segment['end'] - current_segment['start']
                else:
                    if current_segment['duration'] >= self.min_segment_duration:
                        merged_segments.append(current_segment)
                    current_segment = segment.copy()
            
            if current_segment and current_segment['duration'] >= self.min_segment_duration:
                merged_segments.append(current_segment)
            
            logger.info(f"Embedding diarization: {len(merged_segments)} segments, "
                       f"{n_clusters} speakers")
            
            return merged_segments
            
        except Exception as e:
            logger.error(f"Error in embedding diarization: {str(e)}")
            return []
    
    def refine_diarization(
        self,
        segments: List[Dict[str, Any]],
        min_segment_duration: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Refine diarization results.
        
        Args:
            segments: Initial diarization segments
            min_segment_duration: Minimum segment duration to keep
            
        Returns:
            Refined segments
        """
        min_duration = min_segment_duration or self.min_segment_duration
        
        # Filter short segments
        filtered = [s for s in segments if s['duration'] >= min_duration]
        
        # Merge adjacent segments from same speaker
        merged = []
        current = None
        
        for segment in filtered:
            if current is None:
                current = segment.copy()
            elif (segment['speaker'] == current['speaker'] and
                  segment['start'] - current['end'] < 0.3):
                # Merge
                current['end'] = segment['end']
                current['duration'] = current['end'] - current['start']
            else:
                merged.append(current)
                current = segment.copy()
        
        if current:
            merged.append(current)
        
        # Renumber speakers to be sequential
        speaker_map = {}
        speaker_counter = 0
        
        for segment in merged:
            speaker = segment['speaker']
            if speaker not in speaker_map:
                speaker_map[speaker] = f'SPEAKER_{speaker_counter:02d}'
                speaker_counter += 1
            segment['speaker'] = speaker_map[speaker]
        
        return merged
    
    def get_speaker_embeddings(
        self,
        audio_path: Path,
        segments: List[Dict[str, Any]]
    ) -> Dict[str, np.ndarray]:
        """
        Extract speaker embeddings for each speaker.
        
        Args:
            audio_path: Path to audio file
            segments: Diarization segments
            
        Returns:
            Dictionary mapping speaker IDs to embeddings
        """
        import librosa
        
        # Load audio
        audio, sr = librosa.load(str(audio_path), sr=16000)
        
        # Group segments by speaker
        speaker_segments = {}
        for segment in segments:
            speaker = segment['speaker']
            if speaker not in speaker_segments:
                speaker_segments[speaker] = []
            speaker_segments[speaker].append(segment)
        
        # Extract embeddings for each speaker
        speaker_embeddings = {}
        
        for speaker, segs in speaker_segments.items():
            # Collect audio from all segments
            speaker_audio = []
            
            for seg in segs[:10]:  # Limit to first 10 segments
                start_sample = int(seg['start'] * sr)
                end_sample = int(seg['end'] * sr)
                speaker_audio.append(audio[start_sample:end_sample])
            
            # Concatenate audio
            speaker_audio = np.concatenate(speaker_audio)
            
            # Limit to max duration
            max_samples = int(30 * sr)  # 30 seconds max
            if len(speaker_audio) > max_samples:
                speaker_audio = speaker_audio[:max_samples]
            
            # Get embedding
            if hasattr(self.embedding_model, 'encode_batch'):
                # SpeechBrain
                embedding = self.embedding_model.encode_batch(
                    torch.tensor(speaker_audio).unsqueeze(0)
                )
                speaker_embeddings[speaker] = embedding.squeeze().cpu().numpy()
            else:
                # Pyannote
                embedding = self.embedding_model(
                    {'waveform': torch.tensor(speaker_audio).unsqueeze(0).unsqueeze(0),
                     'sample_rate': sr}
                )
                speaker_embeddings[speaker] = embedding.squeeze().cpu().numpy()
        
        return speaker_embeddings