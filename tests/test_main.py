import pytest
import os
from unittest.mock import patch, MagicMock
from main import GitTUI, HAS_PSYCOPG2
from textual.widgets import Static


class TestGitTUI:
    @pytest.fixture
    def app(self):
        return GitTUI()

    def test_init_without_psycopg2(self, app):
        if not HAS_PSYCOPG2:
            assert app.conn is None

    def test_handle_commit_empty_message(self, app):
        # Mock the query_one
        with patch.object(app, "query_one") as mock_query:
            mock_input = MagicMock()
            mock_input.value = ""
            mock_query.return_value = mock_input
            app.handle_commit()
            mock_query.assert_called()

    @patch("subprocess.run")
    @patch.object(GitTUI, "query_one")
    def test_handle_commit_with_message(self, mock_query, mock_run, app):
        mock_run.return_value = MagicMock(stdout="", stderr="", returncode=0)
        mock_input = MagicMock()
        mock_input.value = "test commit"
        mock_static = MagicMock()
        mock_query.side_effect = [mock_input, mock_static]
        app.handle_commit()
        mock_run.assert_called_once_with(
            ["git", "commit", "-m", "'test", "commit'"],
            capture_output=True,
            text=True,
            cwd=os.getcwd(),
        )

    def test_show_history_no_db(self, app):
        app.conn = None
        with patch.object(app, "query_one") as mock_query:
            app.show_history()
            mock_query.assert_called_with("#output", Static)
            # Should update to "Database not available"

    @patch("subprocess.run")
    @patch.object(GitTUI, "query_one")
    def test_run_git_command_success(self, mock_query, mock_run, app):
        mock_run.return_value = MagicMock(
            stdout="status output", stderr="", returncode=0
        )
        mock_static = MagicMock()
        mock_query.return_value = mock_static
        app.run_git_command("git status")
        mock_run.assert_called_once_with(
            ["git", "status"], capture_output=True, text=True, cwd=os.getcwd()
        )
        mock_static.update.assert_called_with("status output")

    @patch("subprocess.run")
    @patch.object(GitTUI, "query_one")
    def test_run_git_command_error(self, mock_query, mock_run, app):
        mock_run.return_value = MagicMock(stdout="", stderr="error", returncode=1)
        mock_static = MagicMock()
        mock_query.return_value = mock_static
        app.run_git_command("git status")
        mock_static.update.assert_called_with("Error (exit code 1):\nerror")
