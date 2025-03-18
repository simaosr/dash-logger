import dash
from dash import html, Input, Output, callback
from dash_logger import init_app, DashLogger, create_logger

# Initialize app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Initialize the logging system
log_manager = init_app(app)

# Get loggers for different components
main_logger = create_logger("main")

logger = DashLogger(id="main-logger", loggerName="main")

# Layout
app.layout = html.Div(
    [
        html.H1("Dash Logger Component Example"),
        logger,
        html.Button("Log Info", id="log-info-button"),
        html.Button("Log Warning", id="log-warning-button"),
        html.Button("Log Error", id="log-error-button"),
        html.Button("Clear Logs", id="clear-logs-btn"),
    ]
)


@callback(
    Output("log-info-button", "n_clicks"),
    Output("log-warning-button", "n_clicks"),
    Output("log-error-button", "n_clicks"),
    Input("log-info-button", "n_clicks"),
    Input("log-warning-button", "n_clicks"),
    Input("log-error-button", "n_clicks"),
    prevent_initial_call=True,
)
def update_log(info_clicks, warning_clicks, error_clicks):
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
