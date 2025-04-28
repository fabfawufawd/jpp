#!/usr/bin/env python3

from typing import Any
import json
import sys

# ANSI colors
COLORS = {
    'reset': '\033[0m',
    'yellow': '\033[38;2;255;255;128m', #ffff80
    'purple': '\033[38;2;149;128;255m', #9580ff
    'white': '\033[97m' #ffffff
}

def pretty_print(data: Any, indent: int = 2) -> None:
    """Formats JSON data with colored output to the terminal.

    Args:
        data: JSON data (dict, list, str, int, float, bool, None).
        indent: Level of indentation in spaces (default is 2).
    """
    match data:
        case dict():
            print(f'{COLORS["white"]}{{')
            for i, (key, value) in enumerate(data.items()):
                is_last = i == len(data) - 1
                print(' ' * indent + f'{COLORS["purple"]}"{COLORS["yellow"]}{key}{COLORS["purple"]}"{COLORS["white"]}: ', end='')
                pretty_print(value, indent + 2)
                print(f'{COLORS["white"]}{"" if is_last else ","}')
            print(' ' * (indent - 2) + f'}}{COLORS["reset"]}', end='')

        case list():
            print(f'{COLORS["white"]}[')
            for i, item in enumerate(data):
                is_last = i == len(data) - 1
                print(' ' * indent, end='')
                pretty_print(item, indent + 2)
                print(f'{COLORS["white"]}{"" if is_last else ","}')
            print(' ' * (indent - 2) + f']{COLORS["reset"]}', end='')

        case bool():
            print(f'{COLORS["purple"]}{str(data).lower()}{COLORS["reset"]}', end='')

        case int() | float():
            str_num = f'{data:.4f}'.rstrip('0').rstrip('.')
            parts = str_num.split('.')
            if len(parts) == 1:
                print(f'{COLORS["purple"]}{parts[0]}{COLORS["reset"]}', end='')
            else:
                print(f'{COLORS["purple"]}{parts[0]}{COLORS["white"]}.{COLORS["purple"]}{parts[1]}{COLORS["reset"]}', end='')

        case None:
            print(f'{COLORS["purple"]}null{COLORS["reset"]}', end='')

        case _:
            print(f'{COLORS["purple"]}"{COLORS["yellow"]}{data}{COLORS["purple"]}"{COLORS["reset"]}', end='')

def main():
    """Processes input from stdin and prints formatted JSON."""
    if not sys.stdin.isatty():
        input_data = sys.stdin.read()
        if len(input_data) > 10 * 1024 * 1024: # 10MB
            print('Warning: Large input detected, processing may be slow', file=sys.stderr)

        try:
            parsed_data = json.loads(input_data)

            if isinstance(parsed_data, dict) and len(parsed_data) == 0:
                print('Error: empty JSON object', file=sys.stderr)
                raise SystemExit(1)

            pretty_print(parsed_data)
            print()
        except json.JSONDecodeError as e:
            print(f'JSON decoding error at position {e.pos}: {e.msg}', file=sys.stderr)
            raise SystemExit(1)
    else:
        print('No input data. Use as: curl ... | myjq', file=sys.stderr)
        raise SystemExit(1)

if __name__ == '__main__':
    main()