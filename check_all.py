#!/usr/bin/env python3

import subprocess
import sys


def run_command(cmd, desc):
    print(f"Running {desc}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    if result.returncode != 0:
        print(f"{desc} failed!")
        return False
    print(f"{desc} passed.")
    return True


def main():
    checks = [
        (["python3", "-m", "ruff", "check", "."], "Ruff linting"),
        (["python3", "-m", "ruff", "format", "--check", "."], "Ruff formatting"),
        (["python3", "-m", "bandit", "-r", "main.py"], "Bandit security scan"),
        (["python3", "run_tests.py"], "Tests with coverage"),
    ]

    all_passed = True
    for cmd, desc in checks:
        if not run_command(cmd, desc):
            all_passed = False

    if all_passed:
        print("All checks passed! Ready to commit/push.")
        sys.exit(0)
    else:
        print("Some checks failed. Fix issues before committing/pushing.")
        sys.exit(1)


if __name__ == "__main__":
    main()
