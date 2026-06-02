"""Data Viz Dashboard — Slash Command."""

def _handle_dashboard(raw_args: str) -> str:
    url = "http://localhost:5000/"
    return f"🚀 **System Intelligence Dashboard**\n\nClick here to open the UI in a new tab:\n{url}"

def register(ctx):
    # Not to 'callback'. comes to 'handler'
    ctx.register_command(
        "dashboard",
        handler=_handle_dashboard,
        description="Open the System Intelligence Dashboard"
    )