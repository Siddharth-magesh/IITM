#!/usr/bin/env python3
"""
Minimal safe 'copilot-cli' demo agent.
- Reads the task description from stdin.
- Supports computing factorials for small integers when the task requests printing N! or "factorial of N".
- Does NOT execute arbitrary code.
"""
import sys
import re
from math import factorial


def parse_and_run(task: str) -> str:
    t = task.lower().strip()

    # Look for patterns like "print 8!" or "prints 8!" or "8!" or "factorial of 8"
    m = re.search(r"(\b\d{1,2})\s*!", t)
    if m:
        n = int(m.group(1))
    else:
        m2 = re.search(r"factorial (of )?(\d{1,2})", t)
        if m2:
            n = int(m2.group(2))
        else:
            return "Unsupported task: agent only supports small factorials (e.g. 'prints 8!')."

    # safety: limit n to reasonable size
    if n < 0 or n > 20:
        return f"Refusing to compute factorial of {n}: supported range 0..20."

    return str(factorial(n))


def main():
    task = sys.stdin.read()
    if not task:
        print("No task provided", file=sys.stderr)
        sys.exit(2)
    try:
        out = parse_and_run(task)
        print(out)
    except Exception as exc:
        print(f"Agent error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
