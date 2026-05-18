"""BFCL math_api tool schemas.

Auto-generated from /ossfs/workspace/bfcl_xiexin/bfcl_eval/data/multi_turn_func_doc/math_api.json
"""

from typing import List, Dict, Any

MATH_API_TOOL_SCHEMAS: List[Dict[str, Any]] = [
    {
        'type': 'function',
        'function': {
            'name': 'absolute_value',
            'description': 'This tool belongs to the Math API, which provides various mathematical operations. Tool description: Calculate the absolute value of a number.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'number': {
                        'type': 'float',
                        'description': 'The number to calculate the absolute value of. '
                    }
                },
                'required': [
                    'number'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'add',
            'description': 'This tool belongs to the Math API, which provides various mathematical operations. Tool description: Add two numbers.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'a': {
                        'type': 'float',
                        'description': 'First number.'
                    },
                    'b': {
                        'type': 'float',
                        'description': 'Second number. '
                    }
                },
                'required': [
                    'a',
                    'b'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'divide',
            'description': 'This tool belongs to the Math API, which provides various mathematical operations. Tool description: Divide one number by another.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'a': {
                        'type': 'float',
                        'description': 'Numerator.'
                    },
                    'b': {
                        'type': 'float',
                        'description': 'Denominator. '
                    }
                },
                'required': [
                    'a',
                    'b'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'imperial_si_conversion',
            'description': 'This tool belongs to the Math API, which provides various mathematical operations. Tool description: Convert a value between imperial and SI units.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'value': {
                        'type': 'float',
                        'description': 'Value to be converted.'
                    },
                    'unit_in': {
                        'type': 'string',
                        'description': 'Unit of the input value.'
                    },
                    'unit_out': {
                        'type': 'string',
                        'description': 'Unit to convert the value to. '
                    }
                },
                'required': [
                    'value',
                    'unit_in',
                    'unit_out'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'logarithm',
            'description': 'This tool belongs to the Math API, which provides various mathematical operations. Tool description: Compute the logarithm of a number with adjustable precision using mpmath.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'value': {
                        'type': 'float',
                        'description': 'The number to compute the logarithm of.'
                    },
                    'base': {
                        'type': 'float',
                        'description': 'The base of the logarithm.'
                    },
                    'precision': {
                        'type': 'integer',
                        'description': 'Desired precision for the result. '
                    }
                },
                'required': [
                    'value',
                    'base',
                    'precision'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'max_value',
            'description': 'This tool belongs to the Math API, which provides various mathematical operations. Tool description: Find the maximum value in a list of numbers.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'numbers': {
                        'type': 'array',
                        'items': {
                            'type': 'float'
                        },
                        'description': 'List of numbers to find the maximum from. '
                    }
                },
                'required': [
                    'numbers'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'mean',
            'description': 'This tool belongs to the Math API, which provides various mathematical operations. Tool description: Calculate the mean of a list of numbers.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'numbers': {
                        'type': 'array',
                        'items': {
                            'type': 'float'
                        },
                        'description': 'List of numbers to calculate the mean of. '
                    }
                },
                'required': [
                    'numbers'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'min_value',
            'description': 'This tool belongs to the Math API, which provides various mathematical operations. Tool description: Find the minimum value in a list of numbers.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'numbers': {
                        'type': 'array',
                        'items': {
                            'type': 'float'
                        },
                        'description': 'List of numbers to find the minimum from. '
                    }
                },
                'required': [
                    'numbers'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'multiply',
            'description': 'This tool belongs to the Math API, which provides various mathematical operations. Tool description: Multiply two numbers.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'a': {
                        'type': 'float',
                        'description': 'First number.'
                    },
                    'b': {
                        'type': 'float',
                        'description': 'Second number. '
                    }
                },
                'required': [
                    'a',
                    'b'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'percentage',
            'description': 'This tool belongs to the Math API, which provides various mathematical operations. Tool description: Calculate the percentage of a part relative to a whole.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'part': {
                        'type': 'float',
                        'description': 'The part value.'
                    },
                    'whole': {
                        'type': 'float',
                        'description': 'The whole value. '
                    }
                },
                'required': [
                    'part',
                    'whole'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'power',
            'description': 'This tool belongs to the Math API, which provides various mathematical operations. Tool description: Raise a number to a power.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'base': {
                        'type': 'float',
                        'description': 'The base number.'
                    },
                    'exponent': {
                        'type': 'float',
                        'description': 'The exponent. '
                    }
                },
                'required': [
                    'base',
                    'exponent'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'round_number',
            'description': 'This tool belongs to the Math API, which provides various mathematical operations. Tool description: Round a number to a specified number of decimal places.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'number': {
                        'type': 'float',
                        'description': 'The number to round.'
                    },
                    'decimal_places': {
                        'type': 'integer',
                        'description': 'The number of decimal places to round to. Defaults to 0. ',
                        'default': 0
                    }
                },
                'required': [
                    'number'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'si_unit_conversion',
            'description': 'This tool belongs to the Math API, which provides various mathematical operations. Tool description: Convert a value from one SI unit to another.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'value': {
                        'type': 'float',
                        'description': 'Value to be converted.'
                    },
                    'unit_in': {
                        'type': 'string',
                        'description': 'Unit of the input value.'
                    },
                    'unit_out': {
                        'type': 'string',
                        'description': 'Unit to convert the value to. '
                    }
                },
                'required': [
                    'value',
                    'unit_in',
                    'unit_out'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'square_root',
            'description': 'This tool belongs to the Math API, which provides various mathematical operations. Tool description: Calculate the square root of a number with adjustable precision using the decimal module.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'number': {
                        'type': 'float',
                        'description': 'The number to calculate the square root of.'
                    },
                    'precision': {
                        'type': 'integer',
                        'description': 'Desired precision for the result. '
                    }
                },
                'required': [
                    'number',
                    'precision'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'standard_deviation',
            'description': 'This tool belongs to the Math API, which provides various mathematical operations. Tool description: Calculate the standard deviation of a list of numbers.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'numbers': {
                        'type': 'array',
                        'items': {
                            'type': 'float'
                        },
                        'description': 'List of numbers to calculate the standard deviation of. '
                    }
                },
                'required': [
                    'numbers'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'subtract',
            'description': 'This tool belongs to the Math API, which provides various mathematical operations. Tool description: Subtract one number from another.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'a': {
                        'type': 'float',
                        'description': 'Number to subtract from.'
                    },
                    'b': {
                        'type': 'float',
                        'description': 'Number to subtract. '
                    }
                },
                'required': [
                    'a',
                    'b'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'sum_values',
            'description': 'This tool belongs to the Math API, which provides various mathematical operations. Tool description: Calculate the sum of a list of numbers.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'numbers': {
                        'type': 'array',
                        'items': {
                            'type': 'float'
                        },
                        'description': 'List of numbers to sum. '
                    }
                },
                'required': [
                    'numbers'
                ]
            }
        }
    }
]
