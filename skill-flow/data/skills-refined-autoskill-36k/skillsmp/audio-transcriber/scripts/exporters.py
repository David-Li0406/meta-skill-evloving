"""Export transcription results to various formats."""

import json
import csv
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import timedelta
import re

logger = logging.getLogger(__name__)


class BaseExporter:
    """Base class for transcript exporters."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize exporter with configuration."""
        self.config = config
        self.include_confidence = config.get('export.include_confidence', True)
        self.include_word_timestamps = config.get('export.include_word_timestamps', True)
        self.max_line_length = config.get('export.max_line_length', 80)
        self.merge_consecutive = config.get('export.merge_consecutive_segments', True)
        self.merge_threshold = config.get('export.merge_threshold_s', 0.5)
    
    def export(self, data: Dict[str, Any], output_path: Path) -> bool:
        """
        Export transcription data to file.
        
        Args:
            data: Transcription data
            output_path: Output file path
            
        Returns:
            Success status
        """
        raise NotImplementedError("Subclasses must implement export method")
    
    def _format_timestamp(self, seconds: float, format_type: str = 'srt') -> str:
        """Format timestamp for different subtitle formats."""
        td = timedelta(seconds=seconds)
        hours = int(td.total_seconds() // 3600)
        minutes = int((td.total_seconds() % 3600) // 60)
        secs = td.total_seconds() % 60
        
        if format_type == 'srt':
            # SRT format: HH:MM:SS,mmm
            return f"{hours:02d}:{minutes:02d}:{secs:06.3f}".replace('.', ',')
        elif format_type == 'vtt':
            # VTT format: HH:MM:SS.mmm
            return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"
        else:
            # Generic format
            return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"
    
    def _wrap_text(self, text: str, max_length: int = 80) -> List[str]:
        """Wrap text to multiple lines."""
        if len(text) <= max_length:
            return [text]
        
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_length:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def _merge_segments(self, segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Merge consecutive segments from same speaker."""
        if not self.merge_consecutive or not segments:
            return segments
        
        merged = []
        current = None
        
        for segment in segments:
            if current is None:
                current = segment.copy()
            elif (segment.get('speaker_name') == current.get('speaker_name') and
                  segment['start'] - current['end'] <= self.merge_threshold):
                # Merge segments
                current['end'] = segment['end']
                current['text'] += ' ' + segment['text']
                
                # Merge words if present
                if 'words' in current and 'words' in segment:
                    current['words'].extend(segment['words'])
            else:
                merged.append(current)
                current = segment.copy()
        
        if current:
            merged.append(current)
        
        return merged


class SRTExporter(BaseExporter):
    """Export transcription to SRT subtitle format."""
    
    def export(self, data: Dict[str, Any], output_path: Path) -> bool:
        """Export to SRT format."""
        try:
            segments = data.get('segments', [])
            merged_segments = self._merge_segments(segments)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                for i, segment in enumerate(merged_segments, 1):
                    start_time = self._format_timestamp(segment['start'], 'srt')
                    end_time = self._format_timestamp(segment['end'], 'srt')
                    
                    # Format text with speaker name if available
                    text = segment['text'].strip()
                    speaker = segment.get('speaker_name', '')
                    
                    if speaker and speaker != 'UNKNOWN':
                        text = f"{speaker}: {text}"
                    
                    # Wrap long lines
                    lines = self._wrap_text(text, self.max_line_length)
                    
                    # Write SRT entry
                    f.write(f"{i}\n")
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write('\n'.join(lines))
                    f.write('\n\n')
            
            logger.info(f"Exported SRT to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting SRT: {str(e)}")
            return False


class VTTExporter(BaseExporter):
    """Export transcription to WebVTT format."""
    
    def export(self, data: Dict[str, Any], output_path: Path) -> bool:
        """Export to VTT format."""
        try:
            segments = data.get('segments', [])
            merged_segments = self._merge_segments(segments)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                # VTT header
                f.write("WEBVTT\n\n")
                
                # Add metadata if available
                if 'language' in data:
                    f.write(f"NOTE Language: {data['language']}\n\n")
                
                for segment in merged_segments:
                    start_time = self._format_timestamp(segment['start'], 'vtt')
                    end_time = self._format_timestamp(segment['end'], 'vtt')
                    
                    # Format text with speaker
                    text = segment['text'].strip()
                    speaker = segment.get('speaker_name', '')
                    
                    if speaker and speaker != 'UNKNOWN':
                        # VTT speaker notation
                        f.write(f"{start_time} --> {end_time}\n")
                        f.write(f"<v {speaker}>{text}\n\n")
                    else:
                        f.write(f"{start_time} --> {end_time}\n")
                        f.write(f"{text}\n\n")
            
            logger.info(f"Exported VTT to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting VTT: {str(e)}")
            return False


class CSVExporter(BaseExporter):
    """Export transcription to CSV format."""
    
    def export(self, data: Dict[str, Any], output_path: Path) -> bool:
        """Export to CSV format."""
        try:
            segments = data.get('segments', [])
            
            fieldnames = [
                'segment_id', 'start_time', 'end_time', 'duration',
                'text', 'speaker_id', 'speaker_name'
            ]
            
            # Add optional fields
            if self.include_confidence:
                fieldnames.extend(['avg_logprob', 'no_speech_prob'])
            
            if self.include_word_timestamps:
                fieldnames.extend(['word_count', 'words_json'])
            
            # Add voice sex fields if present
            if segments and 'voice_sex' in segments[0]:
                fieldnames.extend([
                    'voice_sex_classification', 'voice_sex_confidence',
                    'voice_sex_male_prob', 'voice_sex_female_prob'
                ])
            
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for segment in segments:
                    row = {
                        'segment_id': segment.get('id', ''),
                        'start_time': segment['start'],
                        'end_time': segment['end'],
                        'duration': segment['end'] - segment['start'],
                        'text': segment['text'].strip(),
                        'speaker_id': segment.get('speaker_id', segment.get('speaker', '')),
                        'speaker_name': segment.get('speaker_name', segment.get('speaker', ''))
                    }
                    
                    # Add confidence scores
                    if self.include_confidence:
                        row['avg_logprob'] = segment.get('avg_logprob', '')
                        row['no_speech_prob'] = segment.get('no_speech_prob', '')
                    
                    # Add word information
                    if self.include_word_timestamps and 'words' in segment:
                        row['word_count'] = len(segment['words'])
                        row['words_json'] = json.dumps(segment['words'])
                    
                    # Add voice sex information
                    if 'voice_sex' in segment:
                        voice_sex = segment['voice_sex']
                        row['voice_sex_classification'] = voice_sex.get('classification', '')
                        row['voice_sex_confidence'] = voice_sex.get('confidence', '')
                        probs = voice_sex.get('probabilities', {})
                        row['voice_sex_male_prob'] = probs.get('male_like', '')
                        row['voice_sex_female_prob'] = probs.get('female_like', '')
                    
                    writer.writerow(row)
            
            logger.info(f"Exported CSV to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting CSV: {str(e)}")
            return False


class JSONExporter(BaseExporter):
    """Export transcription to detailed JSON format."""
    
    def export(self, data: Dict[str, Any], output_path: Path) -> bool:
        """Export to JSON format."""
        try:
            # Create enhanced JSON with metadata
            enhanced_data = data.copy()
            
            # Add export metadata
            enhanced_data['export_info'] = {
                'format': 'json',
                'exported_at': self._get_current_timestamp(),
                'include_confidence': self.include_confidence,
                'include_word_timestamps': self.include_word_timestamps,
                'segments_merged': self.merge_consecutive
            }
            
            # Add statistics
            segments = data.get('segments', [])
            if segments:
                enhanced_data['statistics'] = {
                    'total_segments': len(segments),
                    'total_duration': max(s['end'] for s in segments) if segments else 0,
                    'unique_speakers': len(set(
                        s.get('speaker_name', s.get('speaker', 'UNKNOWN')) 
                        for s in segments
                    )),
                    'total_words': sum(len(s.get('words', [])) for s in segments),
                    'average_confidence': sum(
                        s.get('avg_logprob', 0) for s in segments
                    ) / len(segments) if segments else 0
                }
            
            # Process segments for export
            if not self.include_confidence:
                for segment in segments:
                    segment.pop('avg_logprob', None)
                    segment.pop('no_speech_prob', None)
                    segment.pop('compression_ratio', None)
                    segment.pop('temperature', None)
            
            if not self.include_word_timestamps:
                for segment in segments:
                    segment.pop('words', None)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(enhanced_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Exported JSON to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting JSON: {str(e)}")
            return False
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()


class ExportManager:
    """Manage exports to multiple formats."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize export manager."""
        self.config = config
        self.exporters = {
            'srt': SRTExporter(config),
            'vtt': VTTExporter(config),
            'csv': CSVExporter(config),
            'json': JSONExporter(config)
        }
    
    def export_all_formats(
        self,
        data: Dict[str, Any],
        output_dir: Path,
        formats: Optional[List[str]] = None
    ) -> Dict[str, bool]:
        """
        Export to multiple formats.
        
        Args:
            data: Transcription data
            output_dir: Output directory
            formats: List of formats to export (all if None)
            
        Returns:
            Dictionary of format -> success status
        """
        formats = formats or self.config.get('export.formats', ['srt', 'vtt', 'json', 'csv'])
        results = {}
        
        for format_name in formats:
            if format_name in self.exporters:
                output_path = output_dir / f"transcript.{format_name}"
                success = self.exporters[format_name].export(data, output_path)
                results[format_name] = success
            else:
                logger.warning(f"Unknown export format: {format_name}")
                results[format_name] = False
        
        return results
    
    def export_format(
        self,
        data: Dict[str, Any],
        output_path: Path,
        format_name: str
    ) -> bool:
        """
        Export to specific format.
        
        Args:
            data: Transcription data
            output_path: Output file path
            format_name: Export format name
            
        Returns:
            Success status
        """
        if format_name not in self.exporters:
            logger.error(f"Unknown export format: {format_name}")
            return False
        
        return self.exporters[format_name].export(data, output_path)