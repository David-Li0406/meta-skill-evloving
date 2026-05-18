"""BFCL travel_booking tool schemas.

Auto-generated from /ossfs/workspace/bfcl_xiexin/bfcl_eval/data/multi_turn_func_doc/travel_booking.json
"""

from typing import List, Dict, Any

TRAVEL_BOOKING_TOOL_SCHEMAS: List[Dict[str, Any]] = [
    {
        'type': 'function',
        'function': {
            'name': 'authenticate_travel',
            'description': 'This tool belongs to the travel system, which allows users to book flights, manage credit cards, and view budget information. Tool description: Authenticate the user with the travel API',
            'parameters': {
                'type': 'object',
                'properties': {
                    'client_id': {
                        'type': 'string',
                        'description': 'The client applications client_id supplied by App Management'
                    },
                    'client_secret': {
                        'type': 'string',
                        'description': 'The client applications client_secret supplied by App Management'
                    },
                    'refresh_token': {
                        'type': 'string',
                        'description': 'The refresh token obtained from the initial authentication'
                    },
                    'grant_type': {
                        'type': 'string',
                        'description': 'The grant type of the authentication request. Here are the options: read_write, read, write'
                    },
                    'user_first_name': {
                        'type': 'string',
                        'description': 'The first name of the user'
                    },
                    'user_last_name': {
                        'type': 'string',
                        'description': 'The last name of the user'
                    }
                },
                'required': [
                    'client_id',
                    'client_secret',
                    'refresh_token',
                    'grant_type',
                    'user_first_name',
                    'user_last_name'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'book_flight',
            'description': 'This tool belongs to the travel system, which allows users to book flights, manage credit cards, and view budget information. Tool description: Book a flight given the travel information. From and To should be the airport codes in the IATA format.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'access_token': {
                        'type': 'string',
                        'description': 'The access token obtained from the authenticate'
                    },
                    'card_id': {
                        'type': 'string',
                        'description': 'The ID of the credit card to use for the booking'
                    },
                    'travel_date': {
                        'type': 'string',
                        'description': 'The date of the travel in the format YYYY-MM-DD'
                    },
                    'travel_from': {
                        'type': 'string',
                        'description': 'The location the travel is from'
                    },
                    'travel_to': {
                        'type': 'string',
                        'description': 'The location the travel is to'
                    },
                    'travel_class': {
                        'type': 'string',
                        'description': 'The class of the travel'
                    }
                },
                'required': [
                    'access_token',
                    'card_id',
                    'travel_date',
                    'travel_from',
                    'travel_to',
                    'travel_class'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'cancel_booking',
            'description': 'This tool belongs to the travel system, which allows users to book flights, manage credit cards, and view budget information. Tool description: Cancel a booking',
            'parameters': {
                'type': 'object',
                'properties': {
                    'access_token': {
                        'type': 'string',
                        'description': 'The access token obtained from the authenticate'
                    },
                    'booking_id': {
                        'type': 'string',
                        'description': 'The ID of the booking'
                    }
                },
                'required': [
                    'access_token',
                    'booking_id'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'compute_exchange_rate',
            'description': 'This tool belongs to the travel system, which allows users to book flights, manage credit cards, and view budget information. Tool description: Compute the exchange rate between two currencies',
            'parameters': {
                'type': 'object',
                'properties': {
                    'base_currency': {
                        'type': 'string',
                        'description': 'The base currency. [Enum]: USD, RMB, EUR, JPY, GBP, CAD, AUD, INR, RUB, BRL, MXN'
                    },
                    'target_currency': {
                        'type': 'string',
                        'description': 'The target currency. [Enum]: USD, RMB, EUR, JPY, GBP, CAD, AUD, INR, RUB, BRL, MXN'
                    },
                    'value': {
                        'type': 'float',
                        'description': 'The value to convert'
                    }
                },
                'required': [
                    'base_currency',
                    'target_currency',
                    'value'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'contact_customer_support',
            'description': 'This tool belongs to the travel system, which allows users to book flights, manage credit cards, and view budget information. Tool description: Contact travel booking customer support, get immediate support on an issue with an online call.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'booking_id': {
                        'type': 'string',
                        'description': 'The ID of the booking'
                    },
                    'message': {
                        'type': 'string',
                        'description': 'The message to send to customer support'
                    }
                },
                'required': [
                    'booking_id',
                    'message'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_all_credit_cards',
            'description': 'This tool belongs to the travel system, which allows users to book flights, manage credit cards, and view budget information. Tool description: Get all registered credit cards',
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
            'name': 'get_booking_history',
            'description': 'This tool belongs to the travel system, which allows users to book flights, manage credit cards, and view budget information. Tool description: Retrieve all booking history for the user.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'access_token': {
                        'type': 'string',
                        'description': 'The access token obtained from the authenticate method. '
                    }
                },
                'required': [
                    'access_token'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_budget_fiscal_year',
            'description': 'This tool belongs to the travel system, which allows users to book flights, manage credit cards, and view budget information. Tool description: Get the budget fiscal year',
            'parameters': {
                'type': 'object',
                'properties': {
                    'lastModifiedAfter': {
                        'type': 'string',
                        'description': 'Use this field if you only want Fiscal Years that were changed after the supplied date. The supplied date will be interpreted in the UTC time zone. If lastModifiedAfter is not supplied, the service will return all Fiscal Years, regardless of modified date. Example: 2016-03-29T16:12:20. Return in the format of YYYY-MM-DDTHH:MM:SS.',
                        'default': 'None'
                    },
                    'includeRemoved': {
                        'type': 'string',
                        'description': 'If true, the service will return all Fiscal Years, including those that were previously removed. If not supplied, this field defaults to false.',
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
            'name': 'get_credit_card_balance',
            'description': 'This tool belongs to the travel system, which allows users to book flights, manage credit cards, and view budget information. Tool description: Get the balance of a credit card',
            'parameters': {
                'type': 'object',
                'properties': {
                    'access_token': {
                        'type': 'string',
                        'description': 'The access token obtained from the authenticate'
                    },
                    'card_id': {
                        'type': 'string',
                        'description': 'The ID of the credit card'
                    }
                },
                'required': [
                    'access_token',
                    'card_id'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_flight_cost',
            'description': 'This tool belongs to the travel system, which allows users to book flights, manage credit cards, and view budget information. Tool description: Get the list of cost of a flight in USD based on location, date, and class',
            'parameters': {
                'type': 'object',
                'properties': {
                    'travel_from': {
                        'type': 'string',
                        'description': 'The 3 letter code of the departing airport'
                    },
                    'travel_to': {
                        'type': 'string',
                        'description': 'The 3 letter code of the arriving airport'
                    },
                    'travel_date': {
                        'type': 'string',
                        'description': "The date of the travel in the format 'YYYY-MM-DD'"
                    },
                    'travel_class': {
                        'type': 'string',
                        'description': 'The class of the travel. Options are: economy, business, first.'
                    }
                },
                'required': [
                    'travel_from',
                    'travel_to',
                    'travel_date',
                    'travel_class'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_nearest_airport_by_city',
            'description': 'This tool belongs to the travel system, which allows users to book flights, manage credit cards, and view budget information. Tool description: Get the nearest airport to the given location',
            'parameters': {
                'type': 'object',
                'properties': {
                    'location': {
                        'type': 'string',
                        'description': 'The name of the location. [Enum]: Rivermist, Stonebrook, Maplecrest, Silverpine, Shadowridge, London, Paris, Sunset Valley, Oakendale, Willowbend, Crescent Hollow, Autumnville, Pinehaven, Greenfield, San Francisco, Los Angeles, New York, Chicago, Boston, Beijing, Hong Kong, Rome, Tokyo'
                    }
                },
                'required': [
                    'location'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'list_all_airports',
            'description': 'This tool belongs to the travel system, which allows users to book flights, manage credit cards, and view budget information. Tool description: List all available airports',
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
            'name': 'purchase_insurance',
            'description': 'This tool belongs to the travel system, which allows users to book flights, manage credit cards, and view budget information. Tool description: Purchase insurance',
            'parameters': {
                'type': 'object',
                'properties': {
                    'access_token': {
                        'type': 'string',
                        'description': 'The access token obtained from the authenticate'
                    },
                    'insurance_type': {
                        'type': 'string',
                        'description': 'The type of insurance to purchase'
                    },
                    'insurance_cost': {
                        'type': 'float',
                        'description': 'The cost of the insurance'
                    },
                    'booking_id': {
                        'type': 'string',
                        'description': 'The ID of the booking'
                    },
                    'card_id': {
                        'type': 'string',
                        'description': 'The ID of the credit card to use for the'
                    }
                },
                'required': [
                    'access_token',
                    'insurance_type',
                    'booking_id',
                    'insurance_cost',
                    'card_id'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'register_credit_card',
            'description': 'This tool belongs to the travel system, which allows users to book flights, manage credit cards, and view budget information. Tool description: Register a credit card',
            'parameters': {
                'type': 'object',
                'properties': {
                    'access_token': {
                        'type': 'string',
                        'description': 'The access token obtained from the authenticate method'
                    },
                    'card_number': {
                        'type': 'string',
                        'description': 'The credit card number'
                    },
                    'expiration_date': {
                        'type': 'string',
                        'description': 'The expiration date of the credit card in the format MM/YYYY'
                    },
                    'cardholder_name': {
                        'type': 'string',
                        'description': 'The name of the cardholder'
                    },
                    'card_verification_number': {
                        'type': 'integer',
                        'description': 'The card verification number'
                    }
                },
                'required': [
                    'access_token',
                    'card_number',
                    'expiration_date',
                    'cardholder_name',
                    'card_verification_number'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'retrieve_invoice',
            'description': 'This tool belongs to the travel system, which allows users to book flights, manage credit cards, and view budget information. Tool description: Retrieve the invoice for a booking.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'access_token': {
                        'type': 'string',
                        'description': 'The access token obtained from the authenticate'
                    },
                    'booking_id': {
                        'type': 'string',
                        'description': 'The ID of the booking',
                        'default': 'None'
                    },
                    'insurance_id': {
                        'type': 'string',
                        'description': 'The ID of the insurance',
                        'default': 'None'
                    }
                },
                'required': [
                    'access_token'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'set_budget_limit',
            'description': 'This tool belongs to the travel system, which allows users to book flights, manage credit cards, and view budget information. Tool description: Set the budget limit for the user',
            'parameters': {
                'type': 'object',
                'properties': {
                    'access_token': {
                        'type': 'string',
                        'description': 'The access token obtained from the authentication process or initial configuration.'
                    },
                    'budget_limit': {
                        'type': 'float',
                        'description': 'The budget limit to set in USD'
                    }
                },
                'required': [
                    'access_token',
                    'budget_limit'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'travel_get_login_status',
            'description': 'This tool belongs to the travel system, which allows users to book flights, manage credit cards, and view budget information. Tool description: Get the status of the login',
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
            'name': 'verify_traveler_information',
            'description': 'This tool belongs to the travel system, which allows users to book flights, manage credit cards, and view budget information. Tool description: Verify the traveler information',
            'parameters': {
                'type': 'object',
                'properties': {
                    'first_name': {
                        'type': 'string',
                        'description': 'The first name of the traveler'
                    },
                    'last_name': {
                        'type': 'string',
                        'description': 'The last name of the traveler'
                    },
                    'date_of_birth': {
                        'type': 'string',
                        'description': 'The date of birth of the traveler in the format YYYY-MM-DD'
                    },
                    'passport_number': {
                        'type': 'string',
                        'description': 'The passport number of the traveler'
                    }
                },
                'required': [
                    'first_name',
                    'last_name',
                    'date_of_birth',
                    'passport_number'
                ]
            }
        }
    }
]
