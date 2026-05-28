"""Server startup for the web UI.

Provides the entry point to launch the uvicorn server.
"""

import asyncio
import webbrowser

import uvicorn

from .routes import create_app


def run_server(
    host: str = "127.0.0.1",
    port: int = 8765,
    open_browser: bool = True,
    # Execute mode parameters
    task: str = None,
    preset_skills: list = None,
    mode: str = "full",
    run_mode: str = None,
    files: list = None,
    task_name: str = None,
) -> None:
    """Run the web UI server.

    Args:
        host: Server host
        port: Server port
        open_browser: Whether to open browser automatically
        task: Pre-set task (for execute mode)
        preset_skills: Pre-set skills list (for execute mode)
        mode: "full" for complete workflow, "execute" for direct execution
        run_mode: "baseline" | "free-style" | "dag" (for execute mode)
        files: Pre-set files list (for execute mode)
        task_name: Task name for folder naming (for execute mode)
    """
    app = create_app(
        task=task,
        preset_skills=preset_skills,
        mode=mode,
        run_mode=run_mode,
        files=files,
        task_name=task_name,
    )

    if open_browser:
        import threading
        def open_browser_delayed():
            import time
            time.sleep(1)
            webbrowser.open(f"http://{host}:{port}")
        threading.Thread(target=open_browser_delayed, daemon=True).start()

    config = uvicorn.Config(app, host=host, port=port, log_level="warning")
    server = uvicorn.Server(config)

    try:
        asyncio.run(server.serve())
    except KeyboardInterrupt:
        pass
