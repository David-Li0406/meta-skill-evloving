"""BFCL gorilla_file_system tool schemas.

Auto-generated from /ossfs/workspace/bfcl_xiexin/bfcl_eval/data/multi_turn_func_doc/gorilla_file_system.json
"""

from typing import List, Dict, Any

GORILLA_FILE_SYSTEM_TOOL_SCHEMAS: List[Dict[str, Any]] = [
    {
        'type': 'function',
        'function': {
            'name': 'cat',
            'description': 'This tool belongs to the Gorilla file system. It is a simple file system that allows users to perform basic file operations such as navigating directories, creating files and directories, reading and writing to files, etc. Tool description: Display the contents of a file of any extension from currrent directory.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'file_name': {
                        'type': 'string',
                        'description': 'The name of the file from current directory to display. No path is allowed. '
                    }
                },
                'required': [
                    'file_name'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'cd',
            'description': 'This tool belongs to the Gorilla file system. It is a simple file system that allows users to perform basic file operations such as navigating directories, creating files and directories, reading and writing to files, etc. Tool description: Change the current working directory to the specified folder.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'folder': {
                        'type': 'string',
                        'description': 'The folder of the directory to change to. You can only change one folder level at a time. '
                    }
                },
                'required': [
                    'folder'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'cp',
            'description': 'This tool belongs to the Gorilla file system. It is a simple file system that allows users to perform basic file operations such as navigating directories, creating files and directories, reading and writing to files, etc. Tool description: Copy a file or directory from one location to another.  If the destination is a directory, the source file or directory will be copied into the destination directory.  Both source and destination must be local to the current directory.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'source': {
                        'type': 'string',
                        'description': 'The name of the file or directory to copy.'
                    },
                    'destination': {
                        'type': 'string',
                        'description': 'The destination name to copy the file or directory to. If the destination is a directory, the source will be copied into this directory. No file paths allowed. '
                    }
                },
                'required': [
                    'source',
                    'destination'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'diff',
            'description': 'This tool belongs to the Gorilla file system. It is a simple file system that allows users to perform basic file operations such as navigating directories, creating files and directories, reading and writing to files, etc. Tool description: Compare two files of any extension line by line at the current directory.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'file_name1': {
                        'type': 'string',
                        'description': 'The name of the first file in current directory.'
                    },
                    'file_name2': {
                        'type': 'string',
                        'description': 'The name of the second file in current directory. '
                    }
                },
                'required': [
                    'file_name1',
                    'file_name2'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'du',
            'description': 'This tool belongs to the Gorilla file system. It is a simple file system that allows users to perform basic file operations such as navigating directories, creating files and directories, reading and writing to files, etc. Tool description: Estimate the disk usage of a directory and its contents.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'human_readable': {
                        'type': 'boolean',
                        'description': 'If True, returns the size in human-readable format (e.g., KB, MB). ',
                        'default': False
                    }
                },
                'required': []
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'echo',
            'description': 'This tool belongs to the Gorilla file system. It is a simple file system that allows users to perform basic file operations such as navigating directories, creating files and directories, reading and writing to files, etc. Tool description: Write content to a file at current directory or display it in the terminal.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'content': {
                        'type': 'string',
                        'description': 'The content to write or display.'
                    },
                    'file_name': {
                        'type': 'string',
                        'description': 'The name of the file at current directory to write the content to. Defaults to None. ',
                        'default': 'None'
                    }
                },
                'required': [
                    'content'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'find',
            'description': 'This tool belongs to the Gorilla file system. It is a simple file system that allows users to perform basic file operations such as navigating directories, creating files and directories, reading and writing to files, etc. Tool description: Find any file or directories under specific path that contain name in its file name.  This method searches for files of any extension and directories within a specified path that match the given name. If no name is provided, it returns all files and directories in the specified path and its subdirectories. Note: This method performs a recursive search through all subdirectories of the given path.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'path': {
                        'type': 'string',
                        'description': 'The directory path to start the search. Defaults to the current directory (".").',
                        'default': '.'
                    },
                    'name': {
                        'type': 'string',
                        'description': 'The name of the file or directory to search for. If None, all items are returned. ',
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
            'name': 'grep',
            'description': 'This tool belongs to the Gorilla file system. It is a simple file system that allows users to perform basic file operations such as navigating directories, creating files and directories, reading and writing to files, etc. Tool description: Search for lines in a file of any extension at current directory that contain the specified pattern.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'file_name': {
                        'type': 'string',
                        'description': 'The name of the file to search. No path is allowed and you can only perform on file at local directory.'
                    },
                    'pattern': {
                        'type': 'string',
                        'description': 'The pattern to search for. '
                    }
                },
                'required': [
                    'file_name',
                    'pattern'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'ls',
            'description': 'This tool belongs to the Gorilla file system. It is a simple file system that allows users to perform basic file operations such as navigating directories, creating files and directories, reading and writing to files, etc. Tool description: List the contents of the current directory.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'a': {
                        'type': 'boolean',
                        'description': 'Show hidden files and directories. Defaults to False. ',
                        'default': False
                    }
                },
                'required': []
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'mkdir',
            'description': 'This tool belongs to the Gorilla file system. It is a simple file system that allows users to perform basic file operations such as navigating directories, creating files and directories, reading and writing to files, etc. Tool description: Create a new directory in the current directory.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'dir_name': {
                        'type': 'string',
                        'description': 'The name of the new directory at current directory. You can only create directory at current directory.'
                    }
                },
                'required': [
                    'dir_name'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'mv',
            'description': 'This tool belongs to the Gorilla file system. It is a simple file system that allows users to perform basic file operations such as navigating directories, creating files and directories, reading and writing to files, etc. Tool description: Move a file or directory from one location to another.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'source': {
                        'type': 'string',
                        'description': 'Source name of the file or directory to move. Source must be local to the current directory.'
                    },
                    'destination': {
                        'type': 'string',
                        'description': 'The destination name to move the file or directory to. Destination must be local to the current directory and cannot be a path. If destination is not an existing directory like when renaming something, destination is the new file name. '
                    }
                },
                'required': [
                    'source',
                    'destination'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'pwd',
            'description': 'This tool belongs to the Gorilla file system. It is a simple file system that allows users to perform basic file operations such as navigating directories, creating files and directories, reading and writing to files, etc. Tool description: Return the current working directory path.',
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
            'name': 'rm',
            'description': 'This tool belongs to the Gorilla file system. It is a simple file system that allows users to perform basic file operations such as navigating directories, creating files and directories, reading and writing to files, etc. Tool description: Remove a file or directory.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'file_name': {
                        'type': 'string',
                        'description': 'The name of the file or directory to remove. '
                    }
                },
                'required': [
                    'file_name'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'rmdir',
            'description': 'This tool belongs to the Gorilla file system. It is a simple file system that allows users to perform basic file operations such as navigating directories, creating files and directories, reading and writing to files, etc. Tool description: Remove a directory at current directory.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'dir_name': {
                        'type': 'string',
                        'description': 'The name of the directory to remove. Directory must be local to the current directory. '
                    }
                },
                'required': [
                    'dir_name'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'sort',
            'description': 'This tool belongs to the Gorilla file system. It is a simple file system that allows users to perform basic file operations such as navigating directories, creating files and directories, reading and writing to files, etc. Tool description: Sort the contents of a file line by line.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'file_name': {
                        'type': 'string',
                        'description': 'The name of the file appeared at current directory to sort. '
                    }
                },
                'required': [
                    'file_name'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'tail',
            'description': 'This tool belongs to the Gorilla file system. It is a simple file system that allows users to perform basic file operations such as navigating directories, creating files and directories, reading and writing to files, etc. Tool description: Display the last part of a file of any extension.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'file_name': {
                        'type': 'string',
                        'description': 'The name of the file to display. No path is allowed and you can only perform on file at local directory.'
                    },
                    'lines': {
                        'type': 'integer',
                        'description': 'The number of lines to display from the end of the file. Defaults to 10. ',
                        'default': 10
                    }
                },
                'required': [
                    'file_name'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'touch',
            'description': 'This tool belongs to the Gorilla file system. It is a simple file system that allows users to perform basic file operations such as navigating directories, creating files and directories, reading and writing to files, etc. Tool description: Create a new file of any extension in the current directory.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'file_name': {
                        'type': 'string',
                        'description': 'The name of the new file in the current directory. file_name is local to the current directory and does not allow path.'
                    }
                },
                'required': [
                    'file_name'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'wc',
            'description': 'This tool belongs to the Gorilla file system. It is a simple file system that allows users to perform basic file operations such as navigating directories, creating files and directories, reading and writing to files, etc. Tool description: Count the number of lines, words, and characters in a file of any extension from current directory.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'file_name': {
                        'type': 'string',
                        'description': 'Name of the file of current directory to perform wc operation on.'
                    },
                    'mode': {
                        'type': 'string',
                        'description': "Mode of operation ('l' for lines, 'w' for words, 'c' for characters). ",
                        'default': 'l'
                    }
                },
                'required': [
                    'file_name'
                ]
            }
        }
    }
]
