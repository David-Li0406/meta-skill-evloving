"""BFCL ticket_api tool schemas.

Auto-generated from /ossfs/workspace/bfcl_xiexin/bfcl_eval/data/multi_turn_func_doc/ticket_api.json
"""

from typing import List, Dict, Any

TICKET_API_TOOL_SCHEMAS: List[Dict[str, Any]] = [
    {
        'type': 'function',
        'function': {
            'name': 'close_ticket',
            'description': 'This tool belongs to the ticketing system that is part of a company, which allows users to create, view, and manage support business tickets. Tool description: Close a ticket.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'ticket_id': {
                        'type': 'integer',
                        'description': 'ID of the ticket to be closed. '
                    }
                },
                'required': [
                    'ticket_id'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'create_ticket',
            'description': 'This tool belongs to the ticketing system that is part of a company, which allows users to create, view, and manage support business tickets. Tool description: Create a ticket in the system and queue it.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'title': {
                        'type': 'string',
                        'description': 'Title of the ticket.'
                    },
                    'description': {
                        'type': 'string',
                        'description': 'Description of the ticket. Defaults to an empty string.',
                        'default': ''
                    },
                    'priority': {
                        'type': 'integer',
                        'description': 'Priority of the ticket, from 1 to 5. Defaults to 1. 5 is the highest priority. ',
                        'default': 1
                    }
                },
                'required': [
                    'title'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'edit_ticket',
            'description': 'This tool belongs to the ticketing system that is part of a company, which allows users to create, view, and manage support business tickets. Tool description: Modify the details of an existing ticket.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'ticket_id': {
                        'type': 'integer',
                        'description': 'ID of the ticket to be changed.'
                    },
                    'updates': {
                        'type': 'object',
                        'description': 'Dictionary containing the fields to be updated.',
                        'properties': {
                            'title': {
                                'type': 'string',
                                'description': '[Optional] New title for the ticket.'
                            },
                            'description': {
                                'type': 'string',
                                'description': '[Optional] New description for the ticket.'
                            },
                            'status': {
                                'type': 'string',
                                'description': '[Optional] New status for the ticket.'
                            },
                            'priority': {
                                'type': 'integer',
                                'description': '[Optional] New priority for the ticket.'
                            }
                        }
                    }
                },
                'required': [
                    'ticket_id',
                    'updates'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_ticket',
            'description': 'This tool belongs to the ticketing system that is part of a company, which allows users to create, view, and manage support business tickets. Tool description: Get a specific ticket by its ID.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'ticket_id': {
                        'type': 'integer',
                        'description': 'ID of the ticket to retrieve. '
                    }
                },
                'required': [
                    'ticket_id'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_user_tickets',
            'description': 'This tool belongs to the ticketing system that is part of a company, which allows users to create, view, and manage support business tickets. Tool description: Get all tickets created by the current user, optionally filtered by status.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'status': {
                        'type': 'string',
                        'description': 'Status to filter tickets by. If None, return all tickets. ',
                        'default': 'None'
                    }
                },
                'required': []
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'logout',
            'description': 'This tool belongs to the ticketing system that is part of a company, which allows users to create, view, and manage support business tickets. Tool description: Log out the current user.',
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
            'name': 'resolve_ticket',
            'description': 'This tool belongs to the ticketing system that is part of a company, which allows users to create, view, and manage support business tickets. Tool description: Resolve a ticket with a resolution.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'ticket_id': {
                        'type': 'integer',
                        'description': 'ID of the ticket to be resolved.'
                    },
                    'resolution': {
                        'type': 'string',
                        'description': 'Resolution details for the ticket. '
                    }
                },
                'required': [
                    'ticket_id',
                    'resolution'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'ticket_get_login_status',
            'description': 'This tool belongs to the ticketing system that is part of a company, which allows users to create, view, and manage support business tickets. Tool description: Get the login status of the currently authenticated user.',
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
            'name': 'ticket_login',
            'description': 'This tool belongs to the ticketing system that is part of a company, which allows users to create, view, and manage support business tickets. Tool description: Authenticate a user for ticket system.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'username': {
                        'type': 'string',
                        'description': 'Username of the user.'
                    },
                    'password': {
                        'type': 'string',
                        'description': 'Password of the user. '
                    }
                },
                'required': [
                    'username',
                    'password'
                ]
            }
        }
    }
]
