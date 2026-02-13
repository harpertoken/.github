# Workflows

This document describes all GitHub Actions workflows in this repository.

## CI Workflow

Runs tests, linting, and security checks on pull requests and pushes.

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[test]"
      - name: Run tests
        run: python run_tests.py
```

## Release Workflow

Builds and creates GitHub releases when tags are pushed.

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v6
      - name: Set tag name
        run: echo "TAG=${GITHUB_REF_NAME#v}" >> $GITHUB_ENV
      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build
      - name: Build package
        run: python -m build
      - name: Create Release
        uses: softprops/action-gh-release@v2
        with:
          files: ./dist/git-tui-${{ env.TAG }}.tar.gz
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## CLA Workflow

Ensures contributors have signed the Contributor License Agreement.

```yaml
name: CLA

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  cla:
    runs-on: ubuntu-latest
    if: github.repository_owner == 'harpertoken'
    steps:
      - uses: actions/checkout@v4
        with:
          sparse-checkout: |
            signed.json

      - name: Checkout private cla-bot
        uses: actions/checkout@v4
        with:
          repository: bniladridas/cla-bot
          token: ${{ secrets.YOUR_TOKEN_HERE }}
          path: cla-bot

      - name: Copy signed.json to cla-signers.json
        run: |
          cp signed.json cla-signers.json
          cp signed.json cla-bot/cla-signers.json

      - name: Run CLA bot
        uses: ./cla-bot/
        with:
          github-token: ${{ secrets.YOUR_TOKEN_HERE }}
```

## Auto Close PRs

Automatically closes pull requests with no activity.

```yaml
name: Auto Close PRs

on:
  schedule:
    - cron: '0 0 * * *'

jobs:
  auto-close:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/close-pr@v1
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
```

## Lock Merged PRs

Locks merged pull requests to prevent further changes.

```yaml
name: Lock Merged PRs

on:
  pull_request:
    types: [merged]

jobs:
  lock:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/lock-closed-prs@v1
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
```

## Test Trigger

Manually triggers test workflow for debugging.

```yaml
name: Test Trigger

on:
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Test triggered"
```
