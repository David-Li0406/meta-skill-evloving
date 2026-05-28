import subprocess
import sys
import os
from rich.console import Console
from rich.panel import Panel

console = Console()

def run_step(name, command):
    """Executa um passo de verificação."""
    console.print(f"[bold blue]Running:[/bold blue] {name}...")
    try:
        # Se for um script python interno, usar sys.executable
        if command.startswith("python"):
            cmd_list = [sys.executable] + command.split()[1:]
        else:
            cmd_list = command.split()
            
        result = subprocess.run(cmd_list, capture_output=True, text=True)
        
        if result.returncode == 0:
            console.print(f"[bold green]✓ {name} Passed[/bold green]")
            return True
        else:
            console.print(f"[bold red]✗ {name} Failed[/bold red]")
            console.print(Panel(result.stderr or result.stdout, title="Error Output", border_style="red"))
            return False
            
    except Exception as e:
        console.print(f"[bold red]✗ {name} Failed with Exception[/bold red]")
        console.print(str(e))
        return False

def main():
    console.print(Panel("[bold white]🛡️  Biodiagnóstico Pre-Push Check[/bold white]", style="purple"))
    
    # Obter o diretório base do projeto (assumindo que o script está em .agent/skills/.../scripts)
    # Precisamos rodar os comandos na raiz do projeto
    # Ajuste este caminho conforme necessário
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
    os.chdir(project_root)
    console.print(f"Working Directory: [dim]{os.getcwd()}[/dim]\n")

    steps = [
        ("Integrity Check (State vs UI)", "python .agent/skills/reflex-technical-guardrails/scripts/check_integrity.py"),
        ("Reflex Validator", "python .agent/skills/reflex-technical-guardrails/scripts/validate_reflex.py"),
        ("Unit Tests (The Guardian)", "pytest"), 
    ]
    
    failed = False
    for name, cmd in steps:
        if not run_step(name, cmd):
            failed = True
            # Dependendo da rigidez, pode parar no primeiro erro ou rodar tudo
            # break 
            
    if failed:
        console.print("\n[bold red]⛔ Checks Failed - Do Not Push![/bold red]")
        sys.exit(1)
    else:
        console.print("\n[bold green]✅ All Checks Passed - Ready to Push![/bold green]")
        sys.exit(0)

if __name__ == "__main__":
    main()
