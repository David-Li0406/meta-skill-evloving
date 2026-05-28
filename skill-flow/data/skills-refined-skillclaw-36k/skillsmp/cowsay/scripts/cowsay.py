#!/usr/bin/env python3
"""Generate ASCII art of a cow with a speech/thought bubble."""

import argparse
import textwrap


def build_bubble(lines: list[str], think: bool = False) -> list[str]:
    """Build the speech or thought bubble around the message."""
    max_len = max(len(line) for line in lines) if lines else 0

    if think:
        border_left = "("
        border_right = ")"
    else:
        border_left = "<"
        border_right = ">"

    result = []
    result.append(" " + "_" * (max_len + 2))

    if len(lines) == 1:
        result.append(f"{border_left} {lines[0].ljust(max_len)} {border_right}")
    else:
        for i, line in enumerate(lines):
            if i == 0:
                left, right = ("/", "\\") if not think else ("(", ")")
            elif i == len(lines) - 1:
                left, right = ("\\", "/") if not think else ("(", ")")
            else:
                left, right = ("|", "|") if not think else ("(", ")")
            result.append(f"{left} {line.ljust(max_len)} {right}")

    result.append(" " + "-" * (max_len + 2))
    return result


def build_cow(eyes: str = "oo", tongue: str = "", think: bool = False) -> list[str]:
    """Build the cow ASCII art."""
    eye_str = eyes[:2].ljust(2) if eyes else "oo"
    tongue_str = tongue[:2] if tongue else "  "

    connector = "o" if think else "\\"

    return [
        f"        {connector}   ^__^",
        f"         {connector}  ({eye_str})\\_______",
        "            (__)\\       )\\/\\",
        f"             {tongue_str} ||----w |",
        "                ||     ||",
    ]


def cowsay(
    message: str,
    eyes: str = "oo",
    tongue: str = "",
    width: int = 40,
    think: bool = False,
) -> str:
    """Generate cowsay ASCII art."""
    wrapped = textwrap.wrap(message, width=width) if message else [""]

    bubble = build_bubble(wrapped, think)
    cow = build_cow(eyes, tongue, think)

    return "\n".join(bubble + cow)


def main():
    parser = argparse.ArgumentParser(
        description="Generate ASCII art of a cow with a message"
    )
    parser.add_argument(
        "message", nargs="?", default="Moo!", help="The message for the cow to say"
    )
    parser.add_argument(
        "--eyes", "-e", default="oo", help="Custom eye characters (default: oo)"
    )
    parser.add_argument("--tongue", "-T", default="", help="Custom tongue characters")
    parser.add_argument(
        "--width",
        "-W",
        type=int,
        default=40,
        help="Width of speech bubble (default: 40)",
    )
    parser.add_argument(
        "--think",
        action="store_true",
        help="Use thought bubble instead of speech bubble",
    )

    args = parser.parse_args()
    print(cowsay(args.message, args.eyes, args.tongue, args.width, args.think))


if __name__ == "__main__":
    main()
