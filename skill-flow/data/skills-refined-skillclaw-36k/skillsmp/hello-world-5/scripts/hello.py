#!/usr/bin/env python3
"""
Hello World Skill Script
A simple script that outputs an input string.
"""

import sys


def main():
    """
    Main function that outputs the input string.
    If no argument is provided, it prompts for input.
    """
    try:
        if len(sys.argv) > 1:
            # Get the input string from command-line arguments
            message = ' '.join(sys.argv[1:])
        else:
            # Prompt for input if no argument is provided
            # Only use input() if we think we are in an interactive session or need a fallback
            if sys.stdin.isatty():
                message = input("Enter a message: ")
            else:
                print("Error: No message provided and not running interactively.", file=sys.stderr)
                sys.exit(1)
        
        # Output the string
        print(message)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
