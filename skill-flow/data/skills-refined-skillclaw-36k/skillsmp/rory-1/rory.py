#!/usr/bin/env python3
import sys
import argparse
import subprocess
import os

# Ensure the tools directory is in the path
sys.path.append(os.path.join(os.path.dirname(__file__), "tools"))

def main():
    parser = argparse.ArgumentParser(
        description="Rory — Your CMO in the Terminal",
        add_help=False
    )
    parser.add_argument("command", nargs="?", help="Command to run")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    
    # Catch all other arguments
    args, unknown = parser.parse_known_args()

    if not args.command:
        # Show welcome screen if no command
        subprocess.run([sys.executable, "tools/robynn.py"])
        return

    cmd = args.command.lower()

    if cmd in ["config", "status", "usage", "sync", "voice"]:
        # Route to robynn.py
        script_args = [sys.executable, "tools/robynn.py", cmd] + unknown
        subprocess.run(script_args)
    
    elif cmd in ["init", "login"]:
        # Onboarding wizard (login is an alias)
        from tools.onboarding import interactive_init
        domain = unknown[0] if unknown else None
        interactive_init(domain)
    
    elif cmd == "logout":
        # Logout command
        from tools.onboarding import logout
        logout()
    
    elif cmd == "uninstall":
        # Uninstall command
        from tools.onboarding import uninstall
        uninstall()
    
    elif cmd == "research":
        # Route to research.py company
        script_args = [sys.executable, "research.py", "company"] + unknown
        if args.json:
            script_args += ["--output", "json"]
        subprocess.run(script_args)

    elif cmd == "competitors":
        # Route to research.py competitor
        # Filter out --company if it was used as a flag
        target_parts = []
        skip_next = False
        for part in unknown:
            if skip_next:
                skip_next = False
                continue
            if part == "--company":
                skip_next = True
                continue
            target_parts.append(part)
        
        target = " ".join(target_parts)
        if not target and unknown: # Fallback if --company Acme Corp was used
            for i, part in enumerate(unknown):
                if part == "--company" and i + 1 < len(unknown):
                    target = unknown[i+1]
                    break

        script_args = [sys.executable, "research.py", "competitor", target]
        if args.json:
            script_args += ["--output", "json"]
        subprocess.run(script_args)

    elif cmd == "write":
        # Route to remote_cmo.py
        target = " ".join(unknown)
        script_args = [sys.executable, "tools/remote_cmo.py", f"write {target}"]
        subprocess.run(script_args)

    elif cmd == "brief":
        # Route to remote_cmo.py for a brief
        # Filter out --for if it was used as a flag
        brief_parts = []
        skip_next = False
        for part in unknown:
            if skip_next:
                skip_next = False
                continue
            if part == "--for":
                skip_next = True
                continue
            brief_parts.append(part)
        
        brief_for = " ".join(brief_parts)
        if not brief_for and unknown:
             for i, part in enumerate(unknown):
                if part == "--for" and i + 1 < len(unknown):
                    brief_for = unknown[i+1]
                    break

        prompt = f"create a marketing brief for {brief_for}"
        script_args = [sys.executable, "tools/remote_cmo.py", prompt]
        subprocess.run(script_args)

    elif cmd in ["help", "--help", "-h"]:
        try:
            import help_display
            help_display.display_help()
        except ImportError:
            # Fallback if rich is not installed yet
            from tools import help_display
            help_display.display_help()
        except Exception:
            # Final fallback
            print("\nRory — Your CMO in the Terminal")
            print("Powered by Robynn AI\n")
            print("USAGE")
            print("    rory <command> [args]")
            print("    rory \"<natural language request>\"\n")
            print("COMMANDS")
            print("    research <company>        Research a company's marketing strategy")
            print("    competitors <name>        Analyze competitor landscape")
            print("    write <type>              Create content (linkedin, tweet, email, blog)")
            print("    brief --for <type>        Create a marketing brief")
            print("    status                    Check connection status")
            print("    usage                     Check task usage this month")
            print("    init                      Interactive setup wizard")
            print("    config <api_key>          Connect your Robynn account")
            print("    sync                      Verify Brand Hub connection")
            print("    voice                     Preview brand voice settings")
            print("    logout                    Remove account credentials")
            print("    help                      Show this help message\n")
            print("OPTIONS")
            print("    --json                    Output in JSON format\n")
            print("EXAMPLES")
            print("    rory \"Write a LinkedIn post about AI automation\"")
            print("    rory research Stripe")
            print("    rory competitors \"marketing automation\"")
            print("    rory write linkedin post about our new feature")
            print("    rory brief --for \"product launch campaign\"\n")
            print("SETUP")
            print("    1. Get your API key at https://robynn.ai/settings/api-keys")
            print("    2. Run: rory init  (or rory config <your_api_key>)")
            print("    3. Verify: rory status\n")
            print("For more help, visit https://robynn.ai/docs/rory")
    
    else:
        # Default to remote_cmo.py for everything else
        full_query = " ".join([args.command] + unknown)
        script_args = [sys.executable, "tools/remote_cmo.py", full_query]
        subprocess.run(script_args)

if __name__ == "__main__":
    main()

