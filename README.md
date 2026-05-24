<a href="https://github.com/harpertoken/.github" aria-label="git-gui"><img src="profile/mark.svg" width="16" height="16" alt=""> <code>git-gui</code></a>

GUI for common Git operations.

This repository also contains organization defaults for `harpertoken`.

Requires a Python build with Tk support.

## Paths

- `profile/readme.md` - organization profile
- `.github/workflows/update-org-activity.yml` - profile activity updater
- `.github/ISSUE_TEMPLATE/` - issue templates
- `.github/PULL_REQUEST_TEMPLATE.md` - pull request template
- `docs/` - project notes

The activity updater rewrites only:

```md
<!-- ORG_ACTIVITY:START -->
<!-- ORG_ACTIVITY:END -->
```

## Commands

```sh
make install
make run
python run_tests.py
python check_all.py
```

Run directly:

```sh
python main.py
```

Run with Docker:

```sh
docker-compose up --build
```

## Development

```sh
ruff check .
ruff format .
pre-commit install
pre-commit run --all-files
```

Commit messages use conventional commit types. To install the local hook:

```sh
cp scripts/commit-msg .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
```

## Release

```sh
python bump_version.py <major|minor|patch>
```

Tag a version such as `v1.0.0` to trigger the release workflow.
