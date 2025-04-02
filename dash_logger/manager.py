import logging
import threading
import time
import json
from datetime import datetime
from typing import Dict, List, Optional
from threading import Lock
import queue


class DashLoggerNotInitialized(Exception):
    pass


class DashLogManager:
    def __init__(self):
        self._app = None
        self.loggers: Dict[str, logging.Logger] = {}
        self._initialized = False
        self._log_buffer = {}
        self._buffer_lock = Lock()
        self._max_buffer_size = 1000  # Maximum logs to keep per logger
        self._log_subscribers = {}
        self.sessions = {}  # Track session -> logger mapping
        self.inactive_timeout = 3600  # Timeout in seconds (e.g. 1 hour)
        self._cleanup_timer = None

    def init_app(self, app):
        """Initialize with a Dash app"""
        self._app = app
        self._initialized = True

        # Register routes for SSE
        @app.server.route("/logs/stream/<logger_name>")
        def stream_logs(logger_name):
            def generate():
                log_queue = queue.Queue()

                # Register this queue
                with self._buffer_lock:
                    if logger_name not in self._log_subscribers:
                        self._log_subscribers[logger_name] = []
                    self._log_subscribers[logger_name].append(log_queue)

                try:
                    # Send all existing logs first
                    if logger_name in self._log_buffer:
                        for log in self._log_buffer[logger_name]:
                            yield f"data: {json.dumps(log)}\n\n"

                    # Keep connection open and wait for new logs
                    while True:
                        try:
                            log_data = log_queue.get(timeout=30)
                            yield f"data: {json.dumps(log_data)}\n\n"
                        except queue.Empty:
                            # Send keep-alive comment
                            yield ": keep-alive\n\n"
                finally:
                    # Clean up subscription when client disconnects
                    with self._buffer_lock:
                        if logger_name in self._log_subscribers:
                            if log_queue in self._log_subscribers[logger_name]:
                                self._log_subscribers[logger_name].remove(log_queue)

            return app.server.response_class(
                generate(),
                mimetype="text/event-stream",
                headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
            )

    def create_logger(
        self, logger_name: str, logger_level: str = logging.INFO
    ) -> logging.Logger:
        """Create a new logger if it doesn't exist"""
        if not self._initialized:
            raise DashLoggerNotInitialized(
                "DashLogManager not initialized with a Dash app"
            )

        if (
            logger_name not in self.loggers
            or logger_level != self.loggers[logger_name].level
        ):
            return self.update_logger(
                logger_name, clean_handlers=True, logger_level=logger_level
            )

        return self.loggers[logger_name]

    def update_logger(
        self,
        logger_name: str,
        clean_handlers: bool = False,
        logger_level: str = logging.INFO,
    ) -> logging.Logger:
        """Remake logger, or create if it does not exist."""
        if not self._initialized:
            raise DashLoggerNotInitialized(
                "DashLogManager not initialized with a Dash app"
            )

        logger = logging.getLogger(logger_name)
        logger.setLevel(logger_level)

        if clean_handlers:
            logger.handlers = []

        # Initialize buffer for this logger if not exists
        with self._buffer_lock:
            if logger_name not in self._log_buffer:
                self._log_buffer[logger_name] = []

        # Add our custom handler
        dash_handler = DashLogHandler(self, logger_name)
        logger.addHandler(dash_handler)
        self.loggers[logger_name] = logger

        return logger

    def get_logger(self, name, session_id=None):
        """Get or create a logger for specific session"""
        logger_key = f"{name}_{session_id}" if session_id else name

        if logger_key not in self.loggers:
            self.loggers[logger_key] = create_logger(logger_key)
            if session_id:
                self.sessions[session_id] = logger_key
                self._schedule_cleanup()

        return self.loggers[logger_key]

    def clear_logs(self, session_id=None):
        """Clear logs for specific session or all logs"""
        if session_id and session_id in self.sessions:
            logger_key = self.sessions[session_id]
            if logger_key in self.loggers:
                self.loggers[logger_key].handlers = []
                del self.loggers[logger_key]
            del self.sessions[session_id]
        else:
            self.loggers.clear()
            self.sessions.clear()

    def _cleanup_inactive_sessions(self):
        """Remove inactive session loggers"""
        current_time = time.time()
        for session_id, logger_key in list(self.sessions.items()):
            if logger_key in self.loggers:
                last_activity = getattr(self.loggers[logger_key], "last_activity", 0)
                if current_time - last_activity > self.inactive_timeout:
                    self.clear_logs(session_id)

    def _schedule_cleanup(self):
        """Schedule periodic cleanup of inactive sessions"""
        if not self._cleanup_timer:
            self._cleanup_timer = threading.Timer(
                300, self._cleanup_inactive_sessions
            )  # Run every 5 minutes
            self._cleanup_timer.daemon = True
            self._cleanup_timer.start()

    def add_log_entry(self, logger_name: str, log_entry: dict):
        """Add a log entry to the buffer"""
        with self._buffer_lock:
            # Add to buffer
            if logger_name not in self._log_buffer:
                self._log_buffer[logger_name] = []

            self._log_buffer[logger_name].append(log_entry)

            # Trim buffer if needed
            if len(self._log_buffer[logger_name]) > self._max_buffer_size:
                self._log_buffer[logger_name] = self._log_buffer[logger_name][
                    -self._max_buffer_size :
                ]

            # Notify subscribers if any
            if logger_name in self._log_subscribers:
                for subscriber_queue in self._log_subscribers[logger_name]:
                    subscriber_queue.put(log_entry)

    def get_logs(self, logger_name: str, limit: int = 100) -> List[dict]:
        """Get the most recent logs for a logger"""
        with self._buffer_lock:
            if logger_name not in self._log_buffer:
                return []
            return self._log_buffer[logger_name][-limit:]

    def clear_logs(self, logger_name: str = None):
        """Clear logs for a specific logger or all loggers"""
        with self._buffer_lock:
            if logger_name:
                if logger_name in self._log_buffer:
                    self._log_buffer[logger_name] = []
            else:
                for name in self._log_buffer:
                    self._log_buffer[name] = []


class DashLogHandler(logging.Handler):
    def __init__(self, log_manager, logger_name):
        super().__init__()
        self.log_manager = log_manager
        self.logger_name = logger_name

    def emit(self, record):
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger_name": self.logger_name,
        }
        self.log_manager.add_log_entry(self.logger_name, log_entry)


# Create a singleton instance
logger_manager = DashLogManager()


# Convenience functions
def init_app(app) -> DashLogManager:
    """Initialize with a Dash app"""
    logger_manager.init_app(app)
    return logger_manager


def get_logger(logger_name: str, session_id: str | None = None) -> logging.Logger:
    """Get an existing logger or create a new one"""
    return logger_manager.get_logger(logger_name, session_id=session_id["uid"])


def create_logger(logger_name: str, logger_level: str = logging.INFO) -> logging.Logger:
    """Create a new logger"""
    return logger_manager.create_logger(logger_name, logger_level)
