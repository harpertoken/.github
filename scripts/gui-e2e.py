#!/usr/bin/env python3

from pathlib import Path
import os
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from main import GitGUI  # noqa: E402


def run(command, cwd):
    result = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(
            f"{' '.join(command)} failed with {result.returncode}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    return result


def output_text(app):
    return app.output.get("1.0", "end-1c")


def assert_contains(text, expected):
    if expected not in text:
        raise AssertionError(f"expected {expected!r} in:\n{text}")


def buttons_by_text(widget):
    buttons = {}
    for child in widget.winfo_children():
        try:
            if child.winfo_class() == "Button":
                buttons[child.cget("text")] = child
        except Exception:
            pass
        buttons.update(buttons_by_text(child))
    return buttons


def main():
    original_cwd = Path.cwd()

    with tempfile.TemporaryDirectory(prefix="git-gui-e2e-") as temp_dir:
        temp = Path(temp_dir)
        repo = temp / "repo"
        remote = temp / "remote.git"
        repo.mkdir()

        run(["git", "init"], repo)
        run(["git", "config", "user.name", "Git GUI E2E"], repo)
        run(["git", "config", "user.email", "git-gui-e2e@example.invalid"], repo)
        run(["git", "config", "core.hooksPath", "/dev/null"], repo)
        run(["git", "init", "--bare", str(remote)], temp)
        run(["git", "remote", "add", "origin", str(remote)], repo)

        readme = repo / "README.md"
        readme.write_text("first line\n", encoding="utf-8")

        os.chdir(repo)
        app = GitGUI(build_ui=True, connect_db=False)
        app.root.update()
        buttons = buttons_by_text(app.root)
        expected_buttons = {
            "Status",
            "Add All",
            "Diff",
            "Log",
            "Commit",
            "Push",
            "Pull",
            "History",
        }
        missing_buttons = expected_buttons - set(buttons)
        if missing_buttons:
            raise AssertionError(f"missing buttons: {sorted(missing_buttons)}")

        try:
            buttons["Status"].invoke()
            assert_contains(output_text(app), "Untracked files")

            buttons["Add All"].invoke()
            app.commit_var.set("feat: initial commit")
            buttons["Commit"].invoke()
            commit_output = output_text(app)
            assert_contains(commit_output, "feat: initial commit")
            if app.commit_var.get() != "":
                raise AssertionError("commit input was not cleared")

            readme.write_text("first line\nsecond line\n", encoding="utf-8")
            buttons["Diff"].invoke()
            assert_contains(output_text(app), "+second line")

            buttons["Add All"].invoke()
            app.commit_var.set("fix: second commit")
            buttons["Commit"].invoke()
            assert_contains(output_text(app), "fix: second commit")

            buttons["Log"].invoke()
            log_output = output_text(app)
            assert_contains(log_output, "fix: second commit")
            assert_contains(log_output, "feat: initial commit")

            app.run_git_command(["git", "branch", "-M", "main"])
            app.run_git_command(["git", "push", "-u", "origin", "main"])
            push_output = output_text(app)
            if (
                "main -> main" not in push_output
                and "set up to track" not in push_output
            ):
                raise AssertionError(
                    f"push output did not look successful:\n{push_output}"
                )

            buttons["Pull"].invoke()
            assert_contains(output_text(app), "Already up to date")

            buttons["History"].invoke()
            assert_contains(output_text(app), "Database not available")
        finally:
            app.root.destroy()
            os.chdir(original_cwd)

    print("gui e2e ok")


if __name__ == "__main__":
    main()
