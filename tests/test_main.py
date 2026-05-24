import os
from unittest.mock import MagicMock, patch

import pytest

from main import GitGUI, HAS_PSYCOPG2


class TestGitGUI:
    @pytest.fixture
    def app(self):
        return GitGUI(build_ui=False, connect_db=False)

    def test_init_without_psycopg2(self):
        app = GitGUI(build_ui=False, connect_db=HAS_PSYCOPG2)
        if not HAS_PSYCOPG2:
            assert app.conn is None

    def test_handle_commit_empty_message(self, app):
        with patch.object(app, "set_output") as mock_set_output:
            app.handle_commit()
            mock_set_output.assert_called_once_with("Please enter a commit message.")

    @patch("subprocess.run")
    def test_handle_commit_with_message(self, mock_run, app):
        mock_run.return_value = MagicMock(stdout="", stderr="", returncode=0)
        app.commit_var = MagicMock()
        app.commit_var.get.return_value = "test commit"

        app.handle_commit()

        mock_run.assert_called_once_with(
            ["git", "commit", "-m", "test commit"],
            capture_output=True,
            text=True,
            cwd=os.getcwd(),
        )
        app.commit_var.set.assert_called_once_with("")

    def test_show_history_no_db(self, app):
        with patch.object(app, "set_output") as mock_set_output:
            app.show_history()
            mock_set_output.assert_called_once_with("Database not available")

    @patch("subprocess.run")
    def test_run_git_command_success(self, mock_run, app):
        mock_run.return_value = MagicMock(
            stdout="status output", stderr="", returncode=0
        )

        with patch.object(app, "set_output") as mock_set_output:
            app.run_git_command(["git", "status"])

        mock_run.assert_called_once_with(
            ["git", "status"], capture_output=True, text=True, cwd=os.getcwd()
        )
        mock_set_output.assert_called_once_with("status output")

    @patch("subprocess.run")
    def test_run_git_command_error(self, mock_run, app):
        mock_run.return_value = MagicMock(stdout="", stderr="error", returncode=1)

        with patch.object(app, "set_output") as mock_set_output:
            app.run_git_command(["git", "status"])

        mock_set_output.assert_called_once_with("Error (exit code 1):\nerror")
