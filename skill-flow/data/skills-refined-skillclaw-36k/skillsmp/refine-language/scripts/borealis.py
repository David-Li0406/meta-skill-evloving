#!/usr/bin/env python3
"""Kaller LM Studio med Borealis-modellen for å forbedre norsk tekst."""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

# Standardverdier
DEFAULT_API_URL = "http://localhost:1234/v1/chat/completions"
DEFAULT_MODEL = "borealis-4b-instruct-preview"


def load_env_file() -> dict[str, str]:
    """Les konfigurasjon fra .env-fil hvis den finnes."""
    env_vars = {}
    script_dir = Path(__file__).parent
    env_file = script_dir / ".env"

    if not env_file.exists():
        return env_vars

    with open(env_file, encoding="utf-8-sig") as f:  # utf-8-sig håndterer BOM
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                env_vars[key.strip()] = value.strip()

    return env_vars


def get_config(cli_api_url: str | None = None, cli_model: str | None = None) -> tuple[str, str]:
    """Hent API URL og modellnavn. Prioritet: CLI > env var > .env > default."""
    env_file_vars = load_env_file()

    api_url = (
        cli_api_url
        or os.environ.get("BOREALIS_API_URL")
        or env_file_vars.get("BOREALIS_API_URL")
        or DEFAULT_API_URL
    )
    model = (
        cli_model
        or os.environ.get("BOREALIS_MODEL")
        or env_file_vars.get("BOREALIS_MODEL")
        or DEFAULT_MODEL
    )

    return api_url, model


def check_connection(api_url: str, model: str) -> tuple[bool, str]:
    """Sjekk om tjenesten er tilgjengelig. Returnerer (ok, melding)."""
    # Prøv å hente modelliste først (raskere enn en full forespørsel)
    models_url = api_url.replace("/chat/completions", "/models")

    try:
        req = urllib.request.Request(models_url, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            models = [m.get("id", "") for m in result.get("data", [])]

            if model in models:
                return True, f"OK: Tjenesten kjører og modellen '{model}' er tilgjengelig."
            elif models:
                return True, f"ADVARSEL: Tjenesten kjører, men modellen '{model}' er ikke lastet. Tilgjengelige: {', '.join(models)}"
            else:
                return True, f"OK: Tjenesten kjører (kunne ikke verifisere modell)."

    except urllib.error.URLError as e:
        # Prøv chat-endepunktet direkte med en minimal forespørsel
        try:
            payload = {"model": model, "messages": [{"role": "user", "content": "test"}], "max_tokens": 1}
            req = urllib.request.Request(
                api_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                return True, f"OK: Tjenesten kjører på {api_url}"
        except urllib.error.URLError as e2:
            return False, f"FEIL: Kunne ikke koble til {api_url}. Sjekk at tjenesten kjører. ({e2.reason})"
        except Exception as e2:
            return False, f"FEIL: Uventet feil ved tilkobling: {e2}"


def forbedre_tekst(tekst: str, api_url: str, model: str) -> str:
    """Send tekst til Borealis-modellen og returner forbedret versjon."""
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "Du er en norsk språkekspert. Din oppgave er å forbedre tekster på norsk. Behold meningen, men gjør språket klarere, mer presist og bedre formulert. Svar med den forbedrede teksten i sin helhet."
            },
            {
                "role": "user",
                "content": f"Kan du forbedre denne teksten? Svar helst med den forbedrede teksten i sin helhet. Tekst:\n\n{tekst}"
            }
        ],
        "temperature": 0.7
    }

    req = urllib.request.Request(
        api_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    except urllib.error.URLError as e:
        return f"FEIL: Kunne ikke koble til {api_url}. Sjekk at tjenesten kjører. ({e.reason})"
    except (KeyError, IndexError):
        return "FEIL: Uventet respons fra LLM-tjenesten."


def main():
    parser = argparse.ArgumentParser(
        description="Forbedre norsk tekst med Borealis-modellen",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Eksempler:
  python borealis.py "Tekst som skal forbedres"
  python borealis.py --check
  python borealis.py --local "Tekst som skal forbedres"
  python borealis.py --api-url http://localhost:1234/v1/chat/completions "Tekst"

Konfigurasjon (prioritet: CLI > miljøvariabel > .env > standard):
  --api-url / BOREALIS_API_URL: API-endepunkt
  --model / BOREALIS_MODEL: Modellnavn
"""
    )

    parser.add_argument("tekst", nargs="*", help="Teksten som skal forbedres")
    parser.add_argument("--check", action="store_true", help="Sjekk om tjenesten er tilgjengelig")
    parser.add_argument("--local", action="store_true", help="Bruk lokal LM Studio (ignorerer .env)")
    parser.add_argument("--api-url", help="API-endepunkt (overstyrer alle andre kilder)")
    parser.add_argument("--model", help="Modellnavn (overstyrer alle andre kilder)")
    parser.add_argument("--show-config", action="store_true", help="Vis gjeldende konfigurasjon")

    args = parser.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")

    # Hvis --local, ignorer .env og bruk standardverdier
    if args.local:
        api_url = args.api_url or DEFAULT_API_URL
        model = args.model or DEFAULT_MODEL
    else:
        api_url, model = get_config(args.api_url, args.model)

    # Vis konfigurasjon
    if args.show_config or (not args.tekst and not args.check):
        print("Konfigurasjon:")
        print(f"  API URL: {api_url}")
        print(f"  Modell:  {model}")

        if args.local:
            print(f"  Modus:   Lokal (--local)")
        else:
            env_file_vars = load_env_file()
            if env_file_vars:
                print(f"  Kilde:   .env-fil")
            elif os.environ.get("BOREALIS_API_URL") or os.environ.get("BOREALIS_MODEL"):
                print(f"  Kilde:   Miljøvariabler")
            else:
                print(f"  Kilde:   Standardverdier")

        if not args.tekst and not args.check:
            print()
            print("Bruk --check for å verifisere tilkobling, eller oppgi tekst som skal forbedres.")
            sys.exit(0)

    # Sjekk tilkobling
    if args.check:
        ok, melding = check_connection(api_url, model)
        print(melding)
        sys.exit(0 if ok else 1)

    # Forbedre tekst
    if args.tekst:
        tekst = " ".join(args.tekst)

        # Sjekk tilkobling først
        ok, melding = check_connection(api_url, model)
        if not ok:
            print(melding, file=sys.stderr)
            sys.exit(1)

        resultat = forbedre_tekst(tekst, api_url, model)
        print(resultat)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
