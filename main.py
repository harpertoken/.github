#!/usr/bin/env python3

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Input
from textual.containers import Container, Vertical
import subprocess  # nosec B404
import os

try:
    import psycopg2

    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False
from datetime import datetime


class GitTUI(App):
    """A simple TUI for Git operations."""

    def __init__(self):
        super().__init__()
        if HAS_PSYCOPG2:
            try:
                self.conn = psycopg2.connect(
                    dbname=os.environ.get("POSTGRES_DB", "git_tui"),
                    user=os.environ.get("POSTGRES_USER", "user"),
                    password=os.environ.get("POSTGRES_PASSWORD", "password"),
                    host=os.environ.get("POSTGRES_HOST", "localhost"),
                )
                self.create_table()
            except Exception as e:
                print(f"PostgreSQL not available: {e}. Running without database.")
                self.conn = None
        else:
            print("psycopg2 not installed. Running without database.")
            self.conn = None

    def create_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS command_history (
                    id SERIAL PRIMARY KEY,
                    command TEXT,
                    timestamp TIMESTAMP
                )
            """)
            self.conn.commit()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Container():
            with Vertical():
                yield Static("Git TUI", id="title")
                yield Button("Git Status", id="status")
                yield Button("Git Add All", id="add_all")
                yield Button("Git Diff", id="diff")
                yield Button("Git Log", id="log")
                yield Button("Git Commit", id="commit")
                yield Button("Git Push", id="push")
                yield Button("Git Pull", id="pull")
                yield Button("Command History", id="history")
                yield Input(placeholder="Commit message", id="commit_input")
                yield Static("", id="output")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "status":
            self.run_git_command("git status")
        elif button_id == "add_all":
            self.run_git_command("git add .")
        elif button_id == "diff":
            self.run_git_command("git diff")
        elif button_id == "log":
            self.run_git_command("git log --oneline -10")
        elif button_id == "commit":
            self.handle_commit()
        elif button_id == "push":
            self.run_git_command("git push")
        elif button_id == "pull":
            self.run_git_command("git pull")
        elif button_id == "history":
            self.show_history()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "commit_input":
            self.handle_commit()

    def on_key(self, event):
        if event.key == "s":
            self.run_git_command("git status")
        elif event.key == "a":
            self.run_git_command("git add .")
        elif event.key == "d":
            self.run_git_command("git diff")
        elif event.key == "l":
            self.run_git_command("git log --oneline -10")
        elif event.key == "c":
            self.query_one("#commit_input", Input).focus()
        elif event.key == "p":
            self.run_git_command("git push")
        elif event.key == "u":
            self.run_git_command("git pull")
        elif event.key == "h":
            self.show_history()

    def run_git_command(self, command: list[str]):
        try:
            result = subprocess.run(  # nosec B603
                command, capture_output=True, text=True, cwd=os.getcwd()
            )
            output = result.stdout + result.stderr
            if result.returncode != 0:
                output = f"Error (exit code {result.returncode}):\n{output}"
            self.query_one("#output", Static).update(output)
            # Store in db if available
            if self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO command_history (command, timestamp) VALUES (%s, %s)",
                        (command, datetime.now()),
                    )
                    self.conn.commit()
        except Exception as e:
            self.query_one("#output", Static).update(f"Error: {str(e)}")

    def handle_commit(self):
        input_widget = self.query_one("#commit_input", Input)
        message = input_widget.value.strip()
        if not message:
            self.query_one("#output", Static).update("Please enter a commit message.")
            input_widget.focus()
            return
        self.run_git_command(["git", "commit", "-m", message])
        input_widget.value = ""  # Clear input

    def show_history(self):
        if not self.conn:
            self.query_one("#output", Static).update("Database not available")
            return
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT command, timestamp FROM command_history ORDER BY timestamp DESC LIMIT 10"
                )
                rows = cur.fetchall()
                history = "\n".join([f"{row[1]}: {row[0]}" for row in rows])
                self.query_one("#output", Static).update(history or "No history")
        except psycopg2.Error as e:
            self.query_one("#output", Static).update(f"Error: {str(e)}")


def main():
    app = GitTUI()
    app.run()


if __name__ == "__main__":
    main()
