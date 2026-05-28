# Qt Translation Assistant (Parallel Processing)

Automated translation tool for Qt projects using AI models to translate TS (Translation Source) files with parallel processing for maximum efficiency.

## Features

- **Smart Parsing**: Identifies incomplete translations in Qt TS files (detects all unfinished formats)
- **AI-Powered Translation**: Uses advanced language models for accurate translations
- **Parallel Processing**: Multi-threaded batch translation using ThreadPoolExecutor
- **Batch Optimization**: Configurable batch size for optimal API usage
- **100% Format Preservation**: Line-number based replacement preserves ALL original formatting (quotes, spaces, indentation)
- **Error Isolation**: Single batch failure doesn't affect others
- **Retry Logic**: Automatic retries with exponential backoff

## Architecture

This tool uses a parallel processing architecture:

- **TranslationWorker**: Handles AI API calls with retry logic
- **QtTranslationAssistant**: Main orchestration with parallel batch processing
- **ThreadPoolExecutor**: Manages concurrent translation workers

Performance improvements over subagent architecture:
- Direct API calls (no subprocess overhead)
- Batch processing (default 30 strings per batch, vs 10)
- Parallel workers (default 3 concurrent workers)
- ~5-10x faster overall

## Installation

1. Ensure Python 3.7+ is installed
2. Install dependencies:
   ```bash
   pip install requests
   ```

## Configuration

Create `qt_translation_config.json`:

```json
{
  "api_url": "http://localhost:8080/v1/chat/completions",
  "api_key": "your-api-key-here",
  "model": "qwen3-coder-flash",
  "temperature": 0.3
}
```

## Usage

Create config file:
```bash
python translate.py --create-config
```

Translate single file:
```bash
python translate.py /path/to/file.ts --batch-size 30 --max-workers 3
```

Translate directory:
```bash
python translate.py /path/to/translations/ --batch-size 30 --max-workers 3
```

## Parameters

- `--batch-size`: Number of strings per batch (default 30)
- `--max-workers`: Number of parallel workers (default 3)
- `--config`: Path to config file (default qt_translation_config.json)

## Performance

Typical performance:
- 3 workers, batch_size 30: 50-100 strings/second
- 141 strings in ~2.24 seconds
- 80 files in ~2-5 seconds (depends on content)

## Git Diff Friendly

Only translation content is modified (100% format preservation):
- `type="unfinished"` removed from `<translation>` tags
- Translation text updated
- Original XML structure and formatting preserved
- Quote style (single/double) unchanged
- Whitespace and indentation unchanged
- Line endings and encoding unchanged

Supported unfinished formats:
- `<translation type="unfinished"></translation>`
- `<translation type="unfinished" />`
- `<translation type='unfinished'></translation>`
- `<translation type='unfinished' />`
- Multi-line translations with preserved formatting

## Troubleshooting

- API connection issues: Check api_url and api_key in config
- Large files: Increase batch_size to reduce API calls
- Rate limiting: Reduce max_workers or batch_size
- Translation quality: Adjust model or temperature in config
