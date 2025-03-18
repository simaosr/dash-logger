import dash
from dash import html, dcc, Input, Output, callback
import logging
import time
import threading
import random
from dash_logger import init_app, get_logger, DashLogger, create_logger

# Initialize app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Initialize the logging system
log_manager = init_app(app)

# Get loggers for different components
main_logger = create_logger("main", logging.DEBUG)
data_logger = get_logger("data")
system_logger = get_logger("system")

# Layout
app.layout = html.Div(
    [
        html.H1("Dash Logger Component Example"),
        html.Div(
            [
                html.H3("Single Logger View"),
                DashLogger(
                    id="main-logger", loggerName="main", style={"height": "60px"}
                ),
                html.H3("Combined Logger View"),
                DashLogger(
                    id="combined-logger",
                    loggerNames=["data", "system"],
                    twoColumns=True,
                    timestampFormat="%H:%M:%S",
                    # style={"height": "300px"},
                ),
                html.H3("Real-time Logger with Server-Sent Events"),
                DashLogger(
                    id="sse-logger",
                    loggerName="main",
                    # style={"height": "200px"},
                ),
                html.Div(
                    [
                        html.Button(
                            "Generate Log Entries", id="generate-logs-btn", n_clicks=0
                        ),
                        html.Button("Clear Logs", id="clear-logs-btn", n_clicks=0),
                    ],
                    # style={"margin": "20px 0"},
                ),
            ],
            style={"margin": "0 auto"},
        ),
    ]
)


# Callback to generate test logs
@callback(
    Output("generate-logs-btn", "n_clicks"),
    Input("generate-logs-btn", "n_clicks"),
    prevent_initial_call=True,
)
def generate_logs(n_clicks):
    main_logger.info(f"Button clicked {n_clicks} times")

    # Generate a few random logs
    main_logger.debug("This is a debug message 2")
    main_logger.debug("This is a debug message 2")
    main_logger.info("Processing request")

    if random.random() > 0.7:
        main_logger.warning("This operation might take longer than expected")

    data_logger.info("Retrieved 500 records from database")
    data_logger.debug(f"Query took {random.random() * 2:.2f} seconds")

    system_logger.info("System status: OK")

    if random.random() > 0.9:
        system_logger.error("Failed to connect to secondary server")

    return dash.no_update


# Callback to clear logs
@callback(
    Output("clear-logs-btn", "n_clicks"),
    Input("clear-logs-btn", "n_clicks"),
    prevent_initial_call=True,
)
def clear_logs(n_clicks):
    log_manager.clear_logs()
    main_logger.info("Logs cleared")
    return dash.no_update


if __name__ == "__main__":
    app.run(debug=True)
