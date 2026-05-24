#!/usr/bin/env python3

from datetime import datetime
import os
import subprocess  # nosec B404

try:
    import psycopg2

    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

try:
    import tkinter as tk
    from tkinter import scrolledtext

    HAS_TKINTER = True
except ImportError:
    tk = None
    scrolledtext = None
    HAS_TKINTER = False


class GitGUI:
    """A small GUI for common Git operations."""

    def __init__(self, root=None, build_ui=True, connect_db=True):
        self.root = root
        self.conn = None
        self.commit_var = None
        self.output = None

        if connect_db:
            self.connect_database()

        if build_ui:
            if not HAS_TKINTER:
                raise RuntimeError(
                    "Tkinter is not available in this Python build. "
                    "Install a Python distribution with Tk support to run the GUI."
                )
            self.root = self.root or tk.Tk()
            self.build_ui()

    def connect_database(self):
        if not HAS_PSYCOPG2:
            return

        try:
            self.conn = psycopg2.connect(
                dbname=os.environ.get("POSTGRES_DB", "git_tui"),
                user=os.environ.get("POSTGRES_USER", "user"),
                password=os.environ.get("POSTGRES_PASSWORD", "password"),
                host=os.environ.get("POSTGRES_HOST", "localhost"),
            )
            self.create_table()
        except Exception as exc:
            print(f"PostgreSQL not available: {exc}. Running without database.")
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

    def build_ui(self):
        self.root.title("Git GUI")
        self.root.geometry("760x520")

        frame = tk.Frame(self.root, padx=12, pady=12)
        frame.pack(fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(frame)
        button_frame.pack(fill=tk.X)

        actions = [
            ("Status", lambda: self.run_git_command(["git", "status"])),
            ("Add All", lambda: self.run_git_command(["git", "add", "."])),
            ("Diff", lambda: self.run_git_command(["git", "diff"])),
            ("Log", lambda: self.run_git_command(["git", "log", "--oneline", "-10"])),
            ("Push", lambda: self.run_git_command(["git", "push"])),
            ("Pull", lambda: self.run_git_command(["git", "pull"])),
            ("History", self.show_history),
        ]

        for label, command in actions:
            tk.Button(button_frame, text=label, command=command).pack(
                side=tk.LEFT, padx=(0, 8), pady=(0, 10)
            )

        commit_frame = tk.Frame(frame)
        commit_frame.pack(fill=tk.X)

        self.commit_var = tk.StringVar()
        commit_entry = tk.Entry(commit_frame, textvariable=self.commit_var)
        commit_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        commit_entry.bind("<Return>", lambda _event: self.handle_commit())

        tk.Button(commit_frame, text="Commit", command=self.handle_commit).pack(
            side=tk.LEFT
        )

        self.output = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=22)
        self.output.pack(fill=tk.BOTH, expand=True, pady=(12, 0))

    def set_output(self, text):
        if self.output is None:
            return

        self.output.configure(state=tk.NORMAL)
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)
        self.output.configure(state=tk.DISABLED)

    def get_commit_message(self):
        if self.commit_var is None:
            return ""
        return self.commit_var.get().strip()

    def clear_commit_message(self):
        if self.commit_var is not None:
            self.commit_var.set("")

    def run_git_command(self, command: list[str]):
        try:
            result = subprocess.run(  # nosec B603
                command, capture_output=True, text=True, cwd=os.getcwd()
            )
            output = result.stdout + result.stderr
            if result.returncode != 0:
                output = f"Error (exit code {result.returncode}):\n{output}"
            self.set_output(output)
            self.store_command(command)
        except (FileNotFoundError, subprocess.SubprocessError) as exc:
            self.set_output(f"Error: {exc}")

    def store_command(self, command: list[str]):
        if not self.conn:
            return

        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO command_history (command, timestamp) VALUES (%s, %s)",
                (command, datetime.now()),
            )
            self.conn.commit()

    def handle_commit(self):
        message = self.get_commit_message()
        if not message:
            self.set_output("Please enter a commit message.")
            return
        self.run_git_command(["git", "commit", "-m", message])
        self.clear_commit_message()

    def show_history(self):
        if not self.conn:
            self.set_output("Database not available")
            return

        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT command, timestamp FROM command_history "
                    "ORDER BY timestamp DESC LIMIT 10"
                )
                rows = cur.fetchall()
            history = "\n".join(f"{row[1]}: {' '.join(row[0])}" for row in rows)
            self.set_output(history or "No history")
        except psycopg2.Error as exc:
            self.set_output(f"Error: {exc}")


def main():
    app = GitGUI()
    app.root.mainloop()


if __name__ == "__main__":
    main()
