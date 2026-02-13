# SPDX-License-Identifier: MIT
#!/usr/bin/env python3

import subprocess
import sys


def run_tests():
    # Run bandit for security
    bandit_result = subprocess.run(
        [sys.executable, "-m", "bandit", "-r", "main.py"],
        capture_output=True,
        text=True,
    )
    print("Bandit Security Scan:")
    print(bandit_result.stdout)
    if bandit_result.stderr:
        print(bandit_result.stderr)
    if bandit_result.returncode != 0:
        print("Security issues found!")
        return bandit_result.returncode

    # Run pytest with coverage
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--cov=main",
            "--cov-report=html",
            "--cov-report=xml",
            "tests/",
        ],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode


if __name__ == "__main__":
    sys.exit(run_tests())
