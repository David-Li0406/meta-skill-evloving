"""BFCL memory_vector tool schemas.

Auto-generated from /ossfs/workspace/bfcl_xiexin/bfcl_eval/data/multi_turn_func_doc/memory_vector.json
"""

from typing import List, Dict, Any

MEMORY_VECTOR_TOOL_SCHEMAS: List[Dict[str, Any]] = [
    {
        'type': 'function',
        'function': {
            'name': 'archival_memory_add',
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: Add a new entry to the archival memory.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'text': {
                        'type': 'string',
                        'description': 'The text to be added to the archival memory. '
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
            'name': 'archival_memory_clear',
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: Clear all entries in the archival memory.',
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
            'name': 'archival_memory_remove',
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: Remove an entry from the archival memory.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'vec_id': {
                        'type': 'integer',
                        'description': 'The ID of the entry to be removed. '
                    }
                },
                'required': [
                    'vec_id'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'archival_memory_retrieve',
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: Retrieve the most similar entries from the archival memory.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'query': {
                        'type': 'string',
                        'description': 'The query text to search for.'
                    },
                    'top_k': {
                        'type': 'integer',
                        'description': 'The number of top similar entries to retrieve.',
                        'default': 5
                    }
                },
                'required': [
                    'query'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'archival_memory_retrieve_all',
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: Retrieve all entries from the archival memory.',
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
            'name': 'archival_memory_update',
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: Update an entry in the archival memory.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'vec_id': {
                        'type': 'integer',
                        'description': 'The ID of the entry to be updated.'
                    },
                    'new_text': {
                        'type': 'string',
                        'description': 'The new text to replace the old text. '
                    }
                },
                'required': [
                    'vec_id',
                    'new_text'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'core_memory_add',
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: Add a new entry to the core memory.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'text': {
                        'type': 'string',
                        'description': 'The text to be added to the core memory. '
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
            'name': 'core_memory_clear',
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: Clear all entries in the core memory.',
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
            'name': 'core_memory_remove',
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: Remove an entry from the core memory.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'vec_id': {
                        'type': 'integer',
                        'description': 'The ID of the entry to be removed. '
                    }
                },
                'required': [
                    'vec_id'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'core_memory_retrieve',
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: Retrieve the most similar entries from the core memory.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'query': {
                        'type': 'string',
                        'description': 'The query text to search for.'
                    },
                    'top_k': {
                        'type': 'integer',
                        'description': 'The number of top similar entries to retrieve. ',
                        'default': 5
                    }
                },
                'required': [
                    'query'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'core_memory_retrieve_all',
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: Retrieve all entries from the core memory.',
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
            'name': 'core_memory_update',
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: Update an entry in the core memory.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'vec_id': {
                        'type': 'integer',
                        'description': 'The ID of the entry to be updated.'
                    },
                    'new_text': {
                        'type': 'string',
                        'description': 'The new text to replace the old text. '
                    }
                },
                'required': [
                    'vec_id',
                    'new_text'
                ]
            }
        }
    }
]
