"""
WikiTree API Python Client
__main__.py

Command-line interface entry point for the WikiTree API client.
Allows direct API interaction from the shell using explicit named parameters.
Supports a 'help' command to view wrapper documentation.
Copyright (c) 2025 Steven Harris
License: GPL-3.0-only
"""

import sys
import json
import inspect
from .session import WikiTreeSession
from .fields_reference import describe_fields


def main():
    """Command-line entry point for the WikiTree API client."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  wikitree-cli <action> param=value [param=value ...]")
        print("  wikitree-cli help <action>")
        print()
        print("Examples:")
        print("  wikitree-cli getProfile key=Clemens-1 fields=Name,FirstName")
        print("  wikitree-cli help getAncestors")
        sys.exit(1)

    command = sys.argv[1]
    wt = WikiTreeSession()
    
    # Handle CLI help command
    if command.lower() == "help":
        if len(sys.argv) < 3:
            print("Usage: wikitree-cli help <action>")
            sys.exit(1)

        action = sys.argv[2]
        method = getattr(wt, action, None)
        if method is None:
            print(f"No action found: {action}")
            sys.exit(2)
            
        if action.lower() == "fields":
            print(describe_fields())
            sys.exit(0)

        doc = inspect.getdoc(method)
        if not doc:
            print(f"No documentation available for '{action}'.")
        else:
            print(f"\nHelp for {action}:\n")
            print(doc)
        sys.exit(0)

    # Otherwise, treat as API request
    action = command
    args = dict(arg.split("=", 1) for arg in sys.argv[2:] if "=" in arg)

    try:
        result = wt.request(action, **args)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
