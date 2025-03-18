# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class DashLogger(Component):
    """A DashLogger component.
DashLogger component for displaying logs in real-time.

Keyword arguments:

- id (string; required):
    The ID used to identify this component in Dash callbacks.

- className (string; default ""):
    Additional class name for the logger container.

- loggerName (string; optional):
    Name of the logger to display (for single logger view).

- loggerNames (list of strings; optional):
    Names of loggers to display (for combined view).

- maxLogs (number; default 100):
    Maximum number of logs to display.

- timestampFormat (string; default "%Y-%m-%d %H:%M:%S"):
    The format string for the timestamp.

- twoColumns (boolean; default False):
    Whether to display logs in two columns (timestamp and message)."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_logger'
    _type = 'DashLogger'

    @_explicitize_args
    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        loggerName: typing.Optional[str] = None,
        loggerNames: typing.Optional[typing.Sequence[str]] = None,
        maxLogs: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        twoColumns: typing.Optional[bool] = None,
        timestampFormat: typing.Optional[str] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'className', 'loggerName', 'loggerNames', 'maxLogs', 'style', 'timestampFormat', 'twoColumns']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'loggerName', 'loggerNames', 'maxLogs', 'style', 'timestampFormat', 'twoColumns']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(DashLogger, self).__init__(**args)
