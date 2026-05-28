#!/usr/bin/env python3
import os
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List
import time
import threading


class TranslationWorker:
    def __init__(self, config: dict, max_retries: int = 2):
        self.config = config
        self.max_retries = max_retries

    def translate_batch(self, strings_list: List[str], target_language: str,
                        source_file: str = "") -> List[Dict[str, str]]:
        if not strings_list:
            return []

        prompt = self._build_translation_prompt(strings_list, target_language, source_file)

        for attempt in range(self.max_retries):
            try:
                response_text = self._call_llm_api(prompt)
                results = self._parse_translation_response(response_text, strings_list)

                if len(results) == len(strings_list):
                    return results
                else:
                    print(f"  Warning: Result count mismatch (expected {len(strings_list)}, got {len(results)})")

            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries - 1:
                    print(f"  Network error, retrying {attempt + 1}/{self.max_retries}: {str(e)}")
                    time.sleep(2 ** attempt)
                else:
                    print(f"  Translation failed, using original: {str(e)}")
            except Exception as e:
                print(f"  Translation error: {str(e)}")

        return [{'source': s, 'translation': s} for s in strings_list]

    def _build_translation_prompt(self, strings_list: List[str], target_language: str,
                                   source_file: str) -> str:
        prompt = f"""Translate the following strings to {target_language} language.
Source file: {source_file if source_file else 'Unknown'}

String list:
"""

        for i, string in enumerate(strings_list, 1):
            prompt += f"\n{i}. {string}\n"

        example = [{"source": strings_list[0], "translation": "..."}] if strings_list else []
        prompt += f"""

Return the results strictly in the following JSON format, do not add any other text:
{json.dumps(example, ensure_ascii=False, indent=2)}

Important notes:
- Maintain accuracy and terminology consistency
- Ensure correct JSON format
- Do not add explanations or other content outside JSON
"""
        return prompt

    def _call_llm_api(self, prompt: str) -> str:
        import requests
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.config['api_key']}"
        }

        data = {
            'model': self.config.get('model', 'qwen3-coder-flash'),
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
            'temperature': self.config.get('temperature', 0.3),
            'max_tokens': 4000
        }

        response = requests.post(
            self.config['api_url'],
            headers=headers,
            json=data,
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            print(f"  API Response: {response.text}")
            raise Exception(f"API call failed: {response.status_code} - {response.text}")

    def _parse_translation_response(self, response_text: str,
                                     original_strings: List[str]) -> List[Dict[str, str]]:
        try:
            results = json.loads(response_text)
            if isinstance(results, list) and all('source' in r and 'translation' in r for r in results):
                return results
        except json.JSONDecodeError:
            pass

        json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if json_match:
            try:
                results = json.loads(json_match.group(0))
                if isinstance(results, list) and all('source' in r and 'translation' in r for r in results):
                    return results
            except json.JSONDecodeError:
                pass

        print("  Warning: Unable to parse translation response")
        return [{'source': s, 'translation': s} for s in original_strings]


class TranslationBatch:
    def __init__(self, items: List[Dict], target_language: str, source_file: str):
        self.items = items
        self.target_language = target_language
        self.source_file = source_file


class QtTranslationAssistant:
    def __init__(self, config_path: str = "qt_translation_config.json",
                 batch_size: int = 20, max_workers: int = 3):
        self.config = self.load_config(config_path)
        self.batch_size = batch_size
        self.max_workers = max_workers
        self.translator = TranslationWorker(self.config)
        self.lock = threading.Lock()

    def load_config(self, config_path: str) -> dict:
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def find_unfinished_translations(self, ts_file_path: str) -> List[Dict]:
        results = []
        
        with open(ts_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        current_source = None
        
        for line_num, line in enumerate(lines, 1):
            source_match = re.search(r'<source>([^<]+)</source>', line)
            if source_match:
                current_source = source_match.group(1)
                continue
            
            if current_source and '<translation' in line:
                has_unfinished_marker = False
                if 'type="unfinished"' in line or "type='unfinished'" in line:
                    has_unfinished_marker = True
                
                if has_unfinished_marker:
                    if '</translation>' in line or '/>' in line:
                        results.append({
                            'source': current_source,
                            'translation': '',
                            'line_number': line_num,
                            'end_line_number': line_num,
                            'file_path': ts_file_path
                        })
                    else:
                        end_line_num = line_num
                        while end_line_num < len(lines) and '</translation>' not in lines[end_line_num]:
                            end_line_num += 1
                            if end_line_num > line_num + 20:
                                break
                        if end_line_num < len(lines):
                            results.append({
                                'source': current_source,
                                'translation': '',
                                'line_number': line_num,
                                'end_line_number': end_line_num,
                                'file_path': ts_file_path
                            })
                    current_source = None

        return results

    def get_language_from_filename(self, filename: str) -> str:
        name = Path(filename).stem
        if '_' in name:
            parts = name.split('_')
            if len(parts) >= 2:
                return '_'.join(parts[1:])
        return 'unknown'

    def translate_single_file(self, ts_file_path: str) -> dict:
        print(f"\nProcessing: {ts_file_path}")

        unfinished_items = self.find_unfinished_translations(ts_file_path)

        if not unfinished_items:
            return {
                'file': ts_file_path,
                'status': 'skipped',
                'count': 0
            }

        print(f"  Found {len(unfinished_items)} unfinished translations")

        language_code = self.get_language_from_filename(os.path.basename(ts_file_path))
        print(f"  Target language: {language_code}")

        if language_code == 'unknown':
            print("  English source file, using original text...")
            translation_results = []
            for item in unfinished_items:
                translation_results.append({'source': item['source'], 'translation': item['source']})
            self.write_translations_back(ts_file_path, unfinished_items, translation_results)
            return {
                'file': ts_file_path,
                'status': 'completed',
                'count': len(translation_results)
            }

        batches = self._create_batches(unfinished_items, ts_file_path, language_code)
        translation_results = self._translate_batches_parallel(batches)
        self.write_translations_back(ts_file_path, unfinished_items, translation_results)
        print(f"  Translation complete: {len(translation_results)} strings")
        
        return {
            'file': ts_file_path,
            'status': 'completed',
            'count': len(translation_results),
            'language': language_code
        }

    def _create_batches(self, items: List[Dict], source_file: str,
                        target_language: str) -> List[TranslationBatch]:
        batches = []
        for i in range(0, len(items), self.batch_size):
            batch_items = items[i:i + self.batch_size]
            batch = TranslationBatch(batch_items, target_language, source_file)
            batches.append(batch)
        return batches

    def _translate_batches_parallel(self, batches: List[TranslationBatch]) -> List[Dict]:
        all_results = []
        total_batches = len(batches)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_batch = {
                executor.submit(self._translate_single_batch, batch): batch
                for batch in batches
            }

            for i, future in enumerate(as_completed(future_to_batch), 1):
                batch = future_to_batch[future]
                try:
                    results = future.result()
                    all_results.extend(results)
                    print(f"  Batch progress: {i}/{total_batches} complete")
                except Exception as e:
                    print(f"  Batch translation failed: {str(e)}")
                    fallback_results = [
                        {'source': item['source'], 'translation': item['source']}
                        for item in batch.items
                    ]
                    all_results.extend(fallback_results)

        return all_results

    def _translate_single_batch(self, batch: TranslationBatch) -> List[Dict]:
        strings_list = [item['source'] for item in batch.items]
        results = self.translator.translate_batch(strings_list, batch.target_language, batch.source_file)

        if len(results) != len(strings_list):
            print(f"  Warning: Batch result count mismatch")
            results = [{'source': s, 'translation': s} for s in strings_list]

        return results

    def write_translations_back(self, ts_file_path: str, unfinished_items: List[Dict], translation_results: List[Dict]):
        with open(ts_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        translation_map = {item['source']: item['translation'] for item in translation_results}

        modified_count = 0
        for item in unfinished_items:
            source_text = item['source']
            if source_text not in translation_map:
                print(f"  Warning: No translation found for: {source_text}")
                continue
            
            new_translation = translation_map[source_text]
            line_num = item['line_number'] - 1
            end_line_num = item['end_line_number'] - 1
            
            if line_num >= len(lines) or end_line_num >= len(lines):
                print(f"  Warning: Invalid line numbers: {line_num+1} to {end_line_num+1}")
                continue
            
            original_line = lines[line_num]
            
            unfinished_patterns = [
                r'<translation type="unfinished">\s*</translation>',
                r'<translation type="unfinished"\s*</translation>',
                r"<translation type='unfinished'>\s*</translation>",
                r'<translation type="unfinished"\s*/>',
                r"<translation type='unfinished'\s*/>",
            ]
            
            is_unfinished = any(re.search(pattern, original_line) for pattern in unfinished_patterns)
            
            if not is_unfinished:
                print(f"  Warning: Line {line_num+1} doesn't contain unfinished marker")
                continue
            
            if end_line_num == line_num:
                new_line = re.sub(
                    r'<translation[^>]*type=["\']unfinished["\'][^>]*>\s*</translation>',
                    f'<translation>{new_translation}</translation>',
                    original_line
                )
                if new_line == original_line:
                    new_line = re.sub(
                        r'<translation[^>]*type=["\']unfinished["\'][^>]*\s*/>',
                        f'<translation>{new_translation}</translation>',
                        original_line
                    )
                lines[line_num] = new_line
            else:
                new_line = re.sub(
                    r'<translation[^>]*type=["\']unfinished["\'][^>]*>',
                    f'<translation>{new_translation}',
                    original_line
                )
                lines[line_num] = new_line
                
                for i in range(line_num + 1, end_line_num):
                    lines[i] = ''
            
            modified_count += 1

        with open(ts_file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print(f"  Wrote {modified_count} translations back to file")

    def process_directory(self, directory_path: str) -> dict:
        ts_files = list(Path(directory_path).glob('*.ts'))
        print(f"\nFound {len(ts_files)} TS files")

        filtered_files = [
            f for f in ts_files
            if not ('_en.ts' in str(f) or '_en_' in str(f).lower()) or 'zh_CN' in str(f)
        ]
        print(f"Filtered {len(filtered_files)} files to translate\n")

        report = {
            'total_files': len(filtered_files),
            'translated_files': [],
            'skipped_files': [],
            'failed_files': [],
            'total_strings': 0,
            'files_detail': []
        }

        start_time = time.time()

        for ts_file in filtered_files:
            result = self.translate_single_file(str(ts_file))
            report['total_strings'] += result['count']
            
            if result['status'] == 'completed':
                report['translated_files'].append(ts_file.name)
                report['files_detail'].append({
                    'file': ts_file.name,
                    'count': result['count'],
                    'language': result['language']
                })
            elif result['status'] == 'skipped':
                report['skipped_files'].append(ts_file.name)
            else:
                report['failed_files'].append(ts_file.name)

        elapsed = time.time() - start_time

        print("\n" + "=" * 50)
        print("Translation Summary Report")
        print("=" * 50)
        print(f"  Total files processed: {report['total_files']}")
        print(f"  Successfully translated: {len(report['translated_files'])}")
        print(f"  Skipped (no translation needed): {len(report['skipped_files'])}")
        print(f"  Failed: {len(report['failed_files'])}")
        print(f"  Total strings translated: {report['total_strings']}")
        print(f"  Time elapsed: {elapsed:.2f} seconds")
        if report['total_strings'] > 0:
            print(f"  Average speed: {report['total_strings']/elapsed:.1f} strings/sec")
        
        print("\nTranslated files:")
        for detail in report['files_detail']:
            print(f"  - {detail['file']}: {detail['count']} strings ({detail['language']})")
        
        if report['failed_files']:
            print("\nFailed files:")
            for f in report['failed_files']:
                print(f"  - {f}")
        
        print("=" * 50)
        
        return report


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Qt Translation Assistant (Parallel)')
    parser.add_argument('path', help='TS file or directory path')
    parser.add_argument('--config', default='qt_translation_config.json',
                        help='Config file path')
    parser.add_argument('--batch-size', type=int, default=20,
                        help='Number of strings per batch (default 20)')
    parser.add_argument('--max-workers', type=int, default=3,
                        help='Number of parallel workers (default 3)')

    args = parser.parse_args()

    try:
        assistant = QtTranslationAssistant(
            config_path=args.config,
            batch_size=args.batch_size,
            max_workers=args.max_workers
        )

        if os.path.isfile(args.path):
            result = assistant.translate_single_file(args.path)
            print(f"\nResult: {result['status']} - {result['count']} strings")
        elif os.path.isdir(args.path):
            assistant.process_directory(args.path)
        else:
            print(f"Error: Path not found: {args.path}")

    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        print("Hint: Use --create-config to create config file")
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
