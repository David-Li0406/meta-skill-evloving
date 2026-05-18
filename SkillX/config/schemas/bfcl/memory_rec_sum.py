"""BFCL memory_rec_sum tool schemas.

Auto-generated from /ossfs/workspace/bfcl_xiexin/bfcl_eval/data/multi_turn_func_doc/memory_rec_sum.json
"""

from typing import List, Dict, Any

MEMORY_REC_SUM_TOOL_SCHEMAS: List[Dict[str, Any]] = [
    {
        'type': 'function',
        'function': {
            'name': 'memory_append',
            'description': 'This tool belongs to the memory suite, which provides APIs to manage memory data via recursive summarization. Tool description: Append a new text to the end of the memory.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'text': {
                        'type': 'string',
                        'description': 'The text to append to the memory. '
                    }
                },
                'required': [
                    'text'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'memory_clear',
            'description': 'This tool belongs to the memory suite, which provides APIs to manage memory data via recursive summarization. Tool description: Clear all content in the memory, including any from previous interactions. This operation is irreversible.',
            'parameters': {
                'type': 'object',
                'properties': {},
                'required': []
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'memory_replace',
            'description': 'This tool belongs to the memory suite, which provides APIs to manage memory data via recursive summarization. Tool description: Replace a specific text in the memory with new text.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'old_text': {
                        'type': 'string',
                        'description': 'The text to be replaced in the memory.'
                    },
                    'new_text': {
                        'type': 'string',
                        'description': 'The new text to replace the old text.'
                    }
                },
                'required': [
                    'old_text',
                    'new_text'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'memory_retrieve',
            'description': 'This tool belongs to the memory suite, which provides APIs to manage memory data via recursive summarization. Tool description: Retrieve the current content of the memory.',
            'parameters': {
                'type': 'object',
                'properties': {},
                'required': []
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'memory_update',
            'description': 'This tool belongs to the memory suite, which provides APIs to manage memory data via recursive summarization. Tool description: Update the memory with new text. This will replace the existing memory content.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'text': {
                        'type': 'string',
                        'description': 'The new text to set as the memory. '
                    }
                },
                'required': [
                    'text'
                ]
            }
        }
    }
]
