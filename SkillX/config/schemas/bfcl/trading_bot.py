"""BFCL trading_bot tool schemas.

Auto-generated from /ossfs/workspace/bfcl_xiexin/bfcl_eval/data/multi_turn_func_doc/trading_bot.json
"""

from typing import List, Dict, Any

TRADING_BOT_TOOL_SCHEMAS: List[Dict[str, Any]] = [
    {
        'type': 'function',
        'function': {
            'name': 'add_to_watchlist',
            'description': 'This tool belongs to the trading system, which allows users to trade stocks, manage their account, and view stock information. Tool description: Add a stock to the watchlist.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'stock': {
                        'type': 'string',
                        'description': 'the stock symbol to add to the watchlist. '
                    }
                },
                'required': [
                    'stock'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'cancel_order',
            'description': 'This tool belongs to the trading system, which allows users to trade stocks, manage their account, and view stock information. Tool description: Cancel an order.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'order_id': {
                        'type': 'integer',
                        'description': 'ID of the order to cancel. '
                    }
                },
                'required': [
                    'order_id'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'filter_stocks_by_price',
            'description': 'This tool belongs to the trading system, which allows users to trade stocks, manage their account, and view stock information. Tool description: Filter stocks based on a price range.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'stocks': {
                        'type': 'array',
                        'items': {
                            'type': 'string'
                        },
                        'description': 'List of stock symbols to filter.'
                    },
                    'min_price': {
                        'type': 'float',
                        'description': 'Minimum stock price.'
                    },
                    'max_price': {
                        'type': 'float',
                        'description': 'Maximum stock price. '
                    }
                },
                'required': [
                    'stocks',
                    'min_price',
                    'max_price'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'fund_account',
            'description': 'This tool belongs to the trading system, which allows users to trade stocks, manage their account, and view stock information. Tool description: Fund the account with the specified amount.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'amount': {
                        'type': 'float',
                        'description': 'Amount to fund the account with. '
                    }
                },
                'required': [
                    'amount'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_account_info',
            'description': 'This tool belongs to the trading system, which allows users to trade stocks, manage their account, and view stock information. Tool description: Get account information.',
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
            'name': 'get_available_stocks',
            'description': 'This tool belongs to the trading system, which allows users to trade stocks, manage their account, and view stock information. Tool description: Get a list of stock symbols in the given sector.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'sector': {
                        'type': 'string',
                        'description': "The sector to retrieve stocks from (e.g., 'Technology'). "
                    }
                },
                'required': [
                    'sector'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_current_time',
            'description': 'This tool belongs to the trading system, which allows users to trade stocks, manage their account, and view stock information. Tool description: Get the current time.',
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
            'name': 'get_order_details',
            'description': 'This tool belongs to the trading system, which allows users to trade stocks, manage their account, and view stock information. Tool description: Get the details of an order.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'order_id': {
                        'type': 'integer',
                        'description': 'ID of the order. '
                    }
                },
                'required': [
                    'order_id'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_order_history',
            'description': 'This tool belongs to the trading system, which allows users to trade stocks, manage their account, and view stock information. Tool description: Get the stock order ID history.',
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
            'name': 'get_stock_info',
            'description': 'This tool belongs to the trading system, which allows users to trade stocks, manage their account, and view stock information. Tool description: Get the details of a stock.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'symbol': {
                        'type': 'string',
                        'description': 'Symbol that uniquely identifies the stock. '
                    }
                },
                'required': [
                    'symbol'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_symbol_by_name',
            'description': 'This tool belongs to the trading system, which allows users to trade stocks, manage their account, and view stock information. Tool description: Get the symbol of a stock by company name.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'name': {
                        'type': 'string',
                        'description': 'Name of the company. '
                    }
                },
                'required': [
                    'name'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_transaction_history',
            'description': 'This tool belongs to the trading system, which allows users to trade stocks, manage their account, and view stock information. Tool description: Get the transaction history within a specified date range.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'start_date': {
                        'type': 'string',
                        'description': "Start date for the history (format: 'YYYY-MM-DD').",
                        'default': 'None'
                    },
                    'end_date': {
                        'type': 'string',
                        'description': "End date for the history (format: 'YYYY-MM-DD'). ",
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
            'name': 'get_watchlist',
            'description': 'This tool belongs to the trading system, which allows users to trade stocks, manage their account, and view stock information. Tool description: Get the watchlist.',
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
            'name': 'notify_price_change',
            'description': 'This tool belongs to the trading system, which allows users to trade stocks, manage their account, and view stock information. Tool description: Notify if there is a significant price change in the stocks.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'stocks': {
                        'type': 'array',
                        'items': {
                            'type': 'string'
                        },
                        'description': 'List of stock symbols to check.'
                    },
                    'threshold': {
                        'type': 'float',
                        'description': 'Percentage change threshold to trigger a notification. '
                    }
                },
                'required': [
                    'stocks',
                    'threshold'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'place_order',
            'description': 'This tool belongs to the trading system, which allows users to trade stocks, manage their account, and view stock information. Tool description: Place an order.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'order_type': {
                        'type': 'string',
                        'description': 'Type of the order (Buy/Sell).'
                    },
                    'symbol': {
                        'type': 'string',
                        'description': 'Symbol of the stock to trade.'
                    },
                    'price': {
                        'type': 'float',
                        'description': 'Price at which to place the order.'
                    },
                    'amount': {
                        'type': 'integer',
                        'description': 'Number of shares to trade. '
                    }
                },
                'required': [
                    'order_type',
                    'symbol',
                    'price',
                    'amount'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'remove_stock_from_watchlist',
            'description': 'This tool belongs to the trading system, which allows users to trade stocks, manage their account, and view stock information. Tool description: Remove a stock from the watchlist.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'symbol': {
                        'type': 'string',
                        'description': 'Symbol of the stock to remove. '
                    }
                },
                'required': [
                    'symbol'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'trading_get_login_status',
            'description': 'This tool belongs to the trading system, which allows users to trade stocks, manage their account, and view stock information. Tool description: Get the login status.',
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
            'name': 'trading_login',
            'description': 'This tool belongs to the trading system, which allows users to trade stocks, manage their account, and view stock information. Tool description: Handle user login.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'username': {
                        'type': 'string',
                        'description': 'Username for authentication.'
                    },
                    'password': {
                        'type': 'string',
                        'description': 'Password for authentication. '
                    }
                },
                'required': [
                    'username',
                    'password'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'trading_logout',
            'description': 'This tool belongs to the trading system, which allows users to trade stocks, manage their account, and view stock information. Tool description: Handle user logout for trading system.',
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
            'name': 'withdraw_funds',
            'description': 'This tool belongs to the trading system, which allows users to trade stocks, manage their account, and view stock information. Tool description: Withdraw funds from the account balance.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'amount': {
                        'type': 'float',
                        'description': 'Amount to withdraw from the account. '
                    }
                },
                'required': [
                    'amount'
                ]
            }
        }
    }
]
