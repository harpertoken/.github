import pytest
from main import GitTUI


@pytest.mark.asyncio
async def test_app_starts():
    """Basic e2e test: app initializes without errors."""
    app = GitTUI()
    # Just check init, no full UI test due to complexity
    assert app.conn is None or hasattr(app, "conn")
    assert app.title == "GitTUI"
