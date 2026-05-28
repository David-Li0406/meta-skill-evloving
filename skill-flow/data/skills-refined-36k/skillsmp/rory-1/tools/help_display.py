from rich.console import Console

def display_help():
    console = Console()

    console.print("\n[bold]Rory[/bold] — Your CMO in the Terminal")
    console.print("[dim]Powered by Robynn AI[/dim]\n")

    console.print("[bold]USAGE[/bold]")
    console.print("    rory <command> [args]")
    console.print("    rory \"<natural language request>\"\n")

    console.print("[bold]COMMANDS[/bold]")
    console.print("    [green]research <company>[/green]        Research a company's marketing strategy")
    console.print("    [green]competitors <name>[/green]        Analyze competitor landscape")
    console.print("    [green]write <type>[/green]              Create content (linkedin, tweet, email, blog)")
    console.print("    [green]brief --for <type>[/green]        Create a marketing brief")
    console.print("    [green]status[/green]                    Check connection status")
    console.print("    [green]usage[/green]                     Check task usage this month")
    console.print("    [green]init[/green]                      Interactive setup wizard")
    console.print("    [green]config <api_key>[/green]          Connect your Robynn account")
    console.print("    [green]sync[/green]                      Verify Brand Hub connection")
    console.print("    [green]voice[/green]                     Preview brand voice settings")
    console.print("    [green]logout[/green]                    Remove account credentials")
    console.print("    [green]help[/green]                      Show this help message\n")

    console.print("[bold]OPTIONS[/bold]")
    console.print("    --json                    Output in JSON format\n")

    console.print("[bold]EXAMPLES[/bold]")
    console.print("    rory \"Write a LinkedIn post about AI automation\"")
    console.print("    rory research Stripe")
    console.print("    rory competitors \"marketing automation\"")
    console.print("    rory write linkedin post about our new feature")
    console.print("    rory brief --for \"product launch campaign\"\n")

    console.print("[bold]SETUP[/bold]")
    console.print("    1. Get your API key at [underline]https://robynn.ai/settings/api-keys[/underline]")
    console.print("    2. Run: rory init  [dim](or rory config <your_api_key>)[/dim]")
    console.print("    3. Verify: rory status\n")

    console.print("For more help, visit [underline]https://robynn.ai/docs/rory[/underline]")
    console.print("[dim]───[/dim]")
    console.print("What can I help you with? Write content, research companies, or analyze competitors.")

if __name__ == "__main__":
    display_help()
