"""BFCL message_api tool schemas.

Auto-generated from /ossfs/workspace/bfcl_xiexin/bfcl_eval/data/multi_turn_func_doc/message_api.json
"""

from typing import List, Dict, Any

MESSAGE_API_TOOL_SCHEMAS: List[Dict[str, Any]] = [
    {
        'type': 'function',
        'function': {
            'name': 'add_contact',
            'description': 'This tool belongs to the Message API, which is used to manage user interactions in a workspace. Tool description: Add a contact to the workspace.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'user_name': {
                        'type': 'string',
                        'description': 'User name of contact to be added.'
                    }
                },
                'required': [
                    'user_name'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'delete_message',
            'description': 'This tool belongs to the Message API, which is used to manage user interactions in a workspace. Tool description: Delete the latest message sent to a receiver.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'receiver_id': {
                        'type': 'string',
                        'description': 'User ID of the user to send the message to.'
                    }
                },
                'required': [
                    'receiver_id'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_message_stats',
            'description': 'This tool belongs to the Message API, which is used to manage user interactions in a workspace. Tool description: Get statistics about messages for the current user.',
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
            'name': 'get_user_id',
            'description': 'This tool belongs to the Message API, which is used to manage user interactions in a workspace. Tool description: Get user ID from user name.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'user': {
                        'type': 'string',
                        'description': 'User name of the user. '
                    }
                },
                'required': [
                    'user'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'list_users',
            'description': 'This tool belongs to the Message API, which is used to manage user interactions in a workspace. Tool description: List all users in the workspace.',
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
            'name': 'message_get_login_status',
            'description': 'This tool belongs to the Message API, which is used to manage user interactions in a workspace. Tool description: Get the login status of the current user.',
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
            'name': 'message_login',
            'description': 'This tool belongs to the Message API, which is used to manage user interactions in a workspace. Tool description: Log in a user with the given user ID to messeage application.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'user_id': {
                        'type': 'string',
                        'description': 'User ID of the user to log in. '
                    }
                },
                'required': [
                    'user_id'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'search_messages',
            'description': 'This tool belongs to the Message API, which is used to manage user interactions in a workspace. Tool description: Search for messages containing a specific keyword.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'keyword': {
                        'type': 'string',
                        'description': 'The keyword to search for in messages.'
                    }
                },
                'required': [
                    'keyword'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'send_message',
            'description': 'This tool belongs to the Message API, which is used to manage user interactions in a workspace. Tool description: Send a message to a user.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'receiver_id': {
                        'type': 'string',
                        'description': 'User ID of the user to send the message to.'
                    },
                    'message': {
                        'type': 'string',
                        'description': 'Message to be sent.'
                    }
                },
                'required': [
                    'receiver_id',
                    'message'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'view_messages_sent',
            'description': 'This tool belongs to the Message API, which is used to manage user interactions in a workspace. Tool description: View all historical messages sent by the current user.',
            'parameters': {
                'type': 'object',
                'properties': {},
                'required': []
            }
        }
    }
]
