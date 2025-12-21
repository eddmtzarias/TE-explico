"""
File watcher for real-time monitoring of design artifacts.
"""

from pathlib import Path
from typing import Optional, Callable
from ..config.settings import Settings

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileSystemEvent

    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False


class DesignFileHandler(FileSystemEventHandler):
    """Handler for design file system events."""

    def __init__(self, callback: Optional[Callable] = None):
        """
        Initialize the file handler.

        Args:
            callback: Optional callback function for file events
        """
        super().__init__()
        self.callback = callback

    def on_modified(self, event: "FileSystemEvent") -> None:
        """Handle file modification events."""
        if event.is_directory:
            return

        file_path = Path(event.src_path)
        if Settings.is_monitored_file(file_path.name):
            if self.callback:
                self.callback("modified", str(file_path))

    def on_created(self, event: "FileSystemEvent") -> None:
        """Handle file creation events."""
        if event.is_directory:
            return

        file_path = Path(event.src_path)
        if Settings.is_monitored_file(file_path.name):
            if self.callback:
                self.callback("created", str(file_path))

    def on_deleted(self, event: "FileSystemEvent") -> None:
        """Handle file deletion events."""
        if event.is_directory:
            return

        file_path = Path(event.src_path)
        if Settings.is_monitored_file(file_path.name):
            if self.callback:
                self.callback("deleted", str(file_path))


class FileWatcher:
    """File system watcher for monitoring design artifacts."""

    def __init__(self, watch_path: str, callback: Optional[Callable] = None):
        """
        Initialize the file watcher.

        Args:
            watch_path: Directory path to watch
            callback: Optional callback function for file events

        Raises:
            ImportError: If watchdog is not installed
        """
        if not WATCHDOG_AVAILABLE:
            raise ImportError(
                "watchdog package is required for file watching. "
                "Install it with: pip install watchdog"
            )

        self.watch_path = Path(watch_path)
        self.callback = callback
        self.observer: Optional["Observer"] = None
        self.handler = DesignFileHandler(callback=callback)

    def start(self) -> None:
        """Start watching the directory."""
        if not WATCHDOG_AVAILABLE:
            raise ImportError("watchdog package is not available")

        self.observer = Observer()
        self.observer.schedule(self.handler, str(self.watch_path), recursive=True)
        self.observer.start()
        print(f"📡 File watcher started for: {self.watch_path}")

    def stop(self) -> None:
        """Stop watching the directory."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            print("📡 File watcher stopped")

    def is_running(self) -> bool:
        """
        Check if the watcher is running.

        Returns:
            True if the watcher is active
        """
        return self.observer is not None and self.observer.is_alive()
