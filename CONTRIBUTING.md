Use the repository's own contributing notes when they exist.

Otherwise:

- keep changes small
- explain the reason
- include tests for behavior changes

## Commit messages

Use scoped conventional prefixes, lowercase scope in parentheses:

- `docs(scope): ...` for documentation and evidence records
- `feat(scope): ...` for new behavior
- `fix(scope): ...` for bug fixes
- `chore(scope): ...` for maintenance (deps, lockfiles, releases)
- `test(scope): ...` for tests

Examples:

- `docs(sync): update site, readme, roadmap, architecture to Task 15`
- `docs(verification): record task 15 evidence`
- `fix(build): make bootstrap.sh and install.sh executable`
- `chore(deps): bump version to 1.5.25`

Merge pull requests with their branch scope, e.g.
`Merge pull request #56 from bniladridas/docs/sync-task15`.
