#!/usr/bin/env python3

import re
import sys
from pathlib import Path


def bump_version(current_version, bump_type):
    major, minor, patch = map(int, current_version.split("."))
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    else:
        raise ValueError("Invalid bump type. Use major, minor, or patch.")
    return f"{major}.{minor}.{patch}"


def update_pyproject_toml(new_version):
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    updated = re.sub(
        r'version = "\d+\.\d+\.\d+"', f'version = "{new_version}"', content
    )
    pyproject_path.write_text(updated)
    print(f"Updated version to {new_version}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python bump_version.py <major|minor|patch>")
        sys.exit(1)

    bump_type = sys.argv[1]
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    match = re.search(r'version = "(\d+\.\d+\.\d+)"', content)
    if not match:
        print("Version not found in pyproject.toml")
        sys.exit(1)

    current_version = match.group(1)
    new_version = bump_version(current_version, bump_type)
    update_pyproject_toml(new_version)


if __name__ == "__main__":
    main()
