import pytest
from main import GitGUI


@pytest.mark.asyncio
async def test_app_starts():
    """Basic e2e test: app initializes without opening a window."""
    app = GitGUI(build_ui=False, connect_db=False)
    assert app.conn is None or hasattr(app, "conn")
    assert app.root is None
