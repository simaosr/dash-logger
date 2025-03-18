# AUTO GENERATED FILE - DO NOT EDIT

export dashlogger

"""
    dashlogger(;kwargs...)

A DashLogger component.
DashLogger component for displaying logs in real-time.
Keyword arguments:
- `id` (String; required): The ID used to identify this component in Dash callbacks.
- `className` (String; optional): Additional class name for the logger container
- `loggerName` (String; optional): Name of the logger to display (for single logger view)
- `loggerNames` (Array of Strings; optional): Names of loggers to display (for combined view)
- `maxLogs` (Real; optional): Maximum number of logs to display
- `style` (Dict; optional): Additional inline styles for the logger container
- `timestampFormat` (String; optional): The format string for the timestamp
- `twoColumns` (Bool; optional): Whether to display logs in two columns (timestamp and message)
"""
function dashlogger(; kwargs...)
        available_props = Symbol[:id, :className, :loggerName, :loggerNames, :maxLogs, :style, :timestampFormat, :twoColumns]
        wild_props = Symbol[]
        return Component("dashlogger", "DashLogger", "dash_logger", available_props, wild_props; kwargs...)
end

