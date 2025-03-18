# Dash Logger

A Dash logger display component.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Overview

Dash Logger is a versatile and user-friendly logging display component for Dash applications. It provides an intuitive interface for real-time logging and monitoring, making it easier for developers to track application behavior and debug issues.

## Features

- Real-time log updates
- Filter logs by log level (e.g., info, warning, error)
- Search functionality to find specific log entries
- Customizable display settings
- Easy integration with existing Dash applications

## Installation

To install Dash Logger, use pip:

```bash
pip install dash-logger
```

## Usage

Here is a simple example of how to use Dash Logger in a Dash application:

```python
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

if __name__ == "__main__":
    app.run(debug=True)
```

## Configuration

Dash Logger can be customized through various properties. Below are some of the key configuration options:

- `log_level`: The minimum log level to display (default: 'info').
- `max_entries`: The maximum number of log entries to keep (default: 100).

## Contributing

We welcome contributions to Dash Logger! If you have an idea for a new feature or have found a bug, please open an issue or submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
