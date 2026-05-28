#!/usr/bin/env python3
"""
Component Doctor - Audit Script
Analiza archivos CSS y JavaScript para detectar problemas comunes.

Uso:
    python audit.py [path] [--type css|js|all] [--fix]

Ejemplos:
    python audit.py static/css/          # Auditar CSS
    python audit.py static/js/app.js     # Auditar archivo específico
    python audit.py . --type all         # Auditar todo
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Any

# Colores para output
class Colors:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def colorize(text: str, color: str) -> str:
    """Aplica color al texto."""
    return f"{color}{text}{Colors.RESET}"


class Issue:
    """Representa un problema encontrado."""
    def __init__(self, file: str, line: int, severity: str, rule: str, message: str, suggestion: str = ""):
        self.file = file
        self.line = line
        self.severity = severity  # high, medium, low
        self.rule = rule
        self.message = message
        self.suggestion = suggestion

    def __str__(self):
        color = {
            'high': Colors.RED,
            'medium': Colors.YELLOW,
            'low': Colors.BLUE
        }.get(self.severity, Colors.RESET)

        return f"{colorize(f'[{self.severity.upper()}]', color)} {self.file}:{self.line} - {self.message}"


class CSSAuditor:
    """Auditor de archivos CSS."""

    RULES = [
        # Z-index wars
        {
            'pattern': r'z-index:\s*(\d+)',
            'check': lambda m: int(m.group(1)) > 9999,
            'severity': 'medium',
            'rule': 'z-index-overflow',
            'message': 'Z-index muy alto (>9999)',
            'suggestion': 'Usa una escala definida: 10, 20, 30, 50, 100, 1000'
        },
        # !important abuse
        {
            'pattern': r'!important',
            'check': lambda m: True,
            'severity': 'low',
            'rule': 'important-abuse',
            'message': 'Uso de !important',
            'suggestion': 'Aumenta especificidad del selector en vez de usar !important'
        },
        # Hardcoded colors (not variables)
        {
            'pattern': r'(?:color|background|border):\s*#[0-9a-fA-F]{3,6}(?!.*var\()',
            'check': lambda m: True,
            'severity': 'low',
            'rule': 'hardcoded-color',
            'message': 'Color hardcodeado sin variable CSS',
            'suggestion': 'Usa CSS variables: var(--color-primary)'
        },
        # Missing vendor prefixes for backdrop-filter
        {
            'pattern': r'backdrop-filter:',
            'check': lambda m: True,
            'severity': 'medium',
            'rule': 'missing-webkit-prefix',
            'message': 'backdrop-filter necesita -webkit- prefix',
            'suggestion': 'Agrega: -webkit-backdrop-filter: blur(...);'
        },
    ]

    def audit(self, content: str, filename: str) -> List[Issue]:
        """Audita contenido CSS."""
        issues = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            for rule in self.RULES:
                matches = re.finditer(rule['pattern'], line)
                for match in matches:
                    if rule['check'](match):
                        issues.append(Issue(
                            file=filename,
                            line=i,
                            severity=rule['severity'],
                            rule=rule['rule'],
                            message=rule['message'],
                            suggestion=rule['suggestion']
                        ))

        return issues


class JSAuditor:
    """Auditor de archivos JavaScript."""

    RULES = [
        # innerHTML con variables
        {
            'pattern': r'\.innerHTML\s*=\s*[^"\'`]',
            'check': lambda m: True,
            'severity': 'high',
            'rule': 'xss-risk',
            'message': 'Posible vulnerabilidad XSS con innerHTML',
            'suggestion': 'Usa textContent o escapa el contenido'
        },
        # console.log en producción
        {
            'pattern': r'console\.(log|debug|info)\(',
            'check': lambda m: True,
            'severity': 'low',
            'rule': 'console-log',
            'message': 'console.log encontrado',
            'suggestion': 'Elimina para producción o usa logger condicional'
        },
        # eval()
        {
            'pattern': r'\beval\s*\(',
            'check': lambda m: True,
            'severity': 'high',
            'rule': 'eval-usage',
            'message': 'Uso de eval() - riesgo de seguridad',
            'suggestion': 'Evita eval(), usa JSON.parse() o alternativas seguras'
        },
        # var en vez de let/const
        {
            'pattern': r'\bvar\s+',
            'check': lambda m: True,
            'severity': 'low',
            'rule': 'var-usage',
            'message': 'Uso de var (legacy)',
            'suggestion': 'Usa const o let en vez de var'
        },
        # Event listener sin removeEventListener
        {
            'pattern': r'addEventListener\([^)]+\)',
            'check': lambda m: True,
            'severity': 'medium',
            'rule': 'event-listener-leak',
            'message': 'addEventListener encontrado - verificar cleanup',
            'suggestion': 'Asegúrate de llamar removeEventListener en cleanup'
        },
        # setInterval sin clearInterval
        {
            'pattern': r'setInterval\(',
            'check': lambda m: True,
            'severity': 'medium',
            'rule': 'interval-leak',
            'message': 'setInterval encontrado - verificar cleanup',
            'suggestion': 'Guarda referencia y llama clearInterval'
        },
        # onclick inline
        {
            'pattern': r'onclick\s*=',
            'check': lambda m: True,
            'severity': 'medium',
            'rule': 'inline-handler',
            'message': 'onclick inline encontrado',
            'suggestion': 'Usa addEventListener o event delegation'
        },
    ]

    def audit(self, content: str, filename: str) -> List[Issue]:
        """Audita contenido JavaScript."""
        issues = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Skip comments
            stripped = line.strip()
            if stripped.startswith('//') or stripped.startswith('/*'):
                continue

            for rule in self.RULES:
                if re.search(rule['pattern'], line):
                    issues.append(Issue(
                        file=filename,
                        line=i,
                        severity=rule['severity'],
                        rule=rule['rule'],
                        message=rule['message'],
                        suggestion=rule['suggestion']
                    ))

        return issues


class HTMLAuditor:
    """Auditor de archivos HTML."""

    RULES = [
        # Imágenes sin alt
        {
            'pattern': r'<img(?![^>]*\balt=)[^>]*>',
            'severity': 'high',
            'rule': 'missing-alt',
            'message': 'Imagen sin atributo alt',
            'suggestion': 'Agrega alt="descripción" a la imagen'
        },
        # Botones sin type
        {
            'pattern': r'<button(?![^>]*\btype=)[^>]*>',
            'severity': 'medium',
            'rule': 'button-no-type',
            'message': 'Botón sin atributo type',
            'suggestion': 'Agrega type="button" o type="submit"'
        },
        # Links que abren en nueva pestaña sin rel
        {
            'pattern': r'target="_blank"(?![^>]*\brel=)',
            'severity': 'medium',
            'rule': 'unsafe-target-blank',
            'message': 'target="_blank" sin rel="noopener"',
            'suggestion': 'Agrega rel="noopener noreferrer"'
        },
        # Emoji como icono
        {
            'pattern': r'>[\U0001F300-\U0001F9FF]<',
            'severity': 'medium',
            'rule': 'emoji-icon',
            'message': 'Emoji usado como icono',
            'suggestion': 'Usa SVG icons en vez de emojis'
        },
    ]

    def audit(self, content: str, filename: str) -> List[Issue]:
        """Audita contenido HTML."""
        issues = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            for rule in self.RULES:
                if re.search(rule['pattern'], line, re.IGNORECASE):
                    issues.append(Issue(
                        file=filename,
                        line=i,
                        severity=rule['severity'],
                        rule=rule['rule'],
                        message=rule['message'],
                        suggestion=rule['suggestion']
                    ))

        return issues


def get_files(path: str, file_types: List[str]) -> List[Path]:
    """Obtiene lista de archivos a auditar."""
    path = Path(path)

    if path.is_file():
        return [path]

    files = []
    for ext in file_types:
        files.extend(path.rglob(f'*.{ext}'))

    return files


def print_summary(issues: List[Issue]) -> None:
    """Imprime resumen de la auditoría."""
    if not issues:
        print(colorize("\n✓ No se encontraron problemas!", Colors.GREEN))
        return

    # Agrupar por severidad
    by_severity = {'high': [], 'medium': [], 'low': []}
    for issue in issues:
        by_severity[issue.severity].append(issue)

    print(f"\n{Colors.BOLD}=== RESUMEN DE AUDITORÍA ==={Colors.RESET}")
    print(f"Total de problemas: {len(issues)}")
    print(f"  {colorize('Alto:', Colors.RED)} {len(by_severity['high'])}")
    print(f"  {colorize('Medio:', Colors.YELLOW)} {len(by_severity['medium'])}")
    print(f"  {colorize('Bajo:', Colors.BLUE)} {len(by_severity['low'])}")

    print(f"\n{Colors.BOLD}=== PROBLEMAS ENCONTRADOS ==={Colors.RESET}")

    for severity in ['high', 'medium', 'low']:
        if by_severity[severity]:
            print(f"\n{severity.upper()} SEVERITY:")
            for issue in by_severity[severity]:
                print(f"  {issue}")
                if issue.suggestion:
                    print(f"    → {colorize(issue.suggestion, Colors.GREEN)}")


def main():
    parser = argparse.ArgumentParser(
        description='Component Doctor - Audit Script',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('path', nargs='?', default='.', help='Ruta a auditar')
    parser.add_argument('--type', choices=['css', 'js', 'html', 'all'], default='all',
                        help='Tipo de archivos a auditar')

    args = parser.parse_args()

    # Determinar tipos de archivo
    if args.type == 'all':
        file_types = ['css', 'js', 'html']
    else:
        file_types = [args.type]

    # Obtener archivos
    files = get_files(args.path, file_types)

    if not files:
        print(f"No se encontraron archivos {file_types} en {args.path}")
        return

    print(f"{Colors.BOLD}Component Doctor - Auditoría{Colors.RESET}")
    print(f"Analizando {len(files)} archivos...")

    # Auditar
    all_issues = []
    auditors = {
        'css': CSSAuditor(),
        'js': JSAuditor(),
        'html': HTMLAuditor()
    }

    for file_path in files:
        ext = file_path.suffix[1:]  # Remove dot
        if ext not in auditors:
            continue

        try:
            content = file_path.read_text(encoding='utf-8')
            issues = auditors[ext].audit(content, str(file_path))
            all_issues.extend(issues)
        except Exception as e:
            print(f"Error procesando {file_path}: {e}")

    # Mostrar resultados
    print_summary(all_issues)

    # Exit code
    high_count = sum(1 for i in all_issues if i.severity == 'high')
    sys.exit(1 if high_count > 0 else 0)


if __name__ == '__main__':
    main()
