"""BFCL posting_api tool schemas.

Auto-generated from /ossfs/workspace/bfcl_xiexin/bfcl_eval/data/multi_turn_func_doc/posting_api.json
"""

from typing import List, Dict, Any

POSTING_API_TOOL_SCHEMAS: List[Dict[str, Any]] = [
    {
        'type': 'function',
        'function': {
            'name': 'authenticate_twitter',
            'description': 'This tool belongs to the TwitterAPI, which provides core functionality for posting tweets, retweeting, commenting, and following users on Twitter. Tool description: Authenticate a user with username and password.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'username': {
                        'type': 'string',
                        'description': 'Username of the user.'
                    },
                    'password': {
                        'type': 'string',
                        'description': 'Password of the user.'
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
            'name': 'comment',
            'description': 'This tool belongs to the TwitterAPI, which provides core functionality for posting tweets, retweeting, commenting, and following users on Twitter. Tool description: Comment on a tweet for the authenticated user.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'tweet_id': {
                        'type': 'integer',
                        'description': 'ID of the tweet to comment on.'
                    },
                    'comment_content': {
                        'type': 'string',
                        'description': 'Content of the comment.'
                    }
                },
                'required': [
                    'tweet_id',
                    'comment_content'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'follow_user',
            'description': 'This tool belongs to the TwitterAPI, which provides core functionality for posting tweets, retweeting, commenting, and following users on Twitter. Tool description: Follow a user for the authenticated user.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'username_to_follow': {
                        'type': 'string',
                        'description': 'Username of the user to follow.'
                    }
                },
                'required': [
                    'username_to_follow'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_tweet',
            'description': 'This tool belongs to the TwitterAPI, which provides core functionality for posting tweets, retweeting, commenting, and following users on Twitter. Tool description: Retrieve a specific tweet.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'tweet_id': {
                        'type': 'integer',
                        'description': 'ID of the tweet to retrieve.'
                    }
                },
                'required': [
                    'tweet_id'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_tweet_comments',
            'description': 'This tool belongs to the TwitterAPI, which provides core functionality for posting tweets, retweeting, commenting, and following users on Twitter. Tool description: Retrieve all comments for a specific tweet.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'tweet_id': {
                        'type': 'integer',
                        'description': 'ID of the tweet to retrieve comments for.'
                    }
                },
                'required': [
                    'tweet_id'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_user_stats',
            'description': 'This tool belongs to the TwitterAPI, which provides core functionality for posting tweets, retweeting, commenting, and following users on Twitter. Tool description: Get statistics for a specific user.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'username': {
                        'type': 'string',
                        'description': 'Username of the user to get statistics for.'
                    }
                },
                'required': [
                    'username'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_user_tweets',
            'description': 'This tool belongs to the TwitterAPI, which provides core functionality for posting tweets, retweeting, commenting, and following users on Twitter. Tool description: Retrieve all tweets from a specific user.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'username': {
                        'type': 'string',
                        'description': 'Username of the user whose tweets to retrieve.'
                    }
                },
                'required': [
                    'username'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'list_all_following',
            'description': 'This tool belongs to the TwitterAPI, which provides core functionality for posting tweets, retweeting, commenting, and following users on Twitter. Tool description: List all users that the authenticated user is following.',
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
            'name': 'mention',
            'description': 'This tool belongs to the TwitterAPI, which provides core functionality for posting tweets, retweeting, commenting, and following users on Twitter. Tool description: Mention specified users in a tweet.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'tweet_id': {
                        'type': 'integer',
                        'description': 'ID of the tweet where users are mentioned.'
                    },
                    'mentioned_usernames': {
                        'type': 'array',
                        'items': {
                            'type': 'string'
                        },
                        'description': 'List of usernames to be mentioned.'
                    }
                },
                'required': [
                    'tweet_id',
                    'mentioned_usernames'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'post_tweet',
            'description': 'This tool belongs to the TwitterAPI, which provides core functionality for posting tweets, retweeting, commenting, and following users on Twitter. Tool description: Post a tweet for the authenticated user.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'content': {
                        'type': 'string',
                        'description': 'Content of the tweet.'
                    },
                    'tags': {
                        'type': 'array',
                        'items': {
                            'type': 'string'
                        },
                        'description': 'List of tags for the tweet. Tag name should start with #. This is only relevant if the user wants to add tags to the tweet.',
                        'default': []
                    },
                    'mentions': {
                        'type': 'array',
                        'items': {
                            'type': 'string'
                        },
                        'description': 'List of users mentioned in the tweet. Mention name should start with @. This is only relevant if the user wants to add mentions to the tweet.',
                        'default': []
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
            'name': 'posting_get_login_status',
            'description': 'This tool belongs to the TwitterAPI, which provides core functionality for posting tweets, retweeting, commenting, and following users on Twitter. Tool description: Get the login status of the current user.',
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
            'name': 'retweet',
            'description': 'This tool belongs to the TwitterAPI, which provides core functionality for posting tweets, retweeting, commenting, and following users on Twitter. Tool description: Retweet a tweet for the authenticated user.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'tweet_id': {
                        'type': 'integer',
                        'description': 'ID of the tweet to retweet.'
                    }
                },
                'required': [
                    'tweet_id'
                ]
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'search_tweets',
            'description': 'This tool belongs to the TwitterAPI, which provides core functionality for posting tweets, retweeting, commenting, and following users on Twitter. Tool description: Search for tweets containing a specific keyword.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'keyword': {
                        'type': 'string',
                        'description': 'Keyword to search for in the content of the tweets.'
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
            'name': 'unfollow_user',
            'description': 'This tool belongs to the TwitterAPI, which provides core functionality for posting tweets, retweeting, commenting, and following users on Twitter. Tool description: Unfollow a user for the authenticated user.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'username_to_unfollow': {
                        'type': 'string',
                        'description': 'Username of the user to unfollow.'
                    }
                },
                'required': [
                    'username_to_unfollow'
                ]
            }
        }
    }
]
