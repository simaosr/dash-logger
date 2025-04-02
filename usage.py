import random
import uuid
import dash
from dash import html, Input, Output, callback, dcc, State
from dash_logger import init_app, DashLogger, create_logger
from dash_logger.manager import get_logger

# Initialize app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Initialize the logging system
log_manager = init_app(app)


def serve_layout():
    session_id = str(uuid.uuid4())

    # Layout
    return html.Div(
        [
            dcc.Store(id="session", storage_type="session"),
            html.H1("Dash Logger Component Example"),
            DashLogger(id="main-logger", loggerName=f"main_{session_id}"),
            html.Button("Log Info", id="log-info-button"),
            html.Button("Log Warning", id="log-warning-button"),
            html.Button("Log Error", id="log-error-button"),
            html.Button("Clear Logs", id="clear-logs-btn"),
        ]
    )


app.layout = serve_layout


# Add a new callback to initialize session ID if not exists
@callback(
    Output("session", "data"),
    Input("session", "modified_timestamp"),
    State("session", "data"),
)
def initialize_session(ts, data):
    if ts is None or data is None:
        return {"uid": str(uuid.uuid4())}
    return data


# Add a callback to set the logger name based on session
@callback(
    Output("main-logger", "loggerName"),
    Input("session", "data"),
)
def set_logger_name(session_data):
    if session_data and "uid" in session_data:
        return f"main_{session_data['uid']}"
    return "main_default"


@callback(
    Output("log-info-button", "n_clicks"),
    Output("log-warning-button", "n_clicks"),
    Output("log-error-button", "n_clicks"),
    Input("log-info-button", "n_clicks"),
    Input("log-warning-button", "n_clicks"),
    Input("log-error-button", "n_clicks"),
    State("session", "data"),
    prevent_initial_call=True,
)
def update_log(info_clicks, warning_clicks, error_clicks, session_id):
    # Get loggers for different components
    main_logger = get_logger("main", session_id)

    if info_clicks:
        main_logger.info("This is an info message")
    elif warning_clicks:
        main_logger.warning("This is a warning message")
    elif error_clicks:
        main_logger.error("This is an error message")
    return None, None, None


# Callback to clear logs
@callback(
    Output("clear-logs-btn", "n_clicks"),
    Input("clear-logs-btn", "n_clicks"),
    prevent_initial_call=True,
)
def clear_logs(n_clicks):
    log_manager.clear_logs()
    return dash.no_update


if __name__ == "__main__":
    app.run(debug=True)
