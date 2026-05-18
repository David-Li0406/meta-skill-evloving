"""BFCL memory_kv tool schemas.

Auto-generated from /ossfs/workspace/bfcl_xiexin/bfcl_eval/data/multi_turn_func_doc/memory_kv.json
"""

from typing import List, Dict, Any

MEMORY_KV_TOOL_SCHEMAS: List[Dict[str, Any]] = [
    {
        'type': 'function',
        'function': {
            'name': 'archival_memory_add',
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: Add a key-value pair to the long-term memory. Make sure to use meaningful keys for easy retrieval later.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'key': {
                        'type': 'string',
                        'description': 'The key under which the value is stored. The key should be unique and case-sensitive. Keys must be snake_case and cannot contain spaces.'
                    },
                    'value': {
                        'type': 'string',
                        'description': 'The value to store in the long-term memory. '
                    }
                },
                'required': [
                    'key',
                    'value'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'archival_memory_clear',
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: Clear all key-value pairs from the long-term memory, including those from previous interactions. This operation is irreversible.',
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
            'name': 'archival_memory_key_search',
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: Search for key names in the long-term memory that are similar to the query using BM25+ algorithm.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'query': {
                        'type': 'string',
                        'description': 'The query text to search for.'
                    },
                    'k': {
                        'type': 'integer',
                        'description': 'The number of results to return. ',
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
            'name': 'archival_memory_list_keys',
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: List all keys currently in the long-term memory.',
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
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: Remove a key-value pair from the long-term memory.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'key': {
                        'type': 'string',
                        'description': 'The key to remove from the long-term memory. Case-sensitive. '
                    }
                },
                'required': [
                    'key'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'archival_memory_replace',
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: Replace a key-value pair in the long-term memory with a new value.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'key': {
                        'type': 'string',
                        'description': 'The key to replace in the long-term memory. Case-sensitive.'
                    },
                    'value': {
                        'type': 'string',
                        'description': 'The new value associated with the key. '
                    }
                },
                'required': [
                    'key',
                    'value'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'archival_memory_retrieve',
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: Retrieve the value associated with a key from the long-term memory. This function does not support partial key matching or similarity search.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'key': {
                        'type': 'string',
                        'description': 'The key to retrieve. Case-sensitive. The key must match exactly with the key stored in the memory. '
                    }
                },
                'required': [
                    'key'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'core_memory_add',
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: Add a key-value pair to the short-term memory. Make sure to use meaningful keys for easy retrieval later.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'key': {
                        'type': 'string',
                        'description': 'The key under which the value is stored. The key should be unique and case-sensitive. Keys must be snake_case and cannot contain spaces.'
                    },
                    'value': {
                        'type': 'string',
                        'description': 'The value to store in the short-term memory. '
                    }
                },
                'required': [
                    'key',
                    'value'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'core_memory_clear',
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: Clear all key-value pairs from the short-term memory, including those from previous interactions. This operation is irreversible.',
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
            'name': 'core_memory_key_search',
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: Search for key names in the short-term memory that are similar to the query using BM25+ algorithm.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'query': {
                        'type': 'string',
                        'description': 'The query text to search for.'
                    },
                    'k': {
                        'type': 'integer',
                        'description': 'The number of results to return. ',
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
            'name': 'core_memory_list_keys',
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: List all keys currently in the short-term memory.',
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
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: Remove a key-value pair from the short-term memory.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'key': {
                        'type': 'string',
                        'description': 'The key to remove from the short-term memory. Case-sensitive. '
                    }
                },
                'required': [
                    'key'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'core_memory_replace',
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: Replace a key-value pair in the short-term memory with a new value.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'key': {
                        'type': 'string',
                        'description': 'The key to replace in the short-term memory. Case-sensitive.'
                    },
                    'value': {
                        'type': 'string',
                        'description': 'The new value associated with the key. '
                    }
                },
                'required': [
                    'key',
                    'value'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'core_memory_retrieve',
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: Retrieve the value associated with a key from the short-term memory. This function does not support partial key matching or similarity search.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'key': {
                        'type': 'string',
                        'description': 'The key to retrieve. Case-sensitive. The key must match exactly with the key stored in the memory. '
                    }
                },
                'required': [
                    'key'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'core_memory_retrieve_all',
            'description': 'This tool belongs to the memory suite, which provides APIs to interact with a key-value based memory system. Tool description: Retrieve all key-value pairs from the short-term memory.',
            'parameters': {
                'type': 'object',
                'properties': {},
                'required': []
            }
        }
    }
]
