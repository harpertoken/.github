# Adding Contributing Guide to Kilo

This document explains how we added a generic CONTRIBUTING.md file to sync across repositories.

## Overview

We created a generic `CONTRIBUTING.md` file that doesn't reference specific project names, making it reusable across multiple repositories.

## How It Works

1. **Generic Content**: The CONTRIBUTING.md file uses generic terms like "this project" instead of specific names
2. **Customizable Sections**: Each project can modify sections as needed while keeping the overall structure
3. **Kilo Config**: The `.kilo/kilo.json` file excludes the CONTRIBUTING.md from being processed, as it's meant to be synced externally

## File Structure

```
.kilo/
└── kilo.json          # Kilo config (excludes CONTRIBUTING.md)
CONTRIBUTING.md        # Synced externally to other repos
```

## Syncing to Other Repos

To sync the CONTRIBUTING.md to another repository:

1. Copy `CONTRIBUTING.md` to the target repository
2. Customize sections as needed
3. Commit and push

## Why Generic?

Using generic language in CONTRIBUTING.md allows:
- Easy syncing across multiple projects
- Less maintenance overhead
- Consistent contribution guidelines across the organization
