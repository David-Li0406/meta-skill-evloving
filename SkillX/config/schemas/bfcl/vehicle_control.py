"""BFCL vehicle_control tool schemas.

Auto-generated from /ossfs/workspace/bfcl_xiexin/bfcl_eval/data/multi_turn_func_doc/vehicle_control.json
"""

from typing import List, Dict, Any

VEHICLE_CONTROL_TOOL_SCHEMAS: List[Dict[str, Any]] = [
    {
        'type': 'function',
        'function': {
            'name': 'activateParkingBrake',
            'description': 'This tool belongs to the vehicle control system, which allows users to control various aspects of the car such as engine, doors, climate control, lights, and more. Tool description: Activates the parking brake of the vehicle.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'mode': {
                        'type': 'string',
                        'description': 'The mode to set. [Enum]: ["engage", "release"]'
                    }
                },
                'required': [
                    'mode'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'adjustClimateControl',
            'description': 'This tool belongs to the vehicle control system, which allows users to control various aspects of the car such as engine, doors, climate control, lights, and more. Tool description: Adjusts the climate control of the vehicle.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'temperature': {
                        'type': 'float',
                        'description': 'The temperature to set in degree. Default to be celsius.'
                    },
                    'unit': {
                        'type': 'string',
                        'description': 'The unit of temperature. [Enum]: ["celsius", "fahrenheit"]',
                        'default': 'celsius'
                    },
                    'fanSpeed': {
                        'type': 'integer',
                        'description': 'The fan speed to set from 0 to 100. Default is 50.',
                        'default': 50
                    },
                    'mode': {
                        'type': 'string',
                        'description': 'The climate mode to set. [Enum]: ["auto", "cool", "heat", "defrost"]',
                        'default': 'auto'
                    }
                },
                'required': [
                    'temperature'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'check_tire_pressure',
            'description': 'This tool belongs to the vehicle control system, which allows users to control various aspects of the car such as engine, doors, climate control, lights, and more. Tool description: Checks the tire pressure of the vehicle.',
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
            'name': 'displayCarStatus',
            'description': 'This tool belongs to the vehicle control system, which allows users to control various aspects of the car such as engine, doors, climate control, lights, and more. Tool description: Displays the status of the vehicle based on the provided display option.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'option': {
                        'type': 'string',
                        'description': 'The option to display. [Enum]: ["fuel", "battery", "doors", "climate", "headlights", "parkingBrake", "brakePedal", "engine"]'
                    }
                },
                'required': [
                    'option'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'display_log',
            'description': 'This tool belongs to the vehicle control system, which allows users to control various aspects of the car such as engine, doors, climate control, lights, and more. Tool description: Displays the log messages.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'messages': {
                        'type': 'array',
                        'items': {
                            'type': 'string'
                        },
                        'description': 'The list of messages to display.'
                    }
                },
                'required': [
                    'messages'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'estimate_distance',
            'description': 'This tool belongs to the vehicle control system, which allows users to control various aspects of the car such as engine, doors, climate control, lights, and more. Tool description: Estimates the distance between two cities.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'cityA': {
                        'type': 'string',
                        'description': 'The zipcode of the first city.'
                    },
                    'cityB': {
                        'type': 'string',
                        'description': 'The zipcode of the second city.'
                    }
                },
                'required': [
                    'cityA',
                    'cityB'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'estimate_drive_feasibility_by_mileage',
            'description': 'This tool belongs to the vehicle control system, which allows users to control various aspects of the car such as engine, doors, climate control, lights, and more. Tool description: Estimates the milage of the vehicle given the distance needed to drive.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'distance': {
                        'type': 'float',
                        'description': 'The distance to travel in miles.'
                    }
                },
                'required': [
                    'distance'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'fillFuelTank',
            'description': 'This tool belongs to the vehicle control system, which allows users to control various aspects of the car such as engine, doors, climate control, lights, and more. Tool description: Fills the fuel tank of the vehicle. The fuel tank can hold up to 50 gallons.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'fuelAmount': {
                        'type': 'float',
                        'description': 'The amount of fuel to fill in gallons; this is the additional fuel to add to the tank.'
                    }
                },
                'required': [
                    'fuelAmount'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'find_nearest_tire_shop',
            'description': 'This tool belongs to the vehicle control system, which allows users to control various aspects of the car such as engine, doors, climate control, lights, and more. Tool description: Finds the nearest tire shop.',
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
            'name': 'gallon_to_liter',
            'description': 'This tool belongs to the vehicle control system, which allows users to control various aspects of the car such as engine, doors, climate control, lights, and more. Tool description: Converts the gallon to liter.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'gallon': {
                        'type': 'float',
                        'description': 'The amount of gallon to convert.'
                    }
                },
                'required': [
                    'gallon'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_current_speed',
            'description': 'This tool belongs to the vehicle control system, which allows users to control various aspects of the car such as engine, doors, climate control, lights, and more. Tool description: Gets the current speed of the vehicle.',
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
            'name': 'get_outside_temperature_from_google',
            'description': 'This tool belongs to the vehicle control system, which allows users to control various aspects of the car such as engine, doors, climate control, lights, and more. Tool description: Gets the outside temperature.',
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
            'name': 'get_outside_temperature_from_weather_com',
            'description': 'This tool belongs to the vehicle control system, which allows users to control various aspects of the car such as engine, doors, climate control, lights, and more. Tool description: Gets the outside temperature.',
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
            'name': 'get_zipcode_based_on_city',
            'description': 'This tool belongs to the vehicle control system, which allows users to control various aspects of the car such as engine, doors, climate control, lights, and more. Tool description: Gets the zipcode based on the city.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'city': {
                        'type': 'string',
                        'description': 'The name of the city.'
                    }
                },
                'required': [
                    'city'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'liter_to_gallon',
            'description': 'This tool belongs to the vehicle control system, which allows users to control various aspects of the car such as engine, doors, climate control, lights, and more. Tool description: Converts the liter to gallon.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'liter': {
                        'type': 'float',
                        'description': 'The amount of liter to convert.'
                    }
                },
                'required': [
                    'liter'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'lockDoors',
            'description': 'This tool belongs to the vehicle control system, which allows users to control various aspects of the car such as engine, doors, climate control, lights, and more. Tool description: Locks the doors of the vehicle.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'unlock': {
                        'type': 'boolean',
                        'description': 'True if the doors are to be unlocked, False otherwise.'
                    },
                    'door': {
                        'type': 'array',
                        'items': {
                            'type': 'string'
                        },
                        'description': 'The list of doors to lock or unlock. [Enum]: ["driver", "passenger", "rear_left", "rear_right"]'
                    }
                },
                'required': [
                    'unlock',
                    'door'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'pressBrakePedal',
            'description': 'This tool belongs to the vehicle control system, which allows users to control various aspects of the car such as engine, doors, climate control, lights, and more. Tool description: Presses the brake pedal based on pedal position. The brake pedal will be kept pressed until released.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'pedalPosition': {
                        'type': 'float',
                        'description': 'Position of the brake pedal, between 0 (not pressed) and 1 (fully pressed).'
                    }
                },
                'required': [
                    'pedalPosition'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'releaseBrakePedal',
            'description': 'This tool belongs to the vehicle control system, which allows users to control various aspects of the car such as engine, doors, climate control, lights, and more. Tool description: Releases the brake pedal of the vehicle.',
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
            'name': 'setCruiseControl',
            'description': 'This tool belongs to the vehicle control system, which allows users to control various aspects of the car such as engine, doors, climate control, lights, and more. Tool description: Sets the cruise control of the vehicle.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'speed': {
                        'type': 'float',
                        'description': 'The speed to set in m/h. The speed should be between 0 and 120 and a multiple of 5.'
                    },
                    'activate': {
                        'type': 'boolean',
                        'description': 'True to activate the cruise control, False to deactivate.'
                    },
                    'distanceToNextVehicle': {
                        'type': 'float',
                        'description': 'The distance to the next vehicle in meters.'
                    }
                },
                'required': [
                    'speed',
                    'activate',
                    'distanceToNextVehicle'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'setHeadlights',
            'description': 'This tool belongs to the vehicle control system, which allows users to control various aspects of the car such as engine, doors, climate control, lights, and more. Tool description: Sets the headlights of the vehicle.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'mode': {
                        'type': 'string',
                        'description': 'The mode of the headlights. [Enum]: ["on", "off", "auto"]'
                    }
                },
                'required': [
                    'mode'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'set_navigation',
            'description': 'This tool belongs to the vehicle control system, which allows users to control various aspects of the car such as engine, doors, climate control, lights, and more. Tool description: Navigates to the destination.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'destination': {
                        'type': 'string',
                        'description': 'The destination to navigate in the format of street, city, state.'
                    }
                },
                'required': [
                    'destination'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'startEngine',
            'description': 'This tool belongs to the vehicle control system, which allows users to control various aspects of the car such as engine, doors, climate control, lights, and more. Tool description: Starts the engine of the vehicle.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'ignitionMode': {
                        'type': 'string',
                        'description': 'The ignition mode of the vehicle. [Enum]: ["START", "STOP"]'
                    }
                },
                'required': [
                    'ignitionMode'
                ]
            }
        }
    }
]
